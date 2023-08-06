#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

import numpy as np
from Cython.Build import cythonize
from setuptools import find_packages, setup

# Description files
with open("README.rst") as readme_file:
    readme = readme_file.read()
with open("HISTORY.rst") as history_file:
    history = history_file.read()
with open("requirements.txt") as reqs_file:
    reqs = reqs_file.read()
with open("requirements_dev.txt") as reqs_dev_file:
    reqs_dev = reqs_dev_file.read()

# Requirements & test
setup_requirements = reqs
test_requirements = reqs_dev

# Actual setup
setup(
    author="Henrik Ahl",
    author_email="hpa22@cam.ac.uk",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.9",
    ],
    description="3D plant phenotyping.",
    install_requires=setup_requirements,
    license="GNU General Public License v3",
    long_description=readme + "\n\n" + history,
    include_package_data=True,
    keywords="phenotastic",
    name="phenotastic",
    # ext_modules=cythonize('**/*.pyx'),
    include_dirs=[np.get_include()],
    packages=find_packages(include=["phenotastic", "phenotastic.*"]),
    setup_requires=setup_requirements,
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/supersubscript/phenotastic",
    version="0.3.0",
    zip_safe=False,
)
