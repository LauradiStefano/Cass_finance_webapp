# -*- coding: utf-8 -*-
"""
Created on Fri May  3 10:17:26 2019

@author: Diego
"""
from get_gbm_charfn import gbm_charfn
import numpy as np
import math

def gbm_phi(g1, g2, n, N, dt, sigma, r, S0):

    term = 0
    
    for k in range(1,n+1):
       
        term = term + np.log(gbm_charfn(g1+g2*(1-k/(N+1)), dt, sigma, r))# corretto
        

    for k in range(n+1,N+1):
        
        term = term + np.log(gbm_charfn(g2*(1-k/(N+1)), dt, sigma, r))#corretto
    
    output = np.exp(1j*(g1+g2)*math.log(S0))*np.exp(term)

    
    return output

