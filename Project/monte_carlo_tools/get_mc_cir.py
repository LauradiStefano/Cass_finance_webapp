# -*- coding: utf-8 -*-
"""
Created on Wed May 13 15:54:29 2020

@author: Diego
"""
import numpy as np
from scipy.stats import ncx2


def get_mc_cir(X0, alpha, mu, sigma, T, NStep, NPaths):
    dt = T / NStep

    # epsilon1 = 0.5
    # epsilon2 = 0.5

    d = 4 * alpha * mu / sigma ** 2
    sf = 4 * alpha / (sigma ** 2 * (1 - np.exp(-alpha * dt)))

    X_all = np.zeros((NStep + 1, NPaths))

    for j in range(0, NPaths):
        zeros = np.zeros(NStep)
        X = np.append(X0, zeros)
        for i in range(0, NStep):
            lambda_NC = X[i] * sf * np.exp(-alpha * dt)
            X[i + 1] = ncx2.rvs(d, lambda_NC) / sf
            # np.concatenate((first_row,second_component), axis=1)

        X_all[:, j] = X

    return X_all
