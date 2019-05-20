# -*- coding: utf-8 -*-
"""
Created on Tue May  7 00:06:31 2019

@author: Diego
"""

import math

import numpy as np


def gbm_charfn(u, dt, sigma, r):
    output = np.exp(dt * (1j * (r - 0.5 * sigma ** 2) * u - 0.5 * sigma ** 2 * u ** 2))

    return output


def gbm_phi(g1, g2, n, N, dt, sigma, r, S0):
    term = 0

    for k in range(1, n + 1):
        term = term + np.log(gbm_charfn(g1 + g2 * (1 - k / (N + 1)), dt, sigma, r))  # corretto

    for k in range(n + 1, N + 1):
        term = term + np.log(gbm_charfn(g2 * (1 - k / (N + 1)), dt, sigma, r))  # corretto

    output = np.exp(1j * (g1 + g2) * math.log(S0)) * np.exp(term)

    return output


def gbm_ft(s, u, delta, N, dt, sigma, r, S0, K):  # corretto

    term = 0

    for j in range(0, N + 1):
        term = term + gbm_phi(-1j, u - s * 1j * delta, j, N, dt, sigma, r, S0)

    output = np.exp(-r * N * dt) * (term - K * (N + 1) * gbm_phi(0, u - s * 1j * delta, N, N, dt, sigma, r, S0)) / (
            (N + 1) * (s * 1j * u + delta))

    return output


def fr_fourier_transform(x, a):
    m = len(x)

    # first fft
    vect_one = x * np.exp(-math.pi * 1j * a * np.arange(0, m) ** 2)
    vect_two = np.concatenate((vect_one, np.zeros(m)))
    first_fft = np.fft.fft(vect_two)  # correto

    # Second fft
    vect_third = np.exp(math.pi * 1j * a * np.arange(0, m) ** 2)
    vect_fourth = np.exp(math.pi * 1j * a * np.arange(-m, 0) ** 2)
    second_fft = np.fft.fft(np.concatenate((vect_third, vect_fourth)))

    # ifyz
    ifyz = (np.fft.ifft(first_fft * second_fft))

    # f

    f = np.exp(-math.pi * 1j * a * np.arange(0, m) ** 2) * ifyz[0:m]

    return f


def gbm_option(S0, K, T, r, n, sigma, Nfft, lmax, lmin, delta, umax):
    dt = T / n

    # Nfft = 2 ** 12
    #
    # lmax = 2
    # lmin = -lmax
    dl = (lmax - lmin) / Nfft
    l = lmin + np.arange(0, Nfft, 1) * dl

    # delta = 1.5
    # umax = 50
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
