#!/usr/bin/python3.7
# -*- coding: utf-8 -*-


from os import path

from setuptools import setup, find_packages

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(

    name='hpc2ml',
    version='0.0.01',
    description='Crystal extension for pytorch_geometric',
    install_requires=["pymatgen", "ase", "mgetool>=0.0.60"],
    # install_requires=['torch-geometric', "torch", "pymatgen", "ase", "mgetool"],
    include_package_data=True,
    author='wangchangxin',
    author_email='986798607@qq.com',
    python_requires='>=3.6',
    maintainer='wangchangxin',
    platforms=[
        "Windows",
        "Unix",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Natural Language :: English",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: Unix",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],

    packages=find_packages(
        exclude=["*.tests", "*.tests.*", "tests.*", "tests", "test"], ),
    long_description=long_description,
    long_description_content_type='text/markdown'
)
