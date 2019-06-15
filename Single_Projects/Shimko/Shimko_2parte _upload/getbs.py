# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 22:27:07 2019

@author: Diego
"""
import numpy as np
import math
from scipy.stats import norm
import scipy.optimize

def  find_vol(target_value, cp, s0, K, T, risk_free, div_yield):
    
    implied_vol = []

    for j in range(0,len(K)):
        
        function = lambda vol : target_value[j]-bs_price(cp, s0, K[j], T, risk_free, vol, div_yield)
        implied_vol.append(scipy.optimize.brentq(function, a=-2.0, b=2.0, xtol=1e-8))

    return implied_vol 


def bs_price(call_put, s0, K, T, risk_free, sigma, div_yield):
    K = np.array(K)
    N = norm.cdf
    d1 = (np.log(s0 / K) + (risk_free + sigma * sigma / 2.) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)
    if call_put == 1:
        price = s0 * math.exp(-div_yield * T) * N(d1) - K * math.exp(-risk_free * T) * N(d2)
    elif call_put == 0:
        price = K * math.exp(-risk_free * T) * N(-d2) - s0 * math.exp(-div_yield * T) * N(-d1)
    else:  # call_put == 2:
        delta_K_S0 = K - float(s0)

        if delta_K_S0 < 0:
            price = s0 * math.exp(-div_yield * T) * N(d1) - K * math.exp(-risk_free * T) * N(d2)

        else: 
            price = K * math.exp(-risk_free * T) * N(-d2) - s0 * math.exp(-div_yield * T) * N(-d1)




    return price


def bs_vega(s0, K, T, risk_free, sigma):
    n = norm.pdf
    K = np.array(K)
    d1 = (np.log(s0 / K) + (risk_free + sigma * sigma / 2.) * T) / (sigma * math.sqrt(T))

    return s0 * math.sqrt(T) * n(d1)
