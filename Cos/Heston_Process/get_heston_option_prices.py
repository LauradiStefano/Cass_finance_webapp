# -*- coding: utf-8 -*-
"""
Created on Mon Apr 29 16:53:24 2019

@author: Diego
"""

"""
    Compute european option prices assuming heston model with cos method
"""
import math

import numpy as np

from get_heston_bounds import compute_heston_bounds
from get_heston_charfn import heston_charfn


def get_cos_prices(mu, S0, K, r, q, Tt, v0, chi, lam, rho, v_hat, call_put):
    
    call_put = int(call_put)
    price = []
    if Tt==0:
        price=(max(call_put*(S0-K),0))
    
    else:
        
        
        mu=0
        omega=np.log(heston_charfn(-1j, 1, v0, chi, lam, rho, v_hat, mu))
              
        murn=r-q-np.real(omega)
        
        a,b=compute_heston_bounds(murn, Tt, v0, chi, lam, rho, v_hat)

        if call_put == 1 :  # call
    
            V = ((2/(b-a))*(chiFO(0,b,N,a,b)-psiFO(0,b,N,a,b)))
    
        elif call_put == -1 : # put
        
            V = -(2/(b-a))*(chiFO(a,0,N,a,b)-psiFO(a,0,N,a,b))
       
    
    CharFn = heston_charfn(np.arange(0,N,1)*math.pi/(b-a), Tt, v0, chi, lam, rho, v_hat, murn)
    Cfv=np.matrix(CharFn*V)#corretto
    
   
    for j in range (0,len(K)):
       
        k=np.log(S0/K[j])-a #k=np.log(S0)-a                           
        Exp_term=np.matrix(np.exp(1j*math.pi*(k)*np.arange(0,N,1)/(b-a)));#corretto
        
        real_term=np.real(np.dot(Exp_term,Cfv.getT())-0.5*Exp_term[0,0]*Cfv[0,0] )#corretto il secondo termine della sottrazione
        
        price.append(float( K[j]*math.exp(-r*Tt)*real_term))    #transpose CFV

    return price


def chiFO(c, d, N, a, b):
    rangeN = np.arange(0, N, 1)

    rangeN_c = rangeN * math.pi * (c - a) / (b - a)
    rangeN_d = rangeN * math.pi * (d - a) / (b - a)

    chi = (1 / (1 + (rangeN * math.pi / (b - a)) ** 2)) * (
            np.cos(rangeN_d) * math.exp(d) - np.cos(rangeN_c) * math.exp(c) + (rangeN * math.pi / (b - a)) * np.sin(
        rangeN_d) * math.exp(d) - (rangeN * math.pi / (b - a)) * np.sin(rangeN_c) * math.exp(c));

    return chi


def psiFO(c, d, N, a, b):
    rangeN = np.arange(0, N, 1)
    rangeN_c = rangeN * math.pi * (c - a) / (b - a)
    rangeN_d = rangeN * math.pi * (d - a) / (b - a)
    psi = []
    psi.append(d - c)
    for i in range(1, N):
        psi.append((math.sin(rangeN_d[i]) - math.sin(rangeN_c[i])) * (b - a) / (rangeN[i] * math.pi))

    return psi
