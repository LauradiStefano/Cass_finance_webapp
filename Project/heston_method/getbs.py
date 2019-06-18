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
        implied_vol.append(scipy.optimize.brentq(function, a=-2.0, b=2.0, xtol=1e-8))

    return implied_vol


def bs_price(cp_flag, S0, K, T, rf, sigma, q):
    cp_flag = int(cp_flag)
    K = np.array(K)
    N = norm.cdf
    d1 = (np.log(S0 / K) + (rf - q + sigma * sigma / 2.) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)
    if cp_flag == 1:
        price = S0 * math.exp(-q * T) * N(d1) - K * math.exp(-rf * T) * N(d2)
    else:
        price = K * math.exp(-rf * T) * N(-d2) - S0 * math.exp(-q * T) * N(-d1)

    return price
