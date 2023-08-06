"""
======================================================
LomPy (:mod:`lompy`)
======================================================
A python package for the multiscale analysis of spatial point processes

          
.. currentmodule: lompy

======================================================== 
Core functions:

The 'RD' package features yield the multiresolution quantities and the local 
scaling parameters  for uniformly distributed (raster) 2D data

These 'RD' package features yield the multiresolution quantities and local scaling 
parameters for non-uniformly distributed (vector) 2D data

Overview
--------
Routines for the muliresolution quantities:
    
    lompy.MultiresQuantityRD
    lompy.MultiresQuantityVD
    
Routines for the univariate local analysis:
    
    lompy.LocalMsAnalysisRD
    lompy.LocalMsAnalysisVD

Routines for the bivariate local analysis:
    
    lompy.LocalCorrAnalysisRD
    lompy.LocalCorrAnalysisVD

========================================================   
The package includes vizualization routines built on NumPy,
GeoPandas and Matplotlib:

Overview
--------

Vizualization Routine 1:
    
    LomPy.img_arrayVD
    LomPy.img_arrayRD
    
    
Vizualization Routine 2:
    
    LomPy.global_scalingVD
    LomPy.global_scalingRD

Vizualization Routine 3:
    
    LomPy.plot_histo_VD
    LomPy.plot_histo_RD
    
Vizualization Routine 4:
    LomPy.plot_gdf_fit
    LomPy.plot_gdf_radius
    
========================================================   
The package features include a powerful function for linear regression
analysis on large data and other data pre-, and post-processing functions
to aid the workflow with the LomPy package:

Overview
--------
Routines for the linear regression analysis:
    
    lompy.fitwithNan
    
Routines for the histogram computation across scales:
    
    lompy.computehistogramNoNorm

Routines for building a geopandas dataframe from LomPy results:
    
    lompy.build_gdf
    
"""

#Copyright (C) 2023 GNU AGPLv3, LomPy 2023, S.G. Roux and J. Lengyel.
#All rights reserved.
#Contact: stephane.roux@ens-lyon.fr, jankalengyel@gmail.com
#Other Contributors: P. Thiraux, F. Semecurbe

#%%

import warnings
import numpy as np
import pyfftw
import multiprocessing
import types
from sklearn.neighbors import KDTree
from sklearn.neighbors import NearestNeighbors
from functools import partial
import sys
from concurrent.futures import ThreadPoolExecutor
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd
from scipy.stats import t
import pandas as pd
from shapely.geometry import Polygon


#%%
def checkinputdata(data):
    """
    Check the type of data.
    Image (uniformly sampled)?
    Marked?
    How many marks?
    
    isimage, ismarked, Nmark = checkinputdata(data)

    Parameters
    ----------
    data : numpy array of float
        The data to check.

    Returns
    -------
    isimage : Boolean
        Equal to 1 if the data is an image.
    ismarked : Boolean
        Equal to 1 if the data ia a marked point process.
    Nmark : int
        Number oif mark in the data.

    """
    # check input data
    si=data.shape
    if len(si)==1:
        print('Error : the input argument must have at least two dimensions')
        return
    else:
        
        if (si[0]>100) & (si[1]>100):
            isimage=1
            if len(si)>2:
                #print('The input seems to be a set of  images  of size ({:d},{:d}))'.format(si[2]),si[0])
                print('The input seems to be a set of  {:d}  images  of size ({:d},{:d})).'.format(si[2],si[0],si[1]))
                ismarked = 1
                Nmark = si[2]
            else:
                print('The input seems to be an image of size ({:d},{:})'.format(si[0],si[1]))
                ismarked = 0
                Nmark = 0
        else:
            isimage=0
            if si[1]>2:
                print('The input seems to be a marked point process with {:} points and {:d} marks.'.format(si[0],si[1]-2))
                
                ismarked = 1
                Nmark = si[1]-2
            else:
                print('The input seems to be a marked point process with {:} points.'.format(si[0]))
                ismarked = 0
                Nmark = 0
    return isimage, ismarked, Nmark