# -*- coding: utf-8 -*-
"""
Created on Sun Jul 21 10:03:00 2019

@author: Diego
"""
import math

import numpy as np


def z_charfn(u, dt, epsilon, k1, sigma):
    output = np.exp(
        1j * u * epsilon * (1 - np.exp(-k1 * dt)) - (0.25 / k1) * (1 - np.exp(-2 * k1 * dt)) * (sigma * u) ** 2)

    return output


def ONE_FACTOR_phi(g1, g2, n, N, dt, epsilon, k1, sigma, X0):
    m = 1

    for k in range(1, n + 1):
        D = sum(np.exp(-(np.arange(0, n - k + 1, 1)) * k1 * dt))

        B = g1 * np.exp(-n * dt * k1) + np.sum(np.exp(-np.arange(n + 1, N + 1, 1) * dt * k1)) * g2 / N

        m = m * z_charfn(B * math.exp(k * dt * k1) + g2 * D / N, dt, epsilon, k1, sigma)

    for k in range(n + 1, N + 1):
        D = sum(np.exp(-np.arange(0, N - k + 1) * k1 * dt))

        m = m * z_charfn(g2 * D / N, dt, epsilon, k1, sigma)

    output = np.exp(
        1j * (g1 * np.exp(-n * dt * k1) + g2 * np.mean(np.exp(-k1 * dt * np.arange(1, N + 1, 1)))) * X0) * m

    return output


def ONE_FACTOR_FT(u, delta, N, dt, epsilon, k1, sigma, r, X0, K):
    term = 0
    N = int(N)
    for j in range(1, N + 1):
        term = term + ONE_FACTOR_phi(-1j, u - 1j * delta, j, N, dt, epsilon, k1, sigma, X0)

    output = np.exp(-r * N * dt) * (
            term - K * N * ONE_FACTOR_phi(0, u - 1j * delta, N, N, dt, epsilon, k1, sigma, X0)) / (
                     N * (1j * u + delta))

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

    f = np.exp(-math.pi * 1j * a * np.arange(0, m) ** 2) * ifyz[0:m, ]

    return f


def exp_gaussian_option(X0, K, T, r, n, epsilon, k1, sigma, Nfft, lmax, lmin, delta, tolerance):
    dt = T / n

    # Nfft = 2**12

    # lmax = 6
    # lmin = 3

    dl = (lmax - lmin) / Nfft

    lmin = np.fix(lmin / dl) * dl

    l = lmin + np.arange(0, Nfft, 1) * dl

    # delta = 1.5

    umax = 50

    flag = 0

    while flag < 1:

        if abs(ONE_FACTOR_FT(umax, delta, n, dt, epsilon, k1, sigma, r, X0, K)) < tolerance:
            flag = 1

        umax = umax + 20

    du = 2 * umax / Nfft

    u = (np.arange(0, Nfft, 1) - 0.5 * Nfft) * du

    wght = (3 + (-1) ** np.arange(0, Nfft - 2, 1))
    insert_one = 1
    b = np.append(insert_one, (3 + (-1) ** np.arange(0, Nfft - 2, 1)))
    wght = (np.append(b, insert_one)) / 3

    g0 = fr_fourier_transform(
        np.exp(-1j * u * l[0]) * ONE_FACTOR_FT(u, delta, n, dt, epsilon, k1, sigma, r, X0, K) * wght,
        du * dl / (2 * math.pi))
    g1 = np.exp(-delta * l) * np.real(g0 * np.exp(-1j * u[0] * (l - l[0])) * du / (2 * math.pi))

    Ptrue = max(g1)

    lcr = l[g1 == Ptrue]

    Exp_lcr = math.exp(lcr)
    # K_Exp_lcr=K*Exp_lcr
    # plot(l,g1)

    Ptrue_K = 4.555555  # g1[l==0]

    return Ptrue, Exp_lcr, Ptrue_K, l, g1
