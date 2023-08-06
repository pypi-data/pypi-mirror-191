#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
==========================================================
Setup file for LomPy Version 0.1.12
==========================================================

Setup.py to building the wheel for the LomPy package
"""
#Copyright (C) 2023 GNU AGPLv3, LomPy 2023, S.G. Roux and J. Lengyel.
#All rights reserved.

#Contact: stephane.roux@ens-lyon.fr, jankalengyel@gmail.com
#Other Contributors: P. Thiraux, F Semecurbe

from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    readme = fh.read()

setup(
   name='lompy',
   version='0.1.13',
   author='S.G. Roux, J. Lengyel',
   author_email='jankalengyel@gmail.com',
   packages=find_packages(),
   url='https://gitlab.com/sroux67/LomPy',
   license='GNU AGPLv3',
   description='Local Multiscale Analysis of Marked Point Processes',
   long_description = readme,
   install_requires=['pyfftw','numpy','geopandas','matplotlib'],
   platforms=['any'],
   entry_points={"console_scripts": ["lompy = lompy.lompy:main"]},
   #long_description=open('README.txt').read(),
   #install_requires=[],
)