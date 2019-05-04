# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 22:27:07 2019

@author: Diego
"""
import numpy as np
import math
from scipy.stats import norm


def find_vol(target_value, call_put, s0, K, T, risk_free, div_yield):
    MAX_ITERATIONS = 1000
    PRECISION = 1.0e-5
    sigma = 0.5
    # for j in range (int(len(K))):
    for i in range(0, MAX_ITERATIONS):
        price = bs_price(call_put, s0, K, T, risk_free, sigma, div_yield)
        vega = bs_vega(s0, K, T, risk_free, sigma)

        price = price
        diff = target_value - price  # our root

        # print (i, sigma, diff)

        if all(abs(diff) < PRECISION):
            return sigma

        volt = sigma + diff / vega  # f(x) / f'(x)

    # value wasn't found, return best guess so far
    return volt


# implied_vol.append(sigma)
# return implied_vol

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
        delta_K_S0 = np.array(K) - float(s0)
        negative = delta_K_S0 < 0
        positive = delta_K_S0 > 0
        K_Call = (K * negative)
        K_Call = np.array([elem for elem in K_Call if elem != 0])

        K_Put = K * positive
        K_Put = np.array([elem for elem in K_Put if elem != 0])

        d1_Call = (np.log(s0 / K_Call) + (risk_free + sigma * sigma / 2.) * T) / (sigma * math.sqrt(T))
        d2_Call = d1_Call - sigma * math.sqrt(T)

        d1_Put = (np.log(s0 / K_Put) + (risk_free + sigma * sigma / 2.) * T) / (sigma * math.sqrt(T))
        d2_Put = d1_Put - sigma * math.sqrt(T)

        priceC = s0 * math.exp(-div_yield * T) * N(d1_Call) - K_Call * math.exp(-risk_free * T) * N(d2_Call)
        priceP = K_Put * math.exp(-risk_free * T) * N(-d2_Put) - s0 * math.exp(-div_yield * T) * N(-d1_Put)
        price = list(list(priceC) + list(priceP))
        price = np.array(price)

    return price


def bs_vega(s0, K, T, risk_free, sigma):
    n = norm.pdf
    K = np.array(K)
    d1 = (np.log(s0 / K) + (risk_free + sigma * sigma / 2.) * T) / (sigma * math.sqrt(T))

    return s0 * math.sqrt(T) * n(d1)
