
"""
================================================================
Auxiliary routines of the LomPy package  (:mod:`lompy.aux`)
================================================================

.. currentmodule: lompy.aux

The package features include a powerful function for linear regression
analysis on large data and other data pre-, and post-processing functions
to aid the workflow with the LomPy package. 


Overview
--------
Routines for the linear regression analysis:
    
    lompy.aux.fitwithNan
    
Routines for the histogram computation across scales:
    
    lompy.aux.computehistogramNoNorm

Routines for building a geopandas dataframe from LomPy results:
    
    lompy.aux.build_gdf

"""

#Copyright (C) 2023 GNU AGPLv3, LomPy 2023, S.G. Roux and J. Lengyel.
#All rights reserved.
#Contact: stephane.roux@ens-lyon.fr, jankalengyel@gmail.com




import numpy as np
import warnings
from scipy.stats import t
import pandas as pd
import geopandas as gpd
from shapely.geometry import Polygon


#%%
def fitwithNan(Xvector, Yarray, borne=[]):
    '''
        fit a matrix of dim 2 or 3 along first dimension  
        Take care on infinite and nan values in the Yarray
        
        slope, intercept, (pval,rsquare,rmse, stderr) = fitwithNan(Xvector,Yarray,borne=[])
        
        Inputs :
            
            Xvector : vector of x value
        
            Yarray : array od dim 2 or 3 with the size of th first dimension 
                     corresponding to the size of Xvector
                
            borne=[j1, j2] : index of the interval used for then fit  
                           0 < j1 < j2 < len(Xvector). Default j1=0 and j2=len(Xvector).
                         
                          
       Outputs :
           
           slope : the slopes
           intercept : the interceps
           pval : pvalues
           rsquare :  R^2
           rmse     : root mean sqaure errors 
           stderr    : 


     ##

    '''

    if len(borne) == 0:
        j1 = 0
        j2 = Xvector.shape[0]

    else:
        j1 = max(0, borne[0])
        j2 = min(Xvector.shape[0], borne[1])


    if Yarray.ndim == 2:
        Xarraytmp = np.tile(Xvector[:, np.newaxis], (1, Yarray.shape[1]))
        ind = np.isfinite(Yarray)
        Xarray = Xarraytmp*np.nan
        Xarray[ind] = Xarraytmp[ind]
        Xarray = Xarray[j1:j2, :]
        Yarray = Yarray[j1:j2, :]
        lasum = sum(ind[j1:j2, :])

    elif Yarray.ndim == 3:
        Xarraytmp = np.tile(
            Xvector[:, np.newaxis, np.newaxis], (1, Yarray.shape[1], Yarray.shape[2]))
        ind = np.isfinite(Yarray)
        Xarray = Xarraytmp*np.nan
        Xarray[ind] = Xarraytmp[ind]
        Xarray = Xarray[j1:j2, :, :]
        Yarray = Yarray[j1:j2, :, :]
        lasum = sum(ind[j1:j2, :, :])

    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=RuntimeWarning)# statistics
        x_mean = np.nanmean(Xarray, axis=0)
        y_mean = np.nanmean(Yarray, axis=0)
        x_std = np.nanstd(Xarray, axis=0)
        y_std = np.nanstd(Yarray, axis=0)
    
        cov = np.nansum((Xarray-x_mean)*(Yarray-y_mean), axis=0)/lasum
        cor = cov/(x_std*y_std)
        slope = cov/(x_std**2)
        intercept = y_mean-x_mean*slope
    
        n = lasum
        tstats = cor*np.sqrt(n-2)/np.sqrt(1-cor**2)
        stderr = slope/tstats
    
        p_val = t.sf(tstats, n-2)*2
        r_square = np.nansum((slope*Xarray+intercept-y_mean) **
                             2, axis=0)/np.nansum((Yarray-y_mean)**2, axis=0)
        rmse = np.sqrt(np.nansum((Yarray-slope*Xarray-intercept)**2, axis=0)/n)

    return slope, intercept, (p_val,r_square,rmse,stderr)  
# %%
def computehistogramNoNorm(WT,bins):
    """
   
      hist, centers, lastd = computehistogram(WT,bins)
      
      Compute  histogram of the normalized wavelet coefficient
      Return also the standart deviation. 
    
      ##
       S.G.  Roux, ENS Lyon, December 2020,  stephane.roux@ens-lyon.fr
       
    """
    if len(WT.shape)==1:
        WT=WT[:,np.newaxis]
        Nr=WT.shape[1]
    else:
        Nr=WT.shape[1]
    hist=np.zeros((bins,Nr))
    centers=np.zeros((bins,Nr))
    for ir in range(Nr):
        temp=WT[:,ir]
        temp=temp[np.isfinite(temp)]

        htmp, bin_edges = np.histogram(temp, bins=bins)
        centers[:,ir]=(bin_edges[:-1]+bin_edges[1:])/2
        dx=np.mean(np.diff(centers[:,ir]))
        hist[:,ir]=htmp/np.sum(htmp)/dx

    return hist, centers #, lastd


# %%
def build_gdf(gridpoints, radius ,results, crs = "EPSG:2154"):
    """
     gdf_results = restoGeoPandaFrame(gridpoints, radius ,results)

         return a geopanda dataframe

     input :

         gridpoints - two dimensional array with the grid points position [x,y]
         radius     - one dimensional array with scales (>0)
         results    - two dimensional array of size equal len(gridpoints) X len(radius)

    output :

        out - geopanda dataframe

    """

    #  grid dataframe
    df_grid = pd.DataFrame({'x':gridpoints[:,0], 'y':gridpoints[:,1]})
    # get all scales in a single dataframe
    j=0
    mystr = 'R'+radius[j].astype(int).astype('str')
    df_data = pd.DataFrame(results[:,j], columns = [mystr])
    for j in range(1,len(radius)):
        mystr = 'R'+radius[j].astype(int).astype('str')
        df_data.loc[:,mystr] = pd.Series(results[:,j], index=df_data.index)

    gridsize = np.abs(df_grid['x'][0] - df_grid['x'][1])
    gdf_results = gpd.GeoDataFrame( df_data, geometry=[Polygon([(x-gridsize/2, y+gridsize/2), (x+gridsize/2, y+gridsize/2), (x+gridsize/2, y-gridsize/2), (x-gridsize/2, y-gridsize/2), (x-gridsize/2, y+gridsize/2)])
                              for x,y in zip(df_grid.x,df_grid.y)])

    gdf_results.crs = crs


    return gdf_results
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