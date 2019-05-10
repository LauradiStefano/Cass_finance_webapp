# -*- coding: utf-8 -*-
"""
Created on Tue May  7 12:14:26 2019

@author: Diego
"""
import numpy as np
import scipy.stats as si

def newton_vol_call_div(S, K, T, C, r, q, sigma):
#    S = S0
#    T = Tt
#    r = risk_free
#    q = dividend_yield
#    C = target_value
#    K =strikes
    d1 = (np.log(S / K) + (r - q + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = (np.log(S / K) + (r - q - 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    
    fx = S * np.exp(-q * T) * si.norm.cdf(d1, 0.0, 1.0) - K * np.exp(-r * T) * si.norm.cdf(d2, 0.0, 1.0) - C
    
    vega = (1 / np.sqrt(2 * np.pi)) * S * np.exp(-q * T) * np.sqrt(T) * np.exp((-si.norm.cdf(d1, 0.0, 1.0) ** 2) * 0.5)
    
    tolerance = 0.00001
    x0 = sigma
    xnew  = x0
    xold = x0 - 1
        
    while all(abs(xnew - xold)) > tolerance:
    
        xold = xnew
        xnew = (xnew - fx - C) / vega
        
        return abs(xnew)