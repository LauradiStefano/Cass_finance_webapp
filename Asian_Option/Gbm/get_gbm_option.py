# -*- coding: utf-8 -*-
"""
Created on Tue May  7 00:06:31 2019

@author: Diego
"""

import math

import numpy as np
from get_gbm_fr_ft import fr_fourier_transform
from get_gbm_ft import gbm_ft


def gbm_option(S0, K, T, r, n, sigma):
    dt = T / n

    Nfft = 2 ** 12

    lmax = 2
    lmin = -lmax
    dl = (lmax - lmin) / Nfft
    l = lmin + np.arange(0, Nfft, 1) * dl

    delta = 1.5
    umax = 50
    flag = 0

    while flag < 1:

        if abs(gbm_ft(1, umax, delta, n, dt, sigma, r, S0 / K, 1)) < 1E-5:
            flag = 1

        umax = umax + 20

    du = 2 * umax / Nfft

    u = (np.arange(0, Nfft, 1) - 0.5 * Nfft) * du

    insert_one = 1
    b = np.append(insert_one, (3 + (-1) ** np.arange(0, Nfft - 2, 1)))
    wght = (np.append(b, insert_one)) / 3

    g0 = fr_fourier_transform(np.exp(-1j * u * l[0]) * gbm_ft(1, u, delta, n, dt, sigma, r, S0 / K, 1) * wght,
                              du * dl / (2 * math.pi))
    g1 = K * np.exp(-delta * l) * np.real(g0 * np.exp(-1j * u[0] * (l - l[0])) * du / (2 * math.pi))

    Ptrue = max(g1)  # optimal lower bound
    lcr = l[g1 == max(g1)]
    lam = K * np.exp(l)
    K_Exp_lcr = K * math.exp(lcr)  # optimal strike

    Ptrue_K = g1[l == 0]

    return Ptrue, K_Exp_lcr, Ptrue_K, lam, g1

