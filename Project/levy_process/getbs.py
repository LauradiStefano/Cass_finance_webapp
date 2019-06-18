# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 22:27:07 2019

@author: Diego
"""
import math

import numpy as np
import scipy.optimize
from scipy.stats import norm


def find_vol(target_value, cp, s0, K, T, risk_free, div_yield):
    implied_vol = []
    for j in range(0, len(K)):
        function = lambda vol: target_value[j] - bs_price(cp, s0, K[j], T, risk_free, vol, div_yield)
        implied_vol.append(scipy.optimize.brentq(function, a=-10.0, b=10.0, xtol=1e-6))

    return implied_vol


# implied_vol.append(sigma)
# return implied_vol

def bs_price(cp_flag, s0, K, T, risk_free, sigma, div_yield):
    cp_flag = int(cp_flag)
    K = np.array(K)
    N = norm.cdf
    d1 = (np.log(s0 / K) + (risk_free - div_yield + sigma * sigma / 2.) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)
    if cp_flag == 1:
        price = s0 * math.exp(-div_yield * T) * N(d1) - K * math.exp(-risk_free * T) * N(d2)
    else:  # cp_flag == 0:
        price = K * math.exp(-risk_free * T) * N(-d2) - s0 * math.exp(-div_yield * T) * N(-d1)

    return price
