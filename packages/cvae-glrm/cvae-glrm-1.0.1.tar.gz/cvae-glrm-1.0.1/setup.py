#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 13 22:41:42 2023

@author: hill103
"""



import setuptools



with open("requirements.txt", "r") as f:
    requirements = [line.strip() for line in f.readlines()]


with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="cvae-glrm",    # short and all lower case
    version="1.0.1",
    author="Ningshan Li",
    author_email="hill103.2@gmail.com",
    description="Conditional Variational AutoEncoder - Graph Laplacian Regularized Model",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/az7jh2/CVAE-GLRM",
    python_requires=">=3.9.12",    # Minimum Python version
    install_requires=requirements,    # Dependencies
    license_files=["LICENSE"],     # License file
    package_dir={"": "src"},    # py files are in src folder
    # no need to specify 'packages=' since we only have one 'package' corresonding to the src folder
    # also no need to specify 'py_modules=', all py files under src folder will be recognized as modules
    include_package_data=True,    # Must be true to include files
    entry_points = {    # create wrappers for globally accessible function in Python scripts; only function are supported
        "console_scripts": [
            "runCVAEGLRM = cvaeglrm:main",
            "runImputation = imputation:main"
        ]
    },
    classifiers=[
        # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent"]
)