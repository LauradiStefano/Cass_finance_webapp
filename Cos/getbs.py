# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 22:27:07 2019

@author: Diego
"""
import math

import numpy as np
from scipy.stats import norm


def find_vol(target_value, cp, s0, K, T, risk_free, div_yield):
    MAX_ITERATIONS = 1000
    PRECISION = 1.0e-5
    sigma = 0.5
    # for j in range (int(len(K))):
    for i in range(0, MAX_ITERATIONS):
        price = bs_price(cp, s0, K, T, risk_free, sigma, div_yield)
        vega = bs_vega(s0, K, T, risk_free, sigma)
        diff = target_value - price  # our root

        # print (i, sigma, diff)

        if all(abs(diff) < PRECISION):
            return sigma

        volt = sigma + diff / vega  # f(x) / f'(x)

    # value wasn't found, return best guess so far
    return volt


# implied_vol.append(sigma)
# return implied_vol

def bs_price(cp_flag, s0, K, T, risk_free, sigma, div_yield):
    cp_flag = int(cp_flag)
    K = np.array(K)
    N = norm.cdf
    d1 = (np.log(s0 / K) + (risk_free + sigma * sigma / 2.) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)
    if cp_flag == 1:
        price = s0 * math.exp(-div_yield * T) * N(d1) - K * math.exp(-risk_free * T) * N(d2)
    else:  # cp_flag == 0:
        price = K * math.exp(-risk_free * T) * N(-d2) - s0 * math.exp(-div_yield * T) * N(-d1)

    return price


def bs_vega(s0, K, T, risk_free, sigma):
    n = norm.pdf
    K = np.array(K)
    d1 = (np.log(s0 / K) + (risk_free + sigma * sigma / 2.) * T) / (sigma * math.sqrt(T))

    return s0 * math.sqrt(T) * n(d1)
