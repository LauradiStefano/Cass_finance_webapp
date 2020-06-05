# -*- coding: utf-8 -*-
"""
Created on Sat May 16 15:10:53 2020

@author: Diego
"""
import numpy as np
from scipy.stats import ncx2


def get_mc_heston(X0, v0, mu, alpha, beta, eta, rho, T, NStep, NPaths):
    dt = T / NStep

    epsilon1 = 0.5
    epsilon2 = 0.5  # for use in linear combination approx. of variance time-integral

    d = 4 * alpha * beta / eta ** 2  # degrees of freedom
    sf = 4 * alpha / (eta ** 2 * (1 - np.exp(-alpha * dt)))  # scaling factor for use in noncentrality parameter below

    K0 = (mu - rho * alpha * beta / eta) * dt
    K1 = epsilon1 * dt * (rho * alpha / eta - 0.5) - rho / eta
    K2 = epsilon2 * dt * (alpha * rho / eta - 0.5) + rho / eta
    K3 = epsilon1 * dt * (1 - rho ** 2)
    K4 = epsilon2 * dt * (1 - rho ** 2)

    X_all = np.zeros((NStep + 1, NPaths))

    for j in range(0, NPaths):
        zeros = np.zeros(NStep)
        X = np.append(X0, zeros)
        v = np.append(v0, zeros)

        for i in range(0, NStep):
            lambda_NC = v[i] * sf * np.exp(-alpha * dt)
            v[i + 1] = ncx2.rvs(d, lambda_NC) / sf
            X[i + 1] = X[i] + K0 + K1 * v[i] + K2 * v[i + 1] + np.sqrt(K3 * v[i] + K4 *
                                                                       v[i + 1]) * np.random.randn()

        X_all[:, j] = X

    return X_all
