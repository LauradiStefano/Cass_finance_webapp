# -*- coding: utf-8 -*-
"""
Created on Fri May  3 11:30:35 2019

@author: Diego
"""
import numpy as np

from get_gbm_phi import gbm_phi


def gbm_ft(s, u, delta, N, dt, sigma, r, S0, K):  # corretto

    term = 0

    for j in range(0, N + 1):
        term = term + gbm_phi(-1j, u - s * 1j * delta, j, N, dt, sigma, r, S0)

    output = np.exp(-r * N * dt) * (term - K * (N + 1) * gbm_phi(0, u - s * 1j * delta, N, N, dt, sigma, r, S0)) / (
            (N + 1) * (s * 1j * u + delta))

    return output
