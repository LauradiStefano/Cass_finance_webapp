# -*- coding: utf-8 -*-
"""
Created on Thu Jun 25 22:45:56 2020

@author: Diego
"""
from scipy.stats import poisson, norm
import numpy as np


def get_mc_mjd(X0, mu, sigma, lambda_one, mean_jumps, sd_jumps, T, NStep, NPaths):
    dt = T / NStep
    X_all = np.zeros((NStep + 1, NPaths))
    for i in range(0, NPaths):
        X = np.zeros(NStep)
        X = np.insert(X, 0, X0)

        # simulate the number of jumps
        NoJumps = poisson.rvs(lambda_one * dt, size=NStep)  # or use equivalently: NoJumps = poissrnd(lambda*dt);
        MJ = np.zeros(NStep)

        for j in range(0, NStep - 1):
            MJ[j] = sum(norm.rvs(mean_jumps, sd_jumps, size=NoJumps[j]))

        vector = mu * dt + MJ + norm.rvs(0, sigma * np.sqrt(dt), size=NStep)

        X[1:len(X)] = X0 + np.cumsum(vector, axis=0)
        # X = np.reshape(X, (NStep+1, 1))

        X_all[:, i] = X

    return X_all
