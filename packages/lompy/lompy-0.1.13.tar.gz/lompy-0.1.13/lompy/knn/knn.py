#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

==========================================================
k Nearest Neighbours package for LomPy (:mod:`lompy.knn`)
==========================================================

          
.. currentmodule: lompy.knn

These package features yield the multiresolution quantities and local scaleing parameters 
for non-uniformly distributed (vector) 2D data

Overview
--------
Routines for the muliresolution quantities:
    
    lompy.knn.MultiresQuantityVD
    
Routines for the univariate local analysis:
    
    lompy.knn.LocalMsAnalysisVD

Routines for the bivariate local analysis:
    
    lompy.knn.LocalCorrAnalysisVD

"""
#Copyright (C) 2023 GNU AGPLv3, LomPy 2023, S.G. Roux and J. Lengyel.
#All rights reserved.

#Contact: stephane.roux@ens-lyon.fr, jankalengyel@gmail.com
#Other Contributors: P. Thiraux, F Semecurbe

import warnings
import types
import numpy as np
from sklearn.neighbors import KDTree
from sklearn.neighbors import NearestNeighbors
from functools import partial
import sys
from concurrent.futures import ThreadPoolExecutor
#sys.path.append("../conv2D/") ##!!tag pipchange
#import conv2D as conv2D ##!!tag pipchange
import lompy.conv2D as conv2D

#%%
def checkinputdata(data):
    """
    Check the type of data:
    Image (raster)
    Marked (vector)
    Number of marks
    
    isimage, ismarked, Nmark = checkinputdata(data)

    Parameters
    ----------
    data : numpy array of float
        The data to check.

    Returns
    -------
    isimage : Boolean
        Equals to 1 if the data is an image.
    ismarked : Boolean
        Equals to 1 if the data ia a marked point process.
    Nmark : int
        Number of marks in the data.

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
                print('The input is a set of  {:d}  images  of size ({:d},{:d})).'.format(si[2],si[0],si[1]))
                ismarked = 1
                Nmark = si[2]
            else:
                print('The input is an image of size ({:d},{:})'.format(si[0],si[1]))
                ismarked = 0
                Nmark = 0
        else:
            isimage=0
            if si[1]>2:
                print('The input is a marked point process with {:} points and {:d} marks.'.format(si[0],si[1]-2))
                
                ismarked = 1
                Nmark = si[1]-2
            else:
                print('The input is a marked point process with {:} points.'.format(si[0]))
                ismarked = 0
                Nmark = 0
    return isimage, ismarked, Nmark

#%% 
def getoptimblock(datapos, Nanalyse, thresh = 200):
    """
    Define best block positions and sizes.    
    centerstot, sizeblocktot = getoptimblock(datapos, Nanalyse, thresh = 20)
    

    Parameters
    ----------
    datapos : numpy array of float
        list of x and Y position of N points. 
        Array of shape (N, 2).
    Nanalyse : integer
        Number of points used in the batch.
        Must be set accordingly to the memory available.
        
    thresh : float, optional
        Divide block until the number of point inside pass below this threshold.
        The default is 20.

    Returns
    -------
    centerstot : numpy array of float
        List of x and y position of the center of the blocks = shape (Nblock,2).
    sizeblocktot : numpy array of float
        List of size of the blocks = shape (Nblock,).

    """
    
    sizetmp = Nanalyse
    temp = datapos // sizetmp
    block, count = np.unique(temp, axis=0, return_counts = True)
    sizeblock = count * 0 + sizetmp
    centers = block * sizetmp + sizetmp//2   
    
    # above the threshod : we continue to divide
    index, = np.where(count > 2**thresh)
    sizetmp2 = sizetmp // 2
    if len(index)>0:
        counttot  = count[0:index[0]]
        centerstot = centers[0:index[0],:]
        sizeblocktot = sizeblock[0:index[0]]
        
        for iind in range(len(index)):
            iblock = index[iind]
            ii = np.argwhere( np.all((temp - block[iblock]) == 0, axis = 1))
            temp2 = np.squeeze(np.copy(datapos[ii,:]))
            mitemp2 = np.min(temp2,axis = 0)
            temp2 = temp2 - mitemp2[:,np.newaxis].T
            temp2=temp2 // (sizetmp2)
            blocktmp2, counttmp2 = np.unique( temp2, axis = 0, return_counts = True)
            centers2 = blocktmp2 * sizetmp2 + sizetmp2 // 2+ mitemp2
            sizeblock2 = counttmp2 * 0 + sizetmp2
            centerstot = np.append(centerstot,centers2, axis = 0)
            sizeblocktot = np.append(sizeblocktot,sizeblock2, axis = 0)
            counttot = np.append(counttot,counttmp2, axis = 0) 
            #
            if iind + 1 < len(index):
                centerstot = np.append(centerstot, centers[iblock+1:index[iind+1],:], axis = 0)
                sizeblocktot = np.append(sizeblocktot, sizeblock[iblock+1:index[iind+1]], axis = 0)
                counttot = np.append(counttot, count[iblock+1:index[iind+1]], axis = 0)
                
            
        centerstot = np.append( centerstot, centers[index[-1]+1:,:], axis = 0)
        sizeblocktot = np.append( sizeblocktot, sizeblock[index[-1]+1:], axis = 0)
        counttot = np.append( counttot, count[index[-1]+1:], axis = 0)
    else:
        centerstot = centers
        sizeblocktot = sizeblock
        
    return centerstot, sizeblocktot
#
# %%  geo weighting
def EpanechnikovWindow(z):
    return 0.75*(1-z**2) 

def triangularWindow(z):
    return (1 - np.abs(z)) 

def tricubeWindow(z):
    return (70/81)*(1-np.abs(z)**3)**3

def bisquareWindow(z):
    return (1-z**2)**2 

def flatWindow(z):
    return np.ones(z.shape)
#%
def geographicalWeight(dd,T,func):
    
    """
    
    W = geographicalWeight(dist,T,Nr)
    
    return the weight according to the distance dist 
    using a 'local' environment of size T.
    
    Input :

       dist - distance of the point. dist and index as the shame shape
       T    - bandwith of fixed kernel OR bandwith for the pilot density of the adaptive kernel
       Nr   - number of copies for the weight
        
     Output :

       W - the weight. Array of size (len(dd),Nr)
   
    """  

    # Weighting function
    z = dd/T
    W=func(z)
    W[dd>=T]=0
    W=W/np.sum(W,0) 
    W=W[:,np.newaxis]

    return W

#% averaging functions
def localdist(dist,Tloc):
    distout=np.copy(dist)
    distout[dist>Tloc] = np.nan
    distout[dist<=Tloc] = 1
    return distout

#%%
def logaverage(x,w):
    ##########################
    x[x==0] = np.nan
    #w[w==0] = np.nan
    ##########################
    logx=np.log(np.abs(x))
    logx[np.abs(x)==0]=np.nan
    # weight need to be normalized : done
    average=np.nansum(logx*w,axis=0)
    return average

def logaverage2(x,average,w):
    ##########################
    x[x==0] = np.nan
    #w[w==0] = np.nan
    ##########################
    logx=(np.log(np.abs(x))-average)**2
    logx[np.abs(x)==0]=np.nan
    # weight need to be normalized : done
    average2=np.nansum(logx*w,axis=0)
    
    return average2

# %% ---------function for multithreated computations ------ 
def fill(Idx, Dist, val):
    """
    

    Parameters
    ----------
    Idx : TYPE
        DESCRIPTION.
    Dist : TYPE
        DESCRIPTION.
    val : TYPE
        DESCRIPTION.

    Returns
    -------
    A : TYPE
        DESCRIPTION.
    B : TYPE
        DESCRIPTION.

    """
    N = len(Idx)
    M = max( map( len, Idx))
    A = np.full( (N, M), np.nan)
    B = np.full( (N, M), np.nan)
                
    #print(A.shape)
    for i, (aa, bb) in enumerate( zip( Idx, Dist)):
        A[i, :len(aa)] = val[aa]
        B[i, :len(bb)] = bb
    return A, B
#
def threaded_Count_Valued(In, radiustot, val):
    """
    

    Parameters
    ----------
    In : TYPE
        DESCRIPTION.
    radiustot : TYPE
        DESCRIPTION.
    val : TYPE
        DESCRIPTION.

    Returns
    -------
    Count : TYPE
        DESCRIPTION.

    """
    Idx, Dist = In
    valbis, dd = fill( Idx, Dist, val)
    Count = np.zeros( (valbis.shape[0],len(radiustot),3))
    for ir in range( len( radiustot)):
        
        valbis[dd >= radiustot[-1 - ir]] = np.nan
        Count[:, -1 -ir, 0] = np.nansum( np.isfinite(valbis), axis = 1)
        Count[:, -1 -ir, 1] = np.nanmean( valbis, axis = 1)
        Count[:, -1 -ir, 2] = np.nanstd( valbis, axis = 1)
    
    return Count
#
def fill2(Idx, Dist, val):
    """
    

    Parameters
    ----------
    Idx : TYPE
        DESCRIPTION.
    Dist : TYPE
        DESCRIPTION.
    val : TYPE
        DESCRIPTION.

    Returns
    -------
    A : TYPE
        DESCRIPTION.
    B : TYPE
        DESCRIPTION.

    """
    
    N = len(Idx)
    M = max( map( len, Idx))
    A = np.full( (N, M, val.shape[1]), np.nan)
    B = np.full( (N, M), np.nan)
                
    #print(A.shape, val.shape)
    for i, (aa, bb) in enumerate( zip( Idx, Dist)):
        A[i, :len(aa), :] = val[aa,:]
        B[i, :len(bb)] = bb
    return A, B
#
def threaded_All_Valued(In, radiustot, val):
    """
    

    Parameters
    ----------
    In : TYPE
        DESCRIPTION.
    radiustot : TYPE
        DESCRIPTION.
    val : TYPE
        DESCRIPTION.

    Returns
    -------
    Count : TYPE
        DESCRIPTION.

    """
    Idx, Dist = In
    valbis, dd = fill2( Idx, Dist, val)
    #print('------', valbis.shape)
    Count = np.zeros( (valbis.shape[0],len(radiustot),7))
    for ir in range( len( radiustot)):
        
        valbis[dd >= radiustot[-1 - ir],-ir] = np.nan
        # count points
        Count[:, -1 -ir, 0] = np.nansum( np.isfinite(valbis[:,:,-ir]), axis = 1)
        # Mean
        Count[:, -1 -ir, 1] = np.nanmean( valbis[:,:,-ir], axis = 1)
        # std
        Count[:, -1 -ir, 2] = np.nanstd( valbis[:,:,-ir], axis = 1)
        # M2
        Count[:, -1 -ir, 3] = np.nanmean( valbis[:,:,-ir]**2, axis = 1)
        # M4
        Count[:, -1 -ir, 4] = np.nanmean( valbis[:,:,-ir]**4, axis = 1)
        # take the log
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=RuntimeWarning)
            temp  = np.log(np.abs(valbis[:,:,-ir]))           
            temp[np.isinf(temp)] = np.nan
            # c1
            Count[:, -1 -ir, 5] = np.nanmean( temp, axis = 1)
            # c2
            Count[:, -1 -ir, 6] = np.nanstd( temp**2, axis = 1)
    
    return Count


def threaded_corr_coef(In, radiustot, val1,val2):
    """
    

    Parameters
    ----------
    In : TYPE
        DESCRIPTION.
    radiustot : TYPE
        DESCRIPTION.
    val : TYPE
        DESCRIPTION.

    Returns
    -------
    Count : TYPE
        DESCRIPTION.

    """
    Idx, Dist = In
    valbis1, dd = fill2( Idx, Dist, val1)
    valbis2, dd = fill2( Idx, Dist, val2)
    corrcoef = np.zeros( (valbis1.shape[0],len(radiustot),2))
    for ir in range( len( radiustot)):
        
        valbis1[dd >= radiustot[-1 - ir],-ir] = np.nan
        valbis2[dd >= radiustot[-1 - ir],-ir] = np.nan
        
        M01 = np.nanmean( valbis1[:,:,-ir], axis = 1)
        M10 = np.nanmean( valbis2[:,:,-ir], axis = 1)
        M11 = np.nanmean( valbis1[:,:,-ir]*valbis2[:,:,-ir], axis = 1)
        S01 = np.nanstd( valbis1[:,:,-ir], axis = 1)
        S10 = np.nanstd( valbis2[:,:,-ir], axis = 1)
    
        corrcoef[:, -1 -ir,0] = (M11-M01*M10)/(S01*S10)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=RuntimeWarning)
            temp1  = np.log(np.abs(valbis1[:,:,-ir]))           
            temp1[np.isinf(temp1)] = np.nan
            temp2  = np.log(np.abs(valbis2[:,:,-ir]))           
            temp2[np.isinf(temp2)] = np.nan
            M01 = np.nanmean( temp1, axis = 1)
            M10 = np.nanmean( temp2, axis = 1)
            M11 = np.nanmean( temp1*temp2, axis = 1)
            S01 = np.nanstd( temp1, axis = 1)
            S10 = np.nanstd( temp2, axis = 1)
    
            corrcoef[:, -1 -ir,1] = (M11-M01*M10)/(S01*S10)
            
    return corrcoef


#%%
#
def threaded_Log(In, radiustot, val):
    """
    

    Parameters
    ----------
    In : TYPE
        DESCRIPTION.
    radiustot : TYPE
        DESCRIPTION.
    val : TYPE
        DESCRIPTION.

    Returns
    -------
    Count : TYPE
        DESCRIPTION.

    """
    Idx, Dist = In
    Count = np.zeros((len(Idx),len(radiustot)))
    for ir in range(len(radiustot)):
        valbis, dd = fill(Idx,Dist,val[:,ir])
        valbis[dd>=radiustot[-1-ir]]=np.nan
        
        Count[:,-1-ir] = np.nanmean(valbis,axis=1)
    
    return Count

#
def threaded_Log_OneScale(In, radiustot, val):
    Idx, Dist = In
    Count = np.zeros((len(Idx),))
    
    valbis, dd = fill( Idx, Dist, val)
    valbis[dd >= radiustot] = np.nan
    Count = np.nanmean(valbis, axis = 1)
    
    return Count

#
def threaded_Leaders_OneScale(In, radiustot, val,p):
    Idx, Dist = In
    Count = np.zeros((len(Idx),))
    
    valbis, dd = fill( Idx, Dist, val)
    valbis[dd >= radiustot] = np.nan
    Count = np.nansum(np.abs(valbis)**p, axis = 1)**(1/p)
    #Count = Count / np.nansum(np.isfinite(valbis), axis = 1)
    
    return Count

def threaded_MaxLeaders_OneScale(In, radiustot, val):
    Idx, Dist = In
    Count = np.zeros((len(Idx),))
    
    valbis, dd = fill( Idx, Dist, val)
    valbis[dd >= radiustot] = np.nan
    Count = np.nanmax(np.abs(valbis), axis = 1)
    
    return Count

# %% count point with dist<radius
def threaded_Count(dist , radius):   
    """
    
      out = threaded_Count(dist,radius)
      
      Compute  the number of element with distance lower than radius
      Radius can be a vector.
    
       
    """    

    radius = np.atleast_1d(radius)
    Count = np.zeros( ( 1, radius.shape[0]), dtype = 'float')
    for i in range(radius.size):
        dist = dist[ dist< radius[ -1 - i]]
        Count[ 0,-1 - i] = dist.shape[0]
        
    return Count


#%% Leaders knn
def localLeaders(data, Wcoefs, radius, Nanalyse = 2**14, NonUniformData = False, verbose = True, p=2):
    """
    

    Parameters
    ----------
    Wcoef : TYPE
        DESCRIPTION.
    radius : TYPE
        DESCRIPTION.
    Nanalyse : TYPE, optional
        DESCRIPTION. The default is 2**14.
    NonUniformData : TYPE, optional
        DESCRIPTION. The default is False.

    Returns
    -------
    int
        DESCRIPTION.

    """
    
    #% check input data
    si = data.shape
    if si[1] != 2 : 
        raise TypeError('The second dimension of first argument must be of length 2 or 3.')
     
    # select the destination set of points
    destination = data[ :, 0:2]
    N = destination.shape[0]
    
    # check the analysis
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=RuntimeWarning)
        #lcoefs  = np.log(np.abs(Wcoefs))
        lcoefs  = np.copy(Wcoefs)

        
    Nscales = Wcoefs.shape[1]
    Npts = Wcoefs.shape[0]
    if Npts != N:
        raise TypeError("not a good number of points")
   
    radius = np.atleast_1d(radius)
    radiustot = np.sort(radius)
    temp, temp2, indexreadius = np.intersect1d( radius, radiustot, return_indices = True)
    if radius.shape[0] != Nscales:
        raise TypeError("not a good number of scales")
    # some constants
    scalemax = np.max(radiustot)
    
    
    # sub parameters to partition  the data
    if Nanalyse == 0: # this is dangerous
        print('Warning : dangerous if your set of data is large.')
        Nanalyse = N
        Nbunch = 1
    else:
        # find how many bunches
        if NonUniformData:
            centers, sizeblock = getoptimblock( data, Nanalyse)
            if verbose:
                print('Block optimisation for non uniformly spaced data.')
            Nbunch = len(sizeblock)
        else:
            sizetmp = Nanalyse
            temp=data // sizetmp
            block, count = np.unique( temp, axis = 0, return_counts = True)
            centers = block*sizetmp + sizetmp // 2
            sizeblock = count * 0 + sizetmp
            Nbunch = len(block)
            if verbose:
                print('No block optimisation uniformly spaced data.')
            
    
    Nanalyse2 = 2**22
    
    if verbose:
        print('Computation in {:d} bunches :'.format(Nbunch), end = ' ')
    
    # allocation
    Lead = np.nan*np.zeros((N, radius.shape[0]), dtype = float)
    LeadMax = np.nan*np.zeros((N, radius.shape[0]), dtype = float)

    
    # set the worker for knn search
    neigh = NearestNeighbors( n_jobs = 4)
    
    #% loop on the bunches
    for ibunch in range( Nbunch):
        #%
        print(ibunch + 1, end=' ')
        sys.stdout.flush()
              
        center = centers[ ibunch, :]
        sizetmp = sizeblock[ ibunch]
        #grrr
        index,= np.where(((data[:,0] >= center[0]-sizetmp//2) & (data[:,0]< center[0]+sizetmp//2)) & ((data[:,1]>= center[1]-sizetmp//2) & (data[:,1]< center[1]+sizetmp//2)))
        IndexNear, = np.where(((data[:,0] >= center[0]-(sizetmp//2+scalemax+1)) & (data[:,0]< center[0]+(sizetmp//2+scalemax+1))) & ((data[:,1]>= center[1]-(sizetmp//2+scalemax+1)) & (data[:,1]< center[1]+(sizetmp//2+scalemax+1))))
        neigh.fit( data[ IndexNear, :])
        
        # search neiarest neighbors
        Disttot, IdxTot = neigh.radius_neighbors(destination[index,0:2], radius = scalemax, return_distance = True)
        # get the max length of neighbors --> computation by block
        Maxlength = max(map(len, IdxTot))
        Nblock = int(np.ceil( index.shape[0] * Maxlength / Nanalyse2))
        Nptx = len(index) // Nblock+1
        # correct the number of blocks if needed
        if (Nblock -1) * Nptx > min( len(index), Nblock*Nptx):
            Nblock = Nblock - 1
        
        
        for ir in range( Nscales):
            radius = radiustot[ ir]
            malist2 = [(IdxTot[i*Nptx:min(len(index),(i+1)*Nptx)], Disttot[i*Nptx:min(len(index),(i+1)*Nptx)]) for i in range(Nblock)]
           
            partialknnMeanLog = partial( threaded_Leaders_OneScale, radiustot = radius, val = lcoefs[IndexNear,ir], p = p)
            with ThreadPoolExecutor() as executor:
                result_list4 = executor.map( partialknnMeanLog, malist2)
            
            Lead[ index, ir] = np.hstack( list( result_list4))
            partialknnMeanLog = partial( threaded_MaxLeaders_OneScale, radiustot = radius, val = lcoefs[IndexNear,ir])
            with ThreadPoolExecutor() as executor:
                result_list4 = executor.map( partialknnMeanLog, malist2)
            
            LeadMax[ index, ir] = np.hstack( list( result_list4))
            
    
    for ir in range(1, Nscales):
        LeadMax[ index, ir] = np.maximum(LeadMax[:, ir], LeadMax[:, ir-1])
        
    print('.')    
    return Lead, LeadMax

#%% Leaders knn
def localLeadersP(data, Wcoefs, radius, Nanalyse = 2**14, NonUniformData = False, verbose = True, p=2):
    """
    

    Parameters
    ----------
    Wcoef : TYPE
        DESCRIPTION.
    radius : TYPE
        DESCRIPTION.
    Nanalyse : TYPE, optional
        DESCRIPTION. The default is 2**14.
    NonUniformData : TYPE, optional
        DESCRIPTION. The default is False.

    Returns
    -------
    int
        DESCRIPTION.

    """
    
    #% check input data
    si = data.shape
    if si[1] != 2 : 
        raise TypeError('The second dimension of first argument must be of length 2 or 3.')
     
    # select the destination set of points
    destination = data[ :, 0:2]
    N = destination.shape[0]
    
    # check the analysis
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=RuntimeWarning)
        #lcoefs  = np.log(np.abs(Wcoefs))
        lcoefs  = np.copy(Wcoefs)

    Nscales = Wcoefs.shape[1]
    Npts = Wcoefs.shape[0]
    if Npts != N:
        raise TypeError("not a good number of points")
   
    radius = np.atleast_1d(radius)
    radiustot = np.sort(radius)
    temp, temp2, indexreadius = np.intersect1d( radius, radiustot, return_indices = True)
    if radius.shape[0] != Nscales:
        raise TypeError("not a good number of scales")
    # some constants
    scalemax = np.max(radiustot)
    
    
    # sub parameters to partition  the data
    if Nanalyse == 0: # this is dangerous
        print('Warning : dangerous if your set of data is large.')
        Nanalyse = N
        Nbunch = 1
    else:
        # find how many bunches
        if NonUniformData:
            centers, sizeblock = getoptimblock( data, Nanalyse)
            if verbose:
                print('Block optimisation for non uniformly spaced data.')
            Nbunch = len(sizeblock)
        else:
            sizetmp = Nanalyse
            temp=data // sizetmp
            block, count = np.unique( temp, axis = 0, return_counts = True)
            centers = block*sizetmp + sizetmp // 2
            sizeblock = count * 0 + sizetmp
            Nbunch = len(block)
            if verbose:
                print('No block optimisation uniformly spaced data.')
            
    
    Nanalyse2 = 2**22
    
    if verbose:
        print('Computation in {:d} bunches :'.format(Nbunch), end = ' ')
    
    # allocation
    Lead = np.nan*np.zeros((N, radius.shape[0]), dtype = float)

    
    # set the worker for knn search
    neigh = NearestNeighbors( n_jobs = 4)
    
    #% loop on the bunches
    for ibunch in range( Nbunch):
        #%
        print(ibunch + 1, end=' ')
        sys.stdout.flush()
              
        center = centers[ ibunch, :]
        sizetmp = sizeblock[ ibunch]
        #grrr
        index,= np.where(((data[:,0] >= center[0]-sizetmp//2) & (data[:,0]< center[0]+sizetmp//2)) & ((data[:,1]>= center[1]-sizetmp//2) & (data[:,1]< center[1]+sizetmp//2)))
        IndexNear, = np.where(((data[:,0] >= center[0]-(sizetmp//2+scalemax+1)) & (data[:,0]< center[0]+(sizetmp//2+scalemax+1))) & ((data[:,1]>= center[1]-(sizetmp//2+scalemax+1)) & (data[:,1]< center[1]+(sizetmp//2+scalemax+1))))
        neigh.fit( data[ IndexNear, :])
        
        # search neiarest neighbors
        Disttot, IdxTot = neigh.radius_neighbors(destination[index,0:2], radius = scalemax, return_distance = True)
        # get the max length of neighbors --> computation by block
        Maxlength = max(map(len, IdxTot))
        Nblock = int(np.ceil( index.shape[0] * Maxlength / Nanalyse2))
        Nptx = len(index) // Nblock+1
        # correct the number of blocks if needed
        if (Nblock -1) * Nptx > min( len(index), Nblock*Nptx):
            Nblock = Nblock - 1
        
        
        for ir in range( Nscales):
            radius = radiustot[ ir]
            malist2 = [(IdxTot[i*Nptx:min(len(index),(i+1)*Nptx)], Disttot[i*Nptx:min(len(index),(i+1)*Nptx)]) for i in range(Nblock)]
           
            partialknnMeanLog = partial( threaded_Leaders_OneScale, radiustot = radius, val = lcoefs[IndexNear,ir], p = p)
            with ThreadPoolExecutor() as executor:
                result_list4 = executor.map( partialknnMeanLog, malist2)
            
            Lead[ index, ir] = np.hstack( list( result_list4))

        
    print('.')    
    return Lead
#%%
def localWaveTrans(data, radius, Nanalyse = 2**14, destination = np.array([]),NonUniformData = False, verbose = True):
    """
    
     [Count, Wave, CountG] = aveTrans(source, radius, T=None, Nanalyse=2**16, destination = []))
    
    
    
    Compute box-counting and wavelet coefficient on a valued/non valued set of data points.
    
    If the data are not valued, count for every data point
            -- the number of neighboors in ball of radius r (GWFA) : N(r).
            -- the wavelet coeficient at scale r (GWMFA) : 2*N(r)-N(sqrt(2)*r).
    
    If the data are valued, count for every datapoint
            -- the number of neighboors in ball of radius r, the mean and std of the marked value
            -- the wavelet coeficient at scale r on the marked value.
    
    Input :
    
        source     - Non-marked  point process : matrix of size N X 2 for N points
                        where source[i,:]=[X_i,Y_i] with 2D cooprdonate of point i.
                      Marked  point process :  matrix of size Nx3
                        where source[i,:]=[X_i,Y_i, mark_i] with 2D cooprdonate of point i and value
        radius      - list of scales to be investigated
        Nanalyse    - number of points to analyse in one bach. Default is 2**16 points.
                        If Nanalyse=0, compute all the points in once (dangerous!!!)
        destination - Non marked point process (destination_i=[X_I,Y_i]) where the coeficient are calculated
                        Default empty : compute at source position.
    Output :
    
        Count    - matrix of size Nxlength(radius) with box-counting coefficients
        Wave     - matrix of size Nxlength(radius) with wavelet coefficients
        Count    - matrix of size Nx2 with box-counting and wavelet coeficient at scale T
                  
    
    """
 
    #% check input data
    si = data.shape
    if si[1] < 2: # or si[1]>3:
        raise TypeError('The second dimension of first argument must be of length 2 or 3.')
     
    
    
    # select the destination set of points
    if destination.shape[0] == 0: 
        destination = data[:,0:2]
    else:
        sid = destination.shape
        #print(sid)
        if sid[1] != 2 :
            raise TypeError('The ''destination''  argument must be of length 2.')
    
    # check the analysis
    isvalued = 0 
    if si[1] > 2: # valued analysis
        isvalued = 1
        if verbose:
            print('Valued data analysis on {:d} points to {:d} destination points.'.format(data.shape[0],destination.shape[0]))
        val = data[:,2]
        #valtot = data[:,2:]
        #data = data[:,0:2]
        
    else:           # non valued analysis
        val = destination[:,0] * 0 + 1
        if verbose:
            print('Non valued data analysis on {:d} points to {:d} destination points.'.format(data.shape[0],destination.shape[0]))
    
    radius = np.atleast_1d(radius)
    radiustot = np.sort(radius)
    #temp,temp2,indexreadius=np.intersect1d(radius,radiustot, return_indices=True)

    # some constants
    scalemax=np.max(radiustot)
    N = destination.shape[0]
    
    # sub parameters to partition  the data
    if Nanalyse==0: # this is dangerous
        print('Warning : dangerous if your set of data is large.')
        Nanalyse=N
        Nbunch=1
    else:
        # find how many bunchs
        if NonUniformData:
            centers, sizeblock = getoptimblock(destination,Nanalyse)
            Nbunch = len(sizeblock)
            if verbose:
                print('Block optimisation for non uniformly spaced data.')
                       
        else:
            sizetmp = Nanalyse
            temp= destination // sizetmp
            block, count = np.unique(temp, axis=0, return_counts=True)
            centers = block*sizetmp+sizetmp//2
            sizeblock = count*0+sizetmp
            Nbunch = len(block)
            if verbose:
                print('No block optimisation uniformly spaced data.')
            
    
    Nanalyse2 = 2**22
    #print('Nanalyse (bunch) and Nanalyse2 (block)',  Nanalyse, Nanalyse2,t2-t1)
    if verbose:
        print('Computation in {:d} bunches :'.format(Nbunch),end=' ')  
    
   
    if isvalued: # we compute mean, std and count
        Count = np.nan*np.zeros((N,radius.shape[0],3),dtype=float)
        #  store count of valid value, mean and std of the point process mark           
    else:         #  we compute only count
        Count = np.nan*np.zeros((N,radius.shape[0]),dtype=float)
    
    # set the worker for knn search
    neigh = NearestNeighbors(n_jobs=4)
    
    #% loop on the bunches
    for ibunch in range(Nbunch):
        #%
        #ibunch=4
        print(ibunch+1, end=' ')
        sys.stdout.flush()
        #
        center = centers[ibunch,:]
        sizetmp = sizeblock[ibunch]
        #
        index, = np.where(((destination[:,0] >= center[0]-sizetmp//2) & (destination[:,0]< center[0]+sizetmp//2)) & ((destination[:,1]>= center[1]-sizetmp//2) & (destination[:,1]< center[1]+sizetmp//2)))
        IndexNear, = np.where(((destination[:,0] >= center[0]-(sizetmp//2+scalemax+1)) & (destination[:,0]< center[0]+(sizetmp//2+scalemax+1))) & ((destination[:,1]>= center[1]-(sizetmp//2+scalemax+1)) & (destination[:,1]< center[1]+(sizetmp//2+scalemax+1))))
        neigh.fit(destination[IndexNear,:])
        
        if isvalued:  # valued analysis

            Disttot, IdxTot = neigh.radius_neighbors(destination[index,0:2], radius = scalemax, return_distance = True)

            Maxlength = max(map( len, IdxTot))
            
            Nblock = int(np.ceil(index.shape[0] * Maxlength / Nanalyse2))           
            Nptx = len(index) // Nblock + 1
            if (Nblock - 1)*Nptx > min(len(index), Nblock * Nptx):
                Nblock = Nblock - 1
            
            #print(Nblock,Nptx)
            malist2=[(IdxTot[i*Nptx:min(len(index),(i+1)*Nptx)], Disttot[i*Nptx:min(len(index),(i+1)*Nptx)]) for i in range(Nblock)]
            partialknncountbis = partial(threaded_Count_Valued, radiustot = radiustot,val = val[IndexNear])

            
            with ThreadPoolExecutor() as executor:
                result_list3 = executor.map(partialknncountbis, malist2)
            
            Count[index,:,:] = np.vstack(list(result_list3))

            
        else:  # non valued analysis
            Disttot, IdxTot = neigh.radius_neighbors(destination[index,0:2],radius=scalemax,return_distance=True)
            partialcount = partial(threaded_Count, radius=radiustot)
            with ThreadPoolExecutor() as executor:
                result_list = executor.map(partialcount, Disttot)
            
            temp = np.squeeze(np.array(list(result_list)));
            if radius.shape[0] == 1:
                Count[index,:] = temp[:,np.newaxis]
            else:    
                Count[index,:] = temp
            
    del neigh
    print('.')
    
    if isvalued: # compute poor coefs       
        Wcoef = np.copy(Count)
        Wcoef[:,:,1] = Wcoef[:,:,1] - val[:,np.newaxis]    
        return Wcoef, Count
    
    else:
        return Count

# %%
def computeGridValue(tree,Count,lCount,IndexNear,index2,mygrid, radius, Tloc, weightingfunction):
    """

    NWmean, NWstd, Wmean, Wstd, Mom, Cum = computeGridValue(tree,Count,IndexNear,index,mygrid, radius, T, k=0):

    For marked and non-marked point process
    Compute weighted statistics of the number of point location or value.
    The (geographical) weighting is obtained using the bi-squared function of size T.
       
    Input :

       tree      - a kdtree obtained on the IndexNear points (a subset of the Npts total points)
       Count     - matrix of size Nptsxlength(radius) with wavelet coef
       IndexNear - location of the points used for the kdtree
       index     - index of the grid points under investigations
       mygrid    - all the grid points (size (Ngridpts, 2) with X and Y spatial location
       radius   - list of scales to be investigated
       T        - bandwith of fixed kernel OR distance upper boundary of adaptive kernel
       k        - number of min neighbors for the adaptive kernel smoothing. If k=0 : fixed kernel.
        

     Output :

       res - list of two dimensional numpy matrix (of size length(data) X length(radius)

              NWmean  : non weighted mean
              NWstd   : non weighted standart deviation
              Wmean   : weighted mean
              Wstd    : weighted standart deviation
              Mom     : weighted moment (order 0 to 4) of the absolute value of the coefficient. 
              Cum     : weighted cumulant (order one and two) of the coefficient. 


    """

    # make the tree accordingly to k
    Tmax = np.nanmax(Tloc)
    
    neighbors_i_fixed, dist_ie_fixed = tree.query_radius(mygrid[index2,:], r = Tmax, count_only=False, return_distance=True, sort_results=False)

    
    print('.',end='')
    sys.stdout.flush()
 
    # non weighted coef
    tmp_fixed2=[ Count[IndexNear[neighbors_i_fixed[igrid]],:] for igrid in range (len(index2))]
    lead_tmp_fixed2=[ lCount[IndexNear[neighbors_i_fixed[igrid]],:] for igrid in range (len(index2))]
    # number of  coef
    ltmp=np.array([ len(dist_ie_fixed[igrid]) for igrid in range (len(index2))])
    # the weight
    Wfinal2=[  weightingfunction(dist_ie_fixed[igrid], Tloc[igrid]) for igrid in range (len(index2))]
    # compute D0 and moments
    D0 = np.array([(np.nansum( Wfinal2[igrid]*np.abs(tmp_fixed2[igrid])**-1  , axis=0)) for igrid in range(len(index2))])
    D0 = D0**-1
    print('.',end='')
    Mom1 = np.array([np.nansum( np.abs(tmp_fixed2[igrid]) * Wfinal2[igrid], axis=0)  for igrid in range(len(index2))])
    print('.',end='')
    Mom2 = np.array([np.nansum( tmp_fixed2[igrid]**2 * Wfinal2[igrid], axis=0)  for igrid in range(len(index2))])
    print('.',end='')
    print('.',end='')
    Mom4 = np.array([np.nansum( tmp_fixed2[igrid]**4 * Wfinal2[igrid], axis=0)  for igrid in range(len(index2))])
    print('. ',end='')
    sys.stdout.flush()
    
    # compute Non weighted std
    newdist=[ localdist(dist_ie_fixed[igrid],Tloc[igrid])  for igrid in range(len(index2))]
   
    NWstd = np.array([np.nanstd( tmp_fixed2[igrid]*newdist[igrid][:,np.newaxis], axis=0, ddof=1) for igrid in range(len(index2))])
    NWstd[ltmp<=10,:] =0
    NWmean = np.array([np.nanmean( tmp_fixed2[igrid]*newdist[igrid][:,np.newaxis], axis=0) for igrid in range(len(index2))])
    NWmean[ltmp<=10,:]=0          
    print('*',end='')
    sys.stdout.flush()
    
    # compute weighted mean and std
    average = np.array([ np.nansum(tmp_fixed2[igrid]*Wfinal2[igrid], axis=0) for igrid in range(len(index2))])
    Wmean = average
    Wmean[ltmp<=10,:]=0      
    Wstd  = np.array([np.nansum((tmp_fixed2[igrid]-average[igrid])**2*Wfinal2[igrid], axis=0) for igrid in range(len(index2))])
    Wstd[ltmp<=10,:]=0
    Wstd = np.sqrt(Wstd)
    print('* ',end='')
    
    # compute Weighted cumulant
    average= np.array([logaverage(tmp_fixed2[igrid], Wfinal2[igrid]) for igrid in range(len(index2))])    
    Cum1 = average
    Cum1[ltmp<=10,:]=0     
    print('+',end='')
    lead_average =  np.array([logaverage(lead_tmp_fixed2[igrid], Wfinal2[igrid]) for igrid in range(len(index2))])
    Cum2=np.array([logaverage2(lead_tmp_fixed2[igrid],lead_average[igrid], Wfinal2[igrid]) for igrid in range(len(index2))])
    Cum2[ltmp<=10,:]=0   
    print('+ ',end='')
    
    Mean_std=np.stack([Wmean, Wstd], axis = 0)
    Mom12=np.stack([ Mom1, Mom2],axis=0)
    Cum=np.stack([Cum1, Cum2],axis = 0)
    Flatness=Mom4/(3*Mom2**2)
    sys.stdout.flush()   

    return Mean_std, Mom12, Flatness, Cum
# %% Local Multiscale Analysis
# add Tloc and function
def LocalMsAnalysisVD(data,Count,lCount,X,Y,radius, T, adaptive = False, weights = 'flat',  Nanalyse=2**16, Tloc=[]):
    """

    res = WaveSmoothingOptim(data,Wave,X,Y,radius,T,Nanalyse=2**16, k = 0, isvalued=0))

    For marked and non-marked point process
    Compute kernel smoothing of the wavelet coefficient of a dataset of points.
    The geographical weighting is obtained using the bi-squared function of size T.
   
    Input :

       data     - matrix of size Nx2 --> position (x,y) for N points
       mq       - matrix of size Nxlength(radius) with multiresolution quantity count
                  Can be obtained using the function  LomPy.m
       X        - array of dim 2 with x-postion of the grid nodes
       Y        - array of dim 2 with y-postion of the grid nodes : X and Y must have the same size
       radius   - list of scales to be investigated
       T        - bandwith of fixed kernel OR distance upper boundary of adaptive kernel
       Nanalyse - number of points to analyse in one bach. Default is 2**16 points.
       G        - mean of all pilot density estimates
       isvalued - boolean. If = 1 remove the grid point where the value of the point inside thegrid pixel are all 0.
       

     Output :

       res - list of two dimensional numpy matrix (of size length(data) X length(radius)

              res[Ø] = Wmean   : weighted mean
              res[1] = Wstd    : weighted standart deviation
              res[2] = NWratio : non weighted mean
              res[3] = NWstd   : non weighted standart deviation
              res[4] = Mom     : weighted moment (order 0 to 4) of the absolute value
                      of thecoefficient. matrix of size 5 X length(data) X length(radius)
              res[5] = Cum     : weighted cumulant one and two 
                      of thecoefficient. matrix of size 2 X length(data) X length(radius)
    """


    si=data.shape
    if si[1] < 2 or si[1]>3:
        raise TypeError('The second dimension of first argument must be of length 2 or 3.')
        
    if Count.ndim > 2:
        raise TypeError('The second arument must be two or threedimensional.')

    if Count.shape[0] != si[0]:
        raise TypeError('The twofirst arument must have the same length.')

    if radius[radius>T].shape[0] >0:
        raise TypeError('The last argument must be greater than a sqrt(2)*radius.')

    # check grid
    if np.sum(np.abs(np.array(X.shape)-np.array(Y.shape)))>0:
        raise TypeError('X and Y must have the same size.')

    if np.sum(np.diff(X,axis=1,n=2))>0:
        raise TypeError('X must be regulary sampled.')
    else:
        gridsizex=max(X[0][1] - X[0][0],X[1][0] - X[0][0])
        
    if np.sum(np.diff(Y,axis=0,n=2))>0:
        raise TypeError('Y must be regulary sampled.')
    else:
        gridsizey=max(Y[1][0] - Y[0][0],Y[0][1] - Y[0][0])
    
    if gridsizex != gridsizey:
        raise TypeError('X and Y must have same sampling.')
    
    if radius.size != Count.shape[1]:
        raise TypeError('The size of the second arument must be [N,R,M] where R is the number of scales (=radius.size)')
     
    
    # create grid points
    mygrid=np.column_stack([X.flatten(),Y.flatten()])
    gridlength=mygrid.shape[0]
    gridsizecurr = gridsizex
    
    Nanalyse2=300000
    if Nanalyse==0:
        print('Warning : dangerous if your set of data is large.')
        Nanalyse=gridlength
        Nbunch=1
    else: # find how many bunchs       
        Nbunch = np.ceil(gridlength/Nanalyse).astype(int)

    if isinstance(weights, str):
        if weights == 'flat':
            weightingfunction = partial(geographicalWeight,func = flatWindow)
            print('No weight')
        elif weights == 'Epanechnikov':
            weightingfunction = partial(geographicalWeight,func = EpanechnikovWindow)
        elif weights == 'bisquare':
            weightingfunction = partial(geographicalWeight,func = bisquareWindow)
        elif weights == 'triangular':
            weightingfunction = partial(geographicalWeight,func = triangularWindow)
        elif weights == 'tricube':
            weightingfunction = partial(geographicalWeight,func = tricubeWindow)
            
    elif isinstance(weights, types.FunctionType):
        weightingfunction = partial(geographicalWeight,func = weights)
    else:
        raise TypeError('ERROR : weighting is of unknown type.).')
        
    
    # results allocations    
    Cum = np.nan*np.zeros( (2, gridlength,radius.size), dtype=float)
    Mean_Std = np.nan*np.zeros( (2, gridlength,radius.size), dtype=float)
    Mom12 = np.nan*np.zeros( (2, gridlength,radius.size), dtype=float)
    Flatness = np.nan*np.zeros( (gridlength,radius.size), dtype=float)
    if adaptive == True:
        if len(Tloc) ==0: # compute local env
            print('ADAPTIVE KERNEL: Computing pilot density')
            CountT= localWaveTrans(data[:,(0,1)], np.atleast_1d(T))
            WmeanStd_T, Mom_T, Flat_T, Cum_T = LocalMsAnalysisVD(data[:,(0,1)],CountT,X,Y,np.atleast_1d(T), T=T,weights = 'Epanechnikov',Nanalyse=2**16)
            Wmean_Tloc = WmeanStd_T[0,:,0]
            G = np.nanmean(Wmean_Tloc)
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", category=RuntimeWarning)
                lambda_ie = G/Wmean_Tloc
            Tloc = lambda_ie*T
            Tloc[np.isinf(Tloc)] = T
            Tlocmax = np.nanquantile(Tloc,0.95)#.9
            Tloc[Tloc>Tlocmax] = Tlocmax 
            Tlocmin = np.nanquantile(Tloc,0.05)#.05
            Tloc[Tloc<Tlocmin] = Tlocmin 
            T=Tlocmax
            print('ADAPTIVE KERNEL computed.')
        elif X.flatten().shape[0] == Tloc.flatten().shape[0]:
            T=np.nanmax(Tloc)
        else: 
            raise TypeError('ERROR : wrong size for the local environment')
    else:
        Tloc=T*np.ones(X.size)
        
    # Loop on bunch
    for ibunch in range(Nbunch):
        # %
        print('bunch {:d}/{:d} '.format(ibunch+1,Nbunch), end=' ')
        sys.stdout.flush()
        # get data index of current bunch
        index=np.arange(ibunch*Nanalyse,(ibunch+1)*Nanalyse,1)
        index=index[index<gridlength]

        # we restrict the tree to points whithin a radius T (which must be > radius2)
        mi=np.min(mygrid[index,:], axis=0)
        ma=np.max(mygrid[index,:], axis=0)
        IndexNear=np.where((data[:,0] >mi[0]-T) & (data[:,0] <ma[0]+T) & (data[:,1]  >mi[1]-T) & (data[:,1] <ma[1]+T))[0]
         
        # make the tree with the nearest points only
        if IndexNear.shape[0]>0:
                #print('coucou',len(IndexNear))
                tree = KDTree(data[IndexNear,0:2])
                Idxtot = tree.query_radius(mygrid[index,:], r =  np.sqrt(2)*(gridsizecurr/2), count_only=False, return_distance=False)

                # find and remove empty (no point location) grid pixels
                thelengths=np.array([ Idxtot[igrid].shape[0] for igrid in range (len(Idxtot))])
                IdxMin, = np.where(thelengths>0.)
                index = index[IdxMin]
                Idxtot=Idxtot[IdxMin]
                thelengths=thelengths[IdxMin]
                    
                # Managed the number of grid points  (too many neighboors for some)
                cumsumbunch=np.cumsum(thelengths)
                
                Nflowers=int(np.ceil(np.sum(thelengths)/Nanalyse2))
                print('{:d} batch(s).'.format(Nflowers))
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore", category=RuntimeWarning)
                    
                    for iflower in range(Nflowers):
                        i1,=np.where(iflower*Nanalyse2 <= cumsumbunch)
                        i2,=np.where(cumsumbunch <  (iflower+1)*Nanalyse2)
                        flowers=np.intersect1d(i1,i2)
                        Mean_Std[:,index[flowers],:], Mom12[:,index[flowers],:], Flatness[index[flowers],:],Cum[:,index[flowers],:]=computeGridValue(tree,Count,lCount,IndexNear,index[flowers],mygrid, radius,Tloc[index[flowers]],weightingfunction)
                
                print('')

    if adaptive == True:
        return Mean_Std, Mom12, Flatness, Cum, Tloc
    else:
        return Mean_Std, Mom12, Flatness, Cum
        
    
# %% Local Multiscale Analysis
# add Tloc and function
def LmsAnalysisPP(data,Count,lCount,X,Y,radius, T, adaptive = False, weights = 'flat',  Nanalyse=2**16, Tloc=[]):
    """

    res = WaveSmoothingOptim(data,Wave,X,Y,radius,T,Nanalyse=2**16, k = 0, isvalued=0))

    For marked and non-marked point process
    Compute kernel smoothing of the wavelet coefficient of a dataset of points.
    The geographical weighting is obtained using the bi-squared function of size T.
   
    Input :

       data     - matrix of size Nx2 --> position (x,y) for N points
       Wave     - matrix of size Nxlength(radius) with wavelet count
                  Can be obtained using the function  GWFA_count.m
       X        - array of dim 2 with x-postion of the grid nodes
       Y        - array of dim 2 with y-postion of the grid nodes : X and Y must have the same size
       radius   - list of scales to be investigated
       T        - bandwith of fixed kernel OR distance upper boundary of adaptive kernel
       Nanalyse - number of points to analyse in one bach. Default is 2**16 points.
       G        - mean of all pilot density estimates
       isvalued - boolean. If = 1 remove the grid point where the value of the point inside thegrid pixel are all 0.
       

     Output :

       res - list of two dimensional numpy matrix (of size length(data) X length(radius)

              res[Ø] = Wmean   : weighted mean
              res[1] = Wstd    : weighted standart deviation
              res[2] = NWratio : non weighted mean
              res[3] = NWstd   : non weighted standart deviation
              res[4] = Mom     : weighted moment (order 0 to 4) of the absolute value
                      of thecoefficient. matrix of size 5 X length(data) X length(radius)
              res[5] = Cum     : weighted cumulant one and two 
                      of thecoefficient. matrix of size 2 X length(data) X length(radius)

    """


    si=data.shape
    if si[1] < 2 or si[1]>3:
        raise TypeError('The second dimension of first argument must be of length 2 or 3.')
        
    if Count.ndim > 2:
        raise TypeError('The second arument must be two or threedimensional.')

    if Count.shape[0] != si[0]:
        raise TypeError('The twofirst arument must have the same length.')

    if radius[radius>T].shape[0] >0:
        raise TypeError('The last argument must be greater than a sqrt(2)*radius.')

    # # check grid
    # if np.sum(np.abs(np.array(X.shape)-np.array(Y.shape)))>0:
    #     raise TypeError('X and Y must have the same size.')

    # if np.sum(np.diff(X,axis=1,n=2))>0:
    #     raise TypeError('X must be regulary sampled.')
    # else:
    #     gridsizex=max(X[0][1] - X[0][0],X[1][0] - X[0][0])
        
    # if np.sum(np.diff(Y,axis=0,n=2))>0:
    #     raise TypeError('Y must be regulary sampled.')
    # else:
    #     gridsizey=max(Y[1][0] - Y[0][0],Y[0][1] - Y[0][0])
    
    # if gridsizex != gridsizey:
    #     raise TypeError('X and Y must have same sampling.')
    
    if radius.size != Count.shape[1]:
        raise TypeError('The size of the second arument must be [N,R,M] where R is the number of scales (=radius.size)')
     
    
    # create grid points
    mygrid=np.column_stack([X.flatten(),Y.flatten()])
    gridlength=mygrid.shape[0]
    #gridsizecurr = gridsizex
    
    Nanalyse2=300000
    if Nanalyse==0:
        print('Warning : dangerous if your set of data is large.')
        Nanalyse=gridlength
        Nbunch=1
    else: # find how many bunchs       
        Nbunch = np.ceil(gridlength/Nanalyse).astype(int)
    
    #print('Computing in {:d} bunch(es)'.format(Nbunch))
    # choose weighting
    
    if isinstance(weights, str):
        if weights == 'flat':
            weightingfunction = partial(geographicalWeight,func = flatWindow)
            print('No weight')
        elif weights == 'Epanechnikov':
            weightingfunction = partial(geographicalWeight,func = EpanechnikovWindow)
        elif weights == 'bisquare':
            weightingfunction = partial(geographicalWeight,func = bisquareWindow)
        elif weights == 'triangular':
            weightingfunction = partial(geographicalWeight,func = triangularWindow)
        elif weights == 'tricube':
            weightingfunction = partial(geographicalWeight,func = tricubeWindow)
            
    elif isinstance(weights, types.FunctionType):
        weightingfunction = partial(geographicalWeight,func = weights)
    else:
        raise TypeError('ERROR : weighting is of unknown type.).')
        
    
    # results allocations    
    Cum = np.nan*np.zeros( (2, gridlength,radius.size), dtype=float)
    # new alloc :
    Mean_Std = np.nan*np.zeros( (2, gridlength,radius.size), dtype=float)
    Mom12 = np.nan*np.zeros( (2, gridlength,radius.size), dtype=float)
    Flatness = np.nan*np.zeros( (gridlength,radius.size), dtype=float)
    if adaptive == True:
        if len(Tloc) ==0: # compute local env
            print('ADAPTIVE KERNEL: Computing pilot density')
            CountT= localWaveTrans(data[:,(0,1)], np.atleast_1d(T))
            WmeanStd_T, Mom_T, Flat_T, Cum_T = LocalMsAnalysisVD(data[:,(0,1)],CountT,X,Y,np.atleast_1d(T), T=T,weights = 'Epanechnikov',Nanalyse=2**16)
            Wmean_Tloc = WmeanStd_T[0,:,0]
            G = np.nanmean(Wmean_Tloc)
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", category=RuntimeWarning)
                lambda_ie = G/Wmean_Tloc
            Tloc = lambda_ie*T
            Tloc[np.isinf(Tloc)] = T
            Tlocmax = np.nanquantile(Tloc,0.95)#.9
            Tloc[Tloc>Tlocmax] = Tlocmax 
            Tlocmin = np.nanquantile(Tloc,0.05)#.05
            Tloc[Tloc<Tlocmin] = Tlocmin 
            T=Tlocmax
            print('ADAPTIVE KERNEL computed.')
        elif X.flatten().shape[0] == Tloc.flatten().shape[0]:
            T=np.nanmax(Tloc)
        else: 
            raise TypeError('ERROR : wrong size for the local environment')
    else:
        Tloc=T*np.ones(X.size)
        
    # Loop on bunch
    for ibunch in range(Nbunch):
        # %
        print('bunch {:d}/{:d} '.format(ibunch+1,Nbunch), end=' ')
        sys.stdout.flush()
        # get data index of current bunch
        index=np.arange(ibunch*Nanalyse,(ibunch+1)*Nanalyse,1)
        index=index[index<gridlength]

        # we restrict the tree to points whithin a radius T (which must be > radius2)
        mi=np.min(mygrid[index,:], axis=0)
        ma=np.max(mygrid[index,:], axis=0)
        IndexNear=np.where((data[:,0] >mi[0]-T) & (data[:,0] <ma[0]+T) & (data[:,1]  >mi[1]-T) & (data[:,1] <ma[1]+T))[0]
         
        # make the tree with the nearest points only
        if IndexNear.shape[0]>0:
                tree = KDTree(data[IndexNear,0:2])
                Idxtot = tree.query_radius(mygrid[index,:], r = np.nanmax(radius), count_only=False, return_distance=False)
                # find and remove empty (no point location) grid pixels
                thelengths=np.array([ Idxtot[igrid].shape[0] for igrid in range (len(Idxtot))])
                IdxMin, = np.where(thelengths>0.)
                index = index[IdxMin]
                Idxtot=Idxtot[IdxMin]
                thelengths=thelengths[IdxMin]
            
                cumsumbunch=np.cumsum(thelengths)
                
                Nflowers=int(np.ceil(np.sum(thelengths)/Nanalyse2))
                print('{:d} batch(s).'.format(Nflowers))
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore", category=RuntimeWarning)
                    
                    #start = time.process_time()
                    for iflower in range(Nflowers):
                        i1,=np.where(iflower*Nanalyse2 <= cumsumbunch)
                        i2,=np.where(cumsumbunch <  (iflower+1)*Nanalyse2)
                        flowers=np.intersect1d(i1,i2)
                        Mean_Std[:,index[flowers],:], Mom12[:,index[flowers],:], Flatness[index[flowers],:],Cum[:,index[flowers],:]=computeGridValue(tree,Count,lCount,IndexNear,index[flowers],mygrid, radius,Tloc[index[flowers]],weightingfunction)
                
                print('')
    return Mean_Std, Mom12, Flatness, Cum

#%% 
def MultiresQuantitySupportVD(data,radius, Nanalyse=2**14,destination=np.array([]), NonUniformData=False):
    """
     Compute multiscale quantities of the support of  a list of coordinate. 
         - box counting of the finite values  N(r) for each point.
         - Hat wavelet coefs (2* N(r) -N(np.sqrt(2)*r) of the set of finite values 
                                  
    
    Count, HatSupport = MultiresQuantitySupportVD(data,radius, Nanalyse=2**14,destination=np.array([]), NonUniformData=False)
    
    Parameters
    ----------
    data : numpy array of float
        Two dimensional data set of shape  (N, 2) containing the position x and y of N points.
    radius : numpy array of  float
        vector of radius values of shape (Nr,).
    Nanalyse : integer, optional
        Size of the batch. The default is 2**14.
    destination : TYPE, optional
        DESCRIPTION. The default is np.array([]).
    NonUniformData : boolean, optional
        Set to true if the data are not uniformly sampled is space. 
        If true, run faster using optimized batch contents.
        The default is False.

    Raises
    ------
    TypeError 'This is for point process ONLY.
        The data is certainly an image and this function is ONLY for non uniformly sampled data.

    Returns
    -------
    Count : numpy array of float
        Box counting of the number of points in a ball of radius radius around each data points.
        Count.shape = (N, Nr).
    HatSupport : numpy array of float
        Hat wavelet coefficients of the support : 2 * N(r) - N(sqrt(2) * r ).
        Count.shape = (N, Nr).

    """
    # check input data
    isimage, ismarked, Nmark = checkinputdata(data)
    if isimage:
        raise TypeError('This is for point process ONLY.')
    
    # we compute Box Counting B(r) nad B(r)-B(sqrt(2)*r)
    Count1 = localWaveTrans(data, radius, Nanalyse = Nanalyse, destination = destination, NonUniformData = NonUniformData)
    Count2 = localWaveTrans(data, radius*np.sqrt(2), Nanalyse = Nanalyse, destination = destination, NonUniformData = NonUniformData, verbose = False)
    
    Count = Count1
    HatSupport = 2 * Count1 - Count2
        
    return Count, HatSupport

#%% MultiresQuantityMarkVD
def MultiresQuantityMarkVD( data, radius, Nanalyse = 2**14, destination = np.array([]), NonUniformData=False):
    # check input data
    isimage, ismarked, Nmark = checkinputdata( data)
    if isimage:
        raise TypeError('This is for point process ONLY.')
    
    Poor1, Count1 = localWaveTrans(data, radius, Nanalyse = Nanalyse)
    Poor2, Count2 = localWaveTrans(data, radius * np.sqrt(2), Nanalyse = Nanalyse, verbose = False)
    
    print(' ---- Computing leader of coefs.')
    Count = Count1[ :, :, 0]
    HatSupport = 2 * Count1[ :, :, 0] - Count2[ :, :, 0]
    Mean = Count1[ :, :, 1]
    HatMean = Count1[ :, :, 1] - Count2[ :, :, 1]
    LHatMean = localLeadersP(data[:, (0, 1)], HatMean, radius, Nanalyse = 2**14, verbose = False)
    HatStd = Count1[:,:,2] - Count2[:,:,2]
    Poor = Poor1[ :, :, 1]   
    LPoor = localLeadersP( data[:, (0, 1)], Poor, radius, Nanalyse = 2**14, verbose = False)
    Std = Count1[ :, :, 2]
    
    
    return Count, HatSupport, Mean, HatMean, LHatMean, Poor, LPoor, Std, HatStd     
        
#%%  MultiresQuantityVD
def MultiresQuantityVD(data,radius, Nanalyse=2**14,destination=np.array([]), NonUniformData=False, fftplan=[]):
    """
    

    Parameters
    ----------
    data : TYPE
        DESCRIPTION.
    radius : TYPE
        DESCRIPTION.
    Nanalyse : TYPE, optional
        DESCRIPTION. The default is 2**14.

    Returns
    -------
    Count : TYPE
        DESCRIPTION.
    HatSupport : TYPE
        DESCRIPTION.
    HatMean : TYPE
        DESCRIPTION.
    HatStd : TYPE
        DESCRIPTION.
    Poor : TYPE
        DESCRIPTION.
    LogPoor : TYPE
        DESCRIPTION.

    """
    # check input data
    isimage, ismarked, Nmark = checkinputdata(data)
   
    # choose method
    if (ismarked == 0) & (not isimage) :        
        
        #waveletKnnSupport
        Count, HatSupport = MultiresQuantitySupportVD(data,radius, Nanalyse=Nanalyse,destination=destination, NonUniformData=NonUniformData)
        
        Mean = np.array([])
        HatMean = np.array([])
        LHatMean = np.array([])
        Poor = np.array([])
        LPoor = np.array([])
        Std = np.array([])
        HatStd = np.array([])
        
    
    else: # marked points
        if isimage:
            #grrr
            #Count, HatSupport, Mean, HatMean, LHatMean, Poor, LPoor, Std, HatStd = computeHatCoefsConv2d(data, radius)
            Count, HatSupport, Mean, HatMean, LHatMean, Poor, LPoor, Std, HatStd = conv2D.MultiresQuantityConv(data, radius, fftplan=[])
        else:
            #hhhhh
            Count, HatSupport, Mean, HatMean, LHatMean, Poor, LPoor, Std, HatStd  = MultiresQuantityMarkVD(data,radius, Nanalyse=Nanalyse,destination=destination, NonUniformData=NonUniformData)
            
            
                
    return Count, HatSupport, Mean, HatMean, LHatMean, Poor, LPoor, Std, HatStd

def MultiresQuantityConv1d(data, radius, wavelet ='poor'):
    if wavelet == 'harr':
        Count, HatSupport, Mean, HatMean, LHatMean, Poor, LPoor, Std, HatStd  = conv2D.computeHarrCoefsConv1d(data, radius)
    else:# Hat
        Count, HatSupport, Mean, HatMean, LHatMean, Poor, LPoor, Std, HatStd = conv2D.computeCoefsConv1d(data, radius)
    # manque moyenne, log de la moyenne , std et std Hat
    #elif wavelet == 'harr':
    #elif wavelet == 'hat':
    
    return Count, HatSupport, Mean, HatMean, LHatMean, Poor, LPoor, Std, HatStd

# %%
def computeGridValuebivar(tree, Count1, Count2, IndexNear, index, mygrid, radius, Tloc, weightingfunction):
    """

    rhoss = computeGridValuebivarSS(tree,Count,IndexNear,index,mygrid, radius, T, k=0):

    For marked and non-marked point process
    Compute weighted statistics of the number of point location or value.
    The (geographical) weighting is obtained using the bi-squared function of size T.
       
    Input :

       tree      - a kdtree obtained on the IndexNear points (a subset of the Npts total points)
       Count     - matrix of size Nptsxlength(radius) with wavelet coef
       IndexNear - location of the points used for the kdtree
       index     - index of the grid points under investigations
       mygrid    - all the grid points (size (Ngridpts, 2) with X and Y spatial location
       radius   - list of scales to be investigated
       T        - bandwith of fixed kernel OR distance upper boundary of adaptive kernel
       k        - number of min neighbors for the adaptive kernel smoothing. If k=0 : fixed kernel.
        

     Output :

       rhoss - self similar correlation coefficient (of size length(data) X length(radius)

    """
    
    Tmax = np.nanmax(Tloc)
    neighbors_i_fixed, dist_ie_fixed = tree.query_radius(mygrid[index,:], r = Tmax, count_only=False, return_distance=True, sort_results=False)
    print('.',end='')
    sys.stdout.flush()

    # non weighted coef
    tmp_fixed1=[ Count1[IndexNear[neighbors_i_fixed[igrid]],:] for igrid in range (len(index))]
    tmp_fixed2=[ Count2[IndexNear[neighbors_i_fixed[igrid]],:] for igrid in range (len(index))]

    Wfinal=[  weightingfunction(dist_ie_fixed[igrid], Tloc[igrid]) for igrid in range (len(index))]
   
    m01=np.array([ np.nansum(tmp_fixed1[igrid] * Wfinal[igrid], axis=0) for igrid in range(len(index))])
    m10=np.array([ np.nansum(tmp_fixed2[igrid] * Wfinal[igrid], axis=0) for igrid in range(len(index))])   
    m02=np.array([ np.nansum(tmp_fixed1[igrid]**2 * Wfinal[igrid], axis=0) for igrid in range(len(index))])
    m20=np.array([ np.nansum(tmp_fixed2[igrid]**2 * Wfinal[igrid], axis=0) for igrid in range(len(index))])
    m11=np.array([ np.nansum(tmp_fixed1[igrid] * tmp_fixed2[igrid] * Wfinal[igrid], axis=0) for igrid in range(len(index))])   
    var1=m02-m01**2
    var2=m20-m10**2
    rho= (m11-m01*m10)/np.sqrt(var1*var2)
    
    return rho
# 

# %% 
def LocalCorrAnalysisVD(data, Count1, Count2, X, Y, radius, T, adaptive=False, weights = 'flat', Nanalyse=2**16, Tloc=[]):
    """

   res = WaveSmoothingBivar(data,Wave,X,Y,radius,T,Nanalyse=2**16, k = 0)

   For marked and non-marked point process
   Compute kernel smoothing of the wavelet coefficient of a dataset of points.
   The geographical weighting is obtained using the bi-squared function of size T.
   Only for non valued analysis (non marked process)
   
   Input :

       data     - matrix of size Nx2 --> position (x,y) for N points
       Wave     - matrix of size Nxlength(radius) with wavelet count
                  Can be obtained using the function  GWFA_count.m
       X        - array of dim 2 with x-postion of the grid nodes
       Y        - array of dim 2 with y-postion of the grid nodes : X and Y must have the same size
       radius   - list of scales to be investigated
       T        - bandwith of fixed kernel OR distance upper boundary of adaptive kernel
       Nanalyse - number of points to analyse in one bach. Default is 2**16 points.
       k        - number of min neighbors for the adaptive kernel smoothing. If k=0 : fixed kernel.
       

   Output :

       res - list of two dimensional numpy matrix (of size length(data) X length(radius)

              res[Ø] = Wmean   : weighted mean
              res[1] = Wstd    : weighted standart deviation
              res[2] = NWratio : non weighted mean
              res[3] = NWstd   : non weighted standart deviation
              res[4] = Mom     : weighted moment (order 0 to 4) of the absolute value
                      of thecoefficient. matrix of size 5 X length(data) X length(radius)
              res[5] = Cum     : weighted cumulant one and two 
                      of thecoefficient. matrix of size 2 X length(data) X length(radius)

    """
    assert(Count1.shape == Count2.shape)
    
    si=data.shape
    if si[1] < 2 or si[1]>3:
        raise TypeError('The second dimension of first argument must be of length 2 or 3.')

    if Count1.ndim > 2:
        raise TypeError('The second arument must be two or threedimensional.')
   
    if Count1.shape[0] != si[0]:
        raise TypeError('The two first arument must have the same length.')

    if radius[radius>T].shape[0] >0:
        raise TypeError('The last argument must be greater than a sqrt(2)*radius.')
    # check grid
    if np.sum(np.abs(np.array(X.shape)-np.array(Y.shape)))>0:
        raise TypeError('X and Y must have the same size.')

    if np.sum(np.diff(X,axis=1,n=2))>0:
        raise TypeError('X must be regulary sampled.')
    else:
        gridsizex=max(X[0][1] - X[0][0],X[1][0] - X[0][0])
        
    if np.sum(np.diff(Y,axis=0,n=2))>0:
        raise TypeError('Y must be regulary sampled.')
    else:
        gridsizey=max(Y[1][0] - Y[0][0],Y[0][1] - Y[0][0])
    
    if gridsizex != gridsizey:
        raise TypeError('X and Y must have same sampling.')
    
    if radius.size != Count1.shape[1]:
        #print(radius.size, Count.shape[1])
        raise TypeError('The size of the second arument must be [N,R,M] where R is the number of scales (=radius.size)')
 
    # create grid points
    mygrid=np.column_stack([X.flatten(),Y.flatten()])
    gridlength=mygrid.shape[0]
    gridsizecurr = gridsizex


    Npairs=1
    print('There is {:d} different pair(s)'.format(Npairs))
    
    Nanalyse2=300000
    if Nanalyse==0:
        print('Warning : dangerous if your set of data is large.')
        Nanalyse=gridlength
        Nbunch=1
    else: # find how many bunchs        
        Nbunch = int(np.ceil(gridlength/Nanalyse))
    
    # choose weighting  
    if isinstance(weights, str):
        if weights == 'flat':
            weightingfunction = partial(geographicalWeight,func = flatWindow)
            print('No weight')
        elif weights == 'Epanechnikov':
            weightingfunction = partial(geographicalWeight,func = EpanechnikovWindow)
        elif weights == 'bisquare':
            weightingfunction = partial(geographicalWeight,func = bisquareWindow)
        elif weights == 'triangular':
            weightingfunction = partial(geographicalWeight,func = triangularWindow)
        elif weights == 'tricube':
            weightingfunction = partial(geographicalWeight,func = tricubeWindow)            
    elif isinstance(weights, types.FunctionType):
        weightingfunction = partial(geographicalWeight,func = weights)
    else:
        raise TypeError('ERROR : weighting is of unknown type.).')

    if adaptive == True:
        if len(Tloc) ==0: # compute local env
            print('ADAPTIVE KERNEL: Computing pilot density')
            CountT= localWaveTrans(data[:,(0,1)], np.atleast_1d(T))
            WmeanStd_T, Mom_T, Flat_T, Cum_T = LocalMsAnalysisVD(data[:,(0,1)],CountT,X,Y,np.atleast_1d(T), T=T,Nanalyse=2**9)
            Wmean_Tloc = WmeanStd_T[0,:,0]
            G = np.nanmean(Wmean_Tloc)
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", category=RuntimeWarning)
                lambda_ie = G/Wmean_Tloc
            Tloc = lambda_ie*T
            Tloc[np.isinf(Tloc)] = T
            Tlocmax = np.nanquantile(Tloc,0.95)#.9
            Tloc[Tloc>Tlocmax] = Tlocmax 
            Tlocmin = np.nanquantile(Tloc,0.05)#.05
            Tloc[Tloc<Tlocmin] = Tlocmin 
            T=Tlocmax
            print('ADAPTIVE KERNEL computed.')
        elif X.flatten().shape[0] == Tloc.flatten().shape[0]:
            T=np.nanmax(Tloc)
        else: 
            raise TypeError('ERROR : wrong size for the local environment')
    else:
        Tloc=T*np.ones(X.size)

    # results allocations
    rho = np.nan*np.zeros( (gridlength,radius.size), dtype = float)
       
    # loop on the bunch
    for ibunch in range(Nbunch):
        # %
        print('bunch {:d}/{:d} '.format(ibunch+1,Nbunch), end=' ')
        sys.stdout.flush()
        # get data index of current bunch
        index=np.arange(ibunch*Nanalyse,(ibunch+1)*Nanalyse,1)
        index=index[index<gridlength]

        # we restrict the tree to points whithin a radius T 
        mi=np.min(mygrid[index,:], axis=0)
        ma=np.max(mygrid[index,:], axis=0)
        IndexNear=np.where((data[:,0] >mi[0]-T) & (data[:,0] <ma[0]+T) & (data[:,1]  >mi[1]-T) & (data[:,1] <ma[1]+T))[0]

        # make the tree with the nearest points only
        if IndexNear.shape[0]>0:
            tree = KDTree(data[IndexNear,0:2])
            Idxtot = tree.query_radius(mygrid[index,:], r = np.sqrt(2)*gridsizecurr, count_only=False, return_distance=False)
        
        
            # find and remove empty (no point location) grid pixels
            thelengths=np.array([ Idxtot[igrid].shape[0] for igrid in range (len(Idxtot))])
            IdxMin, = np.where(thelengths>0.)
            index = index[IdxMin]
            Idxtot=Idxtot[IdxMin]
            thelengths=thelengths[IdxMin]
        
            # Managed the number of grid points  (too many neighboors for some)
            cumsumbunch=np.cumsum(thelengths)
            Nflowers=int(np.ceil(np.sum(thelengths)/Nanalyse2))
            print('{:d} batch(s).'.format(Nflowers))
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", category=RuntimeWarning)
                for iflower in range(Nflowers):
                    i1,=np.where(iflower*Nanalyse2 <= cumsumbunch)
                    i2,=np.where(cumsumbunch <  (iflower+1)*Nanalyse2)
                    flowers=np.intersect1d(i1,i2)
                    rho[index[flowers],:] = computeGridValuebivar(tree,Count1,Count2,IndexNear,index[flowers],mygrid, radius,Tloc[index[flowers]],weightingfunction)
        print('.')   
       
    return rho

#%% 
def AllLocalQuantities(data, coefs, radius, Nanalyse = 2**14,  NonUniformData = False, verbose = True):
    """
    
     [Count, Wave, CountG] = aveTrans(source, radius, T=None, Nanalyse=2**16, destination = []))
    
    
    
    Compute box-counting and wavelet coefficient on a valued/non valued set of data points.
    
    If the data are not valued, count for every data point
            -- the number of neighboors in ball of radius r (GWFA) : N(r).
            -- the wavelet coeficient at scale r (GWMFA) : 2*N(r)-N(sqrt(2)*r).
    
    If the data are valued, count for every datapoint
            -- the number of neighboors in ball of radius r, the mean and std of the marked value
            -- the wavelet coeficient at scale r on the marked value.
    
    Input :
    
        source     - Non-marked  point process : matrix of size N X 2 for N points
                        where source[i,:]=[X_i,Y_i] with 2D cooprdonate of point i.
                      Marked  point process :  matrix of size Nx3
                        where source[i,:]=[X_i,Y_i, mark_i] with 2D cooprdonate of point i and value
        radius      - list of scales to be investigated
        Nanalyse    - number of points to analyse in one bach. Default is 2**16 points.
                        If Nanalyse=0, compute all the points in once (dangerous!!!)
        destination - Non marked point process (destination_i=[X_I,Y_i]) where the coeficient are calculated
                        Default empty : compute at source position.
    Output :
    
        Count    - matrix of size Nxlength(radius) with box-counting coefficients
        Wave     - matrix of size Nxlength(radius) with wavelet coefficients
        Count    - matrix of size Nx2 with box-counting and wavelet coeficient at scale T
                  
    
    
    Usage exemple :
    

    """
 
    #% check input data
    si = data.shape
    if si[1] < 2: # or si[1]>3:
        raise TypeError('The second dimension of first argument must be of length 2 or 3.')
         
    destination = np.copy(data[:,0:2])
    #val = data[:,2]
    #valtot = data[:,2:]
    #data = data[:,0:2]
            
    radius = np.atleast_1d(radius)
    radiustot = np.sort(radius)
    #temp,temp2,indexreadius=np.intersect1d(radius,radiustot, return_indices=True)

    # some constants
    scalemax=np.max(radiustot)
    N = destination.shape[0]
    
    # sub parameters to partition  the data
    if Nanalyse==0: 
        print('Warning : dangerous if your set of data is large.')
        Nanalyse=N
        Nbunch=1
    else:
        # find how many bunchs
        if NonUniformData:
            centers, sizeblock = getoptimblock(destination, Nanalyse)
            Nbunch = len(sizeblock)
            if verbose:
                print('Block optimisation for non uniformly spaced data.')
                       
        else:
            sizetmp = Nanalyse
            temp= destination // sizetmp
            block, count = np.unique(temp, axis=0, return_counts=True)
            centers = block*sizetmp+sizetmp//2
            sizeblock = count*0+sizetmp
            Nbunch = len(block)
            if verbose:
                print('No block optimisation uniformly spaced data.')
            
    
    Nanalyse2 = 2**22
    if verbose:
        print('Computation in {:d} bunches :'.format(Nbunch),end=' ')  
    
   
    # allocation
    Count = np.nan*np.zeros((N,radius.shape[0],7),dtype=float)
    
    
    # set the workers for knn search
    neigh = NearestNeighbors(n_jobs=4)
    
    #% loop on the bunches
    for ibunch in range(Nbunch):
        #%
        print(ibunch+1, end=' ')
        sys.stdout.flush()
        #
        center = centers[ibunch,:]
        sizetmp = sizeblock[ibunch]
        #
        index, = np.where(((destination[:,0] >= center[0]-sizetmp//2) & (destination[:,0]< center[0]+sizetmp//2)) & ((destination[:,1]>= center[1]-sizetmp//2) & (destination[:,1]< center[1]+sizetmp//2)))
        IndexNear, = np.where(((destination[:,0] >= center[0]-(sizetmp//2+scalemax+1)) & (destination[:,0]< center[0]+(sizetmp//2+scalemax+1))) & ((destination[:,1]>= center[1]-(sizetmp//2+scalemax+1)) & (destination[:,1]< center[1]+(sizetmp//2+scalemax+1))))
        neigh.fit(destination[IndexNear,:])
               
        Disttot, IdxTot = neigh.radius_neighbors(destination[index,0:2], radius = scalemax, return_distance = True)
        Maxlength = max(map( len, IdxTot))        
        Nblock = int(np.ceil(index.shape[0] * Maxlength / Nanalyse2))           
        Nptx = len(index) // Nblock + 1
        if (Nblock - 1)*Nptx > min(len(index), Nblock * Nptx):
            Nblock = Nblock - 1
        
        malist2=[(IdxTot[i*Nptx:min(len(index),(i+1)*Nptx)], Disttot[i*Nptx:min(len(index),(i+1)*Nptx)]) for i in range(Nblock)]
        partialknncountbis = partial(threaded_All_Valued, radiustot = radiustot,val = coefs[IndexNear,:])      
        #%
        with ThreadPoolExecutor() as executor:
            result_list3 = executor.map(partialknncountbis, malist2)
        
        Count[index,:,:] = np.vstack(list(result_list3))
            
            
    del neigh
    print('.')
          
     
    return Count
    
#%%
def AllLocalQCorrCoef(data, coefs1, coefs2, radius, Nanalyse = 2**14,  NonUniformData = False, verbose = True):
    """
    
     [Count, Wave, CountG] = aveTrans(source, radius, T=None, Nanalyse=2**16, destination = []))
    
    
    
    Compute box-counting and wavelet coefficient on a valued/non valued set of data points.
    
    If the data are not valued, count for every data point
            -- the number of neighboors in ball of radius r (GWFA) : N(r).
            -- the wavelet coeficient at scale r (GWMFA) : 2*N(r)-N(sqrt(2)*r).
    
    If the data are valued, count for every datapoint
            -- the number of neighboors in ball of radius r, the mean and std of the marked value
            -- the wavelet coeficient at scale r on the marked value.
    
    Input :
    
        source     - Non-marked  point process : matrix of size N X 2 for N points
                        where source[i,:]=[X_i,Y_i] with 2D cooprdonate of point i.
                      Marked  point process :  matrix of size Nx3
                        where source[i,:]=[X_i,Y_i, mark_i] with 2D cooprdonate of point i and value
        radius      - list of scales to be investigated
        Nanalyse    - number of points to analyse in one bach. Default is 2**16 points.
                        If Nanalyse=0, compute all the points in once (dangerous!!!)
        destination - Non marked point process (destination_i=[X_I,Y_i]) where the coeficient are calculated
                        Default empty : compute at source position.
    Output :
    
        Count    - matrix of size Nxlength(radius) with box-counting coefficients
        Wave     - matrix of size Nxlength(radius) with wavelet coefficients
        Count    - matrix of size Nx2 with box-counting and wavelet coeficient at scale T
                  
        
    """
 
    #% check input data
    si = data.shape
    if si[1] < 2: # or si[1]>3:
        raise TypeError('The second dimension of first argument must be of length 2 or 3.')
         
    destination = np.copy(data[:,0:2])           
    radius = np.atleast_1d(radius)
    radiustot = np.sort(radius)

    # some constants
    scalemax=np.max(radiustot)
    N = destination.shape[0]
    
    # sub parameters to partition  the data
    if Nanalyse==0: # this is dangerous
        print('Warning : dangerous if your set of data is large.')
        Nanalyse=N
        Nbunch=1
    else:
        # find how many bunchs
        if NonUniformData:
            centers, sizeblock = getoptimblock(destination, Nanalyse)
            Nbunch = len(sizeblock)
            if verbose:
                print('Block optimisation for non uniformly spaced data.')
                       
        else:
            sizetmp = Nanalyse
            temp= destination // sizetmp
            block, count = np.unique(temp, axis=0, return_counts=True)
            centers = block*sizetmp+sizetmp//2
            sizeblock = count*0+sizetmp
            Nbunch = len(block)
            if verbose:
                print('No block optimisation uniformly spaced data.')
            
    
    Nanalyse2 = 2**22
    if verbose:
        print('Computation in {:d} bunches :'.format(Nbunch),end=' ')  
    
   
    # allocation
    Count = np.nan*np.zeros((N,radius.shape[0],2),dtype=float)
    
    
    # set the worker for knn search
    neigh = NearestNeighbors(n_jobs=4)
    
    #% loop on the bunches
    for ibunch in range(Nbunch):
        #%
        print(ibunch+1, end=' ')
        sys.stdout.flush()
        #
        center = centers[ibunch,:]
        sizetmp = sizeblock[ibunch]
        #
        index, = np.where(((destination[:,0] >= center[0]-sizetmp//2) & (destination[:,0]< center[0]+sizetmp//2)) & ((destination[:,1]>= center[1]-sizetmp//2) & (destination[:,1]< center[1]+sizetmp//2)))
        IndexNear, = np.where(((destination[:,0] >= center[0]-(sizetmp//2+scalemax+1)) & (destination[:,0]< center[0]+(sizetmp//2+scalemax+1))) & ((destination[:,1]>= center[1]-(sizetmp//2+scalemax+1)) & (destination[:,1]< center[1]+(sizetmp//2+scalemax+1))))
        neigh.fit(destination[IndexNear,:])
               

        Disttot, IdxTot = neigh.radius_neighbors(destination[index,0:2], radius = scalemax, return_distance = True)
        Maxlength = max(map( len, IdxTot))
        
        Nblock = int(np.ceil(index.shape[0] * Maxlength / Nanalyse2))           
        Nptx = len(index) // Nblock + 1
        if (Nblock - 1)*Nptx > min(len(index), Nblock * Nptx):
            Nblock = Nblock - 1        
        malist2=[(IdxTot[i*Nptx:min(len(index),(i+1)*Nptx)], Disttot[i*Nptx:min(len(index),(i+1)*Nptx)]) for i in range(Nblock)]
        partialknncountbis = partial(threaded_corr_coef, radiustot = radiustot,val1 = coefs1[IndexNear,:], val2 = coefs2[IndexNear,:])
        
        #%
        with ThreadPoolExecutor() as executor:
            result_list3 = executor.map(partialknncountbis, malist2)
        
        Count[index,:,:] = np.vstack(list(result_list3))
            
            
    del neigh
    print('.')
          
     
    return Count
    

    
    