# -*- coding: UTF-8 -*-

import setuptools
from setuptools import setup, find_packages

# read the contents of your README file
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="napalm_nokia_olt",
    version="0.0.1",
    author="Dave Macias",
    description=("Network Automation and Programmability Abstraction "
                 "Layer driver for NOKIA OLT "),
    keywords="napalm driver",
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        "Topic :: Utilities",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: BSD License",
    ],
    include_package_data=True,
    install_requires=('napalm>=3',),
)   
