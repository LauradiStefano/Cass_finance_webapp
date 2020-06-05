# -*- coding: utf-8 -*-
"""
Created on Sat May 16 15:51:20 2020

@author: Diego
"""
import numpy as np


def get_mc_gmr(X0, alpha, mu, sigma, T, NStep, NPaths):
    dt = T / NStep
    # Compute the variance of the increments
    vol2 = (1 - np.exp(-2 * alpha * dt)) / (2 * alpha)
    row = NStep + 1
    X_all = np.zeros((row, NPaths))

    for j in range(0, NPaths):
        X = np.zeros(NStep + 1)
        X[0] = X0

        dW = np.random.randn(NStep + 1) * vol2 ** 0.5

        for i in range(0, NStep):
            X[i + 1] = mu + np.exp(-alpha * dt) * (X[i] - mu) + sigma * dW[i]

        X_all[:, j] = X

    return X_all
