# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 22:27:07 2019

@author: Diego
"""
import numpy as np
import math
from scipy.stats import norm


def find_vol(target_value, cp, S0, K, T, rf, q):
    MAX_ITERATIONS = 1000
    PRECISION = 1.0e-5
    sigma = 0.5
    # for j in range (int(len(K))):
    for i in range(0, MAX_ITERATIONS):
        price = bs_price(cp, S0, K, T, rf, sigma, q)
        vega = bs_vega(cp, S0, K, T, rf, sigma, q)

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

def bs_price(cp_flag, S0, K, T, rf, sigma, q):
    K = np.array(K)
    N = norm.cdf
    d1 = (np.log(S0 / K) + (rf + sigma * sigma / 2.) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)
    if cp_flag == 1:
        price = S0 * math.exp(-q * T) * N(d1) - K * math.exp(-rf * T) * N(d2)
    elif cp_flag == 0:
        price = K * math.exp(-rf * T) * N(-d2) - S0 * math.exp(-q * T) * N(-d1)
    elif cp_flag == 2:
        delta_K_S0 = np.array(K) - float(S0)
        negative = delta_K_S0 < 0
        positive = delta_K_S0 > 0
        K_Call = (K * negative)
        K_Call = np.array([elem for elem in K_Call if elem != 0])

        K_Put = K * positive
        K_Put = np.array([elem for elem in K_Put if elem != 0])

        d1_Call = (np.log(S0 / K_Call) + (rf + sigma * sigma / 2.) * T) / (sigma * math.sqrt(T))
        d2_Call = d1_Call - sigma * math.sqrt(T)

        d1_Put = (np.log(S0 / K_Put) + (rf + sigma * sigma / 2.) * T) / (sigma * math.sqrt(T))
        d2_Put = d1_Put - sigma * math.sqrt(T)

        priceC = S0 * math.exp(-q * T) * N(d1_Call) - K_Call * math.exp(-rf * T) * N(d2_Call)
        priceP = K_Put * math.exp(-rf * T) * N(-d2_Put) - S0 * math.exp(-q * T) * N(-d1_Put)
        price = list(list(priceC) + list(priceP))
        price = np.array(price)

    return price


def bs_vega(cp_flag, S0, K, T, rf, sigma, q):
    n = norm.pdf
    K = np.array(K)
    d1 = (np.log(S0 / K) + (rf + sigma * sigma / 2.) * T) / (sigma * math.sqrt(T))

    return S0 * math.sqrt(T) * n(d1)
