#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 24 23:22:21 2019

@author: DRUOT Thierry : original Scilab implementation
         ROCHES Pascal : portage to Python
"""

from numpy import max, ceil, log10, floor, float64, arange,\
                  array, size, vander, zeros


#===========================================================================================================
def to_user_format(value):
    if isinstance(value, tuple):
        lst = list(value)
        for i in arange(len(lst)):
            lst[i] = to_user_format(lst[i])
        value = tuple(lst)
        return value
    if isinstance(value, (float, float64)):
        if value == 0. or value == -0.:
            return format(value, "".join((".4f")))
        else:
            V = abs(value)
            if abs(value) > 1:
                nb_dec = int(max((0,5-ceil(log10(V+1e-4)))))
            else:
                nb_dec = int(3 - floor(log10(V)))
            return format(value, "".join((".",str(nb_dec),"f")))
    else:
        return value

#===========================================================================================================
def trinome(A,Y):
    """
    calculates trinome coefficients from 3 given points
    A = [X2, X, 1]
    """
    X = array([0.,0.,0.])
    X2 = array([0.,0.,0.])

    for i in range(0,3):
        X[i] = A[i][1]
        X2[i] = A[i][0]

    det = X2[0]*(X[1]-X[2])-X2[1]*(X[0]-X[2])+X2[2]*(X[0]-X[1])

    adet = Y[0]*(X[1]-X[2])-Y[1]*(X[0]-X[2])+Y[2]*(X[0]-X[1])

    bdet = X2[0]*(Y[1]-Y[2])-X2[1]*(Y[0]-Y[2])+X2[2]*(Y[0]-Y[1])

    cdet =  X2[0]*(X[1]*Y[2]-X[2]*Y[1])-X2[1]*(X[0]*Y[2]-X[2]*Y[0]) \
          + X2[2]*(X[0]*Y[1]-X[1]*Y[0])

    if det!=0:
        C = [adet/det, bdet/det, cdet/det]
    elif X[0]!=X[2]:
        C = (0, Y[0]-Y[2], Y[2]*X[0]-Y[0]*X[2]/(X[0]-X[2]))
    else:
        C = (0, 0, (Y[0]+Y[1]+Y[2])/3)

    return C


#===========================================================================================================
def lin_interp_1d(x,X,Y):
    """
    linear interpolation without any control
        x current position
        X x position array of the knowing points
        Y y position array of the knowing points
    """

    n = size(X)
    for j in range(1,n):
        if x<X[j] :
            y=Y[j-1]+(Y[j]-Y[j-1])*(x-X[j-1])/(X[j]-X[j-1])
            return y
    y = Y[n-2]+(Y[n-1]-Y[n-2])*(x-X[n-2])/(X[n-1]-X[n-2])
    return y


#===========================================================================================================
def maximize_1d(xini,dx,fct):
    """
    Optimize 1 single variable, no constraint
    xini : initial value of the variable
    dx : fixed search step
    fct : function with the signature : ['fct',p,a1,a2,a3,...,ap-1,ap+1,...,an]
                                        [ 0   ,1, 2, 3, 4,...,  ? ,  ? ,..., n]
    p : x position in signature
                                        fct(a1,a2,a3,...,ap-1,x,ap+1,...,an)
    """

    #===========================================================================================================
    def fct_max_1d(x,*fct):
        namefct = fct[0][0]
        n = len(fct[0])
        if n!=1:
            arg = []
            p = fct[0][1]
            if p==1:
                arg.append(x)
                for i in range (2,n):
                    arg.append(fct[0][i])
            else:
                for i in range (2,p+1):
                    arg.append(fct[0][i])
                arg.append(x)
                for i in range (p+1,n):
                    arg.append(fct[0][i])
            y = namefct(*arg)
            return y
        else:
            y = namefct(x)
            return y
    #-----------------------------------------------------------------------------------------------------------

    X = zeros(3)
    Y = zeros(3)

    X[0] = xini
    Y[0] = fct_max_1d(X[0],fct)

    X[1] = X[0]+dx
    Y[1] = fct_max_1d(X[1],fct)

    if Y[0]>Y[1]:
        dx = -dx
        X[0],X[1] = X[1],X[0]

    X[2] = X[1]+dx
    Y[2] = fct_max_1d(X[2],fct)

    while Y[1]<Y[2]:
        X[0] = X[1]
        X[1] = X[2]
        X[2] = X[2]+dx
        Y[0] = Y[1]
        Y[1] = Y[2]
        Y[2] = fct_max_1d(X[2],fct)

    A=vander(X,3)     #[X**2,X,numpy.ones(3)]

    C = zeros((3))
    C = trinome(A,Y)

    xres = -C[1]/(2*C[0])
    yres = fct_max_1d(xres,fct)

    rc = 1

    return (xres,yres,rc)


#===========================================================================================================
def maximize_1d_v2(xini,dx,fct):
    """
    Optimize 1 single variable, no constraint
    xini : initial value of the variable
    dx : fixed search step
    fct : function with the signature : ['fct',p,a1,a2,a3,...,ap-1,ap+1,...,an]
                                        [ 0   ,1, 2, 3, 4,...,  ? ,  ? ,..., n]
    p : x position in signature
                                        fct(a1,a2,a3,...,ap-1,x,ap+1,...,an)
    """

    #===========================================================================================================
    def fct_max_1d(x,*fct):
        namefct = fct[0][0]
        n = len(fct[0])
        if n!=1:
            arg = []
            p = fct[0][1]
            if p==1:
                arg.append(x)
                for i in range (2,n):
                    arg.append(fct[0][i])
            else:
                for i in range (2,p+1):
                    arg.append(fct[0][i])
                arg.append(x)
                for i in range (p+1,n):
                    arg.append(fct[0][i])
            y = namefct(*arg)
            return y
        else:
            y = namefct(x)
            return y
    #-----------------------------------------------------------------------------------------------------------

    X = zeros(3)
    Y = zeros(3)

    X[0] = xini
    Y[0] = fct_max_1d(X[0],fct)

    X[1] = X[0]+dx
    Y[1] = fct_max_1d(X[1],fct)

    if Y[0]>Y[1]:
        dx = -dx
        X[0],X[1] = X[1],X[0]

    X[2] = X[1]+dx
    Y[2] = fct_max_1d(X[2],fct)

    while Y[1]<Y[2]:
        X[0] = X[1]
        X[1] = X[2]
        X[2] = X[2]+dx
        Y[0] = Y[1]
        Y[1] = Y[2]
        Y[2] = fct_max_1d(X[2],fct)

    A=vander(X,3)     #[X**2,X,numpy.ones(3)]

    C = zeros((3))
    C = trinome(A,Y)

    xres = -C[1]/(2*C[0])
    yres = fct_max_1d(xres,fct)

    rc = 1

    return xres,yres,rc
