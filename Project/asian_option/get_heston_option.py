# -*- coding: utf-8 -*-
"""
Created on Thu May  9 22:12:00 2019

@author: Diego
"""

import math

import numpy as np


def heston_psi0(u1, u2, dt, r, a, b, eta, rho):
    w2 = np.sqrt((a - 1j * u2 * rho * eta) ** 2 + (u2 ** 2 + 1j * u2) * eta ** 2)

    w1 = (a - 1j * u2 * rho * eta - w2 - 1j * u1 * eta ** 2) / (a - 1j * u2 * rho * eta + w2 - 1j * u1 * eta ** 2)

    output = 1j * u2 * (r - rho * a * b / eta) * dt + (a * b / eta ** 2) * (
            (a - w2) * dt - 2 * np.log((w1 * np.exp(-w2 * dt) - 1) / (w1 - 1)))

    return output


def heston_psi1(u1, u2, dt, a, eta, rho):
    w2 = np.sqrt((a - 1j * u2 * rho * eta) ** 2 + (u2 ** 2 + 1j * u2) * eta ** 2)

    w1 = (a - 1j * u2 * rho * eta - w2 - 1j * u1 * eta ** 2) / (a - 1j * u2 * rho * eta + w2 - 1j * u1 * eta ** 2)

    output = ((a - 1j * u2 * rho * eta - w2) - w1 * np.exp(-w2 * dt) * (a - 1j * u2 * rho * eta + w2)) / (
            (1 - w1 * np.exp(-w2 * dt)) * eta ** 2)

    return output


def heston_phi(g1, g2, n, N, dt, r, a, b, eta, rho, S0, v0):
    term = 0
    M = np.size(g2)
    v = np.zeros(M)

    for k in range(N, n, -1):
        term = term + heston_psi0(v, g2 * (1 - k / (N + 1)), dt, r, a, b, eta, rho)
        v = -1j * heston_psi1(v, g2 * (1 - k / (N + 1)), dt, a, eta, rho)

    for k in range(n, 0, -1):

        term = term + heston_psi0(v, g1 + g2 * (1 - k / (N + 1)), dt, r, a, b, eta, rho)
        if k != 0:
            v = -1j * heston_psi1(v, g1 + g2 * (1 - k / (N + 1)), dt, a, eta, rho)

    term = term + heston_psi0(v, g1+g2, 0, r, a, b, eta, rho)
    output = np.exp(1j*(g1+g2)*np.log(S0))*np.exp(heston_psi1(v, g1+g2, 0, a, eta, rho)*v0)*np.exp(term)

    return output


def heston_ft(u, delta, N, dt, r, a, b, eta, rho, S0, v0, K):
    term = 0
    for j in range(0, N + 1):
        term = term + heston_phi(-1j, u - 1j * delta, j, N, dt, r, a, b, eta, rho, S0, v0)

    output = np.exp(-r * N * dt) * (
            term - K * (N + 1) * heston_phi(0, u - 1j * delta, N, N, dt, r, a, b, eta, rho, S0, v0)) / (
                     (N + 1) * (1j * u + delta))

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


def heston_option(S0, K, v0, T, r, n, a, b, eta, rho, Nfft, lmax, lmin, delta, tolerance):
    dt = T / n
    dl = (lmax - lmin) / Nfft
    lmin = np.fix(lmin / dl) * dl
    l = lmin + np.arange(0, Nfft, 1) * dl
    flag = 0
    umax = 50

    while flag < 1:

        if abs(heston_ft(umax, delta, n, dt, r, a, b, eta, rho, S0 / K, v0, 1)) < tolerance:
            flag = 1

        umax = umax + 20

    du = 2 * umax / Nfft

    u = (np.arange(0, Nfft, 1) - 0.5 * Nfft) * du
    insert_one = 1
    yyy = np.append(insert_one, (3 + (-1) ** np.arange(0, Nfft - 2, 1)))
    wght = (np.append(yyy, insert_one)) / 3

    g0 = fr_fourier_transform(
        np.exp(-1j * u * l[0]) * heston_ft(u, delta, n, dt, r, a, b, eta, rho, S0 / K, v0, 1) * wght,
        du * dl / (2 * math.pi))
    g1 = K * np.exp(-delta * l) * np.real(g0 * np.exp(-1j * u[0] * (l - l[0])) * du / (2 * math.pi))

    Ptrue = max(g1)  # optimal lower bound
    lcr = l[g1 == max(g1)]
    # Exp_lcr = K*np.exp(l)
    K_Exp_lcr = K * math.exp(lcr)  # optimal strike
    lam = K * np.exp(l)
    Ptrue_K = g1[l == 0]  #

    return Ptrue, K_Exp_lcr, Ptrue_K, lam, g1
