"""Created on Tue May 29 22:10:18 2018.

@author: henrik
"""
import gc

import mahotas as mh
import networkx as nx
import numpy as np
import pymeshfix as pmf
import pyvista as pv
import scipy.optimize as opt
import tifffile as tiff
import vtk
from clahe import clahe
from imgmisc import autocrop, cut, get_resolution, to_uint8
from pyacvd import clustering
from pymeshfix._meshfix import PyTMesh
from pystackreg import StackReg
from scipy.ndimage import zoom
from scipy.ndimage.filters import gaussian_filter
from scipy.ndimage.morphology import binary_fill_holes, distance_transform_edt
from scipy.signal import wiener
from scipy.spatial import cKDTree
from skimage.measure import marching_cubes
from skimage.segmentation import morphological_chan_vese

# import phenotastic.plot as pl
from phenotastic.misc import car2sph, coord_array, rotate


def rot_matrix_44(angles, invert=False):
    """Generate a 4x4 rotation matrix for.

    Parameters
    ----------
    angles : list, tuple or np.array of length 3
        Input angles in radians. For rotations alpha, beta, gamma, the rotations are applied in
        order beta-gamma-alpha. This ordering is done for historic reasons and may change in future releases.
    invert : bool, optional
        Whether to do invert the rotation. The default is False.

    Returns
    -------
    R : 4x4 np.narray
        The resulting rotation matrix.
    """
    alpha, beta, gamma = angles
    Rx = np.array(
        [
            [1, 0, 0, 0],
            [0, np.cos(alpha), -np.sin(alpha), 0],
            [0, np.sin(alpha), np.cos(alpha), 0],
            [0, 0, 0, 1],
        ],
    )
    Ry = np.array(
        [
            [np.cos(beta), 0, np.sin(beta), 0],
            [0, 1, 0, 0],
            [-np.sin(beta), 0, np.cos(beta), 0],
            [0, 0, 0, 1],
        ],
    )
    Rz = np.array(
        [
            [np.cos(gamma), -np.sin(gamma), 0, 0],
            [np.sin(gamma), np.cos(gamma), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
    )

    if invert == True:
        R = np.linalg.inv(np.matmul(np.matmul(Rz, Ry), Rx))
    elif invert == False:
        R = np.matmul(np.matmul(Rz, Ry), Rx)

    return R


def paraboloid(p, sampling=(200, 200, 200), bounds=None):
    r"""Generate a meshed paraboloid object.

    Parameters
    ----------
    p : 5-tuple of the paraboloid parameters
        Parameters of the folliwing equation:

        .. math::
            z = p_0 x^2 + p_1 y^2 + p_2 x + p_3 y + p_4

    sampling : 3-tuple of ints, optional
        The sampling in XYZ. The default is (200, 200, 200).
    bounds : float or 6-tuple, optional
        The cut-off bounds for the paraboloid in format [X0,X1,Y0,Y1,Z0,Z1]. The default is None.

    Returns
    -------
    output : pyvista.PolyData
        The rotated polydata mesh.
    """
    # Input checks
    p1, p2, p3, p4, p5, alpha, beta, gamma = p
    if bounds is None:
        bounds = [-2000, 2000] * 3
    elif isinstance(bounds, (float, int)):
        bounds = [-bounds, bounds] * 3
    if isinstance(sampling, (int, float)):
        sampling = [sampling] * 3
    bounds = np.array(bounds)

    # Get the bounding box corners in the transformed space
    corners = np.array(
        [
            [bounds[0], bounds[2], bounds[4]],
            [bounds[0], bounds[2], bounds[5]],
            [bounds[0], bounds[3], bounds[4]],
            [bounds[0], bounds[3], bounds[5]],
            [bounds[1], bounds[2], bounds[4]],
            [bounds[1], bounds[2], bounds[5]],
            [bounds[1], bounds[3], bounds[4]],
            [bounds[1], bounds[3], bounds[5]],
        ]
    )
    corners = rotate(corners, [alpha, beta, gamma], invert=False)

    bounds = [
        min(corners[:, 0]),
        max(corners[:, 0]),
        min(corners[:, 1]),
        max(corners[:, 1]),
        min(corners[:, 2]),
        max(corners[:, 2]),
    ]

    # Generate the paraboloid mesh along the z-axis
    # vtkQuadric evaluates the quadric function:
    # F(x,y,z) = a0*x^2 + a1*y^2 + a2*z^2 + a3*x*y + a4*y*z + a5*x*z + a6*x + a7*y + a8*z + a9.
    quadric = vtk.vtkQuadric()
    quadric.SetCoefficients(p1, p2, 0, 0, 0, 0, p3, p4, -1, p5)
    sample = vtk.vtkSampleFunction()
    sample.SetSampleDimensions(sampling)
    sample.SetImplicitFunction(quadric)
    sample.SetModelBounds(bounds)
    sample.Update()

    # Rotate the mesh so that it is in the optimised orientation
    rotmat = rot_matrix_44([alpha, beta, gamma], invert=True)
    trans = vtk.vtkMatrix4x4()
    for ii in range(rotmat.shape[0]):
        for jj in range(rotmat.shape[1]):
            trans.SetElement(ii, jj, rotmat[ii][jj])
    transmat = vtk.vtkMatrixToHomogeneousTransform()
    transmat.SetInput(trans)

    contour = vtk.vtkContourFilter()
    contour.SetInputData(sample.GetOutput())
    contour.Update()

    transfilter = vtk.vtkTransformPolyDataFilter()
    transfilter.SetInputData(contour.GetOutput())
    transfilter.SetTransform(transmat)
    transfilter.Update()

    output = pv.PolyData(transfilter.GetOutput())

    return output


def create_mesh(contour, resolution=[1, 1, 1], step_size=1):
    """Generate a polydata mesh from a binary contour.

    Parameters
    ----------
    contour : np.array of type bool, int or float
        The binary mask of the contour.
    resolution : 3-tuple, optional
        The spatial resolution. The default is [1, 1, 1].
    step_size : float, optional
        Step size of the marching cubes method. The default is 1.

    Returns
    -------
    mesh : pyvista.PolyData
        The output mesh.
    """
    v, f, _, _ = marching_cubes(
        contour,
        0,
        spacing=list(resolution),
        step_size=step_size,
        allow_degenerate=False,
    )
    mesh = pv.PolyData(v, np.c_[[3] * len(f), f].ravel())
    return mesh


def filter_curvature(mesh, curvature_threshold, curvatures=None):
    """Remove mesh vertices based on curvatures.

    Parameters
    ----------
    mesh : pyvista.PolyData
        The input mesh.
    curvature_threshold : tuple of floats
        The curvature threshold.
    curvatures : np.array, optional
        The curvatures. Defaults to None. If None, computes the mean vertex
        curvatures.

    Returns
    -------
    mesh : pyvista.PolyData
        The filtered mesh.
    """
    if isinstance(curvature_threshold, (int, float)):
        curvature_threshold = (-curvature_threshold, curvature_threshold)
    if curvatures is None:
        curvature = mesh.curvature()

    to_remove = curvature < curvature_threshold[0] | curvature > curvature_threshold[1]
    mesh = mesh.remove_points(to_remove)[0]

    return mesh


def label_cellular_mesh(mesh, values, value_tag="values", id_tag="cell_id"):
    """Label the mesh with unique cell identifiers with the given values.

    Parameter
    ---------

    mesh : pyvista.PolyData
        The input mesh.
    values : np.array
        The values to be assigned to the mesh.
    value_tag : str, optional
        The array name for the values in the input mesh. The default is 'values'.
    id_tag : str, optional
        The array name for the cell ids in the input mesh. The default is 'cell_id'.

    Returns
    -------
    mesh : pyvista.PolyData
        The output mesh.
    """
    mesh[value_tag] = np.zeros(mesh.n_points)
    for ii in np.unique(mesh[id_tag]):
        mesh[value_tag][mesh[id_tag] == ii] = values[ii]
    return mesh


def create_cellular_mesh(seg_img, resolution=[1, 1, 1], verbose=True):
    """Generate a cellular mesh from a segmentation image.

    Parameters
    ----------
    seg_img : 3D np.array
        The segmentated image.
    resolution : 3-tuple, optional
        The spatial resolution. The default is [1, 1, 1].
    verbose : bool, optional
        Whether to print the progress. The default is True.

    Returns
    -------
    mesh : pyvista.MultiBlock
        The output mesh object, with each block corresponding to a single cell.
    """
    cells = []
    labels = np.unique(seg_img)[1:]
    n_cells = len(labels)
    for c_idx, cell_id in enumerate(labels):
        if verbose:
            print(f"Now meshing cell {c_idx} (label: {cell_id}) out of {n_cells}")
        cell_img, cell_cuts = autocrop(
            seg_img == cell_id,
            threshold=0,
            n=1,
            return_cuts=True,
            offset=[[2, 2], [2, 2], [2, 2]],
        )
        cell_volume = np.sum(cell_img > 0) * np.product(resolution)

        v, f, _, _ = marching_cubes(
            cell_img,
            0,
            allow_degenerate=False,
            step_size=1,
            spacing=resolution,
        )
        v[:, 0] += cell_cuts[0, 0] * resolution[0]
        v[:, 1] += cell_cuts[1, 0] * resolution[1]
        v[:, 2] += cell_cuts[2, 0] * resolution[2]

        cell_mesh = pv.PolyData(v, np.ravel(np.c_[[[3]] * len(f), f]))
        cell_mesh["cell_id"] = np.full(
            fill_value=cell_id,
            shape=cell_mesh.n_points,
        )
        cell_mesh["volume"] = np.full(
            fill_value=cell_volume,
            shape=cell_mesh.n_points,
        )

        cells.append(cell_mesh)

    multi = pv.MultiBlock(cells)
    poly = pv.PolyData()
    for ii in range(multi.n_blocks):
        poly += multi.get(ii)

    return poly


def contour(
    fin,
    iterations=25,
    smoothing=1,
    masking=0.75,
    crop=True,
    resolution=None,
    clahe_window=None,
    clahe_clip_limit=None,
    gaussian_sigma=None,
    gaussian_iterations=5,
    interpolate_slices=True,
    fill_slices=True,
    lambda1=1,
    lambda2=1,
    stackreg=True,
    target_resolution=[0.5, 0.5, 0.5],
    fill_inland_threshold=None,
    return_resolution=False,
    verbose=True,
):
    """Generate a contour from a 3D image.

    Parameters
    ----------
    fin : str or 3D np.array
        The input image or path to file.
    iterations : int, optional
        The number of iterations for the morphosnakes algorithm. The default is 25.
    smoothing : int, optional
        The number of morphosnakes smoothing iterations per cycle. The default is 1.
    masking : float, optional
        The masking threshold. The default is 0.75.
    crop : bool, optional
        Whether to crop the image. The default is True.
    resolution : 3-tuple, optional
        The spatial resolution. The default is None.
    clahe_window : int, optional
        The window/histogram size for the CLAHE algorithm. The default is None.
    clahe_clip_limit : float, optional
        The clip limit for the CLAHE algorithm. The default is None.
    gaussian_sigma : float, optional
        The sigma for the Gaussian filter. The default is None.
    gaussian_iterations : int, optional
        The number of iterations for the Gaussian filter. The default is 5.
    interpolate_slices : bool, optional
        Whether to interpolate the slices. The default is True.
    fill_slices : bool, optional
        Whether to fill holes in the XY slices. The default is True.
    lambda1 : float, optional
        The lambda1 parameter for the morphosnakes algorithm. The default is 1.
    lambda2 : float, optional
        The lambda2 parameter for the morphosnakes algorithm. The default is 1.
    stackreg : bool, optional
        Whether to run stackreg. The default is True.
    target_resolution : 3-tuple, optional
        The target resolution for the output. The default is [.5,.5,.5].
    fill_inland_threshold : float, optional
        The distance threshold from the object XY periphery to fill. The default is None, which results in no filling.
    return_resolution : bool, optional
        Whether to return the resolution. The default is False.
    verbose : bool, optional
        Whether to print the progress. The default is True.
    """

    if verbose:
        print(f"Reading in data for {fin}")
    if isinstance(fin, str):
        data = tiff.imread(fin)
        data = np.squeeze(data)

    if resolution is None:
        resolution = get_resolution(fin)

    if any(np.less(resolution, 1e-3)):
        resolution = np.multiply(resolution, 1e6)
    if verbose:
        print(f"Resolution for {fin} is {resolution}")

    data = zoom(data, resolution / np.asarray(target_resolution), order=3)

    # Perform stack regularisation
    if stackreg:
        if verbose:
            print(f"Running stackreg for {fin}")
        pretype = data.dtype
        data = data.astype(float)
        sr = StackReg(StackReg.RIGID_BODY)
        if data.ndim > 3:
            trsf_mat = sr.register_stack(np.max(data, 1))
            for ii in range(data.shape[1]):
                data[:, ii] = sr.transform_stack(data[:, ii], tmats=trsf_mat)
        else:
            trsf_mat = sr.register_stack(data)
            data = sr.transform_stack(data, tmats=trsf_mat)
        data[data < 0] = 0
        data = data.astype(pretype)

    # Autocrop the image
    if crop:
        if verbose:
            print(f"Running autocrop for {fin}")
        offset = np.full((3, 2), 5)
        offset[0] = (10, 10)

        if data.ndim > 3:
            _, cuts = autocrop(
                np.max(data, 1),
                2 * mh.otsu(np.max(data, 1)),
                n=10,
                offset=offset,
                return_cuts=True,
            )
            data = cut(data, cuts)
        else:
            data = autocrop(data, 2 * mh.otsu(data), n=10, offset=offset)

    # Perform Wiener filtering
    if verbose:
        print(f"Running wiener filtering for {fin}")
    data = data.astype("float")
    if data.ndim > 3:
        for ii in range(data.shape[1]):
            data[:, ii] = wiener(data[:, ii])
        data = np.max(data, 1)
    else:
        data = wiener(data)
    data = to_uint8(data, False)
    gc.collect()

    # Performing CLAHE
    if verbose:
        print(f"Running CLAHE for {fin}")
    if clahe_window is None:
        clahe_window = (np.array(data.shape) + 4) // 8
    if clahe_clip_limit is None:
        clahe_clip_limit = mh.otsu(data)
    data = clahe(data, win_shape=clahe_window, clip_limit=clahe_clip_limit)
    gc.collect()

    # Performing Gaussian smoothing
    if gaussian_sigma is None:
        gaussian_sigma = [1, 1, 1]
    for ii in range(gaussian_iterations):
        if verbose:
            print(f"Smoothing out {fin} with gaussian smoothing")
            data = gaussian_filter(data, sigma=gaussian_sigma)

    if interpolate_slices:
        raise NotImplementedError("Interpolation not implemented yet")
    #     if verbose:
    #         print(f'Interpolating slices for {fin}')
    #     resolution = np.array(resolution)
    #     data = resize(data, np.round(data.shape * resolution / np.min(resolution)).astype('int'), order=2)
    #     resolution = resolution / (np.round(data.shape * resolution / np.min(resolution)) / data.shape)
    # gc.collect()

    # Perform morphological chan-vese
    if verbose:
        print(f"Running morphological chan-vese for {fin}")
    if isinstance(masking, (float, int)):
        masking = to_uint8(data, False) > masking * mh.otsu(to_uint8(data, False))
    contour = morphological_chan_vese(
        data,
        iterations=iterations,
        init_level_set=masking,
        smoothing=smoothing,
        lambda1=lambda1,
        lambda2=lambda2,
    )

    # Postprocess the contour by filling etc.
    contour = fill_contour(contour, fill_xy=fill_slices, fill_zx_zy=False)

    if fill_inland_threshold is not None:
        if verbose:
            print(f"Filling inland for {fin}")
        contour = fill_inland(contour, fill_inland_threshold)

    # Return outputs
    if return_resolution:
        return contour, resolution
    return contour


def fill_beneath(contour, mode="bottom"):
    """Fill the contour beneath the XY periphery. of a binary object.

    Parameters
    ----------
    contour : np.ndarray
        The contour to fill beneath.
    mode : str, optional
        Whether to fill from the bottom or the top. The default is 'bottom'.

    Returns
    -------
    cimg : np.ndarray
        The filled contour.
    """
    cimg = contour.copy()
    cimg = np.pad(cimg, 1)

    # Get the indices for the first and last non-zero elements
    first = (
        np.argmax(cimg, 0)
        if mode == "first"
        else np.zeros_like(cimg[0], dtype=np.uint16)
    )
    last = cimg.shape[0] - np.argmax(cimg[::-1], 0) - 1
    last[last == cimg.shape[0] - 1] = 0

    # Fill the contour
    for ii in range(cimg.shape[1]):
        for jj in range(cimg.shape[2]):
            cimg[first[ii, jj] : last[ii, jj], ii, jj] = True
    cimg[:, last == 0] = False
    cimg = cimg[1:-1, 1:-1, 1:-1]

    return cimg


def fill_contour(
    contour,
    fill_xy=False,
    fill_zx_zy=False,
    inplace=False,
    zrange=None,
    xrange=None,
    yrange=None,
):
    """Fill contour by closing all the edges (except for the top one), and
    applying a binary fill-holes operation. Note that this causes some errors
    if there is significant curvature on the contour, since the above-signal is
    down-projected. This can cause some erronous sharp edges which ruin the
    contour.

    Parameters
    ----------
    contour : np.ndarray
        Contour to operate on.

    fill_xy : bool, optional
        Flag to also fill in the xy-plane. Note that this can fill actual holes
        that arise if for example two relatively distant primordia touch each
        other at a point that isn't close to the meristem.

    inplace : bool, optional
        Flag to modify object in place.

    Returns
    -------
    new_contour : np.ndarray
        Contour after modification. If inplace == True, nothing is returned.

    Notes
    -----
    Assumes first dimension being Z, ordered from bottom to top. Will remove top
    and bottom slice.
    """
    if not inplace:
        new_contour = contour.copy()
    else:
        new_contour = contour

    new_contour = np.pad(new_contour, 1, "constant", constant_values=1)
    if xrange is None:
        xrange = [0, new_contour.shape[2]]
    else:
        xrange = list(xrange)
        xrange[0] = xrange[0] - 1
    if yrange is None:
        yrange = [0, new_contour.shape[1]]
    else:
        yrange = list(yrange)
        yrange[0] = yrange[0] - 1
    if zrange is None:
        zrange = [0, new_contour.shape[0]]
    else:
        zrange = list(zrange)
        zrange[0] = zrange[0] - 1

    # Close all sides but top
    new_contour[-1] = 0  # top

    # Fill holes form in xz & yz planes.
    if fill_zx_zy:
        for ii in range(*yrange):
            new_contour[
                zrange[0] : zrange[1],
                ii,
                xrange[0] : xrange[1],
            ] = binary_fill_holes(
                new_contour[zrange[0] : zrange[1], ii, xrange[0] : xrange[1]],
            )
        for ii in range(*xrange):
            new_contour[
                zrange[0] : zrange[1],
                yrange[0] : yrange[1],
                ii,
            ] = binary_fill_holes(
                new_contour[zrange[0] : zrange[1], yrange[0] : yrange[1], ii],
            )

    # Remove edges again, also for top
    new_contour[0] = 0
    new_contour[-1] = 0
    new_contour[:, 0] = 0
    new_contour[:, -1] = 0
    new_contour[:, :, 0] = 0
    new_contour[:, :, -1] = 0

    if fill_xy:
        for ii in range(*zrange):
            new_contour[
                ii,
                yrange[0] : yrange[1],
                xrange[0] : xrange[1],
            ] = binary_fill_holes(
                new_contour[ii, yrange[0] : yrange[1], xrange[0] : xrange[1]],
            )

    new_contour = binary_fill_holes(new_contour)
    new_contour = new_contour[1:-1, 1:-1, 1:-1]

    return None if inplace else new_contour


def label_mesh(
    mesh, segm_img, resolution=[1, 1, 1], background=0, mode="point", inplace=False
):
    """Label a mesh using the closest (by euclidean distance) voxel in a
    segmented image.

    Parameters
    ----------
    mesh : pyvista.PolyData
        Mesh to label.
    segm_img : np.ndarray
        Segmented image to use for labeling.
    resolution : list, optional
        Resolution of the segmented image.
    background : int, optional
        Background value in the segmented image.
    mode : str, optional
        Mode to use for labeling. Can be 'point' or 'face'.
    inplace : bool, optional
        Flag to modify object in place.

    Returns
    -------
    new_mesh : pyvista.PolyData
        Mesh after modification. If inplace is True, nothing is returned.
    """
    vertex_flags = [
        "point",
        "points",
        "pts",
        "pt",
        "p",
        "vertex",
        "vertices",
        "vert",
        "verts",
        "v",
    ]
    triangle_flags = [
        "cell",
        "cells",
        "c",
        "triangle",
        "triangles",
        "tri",
        "tris",
        "polygon",
        "polygons",
        "poly",
        "polys",
    ]

    # Get the coordinates of the points in the image
    coords = coord_array(segm_img, resolution).T
    img_raveled = segm_img.ravel()
    coords = coords[img_raveled != background]
    img_raveled = img_raveled[img_raveled != background]

    # Compute the closest coodinate to each point
    tree = cKDTree(coords)
    if mode.lower() in vertex_flags:
        closest = tree.query(mesh.points, k=1)[1]
    elif mode.lower() in triangle_flags:
        centers = mesh.cell_centers().points
        closest = tree.query(centers, k=1)[1]

    # Get the values of the closest points and either assign them to the mesh, or return them
    values = img_raveled[closest]
    if inplace:
        mesh["labels"] = values
    else:
        return values


def project2surface(
    mesh,
    int_img,
    distance_threshold,
    mask=None,
    resolution=[1, 1, 1],
    fct=np.sum,
    background=0,
):
    """Project values to a surface using a distance map. Values are aggregated
    per vertex in the mesh.

    Parameters
    ----------
    mesh : pyvista.PolyData
        Mesh to project values to.
    int_img : np.ndarray
        Image values to project.
    distance_threshold : np.ndarray
        Distance threshold from the surface of values to use for projection.
    mask : np.ndarray, optional
        Mask to apply to the image.
    resolution : list, optional
        Resolution of the image. Default is [1, 1, 1].
    fct : function, optional
        Function to use for aggregation of values. Applies to each vertex in the mesh Default is np.sum.
    background : int, optional
        Background value in the image. Default is 0.
    """

    # Get the coordinates and values of the points in the image
    coords = coord_array(int_img, resolution).T
    if mask is not None:
        int_img[~mask] = background
    img_raveled = int_img.ravel()

    # Don't consider background values
    coords = coords[img_raveled != background]
    img_raveled = img_raveled[img_raveled != background]

    # Filter out points clearly outside of the mesh to reduce computation time
    bounds = np.reshape(mesh.bounds, (-1, 2))
    for ii, bound_pair in enumerate(bounds):
        within_bounds = coords[:, ii] >= bound_pair[0] & coords[:, ii] <= bound_pair[1]
        img_raveled = img_raveled[within_bounds]
        coords = coords[within_bounds]

    # Get distance
    # Updating the normals is needed for the distance orientation
    mesh = mesh.compute_normals()
    ipd = vtk.vtkImplicitPolyDataDistance()
    ipd.SetInput(mesh)
    dists = np.zeros((len(coords),))
    pts = np.zeros((len(coords), 3))
    for ii in range(len(coords)):
        dists[ii] = ipd.EvaluateFunctionAndGetClosestPoint(coords[ii], pts[ii])

    # Filter out the external values
    internal_filter = dists > 0 if distance_threshold > 0 else dists < 0
    l1_coords = coords[internal_filter]

    # Now filter out the values that are too far away
    if distance_threshold < 0:
        l1_filter = dists > distance_threshold & dists < 0
    else:
        l1_filter = dists < distance_threshold & dists > 0
    l1_coords = coords[l1_filter]
    l1_vals = img_raveled[l1_filter]

    # Get the closest point to each vertex and sum up the values for the vertex
    if fct is not np.sum:
        raise NotImplementedError("fct : Only np.sum is implemented for now.")

    tree = cKDTree(mesh.points)
    closest = tree.query(l1_coords, k=1)[1]
    values = np.zeros(mesh.n_points)

    for ii, val in enumerate(l1_vals):
        values[closest[ii]] += val

    return values


def remove_inland_under(mesh, contour, threshold, resolution=[1, 1, 1], invert=False):
    """Remove the part of the mesh that is under the contour and that may have
    arisen due to holes in the contour.

     Parameters
     ----------
     mesh : pyvista.PolyData
         Mesh to remove the inland part from.
     contour : np.ndarray
         Contour to use for the removal.
     threshold : int
         Threshold distance from the contour XY periphery to use for the removal.
     resolution : list, optional
         Resolution of the image. Default is [1, 1, 1].
     invert : bool, optional
         Invert the mesh normals. Default is False.

     Returns
     -------
    output : pyvista.PolyData
         Mesh with the inland part removed.

     Notes
     -----
     This function is in development and may not work as expected.
    """
    # Compute the domain of interest
    cont2d = np.max(contour, 0)
    cont2d = np.pad(cont2d, pad_width=1, constant_values=0, mode="constant")
    distance_map = distance_transform_edt(cont2d)
    distance_map = distance_map[1:-1, 1:-1]
    larger = np.array(np.where(distance_map > threshold)).T
    c = cont2d.astype(int)
    c[larger[:, 0], larger[:, 1]] = 2

    xycoords = np.divide(mesh.points[:, 1:].copy(), resolution[1:])
    xycoords = np.round(xycoords).astype(int)
    xycoords[xycoords < 0] = 0
    xycoords[xycoords[:, 0] > contour.shape[1] - 1, 0] = contour.shape[1] - 1
    xycoords[xycoords[:, 1] > contour.shape[2] - 1, 0] = contour.shape[2] - 1
    inside = c[xycoords[:, 0], xycoords[:, 1]] == 2
    indices = np.where(inside)[0]

    # Use ray-tracing to identify if the point is under the mesh surface or not
    under_indices = []
    target = mesh.bounds[1] + 0.00001 if not invert else mesh.bounds[0] - 0.00001
    for ii in indices:
        pt = mesh.ray_trace(
            mesh.points[ii],
            [target, mesh.points[ii][1], mesh.points[ii][2]],
        )
        if pt[0].shape[0] > 1:
            under_indices.append(ii)
    under_indices = np.array(under_indices)
    under = np.zeros(mesh.n_points, bool)
    if len(under_indices) > 0:
        under[under_indices] = True

    output = mesh.remove_points(under)[0]
    return output


def fill_inland(contour, threshold_distance=0):
    """Fill the contour based on the distance to the contour XY periphery.

    Parameters
    ----------
    contour : np.ndarray
        Contour to fill.
    threshold_distance : int, optional
        Threshold distance from the contour XY periphery to use for the filling.
        Default is 0.

    Returns
    -------
    filled_contour : np.ndarray
        Filled contour.
    """
    # Get a maximum projection of the contour and compute the distane map
    cont2d = np.max(contour, 0)
    cont2d = np.pad(cont2d, pad_width=1, constant_values=0, mode="constant")
    distance_map = distance_transform_edt(cont2d)
    distance_map = distance_map[1:-1, 1:-1]
    larger = np.array(np.where(distance_map > threshold_distance)).T
    c = cont2d.astype(int)
    c[larger[:, 0], larger[:, 1]] = 2

    # Get the first and last indices in the Z-direction for each XY pixel
    first_occurence = np.argmax(contour, 0)
    last_occurence = contour.shape[0] - np.argmax(contour[::-1], 0) - 1
    last_occurence[last_occurence == contour.shape[0] - 1] = 0

    # Fill in the mask
    mask = np.zeros_like(contour)
    for ii in range(mask.shape[1]):
        for jj in range(mask.shape[2]):
            mask[first_occurence[ii, jj] : last_occurence[ii, jj], ii, jj] = True
    mask = mask & (c[1:-1, 1:-1] == 2)

    output = contour.copy()
    output[mask] = True
    output = fill_contour(output, True)

    return output


def repair_small(mesh, nbe=100, refine=True):
    """Repair small holes in a mesh based on the number of edges.

    Parameters
    ----------
    mesh : pyvista.PolyData
        Mesh to repair.
    nbe : int, optional
        Number of edges to use for the repair. Default is 100.
    refine : bool, optional
        Refine the mesh. Default is True.

    Returns
    -------
    output : pyvista.PolyData
        Repaired mesh.
    """
    mfix = PyTMesh(False)
    mfix.load_array(mesh.points, mesh.faces.reshape(-1, 4)[:, 1:])
    if nbe is None:
        nbe = -1
    mfix.fill_small_boundaries(nbe=nbe, refine=refine)
    vert, faces = mfix.return_arrays()

    output = pv.PolyData(vert, np.ravel(np.c_[[[3]] * len(faces), faces]))
    output = output.clean()
    output = output.triangulate()
    return output


def correct_bad_mesh(mesh, verbose=True):
    """Correct a bad (non-manifold) mesh with two methods: 1) method
    removesmallcomponents from the pymeshfixpackage, and 2) identifying
    leftover non-manifold edges and removing all the points in these.

    Parameters
    ----------
    mesh : pyvista.PolyData
        Input mesh.

    verbose : bool, optional
        Flag to print out operation procedure.

    Notes
    -----
    - Assumes a triangulated mesh.
    - Recalculation of cell and point attributes will have to be redone
    - All points in non-manifold edges will be removed. This could in principle
      be improved upon, since one point may be sufficient to create a manifold
      mesh.

    Returns
    -------
    new_poly : pyvista.PolyData
        Corrected mesh.
    """
    try:
        from pymeshfix import _meshfix
    except ImportError:
        raise ImportError(
            "Package pymeshfix not found. Install to use this function.",
        )

    new_poly = ECFT(mesh, 0)
    nm = non_manifold_edges(new_poly)

    while nm.n_points > 0:
        if verbose:
            print("Trying to remove %d points" % nm.GetNumberOfPoints())

        # Create pymeshfix object from our mesh
        meshfix = _meshfix.PyTMesh()
        v, f = mesh.points, mesh.faces.reshape(-1, 4)[:, 1:]
        meshfix.load_array(v, f)

        # Remove smaller components
        meshfix.remove_smallest_components()
        v2, f2 = meshfix.return_arrays()
        f2 = np.hstack([np.append(len(ii), ii) for ii in f2])

        # Create new polydata from cleaned out mesh
        new_poly = pv.PolyData(v2, f2)
        new_poly = ECFT(new_poly, 0)

        # If we still have non-manifold edges, force remove these points
        nm = non_manifold_edges(new_poly)
        nmpts = nm.points
        mpts = new_poly.points
        ptidx = np.array([np.where((mpts == ii).all(axis=1))[0][0] for ii in nmpts])

        mask = np.zeros((mpts.shape[0],), dtype=bool)
        if ptidx.shape[0] > 0:
            mask[ptidx] = True
        new_poly = new_poly.remove_points(mask)[0]

        new_poly = ECFT(new_poly, 0)
        nm = non_manifold_edges(new_poly)

    new_poly = ECFT(new_poly, 0)

    return new_poly


def remove_bridges(mesh, verbose=True):
    """Remove triangles where all vertices are part of the mesh.

    Parameters
    ----------
    mesh : pyvista.PolyData
        Mesh to operate on.

    verbose : bool, optional
        Flag to print processing steps.

    Notes
    -----
    Assumes triangulated mesh.

    Returns
    -------
    new_mesh : pyvista.PolyData
        Mesh after bridge removal.
    """
    new_mesh = mesh

    while True:
        # Retrieve triangles on the border
        faces = new_mesh.faces.reshape(-1, 4)[:, 1:]
        f_flat = faces.ravel()
        boundary = boundary_points(new_mesh)
        border_faces = faces[
            np.unique(
                np.where(np.in1d(f_flat, boundary))[0] // 3,
            )
        ]

        # Find pts to remove
        all_boundary = np.array([np.all(np.in1d(ii, boundary)) for ii in border_faces])
        remove_pts = np.unique(border_faces[all_boundary].flatten())

        if verbose:
            print("Removing %d points" % len(remove_pts))
        if len(remove_pts) == 0:
            break

        # Actually remove
        mask = np.zeros((new_mesh.n_points,), dtype=np.bool)
        mask[remove_pts] = True

        new_mesh = new_mesh.remove_points(mask, keep_scalars=False)[0]
        new_mesh = ECFT(new_mesh, 0)

    return new_mesh


def remove_normals(mesh, threshold_angle=0, flip=False, angle="polar"):
    """Remove points based on the point normal angle.

    Currently only considering the polar angle.

    Parameters
    ----------
    mesh : pyvista.PolyData
        Mesh on which to operate.

    threshold_angle : float, optional
        Threshold for the polar angle (theta). Values smaller than this will be
        removed. Default = 0.

    flip : bool, optional
         Flag to flip normal orientation. Default = False.

    Returns
    -------
    new_mesh : pyvista.PolyData
        Mesh with the resulting vertices removed.
    """
    normals = mesh.point_normals.copy()
    if flip:
        normals *= -1.0
    normals = car2sph(normals) / (2.0 * np.pi) * 360.0

    if angle == "polar":
        angle_index = 1
    elif angle == "azimuth":
        angle_index = 2
    else:
        raise ValueError(
            "Parameter 'angle' can only take attributes 'polar' and 'azimuth'.",
        )

    to_remove = normals[:, angle_index] < threshold_angle
    new_mesh = mesh.remove_points(to_remove, keep_scalars=False)[0]
    return new_mesh


def smooth_boundary(mesh, iterations=20, sigma=0.1, inplace=False):
    """Smooth the boundary of a mesh using Laplacian smoothing:

    .. math::
        x_{n+1} = x_n - \sigma (x_n - \sum_{j \in \mathcal{N}_x} x_j} / \vert \mathcal{N}_x \vert)

    Parameters
    ----------
    mesh : pyvista.PolyData
        Mesh to smooth.
    iterations : int, optional
        Number of smoothing iterations.  Default is 20.
    sigma : float, optional
        Smoothing sigma.  Default is 0.1.
    inplace : bool, optional
        Update mesh in-place.  Default is False.

    Returns
    -------
    pyvista.PolyData
        Smoothed mesh.
    """
    mesh = mesh.copy() if not inplace else mesh

    # Get boundary information and index correspondences
    boundary = boundary_edges(mesh)
    bdpts = boundary.points
    from_ = np.array([mesh.FindPoint(ii) for ii in bdpts])

    # TODO this method does not work on a skeletonized mesh, but it would be far more
    # computationally effective doing that
    neighs = []
    for ii in range(boundary.n_points):
        pt_neighs = vertex_neighbors(boundary, ii, include_self=False)
        for jj in range(pt_neighs.shape[0]):
            neighs.append((ii, pt_neighs[jj]))

    # Find holes (cycles) in the mesh
    net = nx.Graph(neighs)
    cycles = nx.cycle_basis(net)
    cycles.sort(key=lambda x: len(x), reverse=True)
    cycles = [np.array(ii) for ii in cycles]

    # Smooth boundary using Laplacian smoothing:
    # x_new = x_old - sigma * (x_old - mean(x_xneighs))
    new_pts_prev = bdpts.copy()
    new_pts_now = bdpts.copy()
    for iter in range(iterations):
        new_pts_prev = new_pts_now.copy()
        for ii in range(len(cycles)):
            for jj in range(len(cycles[ii])):
                new_pts_now[cycles[ii][jj]] = new_pts_prev[cycles[ii][jj]] - sigma * (
                    new_pts_prev[cycles[ii][jj]]
                    - np.mean(
                        np.array(
                            [
                                new_pts_prev[cycles[ii][jj]],
                                new_pts_prev[cycles[ii][jj - 1]],
                                new_pts_prev[cycles[ii][(jj + 1) % len(cycles[ii])]],
                            ],
                        ),
                        axis=0,
                    )
                )

    # Update coordinates
    for ii in range(len(cycles)):
        mesh.points[from_[cycles[ii]]] = new_pts_now[cycles[ii]]

    return None if inplace else mesh


def process_mesh(
    mesh,
    hole_repair_threshold=100,
    downscaling=0.01,
    upscaling=2,
    threshold_angle=60,
    top_cut="center",
    tongues_radius=None,
    tongues_ratio=4,
    smooth_iter=200,
    smooth_relax=0.01,
    curvature_threshold=0.4,
    inland_threshold=None,
    contour=None,
):
    """Convenience function for postprocessing a mesh.

     Parameters
     ----------
     mesh : pyvista.PolyData
         Mesh to process.
     hole_repair_threshold : float, optional
         Threshold for the hole repair algorithm.  Default is 100.
     downscaling : float, optional
         Downscaling factor for the mesh.  Default is 0.01.
     upscaling : float, optional
         Upscaling factor for the mesh.  Default is 2.
     threshold_angle : float, optional
         Threshold for the polar angle (theta). Values smaller than this will be
         removed. Default = 60.
     top_cut : str or tuple, optional
         Top cut location.  Default is 'center'.
     tongues_radius : float, optional
         Radius of the tongues.  Default is None.
     tongues_ratio : float, optional
         Ratio of the tongues.  Default is 4.
     smooth_iter : int, optional
         Number of smoothing iterations.  Default is 200.
     smooth_relax : float, optional
         Smoothing relaxation factor.  Default is 0.01.
     curvature_threshold : float, optional
         Threshold for the curvature.  Default is 0.4.
     inland_threshold : float, optional
         Threshold for the inland removal.  Default is None.
     contour : pyvista.PolyData, optional
         Contour to use for the inland removal.  Default is None.

     Returns
     -------
    mesh :  pyvista.PolyData
         Processed mesh.
    """

    if top_cut == "center":
        top_cut = (mesh.center[0], 0, 0)

    # Scale the mest and repair small holes
    mesh = remesh(mesh, int(mesh.n_points * downscaling), sub=0)
    mesh = repair_small(mesh, hole_repair_threshold)

    # Remove vertices based on the vertex normal angle
    if threshold_angle:
        mesh.rotate_y(-90)
        mesh = remove_normals(
            mesh,
            threshold_angle=threshold_angle,
            angle="polar",
        )
        mesh.rotate_y(90)
        mesh = make_manifold(mesh, hole_repair_threshold)
        mesh = mesh.extract_largest()
        mesh.clear_arrays()
        mesh = correct_normal_orientation_topcut(mesh, top_cut)

    # Remove vertices based on whether they are "inside the contour"
    if inland_threshold is not None:
        mesh = remove_inland_under(mesh, contour, threshold=inland_threshold)
        mesh = mesh.extract_largest()
        mesh = repair_small(mesh, hole_repair_threshold)
    mesh = ECFT(mesh, hole_repair_threshold)

    # Remove "tongues" from the mesh
    if tongues_radius is not None:
        mesh = remove_tongues(
            mesh,
            radius=tongues_radius,
            threshold=tongues_ratio,
            hole_edges=hole_repair_threshold,
        )

    # General post-processing. Smooth the mesh, remove small holes, and regularise the faces.
    mesh = mesh.extract_largest()
    mesh = repair_small(mesh, hole_repair_threshold)
    mesh = mesh.smooth(smooth_iter, smooth_relax)
    mesh = remesh(mesh, upscaling * mesh.n_points)
    mesh = smooth_boundary(mesh, smooth_iter, smooth_relax)

    return mesh


def remove_tongues(mesh, radius, threshold=6, hole_edges=100, verbose=True):
    """Remove "tongues" in mesh.

    All boundary points within a given radius are considered. The ones where the
    fraction of the distance along the boundary, as divided by the euclidean
    distance, is greater than the given threshold.

    Parameters
    ----------
    mesh : pyvista.PolyData
        Mesh to operate on.

    radius : float
        Radius for boundary point neighbourhood.

    threshold : float, optional
        Threshold for fraction between boundary distance and euclidean distance.
        Default = 6.

    Returns
    -------
    mesh : pyvista.PolyData
        Resulting mesh.
    """
    while True:
        # Get boundary information and index correspondences
        boundary = boundary_edges(mesh)
        bdpts = boundary.points
        from_ = np.array([mesh.FindPoint(ii) for ii in bdpts])

        all_neighs = vertex_neighbors_all(mesh, include_self=False)
        all_edges = []
        for ii, pt_neighs in enumerate(all_neighs):
            for jj, neigh in enumerate(pt_neighs):
                all_edges.append((ii, neigh))
        all_edges = np.array(all_edges)

        weighted_all_edges = np.c_[
            all_edges,
            np.sum(
                (mesh.points[all_edges[:, 0]] - mesh.points[all_edges[:, 1]]) ** 2,
                1,
            )
            ** 0.5,
        ]
        all_net = nx.Graph()
        all_net.add_weighted_edges_from(weighted_all_edges)

        # Find the cycles, i.e. the different boundaries we have
        # list(get_connected_vertices_all(boundary, include_self=False))
        neighs = []
        for ii in range(boundary.n_points):
            pt_neighs = vertex_neighbors(boundary, ii, include_self=False)
            for jj in range(pt_neighs.shape[0]):
                neighs.append((ii, pt_neighs[jj]))
        neighs = np.array(neighs)

        weighted_edges = np.c_[
            neighs,
            np.sum(
                (bdpts[neighs[:, 0]] - bdpts[neighs[:, 1]]) ** 2,
                1,
            )
            ** 0.5,
        ]
        bdnet = nx.Graph()
        bdnet.add_weighted_edges_from(weighted_edges)

        cycles = nx.cycle_basis(bdnet)
        cycles.sort(key=lambda x: len(x), reverse=True)
        cycles = [np.array(ii, dtype=int) for ii in cycles]
        # boundary.plot(notebook=False, scalars=np.isin(np.arange(boundary.n_points), cycles[-1]).astype('int'), line_width=3)

        # Loop over the cycles and find boundary points within radius
        to_remove = []
        for ii, cycle in enumerate(cycles):
            if verbose:
                print(f"Running cycle {ii} with {len(cycle)} points")
            cpts = bdpts[cycle]

            # Get the boundary points (in same loop) within a certain radius
            tree = cKDTree(cpts)
            neighs = tree.query_ball_point(cpts, radius)
            neighs = [np.array(neigh) for neigh in neighs]
            neighs = [neigh[neigh != idx] for idx, neigh in enumerate(neighs)]

            # Get shortest geodesic path from every point in the cycle to all of it's
            # neighbours within the radius
            bd_dists, int_dists = [], []
            for jj in range(len(cpts)):
                bd_path_lengths, int_path_lengths = [], []
                for kk in range(len(neighs[jj])):
                    bd_length = nx.shortest_path_length(
                        bdnet,
                        source=cycle[jj],
                        target=cycle[neighs[jj][kk]],
                        weight="weight",
                    )
                    int_length = nx.shortest_path_length(
                        all_net,
                        source=from_[cycle[jj]],
                        target=from_[cycle[neighs[jj][kk]]],
                        weight="weight",
                    )

                    bd_path_lengths.append(bd_length)
                    int_path_lengths.append(int_length)

                bd_path_lengths = np.array(bd_path_lengths)
                int_path_lengths = np.array(int_path_lengths)
                bd_dists.append(bd_path_lengths)
                int_dists.append(int_path_lengths)

            frac = [bd_dists[jj] / int_dists[jj] for jj in range(len(neighs))]

            # Find which ones to (possibly) remove
            removal_anchors = []
            for kk in range(len(frac)):
                for jj in range(len(frac[kk])):
                    if frac[kk][jj] > threshold:
                        removal_anchors.append((kk, neighs[kk][jj]))
            removal_anchors = np.array(removal_anchors)

            # Recalculate the geodesic path between two points
            for jj in range(len(removal_anchors)):
                gdpts = nx.shortest_path(
                    all_net,
                    source=from_[cycles[ii][removal_anchors[jj][0]]],
                    target=from_[cycles[ii][removal_anchors[jj][1]]],
                    weight="weight",
                )
                gdpts = np.array(gdpts, dtype="int")
                to_remove.extend(gdpts)

        to_remove = np.unique(to_remove)

        if len(to_remove) == 0:
            break

        # Remove points and do some cleanup
        mesh = mesh.remove_points(to_remove, keep_scalars=False)[0]
        mesh = repair_small(mesh, hole_edges)
        mesh = make_manifold(mesh, hole_edges)
        mesh = ECFT(mesh, hole_edges)

    mesh = mesh.clean()
    return mesh


def repair(mesh):
    """Repair a mesh using MeshFix."""
    tmp = pmf.MeshFix(mesh)
    tmp.repair(True)
    return tmp.mesh


def remesh(mesh, n, sub=3):
    """Regularise the mesh faces using the ACVD algorithm.

    Parameters
    ----------
    mesh : pyvista.PolyData
        The mesh to regularise.
    n : int
        The number of clusters (i.e. output number of faces) to use.
    sub : int, optional
        The number of subdivisions to use when clustering.  The default is 3.

    Returns
    -------
    output : pyvista.PolyData
        The regularised mesh.
    """
    clus = clustering.Clustering(mesh)
    clus.subdivide(sub)  # 2 also works
    clus.cluster(n)
    output = clus.create_mesh()
    output = output.clean()
    return output


def make_manifold(mesh, hole_edges=300):
    """Make a mesh manifold by removing non-manifold edges."""
    mesh = mesh.copy()
    edges = mesh.extract_feature_edges(
        boundary_edges=False,
        feature_edges=False,
        manifold_edges=False,
        non_manifold_edges=True,
    )
    while edges.n_points > 0:
        to_remove = [mesh.FindPoint(pt) for pt in edges.points]
        print(f"Removing {len(to_remove)} points")
        mesh = mesh.remove_points(to_remove)[0]
        mesh = mesh.extract_largest()
        mesh = repair_small(mesh, nbe=hole_edges)
        mesh = mesh.clean()
        edges = mesh.extract_feature_edges(
            boundary_edges=False,
            feature_edges=False,
            manifold_edges=False,
            non_manifold_edges=True,
        )

    return mesh


def drop_skirt(mesh, maxdist, flip=False):
    """Downprojects the boundary to the lowest point in the z-direction.

    Parameters
    ----------
    mesh : pyvista.PolyData
        Mesh to operate on.

    maxdist : float
        Distance in z-direction from the lowest point in the mesh to consider.

    Returns
    -------
    new_mesh : pyvista.PolyData
        Mesh with boundary downprojected.
    """
    lowest = mesh.bounds[int(flip)]
    boundary = boundary_edges(mesh)

    mpts = mesh.points
    bdpts = boundary.points
    idx_in_parent = np.array([mesh.FindPoint(ii) for ii in bdpts])

    to_adjust = idx_in_parent[bdpts[:, 0] - lowest < maxdist]
    mpts[to_adjust, 0] = lowest

    new_mesh = pv.PolyData(mpts, mesh.faces)

    return new_mesh


def boundary_points(mesh):
    """Get vertex indices of points in the boundary."""
    boundary = boundary_edges(mesh)
    bdpts = boundary.points
    indices = np.array([mesh.FindPoint(ii) for ii in bdpts])

    return indices


def remesh_decimate(mesh, iters, upfactor=2, downfactor=0.5, verbose=True):
    """Iterative remeshing/decimation.

    Can be thought of as an alternative
    smoothing approach. The input mesh is remeshed with a factor times the
    original number of vertices, and then downsampled by another factor.

    Parameters
    ----------
    mesh : pyvista.PolyData
        Mesh to operate on.

    iters : int
        Number of iterations.

    upfactor : float, optional
        Factor with which to upsample. Default = 2.

    downfactor : float, optional
        Factor with which to downsample. Default = 0.5.

    verbose : bool, optional
        Flag for whether to print operation steps. Default = True.

    Returns
    -------
    mesh : pyvista.PolyData
        Processed mesh.
    """
    for ii in range(iters):
        mesh = correct_bad_mesh(mesh, verbose=verbose)
        mesh = ECFT(mesh, 0)

        mesh = remesh(mesh, mesh.GetNumberOfPoints() * 2)
        mesh = mesh.compute_normals(inplace=False)
        mesh = mesh.decimate(
            0.5,
            volume_preservation=True,
            normals=True,
            inplace=False,
        )
        mesh = ECFT(mesh, 0)

    return mesh


def non_manifold_edges(mesh):
    """Get non-manifold edges."""
    edges = mesh.extract_feature_edges(
        boundary_edges=False,
        non_manifold_edges=True,
        feature_edges=False,
        manifold_edges=False,
    )
    return edges


def boundary_edges(mesh):
    """Get boundary edges."""
    edges = mesh.extract_feature_edges(
        boundary_edges=True,
        non_manifold_edges=False,
        feature_edges=False,
        manifold_edges=False,
    )
    return edges


def manifold_edges(mesh):
    """Get manifold edges."""
    edges = mesh.extract_feature_edges(
        boundary_edges=False,
        non_manifold_edges=False,
        feature_edges=False,
        manifold_edges=True,
    )
    return edges


def feature_edges(mesh, angle=30):
    """Get feature edges defined by given angle."""
    edges = mesh.extract_feature_edges(
        feature_angle=angle,
        boundary_edges=False,
        non_manifold_edges=False,
        feature_edges=True,
        manifold_edges=False,
    )
    return edges


def vertex_neighbors(mesh, index, include_self=True):
    """Get the indices of the vertices connected to a given vertex.

    Parameters
    ----------
    mesh : pyvista.PolyData
        Mesh to operate on.
    index : int
        Index of the vertex.
    include_self : bool, optional
        Whether to include the vertex itself in the list of neighbors.
        Default = True.

    Returns
    -------
    connected_vertices : list
        List of indices of the connected vertices.
    """
    connected_vertices = []
    if include_self:
        connected_vertices.append(index)

    cell_id_list = vtk.vtkIdList()
    mesh.GetPointCells(index, cell_id_list)

    # Loop through each cell using the seed point
    for ii in range(cell_id_list.GetNumberOfIds()):
        cell = mesh.GetCell(cell_id_list.GetId(ii))

        if cell.GetCellType() == 3:
            point_id_list = cell.GetPointIds()

            # add the point which isn't the seed
            to_add = (
                point_id_list.GetId(1)
                if point_id_list.GetId(0) == index
                else point_id_list.GetId(0)
            )
            connected_vertices.append(to_add)
        else:
            # Loop through the edges of the point and add all points on these.
            for jj in range(cell.GetNumberOfEdges()):
                point_id_list = cell.GetEdge(jj).GetPointIds()

                # add the point which isn't the seed
                to_add = (
                    point_id_list.GetId(1)
                    if point_id_list.GetId(0) == index
                    else point_id_list.GetId(0)
                )
                connected_vertices.append(to_add)

    connected_vertices = np.unique(connected_vertices)

    return connected_vertices


def vertex_neighbors_all(mesh, include_self=True):
    """Get all vertex neighbors.

    Parameters
    ----------
    mesh : pyvista.PolyData
        Mesh to operate on.
    include_self : bool, optional
        Whether to include the vertex itself in the list of neighbors.
        Default = True.

    Returns
    -------
    connectivities : list
        List of lists of indices of the connected vertices.
    """
    connectivities = [[]] * mesh.n_points
    for ii in range(mesh.n_points):
        connectivities[ii] = vertex_neighbors(mesh, ii, include_self)

    return connectivities


def correct_normal_orientation_topcut(mesh, origin):
    """Correct normal orientation of a mesh by flipping normals if the sum of
    the normals is negative after having cropped off the top of the mesh."""

    mesh.clear_arrays()
    if mesh.clip(normal="-x", origin=origin).point_normals[:, 0].sum() > 0:
        mesh.flip_normals()
    return mesh


def ECFT(mesh, hole_edges=300, inplace=False):
    """Perform ExtractLargest, Clean, FillHoles, and TriFilter operations in
    sequence.

    Parameters
    ----------
    mesh : pyvista.PolyData
        Mesh to operate on.

    holesize : float, optional
        Size of holes to fill. Default = 100.0.

    inplace : bool, optional
        Flag for performing operation in-place. Default = False.

    Returns
    -------
    new_mesh : pyvista.PolyData
        Mesh after operation. Returns None if inplace == True.
    """
    if inplace:
        new_mesh = mesh
    else:
        new_mesh = mesh.copy()

    new_mesh = new_mesh.extract_largest()
    new_mesh = new_mesh.clean()
    new_mesh = repair_small(mesh, nbe=hole_edges)
    new_mesh = new_mesh.triangulate()
    new_mesh.clean()

    return None if inplace else new_mesh


def define_meristem(mesh, method="central_mass", res=(1, 1, 1), return_coord=False):
    """Determine which domain in the segmentation that corresponds to the
    meristem. Some methods are deprecated and should not be used.

    Parameters
    ----------
        mesh : pyvista.PolyData
        Mesh to operate on.

    pdata : pd.DataFrame
        Corresonding point data for input mesh.

    method : str, optional
        Method for defining the meristem to use. Default = 'central_mass'.

    res : 3-tuple, optional
        Resolution of the dimensions. Default = (1,1,1).

    fluo : np.ndarray, optional
        Intensity matrix.

    Returns
    -------
    meristem, ccoord : int, 3-tuple
        Domain index of the meristem, as well as the center coordinates using
        the given method.
    """
    # TODO: Sort out this function
    ccoord = np.zeros((3,))
    if method == "central_mass":
        com = vtk.vtkCenterOfMass()
        com.SetInputData(mesh)
        com.Update()
        ccoord = np.array(com.GetCenter())
    elif method == "central_bounds":
        ccoord = np.mean(np.reshape(mesh.GetBounds(), (3, 2)), axis=1)

    m_idx = np.argmin(((mesh.points - ccoord) ** 2).sum(1) ** 0.5)
    meristem = mesh["domains"][m_idx]
    if return_coord:
        return meristem, ccoord
    else:
        return meristem


def erode(mesh, iterations=1):
    mesh = mesh.copy()
    for iter_ in range(iterations):
        if mesh.n_points == 0:
            break
        mesh = mesh.remove_points(boundary_points(mesh))[0]
    return mesh


def fit_paraboloid(data, init=[1, 1, 1, 1, 1, 0, 0, 0], return_success=False):
    """Fit a paraboloid to arbitrarily oriented 3D data.

    The paraboloid data can by oriented along an arbitrary axis --
    not necessarily x, y, z. The function rotates the data points and returns
    the rotation angles along the x, y, z axis.

    Returns the parameters for a paraboloid along the z-axis. The angles can be
    used to correct the paraboloid for rotation.

    Paraboloid equation : p1 * x**2. + p2 * y**2. + p3 * x + p4 * y + p5 = z

    Parameters
    ----------
    data : np.ndarray
        Data to fit the paraboloid to.

    init : 8-tuple
        Initial parameters for the paraboloid.

    Returns
    -------
    popt : np.array
        Parameters after optimisation.
    """

    def errfunc(p, coord):
        p1, p2, p3, p4, p5, alpha, beta, gamma = p
        coord = rotate(coord, [alpha, beta, gamma])

        x, y, z = np.array(coord).T
        return abs(p1 * x**2.0 + p2 * y**2.0 + p3 * x + p4 * y + p5 - z)

    popt, _1, _2, _3, _4 = opt.leastsq(
        errfunc,
        init,
        args=(data,),
        full_output=True,
    )
    if return_success:
        return popt, _4 in [1, 2, 3, 4]
    return popt


def vertex_cycles(mesh):
    """Find cycles (holes/boundaries) in a mesh.

    Parameters
    ----------
    mesh : pyvista.PolyData
        Mesh to operate on.

    Returns
    -------
    cycles : list
        List of cycles, each cycle is a list of vertex indices.
    """
    neighs = vertex_neighbors(mesh, True)
    pairs = []
    for ii in range(mesh.n_points):
        for pp in neighs[ii]:
            pairs.append((ii, pp))
    net = nx.Graph(pairs)
    cycles = nx.cycle_basis(net)
    cycles.sort(key=lambda x: len(x), reverse=True)
    return cycles


""" def connect_bottom(mesh, offset=0, invert=False, inplace=False):
    boundary = mesh.extract_feature_edges(0, 1, 0, 0, 0).extract_largest()

    cycles = vertex_cycles(boundary)
    cycle = np.array(cycles[0])

    corresp_in_orig = np.array([
        mesh.FindPoint(pp)
        for pp in boundary.points[cycle]
    ])

    pts = mesh.points
    faces = mesh.faces.reshape((-1, 4))[:, 1:]

    pts = np.vstack([mesh.points, boundary.center_of_mass()])
    if invert:
        pts[-1, 0] = np.min(mesh.points[:, 0]) - offset
    else:
        pts[-1, 0] = np.max(mesh.points[:, 0]) + offset

    faces_to_append = []
    for ii in range(corresp_in_orig.shape[0]):
        faces_to_append.append(
            [corresp_in_orig[ii], corresp_in_orig[ii - 1], len(pts) - 1],
        )
    faces = np.vstack([faces, faces_to_append])
    faces = np.hstack([[[3]] * len(faces), faces])
    faces = np.ravel(faces)

    if inplace:
        mesh.points = pts
        mesh.faces = faces
        return
    else:
        return pv.PolyData(pts, faces)
 """


def correct_normal_orientation(mesh, relative="x", inplace=False):
    """Correct the orientation of the normals of a mesh."""
    mesh = mesh if inplace else mesh.copy()
    normals = mesh.point_normals

    if (
        (relative == "x" and normals[:, 0].sum() > 0)
        or (relative == "y" and normals[:, 1].sum() > 0)
        or (relative == "z" and normals[:, 2].sum() > 0)
    ):
        mesh.flip_normals()

    return None if inplace else mesh


def fit_paraboloid_mesh(mesh, return_coord=False):
    """Fit a paraboloid to a mesh.

    Parameters
    ----------
    mesh : pyvista.PolyData
        Mesh to fit paraboloid to.

    Returns
    -------
    popt, apex : 8-tuple, 3-tuple
        Parameters for the paraboloid, as well as the coordinates for the
        paraboloid apex.
    """
    popt = fit_paraboloid(
        mesh.points,
    )
    if return_coord:
        apex = paraboloid_apex(popt)
        return popt, apex
    else:
        return popt


def paraboloid_apex(p):
    """Return the apex coordinates of a paraboloid.

    Use the return of fit_paraboloid() to compute the apex of the paraboloid.
    The return is in the coordinate system of the data, meaning that the
    coordinates have been corrected for the rotation angles.

    Parameters
    ----------
    p : 8-tuple
        Parameters defining the paraboloid.

    Returns
    -------
    coords : np.array
        Coordinates for the paraboloid apex.
    """
    p1, p2, p3, p4, p5, alpha, beta, gamma = p
    x = -p3 / (2.0 * p1)
    y = -p4 / (2.0 * p2)
    z = p1 * x**2.0 + p2 * y**2.0 + p3 * x + p4 * y + p5

    coords = rotate(
        np.array(
            [
                [x, y, z],
            ],
        ),
        [alpha, beta, gamma],
        True,
    )[0]

    return coords


""" def downproject_border(mesh, value, axis=0, flip=False):

    lowest = value
    boundary = boundary_edges(mesh)

    mpts = mesh.points
    bdpts = boundary.points
    idx_in_parent = np.array([mesh.FindPoint(ii) for ii in bdpts])

    to_adjust = idx_in_parent[bdpts[:, 0] > value]
    mpts[to_adjust, axis] = lowest

    new_mesh = pv.PolyData(mpts, mesh.faces)

    return new_mesh
 """
