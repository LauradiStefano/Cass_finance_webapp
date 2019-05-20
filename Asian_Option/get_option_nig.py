# -*- coding: utf-8 -*-
"""
Created on Mon May 20 13:08:14 2019

@author: Diego
"""

# -*- coding: utf-8 -*-
"""
Created on Tue May  7 00:06:31 2019

@author: Diego
"""

import math

import numpy as np


def nig_charfn(u, dt, a, b, d, r):
    output = np.exp(dt * (1j * (r + d * (np.sqrt(a ** 2 - (b + 1) ** 2) - np.sqrt(a ** 2 - b ** 2))) * u - d * (
            np.sqrt(a ** 2 - (b + 1j * u) ** 2) - np.sqrt(a ** 2 - b ** 2))))

    return output


# function output = NIGCharFn(u, dt, a, b, d, r)
# output = exp(dt*(1i*(r+d*(sqrt(a^2-(b+1)^2)-sqrt(a^2-b^2)))*u-d*(sqrt(a^2-(b+1i*u).^2)-sqrt(a^2-b^2))));
# end

def nig_phi(g1, g2, n, N, dt, a, b, d, r, S0):
    term = 0

    for k in range(1, n + 1):
        term = term + np.log(nig_charfn(g1 + g2 * (1 - k / (N + 1)), dt, a, b, d, r))  # corretto

    for k in range(n + 1, N + 1):
        term = term + np.log(nig_charfn(g2 * (1 - k / (N + 1)), dt, a, b, d, r))  # corretto

    output = np.exp(1j * (g1 + g2) * math.log(S0)) * np.exp(term)

    return output


def nig_ft(u, delta, N, dt, a, b, d, r, S0, K):  # corretto

    term = 0

    for j in range(0, N + 1):
        term = term + nig_phi(-1j, u - 1j * delta, j, N, dt, a, b, d, r, S0)

    output = np.exp(-r * N * dt) * (term - K * (N + 1) * nig_phi(0, u - 1j * delta, N, N, dt, a, b, d, r, S0)) / (
            (N + 1) * (1j * u + delta));

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


def nig_option(S0, K, T, r, n, a, b, d, Nfft, lmax, lmin, delta, umax):
    dt = T / n
    dl = (lmax - lmin) / Nfft
    lmin = np.fix(lmin / dl) * dl
    l = lmin + np.arange(0, Nfft, 1) * dl

    flag = 0

    while flag < 1:

        if abs(nig_ft(umax, delta, n, dt, a, b, d, r, S0 / K, 1)) < 1E-5:
            flag = 1

        umax = umax + 20

    du = 2 * umax / Nfft

    u = (np.arange(0, Nfft, 1) - 0.5 * Nfft) * du
    insert_one = 1
    build_array = np.append(insert_one, (3 + (-1) ** np.arange(0, Nfft - 2, 1)))
    wght = (np.append(build_array, insert_one)) / 3

    g0 = fr_fourier_transform(np.exp(-1j * u * l[0]) * nig_ft(u, delta, n, dt, a, b, d, r, S0 / K, 1) * wght,
                              du * dl / (2 * math.pi))
    g1 = K * np.exp(-delta * l) * np.real(g0 * np.exp(-1j * u[0] * (l - l[0])) * du / (2 * math.pi))

    Ptrue = max(g1)  # optimal lower bound
    lcr = l[g1 == max(g1)]
    lam = K * np.exp(l)
    K_Exp_lcr = K * math.exp(lcr)  # optimal strike

    Ptrue_K = g1[l == 0]  #

    return Ptrue, K_Exp_lcr, Ptrue_K, lam, g1
