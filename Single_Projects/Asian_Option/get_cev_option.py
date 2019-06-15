# -*- coding: utf-8 -*-
"""
Created on Tue May 21 09:29:16 2019

@author: Diego
"""
import math

import numpy as np


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

    f = np.exp(-math.pi * 1j * a * np.arange(0, m) ** 2) * ifyz[0:m, ]

    return f


def factor2(m, gamma, dt, r, sig):
    if gamma < 2:

        b = r * (gamma - 2)
        g = r * (2 - gamma)

    else:

        b = r * (2 - gamma)
        g = r * (gamma - 2)

    s = sig * (2 - gamma)
    output = m * ((g - b) + np.exp(-g * dt) * (g + b)) / (
            s ** 2 * m * (1 - np.exp(-g * dt)) + (g + b) + np.exp(-g * dt) * (g - b))

    return output


def factor1spot(m, gamma, dt, r, sig):
    if gamma < 2:
        a = (sig ** 2 / 2) * (gamma - 3) * (gamma - 2)
        b = r * (gamma - 2)
        g = r * (2 - gamma)

    else:
        a = (-sig ** 2 / 2) * (2 - gamma)
        b = r * (2 - gamma)
        g = r * (gamma - 2)

    s = sig * (2 - gamma)
    numer = 2 * g * np.exp((b - g) * dt / 2)
    denom = s ** 2 * m * (1 - np.exp(-g * dt)) + (g + b) + np.exp(-g * dt) * (g - b)
    output = a * (-2 / s ** 2) * np.log(numer / denom)

    return output


def factor1(m, gamma, dt, r, sig):
    if gamma < 2:
        a = (sig ** 2 / 2) * (gamma - 1) * (gamma - 2)
        b = r * (gamma - 2)
        g = r * (2 - gamma)

    else:
        a = (sig ** 2 / 2) * (2 - gamma)
        b = r * (2 - gamma)
        g = r * (gamma - 2)

    s = sig * (2 - gamma)
    numer = 2 * g * np.exp((b - g) * dt / 2)
    denom = s ** 2 * m * (1 - np.exp(-g * dt)) + (g + b) + np.exp(-g * dt) * (g - b)
    output = a * (-2 / s ** 2) * np.log(numer / denom)

    return output


def CEVSpotPhi(g1, g2, n, N, dt, r, sig, gamma, X0):
    #    N=12
    #    g1 = 0
    #    g2 = u-1j*delta
    #    sig = sigma
    #    X0 = 1
    #    j = 0
    g = -1j * g1
    m = -1j * g2
    #    n=j
    Lam = g * (n == N) + m / (N + 1)

    if n < N:
        C = factor1(Lam, gamma, dt, r, sig)

    else:  # n == N:
        C = factor1spot(Lam, gamma, dt, r, sig)

    A = factor2(Lam, gamma, dt, r, sig)

    for j in range(N - 1, 0, -1):

        Lam = A + g * (n == j) + m / (N + 1)
        if n >= j:
            C = C + factor1spot(Lam, gamma, dt, r, sig)
        else:
            C = C + factor1(Lam, gamma, dt, r, sig)

        A = factor2(Lam, gamma, dt, r, sig)

    Lam = A + g * (n == 0) + m / (N + 1)
    output = np.exp(-C - Lam * X0)

    return output


def CEVPhi(g1, g2, n, N, dt, r, sig, gamma, X0):
    #    g1 = 0
    #    g2 = u-1j*delta
    g = -1j * g1
    m = -1j * g2
    Lam = g * (n == N) + m / (N + 1)
    C = factor1(Lam, gamma, dt, r, sig)
    A = factor2(Lam, gamma, dt, r, sig)

    for j in range(N - 1, 0, -1):
        Lam = A + g * (n == j) + m / (N + 1)
        C = C + factor1(Lam, gamma, dt, r, sig)
        A = factor2(Lam, gamma, dt, r, sig)

    Lam = A + g * (n == 0) + m / (N + 1)
    output = np.exp(-C - Lam * X0)

    return output


def CEVFTGammaAboveTwo(u, delta, N, dt, r, sigma, gamma, X0, K):
    term = 0
    for j in range(0, N + 1):
        term = term + X0 ** (1 / (2 - gamma)) * np.exp(r * j * dt) * CEVSpotPhi(0, u - 1j * delta, j, N, dt, r, sigma,
                                                                                gamma, X0)

    output = np.exp(-r * N * dt) * (-term + K * (N + 1) * CEVPhi(0, u - 1j * delta, N, N, dt, r, sigma, gamma, X0)) / (
            (N + 1) * (1j * u + delta))

    return output


def CEVFT(u, delta, N, dt, r, sigma, gamma, X0, K):
    term = 0
    for j in range(0, N + 1):
        term = term + X0 ** (1 / (2 - gamma)) * np.exp(r * j * dt) * CEVSpotPhi(0, u - 1j * delta, j, N, dt, r, sigma,
                                                                                gamma, X0)

    output = np.exp(-r * N * dt) * (term - K * (N + 1) * CEVPhi(0, u - 1j * delta, N, N, dt, r, sigma, gamma, X0)) / (
            (N + 1) * (1j * u + delta))

    return output


def cev_option(S0, K, T, r, n, beta, Nfft, lmax, lmin, delta, tolerance):
    F = S0
    S0 = S0 / F
    K = K / F

    dt = T / n

    # Nfft = 2**15
    # lmax = 3
    # lmin = -lmax
    dl = (lmax - lmin) / Nfft
    lmin = np.fix(lmin / dl) * dl
    # lmin = K+fix((lmin-K)/dl)*dl
    l = lmin + np.arange(0, Nfft, 1) * dl
    gamma = 2 * (beta + 1)
    sigma = 0.25 * (S0) ** -beta

    if gamma > 2:
        # delta = -1.5
        umax = 10
        flag = 0
        while flag < 1:
            if abs(CEVFTGammaAboveTwo(umax, delta, n, dt, r, sigma, gamma, S0 ** (2 - gamma), K)) < tolerance:
                flag = 1

            umax = umax + 10

    else:
        # delta = 1.5
        umax = 10
        flag = 0
        while flag < 1:
            if abs(CEVFT(umax, delta, n, dt, r, sigma, gamma, S0 ** (2 - gamma), K)) < tolerance:
                flag = 1

            umax = umax + 10

    du = 2 * umax / Nfft

    u = (np.arange(0, Nfft, 1) - 0.5 * Nfft) * du
    insert_one = 1
    yyy = np.append(insert_one, (3 + (-1) ** np.arange(0, Nfft - 2, 1)))
    wght = (np.append(yyy, insert_one)) / 3

    if gamma > 2:
        g0 = fr_fourier_transform(
            np.exp(-1j * u * l[0]) * CEVFTGammaAboveTwo(u, delta, n, dt, r, sigma, gamma, S0 ** (2 - gamma), K) * wght,
            du * dl / (2 * math.pi))
    else:
        g0 = fr_fourier_transform(
            np.exp(-1j * u * l[0]) * CEVFT(u, delta, n, dt, r, sigma, gamma, S0 ** (2 - gamma), K) * wght,
            du * dl / (2 * math.pi))

    g1 = np.exp(-delta * l) * np.real(g0 * np.exp(-1j * u[0] * (l - l[0])) * du / (2 * math.pi))
    Ptrue = F * max(g1)
    lcr = (l[g1 == max(g1)]) ** (1 / (2 - gamma))
    K_Exp_lcr = F * lcr  # optimal strike
    lam = K * np.exp(l)
    Ptrue_K = F * g1[(l ** (1 / (2 - gamma))) == 0]

    return Ptrue, K_Exp_lcr, Ptrue_K, lam, g1
