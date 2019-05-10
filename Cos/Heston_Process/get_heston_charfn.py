# -*- coding: utf-8 -*-
"""
Created on Mon Apr 29 13:51:41 2019

@author: Diego
"""

"""
  
   Tt : time to maturity
   v0 : varianza iniziale
   chi : volatility of volatility
   lam : speed of mean reverse
   rho : correlation between volatility and underlying asset wierner processes
   u_hat : volatilità media
"""   


import numpy as np
def heston_charfn(N, Tt, v0, chi, lam, rho, v_hat, mu):
    
    rangeN=np.arange(0,N,1)
    D = np.sqrt((lam-1j*rho*chi*rangeN)**2 + (rangeN**2-1j*rangeN)*chi**2)
    G = (lam-1j*rho*chi*rangeN-D)/(lam-1j*rho*chi*rangeN+D)
    

    
    #First term of product
    hest_1= 1j*rangeN*mu*Tt 
    hest_2 = (v0/chi**2)*((1-np.exp(-D*Tt))/(1-G*np.exp(-D*Tt)))
    hest_3 = lam-1j*rho*chi*rangeN-D
    
    heston_first_term =np.exp(hest_1+hest_2*hest_3)
    
    #Second term of product
    
    hest_4 = Tt*(lam-1j*rho*chi*rangeN-D)
    hest_5 = 2*np.log((1-G*np.exp(-D*Tt))/(1-G))
    
    heston_second_term = np.exp(((lam*v_hat)/chi**2)*(hest_4-hest_5))
    
    heston_charfn = heston_first_term*heston_second_term
    
    return heston_charfn




