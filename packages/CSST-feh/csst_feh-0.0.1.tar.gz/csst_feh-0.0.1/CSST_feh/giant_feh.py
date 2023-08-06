def giant_feh(u,g,i,error):
    '''
    This program is designed specially to estimate the metallicity of the giant stars 
from the CSST filter systems using metallicity-depedent stellar loci of (u-g) versus
(g-i), the metallicity can be derived with the maximum likelihood approach in the meanwhile.

    Args:
        u: array-like, shape (n, )
           CSST u band
        
        g: array-like, shape (n, )
           CSST g band
           
        i: array-like, shape (n, )
           CSST i band
           
        error: float
           color error. An assumption that (u-g) and (g-i) are independent Gaussian variables
           is made.
           
    The output are two files named giant_feh_predicted.csv and giant_feh_error.csv, 
the former stores the photometric metallicity and the latter stores the random error 
of photometric metallicity.
    '''

    import numpy as np
    import pandas as pd
    import glob
    import os

    xdata=g-i
    ydata=u-g
    #First step: refuse data beyond the applicability range
    m=[]
    n=[]
    a,b=0.53,1.24   #a,b denote lower and upper limit of given (g-i), respectively
    ind=np.where((xdata>a)&(xdata<b))
    xdata=xdata[ind]
    ydata=ydata[ind]  
    c=-4*np.ones(len(xdata))  # c is [Fe/H]=-4 contour       
    a00=1.9400406           # ten polynimial coefficients
    a01=0.11089336
    a02=0.00253652
    a03=-0.00101453
    a10=-2.96171442
    a11=0.24486613
    a12=0.04771319
    a20=4.24879783
    a21=0.04468856
    a30=-1.2559049
    need=a00+a01*c+a02*c**2+a03*c**3+a10*xdata+a11*xdata*c+a12*xdata*c**2\
             +a20*xdata**2+a21*xdata**2*c+a30*xdata**3 
    ind=np.where(ydata>=need)     # choose data that above [Fe/H]=-4 contour
    xdata=xdata[ind]
    ydata=ydata[ind]  
    for i in np.arange(0,len(xdata)):
        x=xdata[i]
        y=ydata[i]
        m.append(x)   # m is a list to store (g-i) data
        n.append(y)   # n is a list to store (u-g) data
    np.savetxt("g-i_use.csv",m)
    np.savetxt("u-g_use.csv",n)  
             
    #Second step: predict [Fe/H] with derived polynomial
    m=[]
    n=[]
    xdata=np.loadtxt("g-i_use.csv",delimiter=',') 
    ydata=np.loadtxt("u-g_use.csv",delimiter=',')
    for i in np.arange(0,len(xdata)):
        x1=xdata[i]                        # x1 denotes (g-i) 
        y1=ydata[i]                        # y1 denotes (u-g) 
        f1=np.linspace(-4,0.5,91)           # given [Fe/H]
        x10=x1+error*np.random.randn(91)       #g,i are both Gaussian variables
        y10=y1+error*np.random.randn(91)       #u,g are both Gaussian variables
        need=a00+a01*f1+a02*f1**2+a03*f1**3+a10*x10+a11*x10*f1+a12*x10*f1**2\
             +a20*x10**2+a21*x10**2*f1+a30*x10**3    
        sigma1=0.013062754676023238-0.002093386575314095 *x1   #given (g-i) random error
        sigma2=0.02765716484703738-0.0019499350415479824 *y1   #given (u-g) random error                  
        likelihood=((2*np.pi)**0.5*sigma2)**(-1)*(np.e)**(-((y10-need)**2)/(2*sigma2**2))
        f=np.argmax(likelihood)
        m.append(f1[f])
        sigma_feh=((sigma2**2-sigma1**2*(a10+a11*f1[f]+a12*(f1[f])**2+\
                    2*a20*x1+2*a21*x1*f1[f]+3*a30*x1**2)**2)/(a01+2*a02*f1[f]\
                   +3*a03*(f1[f])**2+a11*x1+2*a12*x1*f1[f]+a21*x1**2))**0.5
        np.seterr(divide='ignore',invalid='ignore')
        n.append(sigma_feh)
    np.savetxt("giant_feh_predicted.csv",m)
    np.savetxt("giant_feh_error.csv",n)

    #Last step: delete intermediate files
    os.remove("u-g_use.csv")
    os.remove("g-i_use.csv")