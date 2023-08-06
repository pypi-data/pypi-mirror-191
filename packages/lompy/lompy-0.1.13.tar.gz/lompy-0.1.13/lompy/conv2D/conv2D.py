"""
======================================================
2D Convolution package for LomPy (:mod:`lompy.conv2D`)
======================================================
          
.. currentmodule: lompy.conv2D

The package features yield the multiresolution quantities and the local 
scaling parameters  for uniformly distributed (raster) 2D data


Overview
--------
Routines for the muliresolution quantities:
    
    lompy.conv2D.MultiresQuantityRD
    
Routines for the univariate local analysis:
    
    lompy.conv2D.LocalMsAnalysisRD

Routines for the bivariate local analysis:
    
    lompy.conv2D.LocalCorrAnalysisRD

"""

#Copyright (C) 2023 GNU AGPLv3, LomPy 2023, S.G. Roux and J. Lengyel.
#All rights reserved.
#Contact: stephane.roux@ens-lyon.fr, jankalengyel@gmail.com
#Other Contributors: P. Thiraux


import warnings
import numpy as np
import pyfftw
import multiprocessing

#%% 
pyfftw.interfaces.cache.enable()
pyfftw.config.NUM_THREADS = multiprocessing.cpu_count()
N_threads = multiprocessing.cpu_count()

#%%
def prepare_plan2d(Nx, Ny, N_threads = N_threads):
    """
    create plan for fftw
    
    a,fft_a, fft_object, b,ffti_b, ffti_object = prepare_plan2d(Nx, Ny, N_threads = N_threads)

    Parameters
    ----------
    Nx : integer
        x dimension of the plan.
    Ny : integer
        y dimension of the plan
    N_threads : integer, optional
        Number of thread to use. The default is multiprocessing.cpu_count.

    Returns
    -------
    a : numpy array of float64
        aligned memory.
    fft_a : numpy array of complex128
        aligned memory for fft.
    fft_object : fftw object.
        FORWARD fft_object.
    b : numpy array of float64
        aligned memory.
    ffti_b : numpy array of complex128
        aligned memory for fft.
    ffti_object : fftw object.
        BACKWARD' fft_object.

    """
    a     = pyfftw.empty_aligned((Nx, Ny), dtype='float64')
    fft_a = pyfftw.empty_aligned((Nx, Ny//2+1), dtype='complex128')
    fft_object = pyfftw.FFTW(a, fft_a, axes=(0,1), direction='FFTW_FORWARD', threads=N_threads)
        
    ffti_object = pyfftw.FFTW(fft_a, a, axes=(0,1), direction='FFTW_BACKWARD', threads=N_threads)
    return  fft_object, ffti_object

#%%
def do_fftplan2d( N, scales, N_threads = N_threads, wavelet = 'poor'):
    """
    Create fftw plan for fast wavelet transform
    
    a,fft_a, fft_object, b,ffti_b, ffti_object = do_fftplan2d( N, scales, N_threads = N_threads, wavelet = 'poor')

    Parameters
    ----------
    N : integer
        DESCRIPTION.
    scales : float
        vector of positive float.
    N_threads : integer, optional
        Number of thread to use. The default is multiprocessing.cpu_count..
    wavelet : TYPE, optional
        Wavelet to use. The default is 'poor'.

    Returns
    -------
    a : numpy array of float64
        aligned memory.
    fft_a : numpy array of complex128
        aligned memory for fft.
    fft_object : fftw object.
        FORWARD fft_object.
    b : numpy array of float64
        aligned memory.
    ffti_b : numpy array of complex128
        aligned memory for fft.
    ffti_object : fftw object.
        BACKWARD fft_object.

    """
    
    N1, N2 = N
    scales = np.atleast_1d(scales)
    if len(scales) == 1:
        maxradius = int(np.ceil(np.max(scales)))
    else:
        if np.char.equal(wavelet,'poor'):
            maxradius = int(np.ceil(np.max(scales)))
        else:
            maxradius = int(np.ceil(np.sqrt(2)*np.max(scales)))
    
    # add border
    N1 = N1 + 2 * maxradius
    N2 = N2 + 2 * maxradius
    Nk = 2 * maxradius + 1
    
    Nfft1 = N1 + Nk - 1
    Nfft2 = N2 + Nk - 1
    fft_object, ffti_object = prepare_plan2d(Nfft1, Nfft2, N_threads)

    return fft_object, ffti_object
#%
#%% 
def convFFTW(a, TFW, fft_object,ffti_object):
    """
    compute the inverse Fourier transform of the product of  
    FFT(a), the Fourier tranform of a,  by TFW. 
    
    temp2 = convFFTW(a, TFW, fft_object,ffti_object)
    
    Parameters
    ----------
    a : numpy array of float64
        signal or image.
    TFW : numpy array of complex128
        Fourier transform of a kernel.
    fft_object : fftw object.
        fftw object to use for FORWARD direction.
    ffti_object : ftw object.
        fftw object to use for BACKWARD direction.

    Returns
    -------
    temp2 : float64
        results.

    """
    b = fft_object(a)
    
    ar=ffti_object(b*TFW)
    temp2=np.copy(ar)
    return temp2
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

#%%
def threshkernelangle(kernel,thetaTot,theta,dtheta):
    
    if theta+dtheta/2 > np.pi:
        kernel[(thetaTot > theta+dtheta/2-2*np.pi) & (thetaTot < theta-dtheta/2)]=0
    elif theta-dtheta/2 < -np.pi:
        kernel[(thetaTot < theta-dtheta/2+2*np.pi) & (thetaTot > theta+dtheta/2)]=0
    else:
        kernel[thetaTot <= theta-dtheta/2]=0
        kernel[thetaTot > theta+dtheta/2]=0    
    return kernel
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
    using a local environment of T.
    
    Input :

       dist - distance of the point. dist and index as the shame shape
       T    - bandwith of fixed kernel OR distance upper boundary of adaptive kernel
       Nr   - number of replication of the weight
        
     Output :

       W - the weight. Array of size (len(dd),Nr)
   

    """  

    z = dd/T 
    W=func(z)
    W[dd>=T]=0
    W=W/np.sum(W,0)
    W=W[:,np.newaxis]
    return W

#%% 
def MultiresQuantityRD(image, radiustot, fftplan=[], theta=[], dtheta=[], p=2):
    """
    Compute multiscale quantities from an image (raster data structure). 
    The image can contain non-finite values.
        - box counting of the finite values  N(r) for each pixel
        - Hat wavelet coefficient (2* N(r) -N(np.sqrt(2)*r) of the set of finite values 
        - local mean, std, hat wavelet, and poor wavelet coefficient 
        of the image (discarding non-finite values) 
    
    Count, HatSupport, Mean, LMean, HatMean, LHatMean, Poor, LPoor, Std, HatStd = MultiresQuantityRD(image, radiustot, fftplan=[])


    Parameters
    ----------
    data: numpy array of float
        Two-dimensional data set of shape  (Nx, Ny).
    radius: numpy array of float
        vector of radius values of shape (Nr,).
    fftplan: fftw object, optional
        For fast computation, we can prepare fftw plan using the function
        do_fftplan2d. The default is [].

    Raises
    ------
    TypeError This is for image ONLY.
        The input data is not an image: a numpy array of size (Nx,Ny).

    Returns
    -------
    Count : numpy array of float
        box counting coefficient of the support: numpy array of  shape  (Nr, Nx, Ny).
        It's the number of non-nan values in a ball of radius r : N_x(r)
    HatSupport : numpy array of float
        Hat wavelet coefficient of the support: numpy array of  shape  (Nr, Nx, Ny).
        Defined as  2*N_x(r)-N_x(np.sqrt(2)*r)
    Mean : numpy array of float
        Local average (on a ball of size radius) of the mark : numpy array of  shape  (Nr, Nx, Ny).
        M_x(r)
    LMean : numpy array of float
        Local average of the logarithm of the mark: numpy array of  shape  (Nr, Nx, Ny).
    HatMean : numpy array of float
        Hat wavelet coefficient of the mark: numpy array of shape  (Nr, Nx, Ny).
        Defined as  M_x(r)-M_x(np.sqrt(2)*r)
    LHatMean : numpy array of float
        local Logarithm of Hat wavelet coefficient of the mark: numpy array of  shape  (Nr, Nx, Ny).
    Poor : numpy array of float
        Poor wavelet coefficient of the mark: numpy array of shape  (Nr, Nx, Ny).
        Defined as  data_x-M_x(r)
    LPoor : numpy array of float
        local Logarithm of  Poor wavelet coefficient of the mark: numpy array of  shape  (Nr, Nx, Ny).      
    Std : numpy array of float
        Local standard deviation (on a ball of size radius)  of the mark.
        numpy array of shape  (Nr, Nx, Ny). 
    HatStd : numpy array of float
        Local standard deviation (on a ball of size radius)  of the Hat wavelet coefficients. 
        numpy array of shape  (Nr, Nx, Ny). 

    """
    isimage, ismarked, Nmark = checkinputdata(image)
    if not isimage:
        raise TypeError('This is for image ONLY.')
    
    isAni = False
    if len(dtheta)+len(theta) == 2: # anisotropic case
        isAni = True
    image[np.isinf(image)] = np.nan
    maxradius = int(np.ceil(np.sqrt(2)*np.max(radiustot)))
    im = np.pad(image, ((maxradius, maxradius) ,(maxradius, maxradius)), constant_values=((np.nan, np.nan),(np.nan, np.nan)))
    
    IndNan = np.isnan(im)
    imcopy = np.copy(im)
    imcopy[IndNan] = 0
    im01 = np.ones(im.shape)
    im01[IndNan] = 0
    
    N1,N2 = imcopy.shape
    Nborder = int(np.ceil(np.sqrt(2)*np.max(radiustot)))
    Nk = 2*Nborder+1
    
    # define distance for filter
    y, x = np.ogrid[-Nborder:Nborder+1, -Nborder:Nborder+1]
    d = x**2 + y**2
    thetaTot = np.flip(np.arctan2(y,x),axis=0)
    
    # fftw plan
    Nfft1 = N1+Nk-1
    Nfft2 = N2+Nk-1
    
    if len(fftplan)==0:
        fft_object,  ffti_object = prepare_plan2d(Nfft1, Nfft2, N_threads)
    else:
        fft_object,  ffti_object = fftplan
   

    # allocations
    HatSupport = np.zeros((radiustot.shape[0], N1, N2))
    HatStd = np.zeros((radiustot.shape[0], N1, N2))
    Mean = np.zeros((radiustot.shape[0], N1, N2))
    HatMean = np.zeros((radiustot.shape[0], N1, N2))
    Poor  = np.zeros((radiustot.shape[0], N1, N2))
    Std = np.zeros((radiustot.shape[0], N1, N2))
    Count = np.zeros((radiustot.shape[0], N1, N2))
    
    LeadPoor = np.zeros((radiustot.shape[0], N1, N2))
    LeadHat = np.zeros((radiustot.shape[0], N1, N2))
    # loop on scales
    for ir in range(radiustot.shape[0]):
        # %
        print(ir, end=' ', flush = True)
        # first scale
        kernel = np.zeros((Nk,Nk))
        kernel[np.sqrt(d) <= radiustot[ir]]=1
        if isAni:
            kernel=threshkernelangle(kernel,thetaTot,theta,dtheta)
        TFW = np.copy(fft_object(np.pad(kernel, ((0, Nfft1-Nk) ,(0, Nfft2-Nk)), constant_values=((0, 0),(0,0)))))
        # count finite coefs
        imtmp = np.pad(im01, ((0, Nk-1) ,(0, Nk-1)  ), constant_values=((0, 0),(0,0)))
        CountValid1 = convFFTW(imtmp, TFW, fft_object,ffti_object)[Nborder:Nfft1-Nborder, Nborder:Nfft2-Nborder]       
        CountValid1[CountValid1 < 0.1] = np.nan # must be integer >0
        Cc = np.copy(CountValid1)
        Cc[IndNan] = np.nan
        # mean
        imtmp = np.pad(imcopy, ((0, Nk-1) ,(0, Nk-1)  ), constant_values=((0, 0),(0,0)))      
        lasum = convFFTW(imtmp, TFW, fft_object,ffti_object)[Nborder:Nfft1-Nborder, Nborder:Nfft2-Nborder]
        lamean = lasum / CountValid1
        lamean[IndNan] = np.nan
        # moment of order 2 and std
        lasum = convFFTW(imtmp**2, TFW, fft_object,ffti_object)[Nborder:Nfft1-Nborder, Nborder:Nfft2-Nborder]      
        M2 = lasum / CountValid1
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category = RuntimeWarning)
            lavar = np.maximum(M2-lamean**2,0)
            lastd = np.sqrt(lavar)   
        lastd[IndNan] = np.nan
        
        # Allocations
        Count[ir,:,:] = Cc
        Poor[ir,:,:] = lamean - im
        Mean[ir,:,:] = lamean
        Std[ir,:,:] = lastd

        
        # 2nd scales : for hat wavelet
        kernel = np.zeros((Nk,Nk))
        kernel[(np.sqrt(d) <= np.sqrt(2)*radiustot[ir]) & (np.sqrt(d) > radiustot[ir])] = 1
        if isAni:
            kernel=threshkernelangle(kernel,thetaTot,theta,dtheta)
        TFW = np.copy(fft_object(np.pad(kernel, ((0, Nfft1-Nk) ,(0, Nfft2-Nk)), constant_values=((0, 0),(0,0)))))
        # count finite coefs
        imtmp = np.pad(im01, ((0, Nk-1) ,(0, Nk-1)  ), constant_values=((0, 0),(0,0)))
        CountValid2 = convFFTW(imtmp, TFW, fft_object,ffti_object)[Nborder:Nfft1-Nborder, Nborder:Nfft2-Nborder]       
        CountValid2[CountValid2 < 0.1] = np.nan 
        Cc2 = np.copy(CountValid2)
        Cc2[IndNan] = np.nan
        # mean
        imtmp = np.pad(imcopy, ((0, Nk-1) ,(0, Nk-1)  ), constant_values=((0, 0),(0,0)))      
        lasum2 = convFFTW(imtmp, TFW, fft_object,ffti_object)[Nborder:Nfft1-Nborder, Nborder:Nfft2-Nborder]
        lamean2 = lasum2 / CountValid2
        lamean2[IndNan] = np.nan
        # moment of order2
        lasum = convFFTW(imtmp**2, TFW, fft_object,ffti_object)[Nborder:Nfft1-Nborder, Nborder:Nfft2-Nborder]
        M2 = lasum / CountValid2
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category = RuntimeWarning)
            lavar = np.maximum(M2 - lamean**2, 0)
            lastd2 = np.sqrt(lavar)              
        lastd2[IndNan] = np.nan
        # allocation
        HatSupport[ir,:,:] = Cc - Cc2
        HatMean[ir,:,:] = lamean - lamean2       
        HatStd[ir,:,:] = lastd - lastd2
        
        # Poor  Leaders
        Leadtmp=np.abs(Poor[ir,:,:])
        isnanLead = np.isnan(Leadtmp)
        
        kernel = np.zeros((Nk,Nk))
        kernel[np.sqrt(d) <= radiustot[ir]]=1
        TFW = np.copy(fft_object(np.pad(kernel, ((0, Nfft1-Nk) ,(0, Nfft2-Nk)), constant_values=((0, 0),(0,0)))))
        
        tmp = np.ones(Leadtmp.shape)
        tmp[isnanLead] = 0
        imtmp = np.pad(tmp, ((0, Nk-1) ,(0, Nk-1)  ), constant_values=((0, 0),(0,0)))
        CountValid = convFFTW(imtmp, TFW, fft_object,ffti_object)[Nborder:Nfft1-Nborder, Nborder:Nfft2-Nborder]       
        CountValid[CountValid < 0.1] = np.nan
        Leadtmp[isnanLead] = 0
        imtmp = np.pad(Leadtmp, ((0, Nk-1) ,(0, Nk-1)  ), constant_values=((0, 0),(0,0)))      
        lasum = convFFTW(imtmp**p, TFW, fft_object,ffti_object)[Nborder:Nfft1-Nborder, Nborder:Nfft2-Nborder]
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category = RuntimeWarning)
            lasum = lasum**(1/p) #/ CountValid
            #### ITT
            lasum[isnanLead]= np.nan 
        LeadPoor[ir,:,:] = lasum 
        
        # Poor  Hat
        Leadtmp=np.abs(HatMean[ir,:,:])
        isnanLead = np.isnan(Leadtmp)
        tmp = np.ones(Leadtmp.shape)
        tmp[isnanLead] = 0
        imtmp = np.pad(tmp, ((0, Nk-1) ,(0, Nk-1)  ), constant_values=((0, 0),(0,0)))
        CountValid = convFFTW(imtmp, TFW, fft_object,ffti_object)[Nborder:Nfft1-Nborder, Nborder:Nfft2-Nborder]       
        CountValid[CountValid < 0.1] = np.nan
        Leadtmp[isnanLead] = 0
        imtmp = np.pad(Leadtmp**p, ((0, Nk-1) ,(0, Nk-1)  ), constant_values=((0, 0),(0,0)))      
        lasum = convFFTW(imtmp, TFW, fft_object,ffti_object)[Nborder:Nfft1-Nborder, Nborder:Nfft2-Nborder]
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category = RuntimeWarning)
            lasum = lasum**(1/p)
            ####ITT
            lasum[isnanLead]= np.nan 
        LeadHat [ir,:,:] = lasum 

        
        
    print('.')         
    HatMean = HatMean[:, maxradius:-maxradius, maxradius:-maxradius]
    Poor = Poor[:, maxradius:-maxradius, maxradius:-maxradius]
    Mean = Mean[:, maxradius:-maxradius, maxradius:-maxradius]
    Std = Std[:, maxradius:-maxradius, maxradius:-maxradius]    
    Count = Count[:, maxradius:-maxradius, maxradius:-maxradius]    
    HatStd = HatStd[:, maxradius:-maxradius, maxradius:-maxradius]    
    HatSupport = HatSupport[:, maxradius:-maxradius, maxradius:-maxradius]     
    LeadPoor = LeadPoor[:, maxradius:-maxradius, maxradius:-maxradius] 
    LeadHat = LeadHat[:, maxradius:-maxradius, maxradius:-maxradius]     
    Count = Count.transpose(1, 2, 0)
    HatSupport = HatSupport.transpose(1, 2, 0)
    Mean = Mean.transpose(1, 2, 0)
    HatMean = HatMean.transpose(1, 2, 0)
    Poor = Poor.transpose(1, 2, 0)
    Std = Std.transpose(1, 2, 0)
    HatStd = HatStd.transpose(1, 2, 0)
    LeadPoor = LeadPoor.transpose(1, 2, 0)
    LeadHat = LeadHat.transpose(1, 2, 0)
    return Count, HatSupport, Mean, HatMean, LeadHat, Poor, LeadPoor, Std, HatStd 
#%%
def bisquarekernel(x):
    '''
        return bisaquare kernel weigths (1-x**2)**2 ewith -1< x< 1
        
        
        w=isquarekernel(x)
        
        Input :
            x vector of value taken between -1 and 1.
            
        Output :            
        
            w weigths values
        
     ##

    '''

    A = (1-x**2)**2
    A[np.abs(x) > 1] = 0
    #ITT norm
    return A
#%%
def LocalMsAnalysisRD(coefs,lcoefs,L, window='flatcircle',fftplan=[], gridsize=1):
    '''
        Compute localized statistics (moments and cumulants).
        
        Mom1, Mom2, Flatness ,Cum1, Cum2 = LocalMsAnalysisRD(coefs,lcoefs,L,window)
        
        Inputs :
            
            coefs  : set of ceoficients used to compute moments and flatness
            
            lcoefs:  set of leader coefficients used to compute the cumulants
            
            L : size of the average (integer stricty positif)
            
            window : weighting function to use. Default : window='flat'.
                     can be window='bisquare'
            
        Outputs :   
            
            Mom1, Mom2 : localized moment of order one and two
            
            Flatness : localized flatness
            
            cum1, cum2 : localized log cumulant of order one and two
            
        
     ##

    '''
    
    assert(coefs.shape == lcoefs.shape)
    # transpose axis
    coefs = coefs.transpose(2, 0, 1)
    lcoefs = lcoefs.transpose(2, 0, 1)
    
    LGcoefs = np.copy(coefs)
    LGcoefs = np.log(np.abs(LGcoefs))
    LGcoefs[np.isinf(LGcoefs)] = np.nan
    
    LGlcoefs = np.copy(lcoefs)
    LGlcoefs = np.log(np.abs(LGlcoefs))
    LGlcoefs[np.isinf(LGlcoefs)] = np.nan
    
    # take care of border effect --> pad by nan nan 
    imCoefs = np.pad(coefs, ((0, 0), (L, L) ,(L, L)), constant_values=((np.nan, np.nan), (np.nan, np.nan), (np.nan, np.nan)))
    imLCoefs = np.pad(lcoefs, ((0, 0), (L, L) ,(L, L)), constant_values=((np.nan, np.nan), (np.nan, np.nan), (np.nan, np.nan)))
    
    imLGcoefs = np.pad(LGcoefs, ((0, 0), (L, L) ,(L, L)), constant_values=((np.nan, np.nan), (np.nan, np.nan), (np.nan, np.nan)))
    imLGlcoefs = np.pad(LGlcoefs, ((0, 0), (L, L) ,(L, L)), constant_values=((np.nan, np.nan), (np.nan, np.nan), (np.nan, np.nan)))
    
    # size parameters    
    Nscale, N1, N2 = imCoefs.shape
     
    # choose the windows (the weigths) for average  
    y, x = np.ogrid[-L:L+1, -L:L+1]     
    d = np.sqrt( x**2 + y**2 ) /L
    if np.char.equal(window,'flatsquare'):
        W = np.ones((2*L+1,2*L+1))
    elif np.char.equal(window,'bisquare'):  
        W = bisquarekernel(d)
    elif np.char.equal(window,'flatcircle'):
        W=np.copy(d)
        W[d<=1]=1
        W[d>1]=0    
    else:
        W = np.ones((2*L+1,2*L+1))
        print('Not yet implemented --> take flat window instead\n')
    Wgrid = np.zeros((2*L+1,2*L+1))
    Wgrid[d<gridsize/L]=1
    Nk = 2*L+1
    Nfft1 = N1+Nk-1
    Nfft2 = N2+Nk-1
    if len(fftplan)==0:
        fft_object,  ffti_object = prepare_plan2d(Nfft1, Nfft2, N_threads)
    else:
        fft_object, ffti_object = fftplan
   
    TFW=np.copy(fft_object(np.pad(Wgrid, ((0, Nfft1-Nk) ,(0, Nfft2-Nk)), constant_values=((0, 0),(0,0)))))
    Coefs1 = np.copy(imCoefs[0,:,:])
    iNan=np.isnan(Coefs1)
    imtmp=np.ones((N1,N2))
    imtmp[iNan]=0
    imtmp=np.pad(imtmp, ((0, Nk-1) ,(0, Nk-1)  ), constant_values=((0, 0),(0,0)))
    CountValid=convFFTW(imtmp, TFW, fft_object,ffti_object)[L:Nfft1-L,L:Nfft2-L]       
    Index0 = CountValid < 0.5
    
    # fft of the window
    TFW=np.copy(fft_object(np.pad(W, ((0, Nfft1-Nk) ,(0, Nfft2-Nk)), constant_values=((0, 0),(0,0)))))
   
    
    # results allocations
    Mean_Std_loc = np.zeros((2, Nscale, N1, N2))*np.nan
    Mom12_loc = np.zeros((2, Nscale, N1, N2))*np.nan
    Cum12_loc = np.zeros((2, Nscale, N1, N2))*np.nan
    Cum1leader_loc = np.zeros((Nscale, N1, N2))*np.nan

    Mom4_loc = np.zeros((Nscale, N1, N2))*np.nan
    Flatness = np.zeros((Nscale, N1, N2))*np.nan

     
    # loop on scales
    for i in range(Nscale):
        print(i,end=' ',flush=True)
        Coefs1 = np.copy(imCoefs[i,:,:])
        iNan=np.isnan(Coefs1)
        imtmp=np.ones((N1,N2))
        imtmp[iNan]=0
        imtmp=np.pad(imtmp, ((0, Nk-1) ,(0, Nk-1)  ), constant_values=((0, 0),(0,0)))
        CountValid=convFFTW(imtmp, TFW, fft_object,ffti_object)[L:Nfft1-L,L:Nfft2-L]       
        CountValid[CountValid < 0.1] = np.nan # must be integer >0
                    
        Coefs1[iNan]=0
        # compute moments and flatness
        imtmp=np.pad(Coefs1, ((0, Nk-1) ,(0, Nk-1)  ), constant_values=((0, 0),(0,0)))      
        lasum=convFFTW(imtmp, TFW, fft_object,ffti_object)[L:Nfft1-L,L:Nfft2-L]
        lasum[Index0]=np.nan
        Mean_Std_loc[0,i,:,:]=lasum/CountValid
        lasum=convFFTW(np.abs(imtmp), TFW, fft_object,ffti_object)[L:Nfft1-L,L:Nfft2-L]
        lasum[Index0]=np.nan
        Mom12_loc[0,i,:,:]=lasum/CountValid
        lasum=convFFTW(imtmp**2, TFW, fft_object,ffti_object)[L:Nfft1-L,L:Nfft2-L]
        lasum[Index0]=np.nan
        Mom12_loc[1,i,:,:]=lasum/CountValid
        Mean_Std_loc [1,i,:,:]= Mom12_loc[1,i,:,:] - Mean_Std_loc [0,i,:,:]**2
        lasum=convFFTW(imtmp**4, TFW, fft_object,ffti_object)[L:Nfft1-L,L:Nfft2-L]
        lasum[Index0]=np.nan
        Mom4_loc[i,:,:]=lasum/CountValid
        
        Flatness[i,:,:]= Mom4_loc[i,:,:]/(3*Mom12_loc[1,i,:,:]**2)
        
        # normalisation
        LCoefs1 = np.copy(imLCoefs[i,:,:])
        iNan=np.isnan(LCoefs1)
        imtmp=np.ones((N1,N2))
        imtmp[iNan]=0
        imtmp=np.pad(imtmp, ((0, Nk-1) ,(0, Nk-1)  ), constant_values=((0, 0),(0,0)))
        CountValid=convFFTW(imtmp, TFW, fft_object,ffti_object)[L:Nfft1-L,L:Nfft2-L]       
        CountValid[CountValid < 0.1] = np.nan # must be integer >0
        #
        ####ITT compute C1 from log coeff
        #logCoefs = np.copy(Coefs1)
        #logCoefs = np.log(np.abs(logCoefs))
        #logCoefs[np.isinf(logCoefs)] = np.nan
        logCoefs = np.copy(imLGcoefs[i,:,:])
        iNanLC=np.isnan(logCoefs)
        logCoefs[iNanLC] =0
        imtmp=np.pad(logCoefs, ((0, Nk-1) ,(0, Nk-1)  ), constant_values=((0, 0),(0,0)))      
        lasum=convFFTW(imtmp, TFW, fft_object,ffti_object)[L:Nfft1-L,L:Nfft2-L]
        lasum[Index0]=np.nan
        Cum12_loc[0,i,:,:]=lasum/CountValid       
        
        #
        #logLCoefs = np.copy(LCoefs1)
        #logLCoefs = np.log(np.abs(logLCoefs))
        #logLCoefs[np.isinf(logLCoefs)] = np.nan
        logLCoefs = np.copy(imLGlcoefs[i,:,:])
        logLCoefs[np.isnan(logLCoefs)] = 0
        imtmp=np.pad(logLCoefs, ((0, Nk-1) ,(0, Nk-1)  ), constant_values=((0, 0),(0,0)))      
        lasum=convFFTW(imtmp, TFW, fft_object,ffti_object)[L:Nfft1-L,L:Nfft2-L]
        lasum[Index0]=np.nan
        Cum1leader_loc[i,:,:]=lasum/CountValid
        #Cum12_loc[0,i,:,:]=lasum/CountValid  
        lasum=convFFTW(imtmp**2, TFW, fft_object,ffti_object)[L:Nfft1-L,L:Nfft2-L]
        lasum[Index0]=np.nan
        Cum12_loc[1,i,:,:]=lasum/CountValid-Cum1leader_loc[i,:,:]**2
        #Cum12_loc[1,i,:,:]=lasum/CountValid-Cum12_loc[0,i,:,:]**2
        
    print('.')
    
    Mean_Std_loc = Mean_Std_loc[:,:,L:-L,L:-L]
    Mom12_loc = Mom12_loc[:,:,L:-L,L:-L]
    Cum12_loc = Cum12_loc[:,:,L:-L,L:-L]
    Flatness = Flatness[:,L:-L,L:-L]
    
    # swap axes
    Mean_Std_loc = Mean_Std_loc.transpose(0,2,3,1)
    Mom12_loc = Mom12_loc.transpose(0,2,3,1)
    Cum12_loc = Cum12_loc.transpose(0,2,3,1)
    Flatness = Flatness.transpose(1,2,0)
    return Mean_Std_loc, Mom12_loc, Flatness ,Cum12_loc
#%%
def LocalCorrAnalysisRD(Coefs1sig,Coefs2sig,L, window='flatcircle',fftplan=[], gridsize=1):
    '''
        Compute localized correlation coeficients between two sets of values.
        
        rho = LocalCorrAnalysisRD(Coefs1,Coefs2,L, window)
    
    
        Inputs :
            
            coefs1  : first set of ceoficients 
            
            coefs2  : second set of ceoficients 
           
            L : size of the average (integer stricty positif)
           
            window : weighting function to use. Default : window='flat'.
                     can be window='bisquare'
           
       Outputs :   

            rho : localized correlation coeficients
           
    '''
    
    assert(Coefs1sig.shape == Coefs2sig.shape)
    # transpose axis
    Coefs1sig = Coefs1sig.transpose(2, 0, 1)
    Coefs2sig = Coefs2sig.transpose(2, 0, 1)
    
    # take care of border effect --> pad by nan nan 
    imCoefs1 = np.pad(Coefs1sig, ((0, 0), (L, L) ,(L, L)), constant_values=((np.nan, np.nan), (np.nan, np.nan), (np.nan, np.nan)))
    imCoefs2 = np.pad(Coefs2sig, ((0, 0), (L, L) ,(L, L)), constant_values=((np.nan, np.nan), (np.nan, np.nan), (np.nan, np.nan)))
    
    # size parameters       
    Nscale, N1, N2 = imCoefs1.shape
     
    # choose the windows (the weigths) for average  
    y, x = np.ogrid[-L:L+1, -L:L+1]     
    d = np.sqrt( x**2 + y**2 ) /L
    
    if np.char.equal(window,'flat'):
        W = np.ones((2*L+1,2*L+1))
        #y, x = np.ogrid[-L:L+1, -L:L+1]     
        #d = np.sqrt( x**2 + y**2 ) /L
    elif np.char.equal(window,'bisquare'):
        #y, x = np.ogrid[-L:L+1, -L:L+1]     
        #d = np.sqrt( x**2 + y**2 ) /L
        W = bisquarekernel(d)
    elif np.char.equal(window,'flatcircle'):
        W=np.copy(d)
        W[d<=1]=1
        W[d>1]=0    
        ###ITT
    else:
        #y, x = np.ogrid[-L:L+1, -L:L+1]     
        #d = np.sqrt( x**2 + y**2 ) /L
        W = np.ones((2*L+1,2*L+1))
        print('Not yet implemented --> take flat window instead\n')
     
    # for grid size
    Wgrid = np.zeros((2*L+1,2*L+1))
    Wgrid[d<gridsize/L]=1
    
    # fftw plan
    Nk = 2*L+1
    Nfft1 = N1+Nk-1
    Nfft2 = N2+Nk-1
    if len(fftplan)==0:
        fft_object,  ffti_object = prepare_plan2d(Nfft1, Nfft2, N_threads)
    else:
        fft_object, ffti_object = fftplan

    TFW=np.copy(fft_object(np.pad(Wgrid, ((0, Nfft1-Nk) ,(0, Nfft2-Nk)), constant_values=((0, 0),(0,0)))))
    Coefs1 = np.copy(imCoefs1[0,:,:])
    iNan=np.isnan(Coefs1)
    imtmp=np.ones((N1,N2))
    imtmp[iNan]=0
    imtmp=np.pad(imtmp, ((0, Nk-1) ,(0, Nk-1)  ), constant_values=((0, 0),(0,0)))
    CountValid=convFFTW(imtmp, TFW, fft_object,ffti_object)[L:Nfft1-L,L:Nfft2-L]       
    Coefs2 = np.copy(imCoefs2[0,:,:])
    iNan=np.isnan(Coefs1)
    imtmp=np.ones((N1,N2))
    imtmp[iNan]=0
    imtmp=np.pad(imtmp, ((0, Nk-1) ,(0, Nk-1)  ), constant_values=((0, 0),(0,0)))
    CountValid2=convFFTW(imtmp, TFW, fft_object,ffti_object)[L:Nfft1-L,L:Nfft2-L]       
    Index0=(CountValid < 0.5) & (CountValid2 < 0.5)
    
   
    TFW=np.copy(fft_object(np.pad(W, ((0, Nfft1-Nk) ,(0, Nfft2-Nk)), constant_values=((0, 0),(0,0)))))  
    rho = np.zeros((Nscale, N1, N2))*np.nan
    
    for i in range(Nscale):
        print(i,end=' ',flush=True)
        Coefs1 = np.copy(imCoefs1[i,:,:])
        Coefs2 = np.copy(imCoefs2[i,:,:])
        
        iNan1 = np.isnan(Coefs1)
        iNan2 = np.isnan(Coefs2)
        
        
        # Normalisation
        imtmp=np.ones((N1,N2))
        imtmp[iNan1]=0
        imtmp=np.pad(imtmp, ((0, Nk-1) ,(0, Nk-1)  ), constant_values=((0, 0),(0,0)))
        CountValid1=convFFTW(imtmp, TFW, fft_object,ffti_object)[L:Nfft1-L,L:Nfft2-L]       
        CountValid1[CountValid1 < 1e-5] = np.nan # must be integer >0
        imtmp=np.ones((N1,N2))
        imtmp[iNan2]=0
        imtmp=np.pad(imtmp, ((0, Nk-1) ,(0, Nk-1)  ), constant_values=((0, 0),(0,0)))
        CountValid2=convFFTW(imtmp, TFW, fft_object,ffti_object)[L:Nfft1-L,L:Nfft2-L]       
        CountValid2[CountValid2 < 1e-5] = np.nan # must be integer >0
        imtmp=np.ones((N1,N2))
        imtmp[iNan1]=0
        imtmp[iNan2]=0
        imtmp=np.pad(imtmp, ((0, Nk-1) ,(0, Nk-1)  ), constant_values=((0, 0),(0,0)))
        CountValid12=convFFTW(imtmp, TFW, fft_object,ffti_object)[L:Nfft1-L,L:Nfft2-L]       
        CountValid12[CountValid12 < 1e-5] = np.nan # must be integer >0
        
        Coefs1[iNan1]=0
        Coefs2[iNan2]=0
        imtmp=np.pad(Coefs1, ((0, Nk-1) ,(0, Nk-1)  ), constant_values=((0, 0),(0,0)))      
        lasum=convFFTW(imtmp, TFW, fft_object,ffti_object)[L:Nfft1-L,L:Nfft2-L]
        lasum[Index0] = np.nan
        moy1=lasum/CountValid1
        
        lasum=convFFTW(imtmp**2, TFW, fft_object,ffti_object)[L:Nfft1-L,L:Nfft2-L]
        lasum[Index0] = np.nan
        M2_1=lasum/CountValid1
        var1 = M2_1 - moy1**2    
        var1[var1< 1e-5]=np.nan  

        imtmp=np.pad(Coefs2, ((0, Nk-1) ,(0, Nk-1)  ), constant_values=((0, 0),(0,0)))      
        lasum=convFFTW(imtmp, TFW, fft_object,ffti_object)[L:Nfft1-L,L:Nfft2-L]
        lasum[Index0] = np.nan
        moy2=lasum/CountValid2
        lasum=convFFTW(imtmp**2, TFW, fft_object,ffti_object)[L:Nfft1-L,L:Nfft2-L]
        M2_2=lasum/CountValid2
        var2 = M2_2 - moy2**2   
        var2[var2< 1e-5]=np.nan  
        imtmp=np.pad(Coefs1*Coefs2, ((0, Nk-1) ,(0, Nk-1)  ), constant_values=((0, 0),(0,0)))      
        lasum=convFFTW(imtmp, TFW, fft_object,ffti_object)[L:Nfft1-L,L:Nfft2-L]
        lasum[Index0] = np.nan
        moy_cross=lasum/CountValid12
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=RuntimeWarning)
            rho[i,:,:] = (moy_cross - moy1*moy2)/np.sqrt(var1*var2)
           
    print('.')
    rho = rho[:,L:-L,L:-L]
    # swap axes
    rho = rho.transpose(1,2,0)
    return rho
