def dwarf_feh(u,g,i,error):
    '''
    This program is designed specially to estimate the metallicity of the dwarf stars 
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
    
    The output are two files named dwarf_feh_predicted.csv and dwarf_feh_error.csv, 
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
    a,b=0.66,1.24   #a,b denote the lower and upper limit of given (g-i), respectively
    ind=np.where((xdata>a)&(xdata<b))
    xdata=xdata[ind]
    ydata=ydata[ind]  
    for i in np.arange(0,len(xdata)):
        x=xdata[i]
        y=ydata[i]
        m.append(x)   # m is a list to store (g-i) data
        n.append(y)   # n is a list to store (u-g) data
    np.savetxt("dwarf_g-i.csv",m)
    np.savetxt("dwarf_u-g.csv",n)  
        
    xdata,ydata=g-i,u-g      
    m=[]
    n=[]
    a,b=0.39,0.66   
    ind=np.where((xdata>a)&(xdata<b))
    xdata=xdata[ind]
    ydata=ydata[ind]
    c=-1.5*np.ones(len(xdata))  # c is [Fe/H]=-1.5 contour
    a00= 1.04509737              # ten polynmial coefficients
    a01= 0.13847731
    a02= 0.02231436
    a03=-0.00305052
    a10=-0.84510066
    a11= 0.18719969
    a12=-0.00678258 
    a20= 2.57309411
    a21=-0.0508573
    a30=-0.92393672
    need=a00+a01*c+a02*c**2+a03*c**3+a10*xdata+a11*xdata*c+a12*xdata*c**2\
             +a20*xdata**2+a21*xdata**2*c+a30*xdata**3       # choose data above [Fe/H]= -1.5 contour when 0.39<(g-i)<0.66
    ind=np.where(ydata>=need)   
    xdata=xdata[ind]
    ydata=ydata[ind] 
    for i in np.arange(0,len(xdata)):
        x=xdata[i]
        y=ydata[i]
        m.append(x)   
        n.append(y)   
    np.savetxt("dwarf1_g-i.csv",m)
    np.savetxt("dwarf1_u-g.csv",n)

    xdata,ydata=g-i,u-g
    m=[]
    n=[]
    a,b=0.26,0.39   
    ind=np.where((xdata>a)&(xdata<b))
    xdata=xdata[ind]
    ydata=ydata[ind]
    c=-1*np.ones(len(xdata))  # c is [Fe/H]=-1 contour  
    need=a00+a01*c+a02*c**2+a03*c**3+a10*xdata+a11*xdata*c+a12*xdata*c**2\
             +a20*xdata**2+a21*xdata**2*c+a30*xdata**3 
    ind=np.where(ydata>=need)     # choose data that above [Fe/H]=-1 contour when 0.26<(g-i)<0.39
    xdata=xdata[ind]
    ydata=ydata[ind]  
    for i in np.arange(0,len(xdata)):
        x=xdata[i]
        y=ydata[i]
        m.append(x)   
        n.append(y)   
    np.savetxt("dwarf2_g-i.csv",m)
    np.savetxt("dwarf2_u-g.csv",n)

    csv_list=glob.glob('*g-i.csv')
    for i in csv_list:
        fr=open(i,'r',encoding='utf-8').read()
        with open('g-i_use.csv','a',encoding='utf-8') as f:
            f.write(fr)         
    csv_list=glob.glob('*u-g.csv')
    for i in csv_list:
        fr=open(i,'r',encoding='utf-8').read()
        with open('u-g_use.csv','a',encoding='utf-8') as f:
            f.write(fr)
            
    #Second step: predict [Fe/H] with derived polynomial
    m=[]
    n=[]
    xdata=np.loadtxt("g-i_use.csv",delimiter=',') 
    ydata=np.loadtxt("u-g_use.csv",delimiter=',')

    for i in np.arange(0,len(xdata)):
        x1=xdata[i]                        # x1 denotes (g-i) 
        y1=ydata[i]                        # y1 denotes (u-g) 
        if (x1>0.66):
            f1=np.linspace(-4,1,101)                # given [Fe/H]
            x10=x1+error*np.random.randn(101)       #g,i are both Gaussian variables
            y10=y1+error*np.random.randn(101)       #u,g are both Gaussian variables
            need=a00+a01*f1+a02*f1**2+a03*f1**3+a10*x10+a11*x10*f1+a12*x10*f1**2\
             +a20*x10**2+a21*x10**2*f1+a30*x10**3
            sigma1=0.013062754676023238-0.002093386575314095* x1   #given (g-i) random error
            sigma2=0.02765716484703738-0.0019499350415479824 *y1   #given (u-g) random error                       
            likelihood=((2*np.pi)**0.5*sigma2)**(-1)*(np.e)**(-((y10-need)**2)/(2*sigma2**2))
            f=np.argmax(likelihood)
            m.append(f1[f])                         # m is a list to store [Fe/H]
            sigma_feh=((sigma2**2-sigma1**2*(a10+a11*f1[f]+a12*(f1[f])**2+\
                    2*a20*x1+2*a21*x1*f1[f]+3*a30*x1**2)**2)/(a01+2*a02*f1[f]\
                   +3*a03*(f1[f])**2+a11*x1+2*a12*x1*f1[f]+a21*x1**2))**0.5
            np.seterr(divide='ignore',invalid='ignore')
            n.append(sigma_feh)                # n is a list to store the tandom error of [Fe/H]
        elif (0.39<=x1<=0.66):
            f1=np.linspace(-1.5,1,51)                    
            x10=x1+error*np.random.randn(51)       
            y10=y1+error*np.random.randn(51)       
            need=a00+a01*f1+a02*f1**2+a03*f1**3+a10*x10+a11*x10*f1+a12*x10*f1**2\
                +a20*x10**2+a21*x10**2*f1+a30*x10**3 
            sigma1=0.013062754676023238-0.002093386575314095 *x1   
            sigma2=0.02765716484703738-0.0019499350415479824 *y1   
            likelihood=((2*np.pi)**0.5*sigma2)**(-1)*(np.e)**(-((y10-need)**2)/(2*sigma2**2))
            f=np.argmax(likelihood)
            m.append(f1[f]) 
            sigma_feh=((sigma2**2-sigma1**2*(a10+a11*f1[f]+a12*(f1[f])**2+\
                    2*a20*x1+2*a21*x1*f1[f]+3*a30*x1**2)**2)/(a01+2*a02*f1[f]\
                    +3*a03*(f1[f])**2+a11*x1+2*a12*x1*f1[f]+a21*x1**2))**0.5
            np.seterr(divide='ignore',invalid='ignore')
            n.append(sigma_feh)
        else:
            f1=np.linspace(-1,1,41)                    
            x10=x1+error*np.random.randn(41)       
            y10=y1+error*np.random.randn(41)       
            need=a00+a01*f1+a02*f1**2+a03*f1**3+a10*x10+a11*x10*f1+a12*x10*f1**2\
             +a20*x10**2+a21*x10**2*f1+a30*x10**3 
            sigma1=0.013062754676023238-0.002093386575314095 *x1   
            sigma2=0.02765716484703738-0.0019499350415479824 *y1   
            likelihood=((2*np.pi)**0.5*sigma2)**(-1)*(np.e)**(-((y10-need)**2)/(2*sigma2**2))
            f=np.argmax(likelihood)
            m.append(f1[f])
            sigma_feh=((sigma2**2-sigma1**2*(a10+a11*f1[f]+a12*(f1[f])**2+\
                    2*a20*x1+2*a21*x1*f1[f]+3*a30*x1**2)**2)/(a01+2*a02*f1[f]\
                     +3*a03*(f1[f])**2+a11*x1+2*a12*x1*f1[f]+a21*x1**2))**0.5
            np.seterr(divide='ignore',invalid='ignore')
            n.append(sigma_feh)
    np.savetxt("dwarf_feh_predicted.csv",m)
    np.savetxt("dwarf_feh_error.csv",n)
    
    #Last step: delete intermediate files
    os.remove("dwarf_u-g.csv")
    os.remove("dwarf_g-i.csv")
    os.remove("dwarf1_u-g.csv")
    os.remove("dwarf1_g-i.csv")
    os.remove("dwarf2_u-g.csv")
    os.remove("dwarf2_g-i.csv")
    os.remove("u-g_use.csv")
    os.remove("g-i_use.csv")