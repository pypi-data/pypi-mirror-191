
"""
======================================================
Visualization package for LomPy (:mod:`lompy.viz`)
======================================================
          
.. currentmodule: LomPy.viz

This subpackage includes vizualization routines built on NumPy, GeoPandas and Matplotlib

Routine 1:
    
    LomPy.viz.img_arrayVD
    LomPy.viz.img_arrayRD
    
    
Routine 2:
    
    LomPy.viz.global_scalingVD
    LomPy.viz.global_scalingRD

Routine 3:
    
    LomPy.viz.plot_histo_VD
    LomPy.viz.plot_histo_RD
    
Routine 4:
    LomPy.viz.plot_gdf_fit
    LomPy.viz.plot_gdf_radius
"""

#Copyright (C) 2023 GNU AGPLv3, LomPy 2023, S.G. Roux and J. Lengyel.
#All rights reserved.
#Contact: stephane.roux@ens-lyon.fr, jankalengyel@gmail.com
#Other Contributors: P. Thiraux

#%%
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sys
#sys.path.append("../aux/")##!!tag pipchange
#import aux as aux ##!!tag pipchange
import lompy.aux as aux
import geopandas as gpd
#%%


def img_arrayVD(data, X, Y, figsize =(8,8) , cmap = 'Spectral', vmin = np.array([]), vmax = np.array([]), colorbar = False):
    """Return image object from 1D array   
      
    Parameters
    ---------------------
    data : numpy.array
        The values to be visualized (1D)   
    X,Y : numpy.ndarray
        The grid resolution, X and Y must have the same size 
    figsize: tuple with two elements, optional
        The size of the final image
    cmap: matplotlib.colors.Colormap object, optional
        Default is using "Spectral"
    vmin, vmax: float, optional
        Parameters to construct a matplotlib.colors.Normalize()
        Default: np.nanquantile(data,0.015), np.nanquantile(data,0.985)
    colorbar: boolean, optional 
        if True it displays a matplotlib.pyplot.colorbar, default False
        
    Returns
    ______________________
    im : 2D image with scalar data
                            
    Example
    ---------------------
    im = img_arrayVD(data, X, Y)     
    
    Notes
    ---------------------
    matplotlib.pyplot.imshow is used to return a 2D image with scalar 
    data - of a predefined resolution - using a 1D numpy array as input
    """ 
    
    
    if data.shape[0] == X.shape[0]*X.shape[1]:
        if isinstance(vmin, (np.floating, float)) == False:
            vmin = np.nanquantile(data,0.015)
            vmax = np.nanquantile(data,0.985)
        im = plt.imshow(np.reshape(data,(X.shape[0],Y.shape[1])), cmap = cmap, origin = 'lower', vmin = vmin, vmax=vmax)
        plt.xticks([], [])
        plt.yticks([], [])
        if colorbar == True:
            plt.colorbar()
        return im
    else:
        print('data and XY must have the same shape')
    
#%%    
    
    
def img_arrayRD(data, figsize =(8,8) , cmap = 'Spectral', vmin = np.array([]), vmax = np.array([]), colorbar = False):
    """Return image object from 2D scalar data   
      
    Parameters
    ---------------------
    data : numpy.narray
        The values to be visualized (2D scalar data)   
    figsize: tuple with two elements, optional
        The size of the final image
    cmap: matplotlib.colors.Colormap object, optional
        Default is using "Spectral"
    vmin, vmax: float, optional
        Parameters to construct a matplotlib.colors.Normalize()
        Default: np.nanquantile(data,0.015), np.nanquantile(data,0.985)
    colorbar: boolean, optional 
        if True it displays a matplotlib.pyplot.colorbar, default False
        
    Returns
    ______________________
    im : 2D image with scalar data
                            
    Example
    ---------------------
    im = img_array2D(data)     
    
    Notes
    ---------------------
    matplotlib.pyplot.imshow is used to return a 2D image with scalar 
    data - of a predefined resolution - using a 1D numpy array as input
    """ 
    
    
    if len(data.shape) == 2:
        if isinstance(vmin, (np.floating, float)) == False:
            vmin = np.nanquantile(data,0.015)
            vmax = np.nanquantile(data,0.985)
        im = plt.imshow(data, cmap = cmap, origin = 'lower', vmin = vmin, vmax=vmax)
        plt.xticks([], [])
        plt.yticks([], [])
        if colorbar == True:
            plt.colorbar()
        return im
    else:
        print('data must be 2D scalar data')
#%%
def global_scalingVD(data, radius, ml=[], label=[] , color = 'black', alpha = 0.9, linewidth = 1., markersize=3.75):
    """Return a plot of global scaling from vector data results (KNN) 
    
    Parameters
    ---------------------
    data : numpy.narray
        The values to be visualized 
    radius: numpy.array
        The radii used for the multiscale analysis
    cmap: matplotlib.colors.Colormap object, optional
        Default is using "Spectral"
    alpha: float, optional
    color: string, optional
    linewidth: float, optional
        
    Returns
    ______________________
    matplotlib line plot of global scaling
                            
    Example
    ---------------------
    global_scalingVD(data, radius)

    Notes
    _____________________
    matplotlib.pyplot.plot is used to plot line, y versus x  
    """
    if data.shape[1] == len(radius):
        tmp=np.nanmean(data,axis=0)         
        plt.plot(np.log(radius),(tmp.T), ml , label=label, color = color, alpha=alpha, linewidth=linewidth, markersize = markersize)
    else:
        print('The second dimension of the data must be equal to the length of radii')


def global_scalingRD(data, radius, ml=[], label=[] , color = 'black', alpha = 0.9, linewidth = 1., markersize=5.):
    """Return a plot of global scaling from raster data results (conv2D)
    
    Parameters
    ---------------------
    data : numpy.narray
        The scalar data to be visualized 
    radius: numpy.array
        The radii used for the multiscale analysis
    cmap: matplotlib.colors.Colormap object, optional
        Default is using "Spectral"
    alpha: float, optional
    color: color, optional
    linewidth: float, optional
        
    Returns
    ______________________
    matplotlib line plot of global scaling
                            
    Example
    ---------------------
    global_scalingVD(data, radius)

    Notes
    _____________________
    matplotlib.pyplot.plot is used to plot line, y versus x  
    """
    if data.shape[2] == len(radius):
        tmp =  np.nanmean(data.reshape(-1,len(radius)), axis =0)             
        plt.plot(np.log(radius),(tmp.T), ml , label=label, color = color, alpha=alpha, linewidth=linewidth, markersize = markersize)
    else: 
        print('The third dimension of the data must be equal to the length of radii')
#%%

def gplot_df_fit(data, fit, grid, radius, figsize =(20,20) , scheme="quantiles", k=6, cmap = 'Spectral', edgecolor = 'face', legend = False):
    """Visualize LomPy scaling exponents on maps
    """
    gdf = aux.build_gdf(grid, radius, data)
    if data.shape[1] == len(radius):
        gdf['fit'] = fit
        fig, ax =plt.figure(figsize=figsize)
        gdf.plot(column=gdf.fit, scheme=scheme,  k=k, ax = ax, cmap = cmap, edgecolor = edgecolor, legend = legend)
        plt.axis('off')
        plt.tight_layout()
        if legend == True:
            plt.legend()
    else:
        print('The second dimension of the data must be equal to the length of radii')

#%%

def plot_gdf_radius(data, fit, grid, radius, vizradius, figsize =(20,20) , scheme="quantiles", k=6, cmap = 'Spectral', edgecolor = 'face', legend = False):
    """Visualize LomPy scaling functions on maps
    """
    gdf = aux.build_gdf(grid, radius, data)
    if data.shape[1] == len(radius):
        gdf['rr'] = gdf.loc[vizradius]
        fig, ax =plt.figure(figsize=figsize)
        gdf.plot(column=gdf.rr, scheme=scheme,  k=k, ax = ax, cmap = cmap, edgecolor = edgecolor, legend = legend)
        plt.axis('off')
        plt.tight_layout()
        if legend == True:
            plt.legend()
    else:
        print('The second dimension of the data must be equal to the length of radii')
#%%
def plot_histo_VD(data, bins = 50, color = 'black', label=[] , alpha = 0.95, linestyle ='--', linewidth = 1., marker = 's', markersize=3.75):
    """Plot histogram of the scaling exponent, derived from vector data
    """
    vv = aux.computehistogramNoNorm(data,int(bins))
    plt.plot(vv[1],vv[0], color = color, label =label, alpha = alpha, linestyle=linestyle, linewidth = linewidth, marker = marker, markersize=markersize)

def plot_histo_RD(data, bins = 50, color = 'grey', label=[] , alpha = 0.95,  linestyle ='--', linewidth = 1., marker = 'v',markersize=5.):
    """Plot histogram of the scaling exponent, derived from raster data
    """
    vv = aux.computehistogramNoNorm(data.flatten(),int(bins))
    plt.plot(vv[1],vv[0], color = color, label =label, alpha = alpha, linestyle=linestyle, linewidth = linewidth, marker = marker, markersize=markersize)    
