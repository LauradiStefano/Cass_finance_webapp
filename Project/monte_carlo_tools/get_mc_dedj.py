# -*- coding: utf-8 -*-
"""
Created on Tue Jun 30 20:00:18 2020

@author: Diego
"""
from scipy.stats import poisson, norm
import numpy as np


def get_mc_dedj(X0, mu, sigma, lambda_one, p, eta_p, eta_m, T, NStep, NPaths):
    # mu = mu_dejd
    # sigma = sigma_dejd 
    # lambda_one = lambda_dejd 
    # p = p_dejd 
    # eta_p = eta1_dejd 
    # eta_m = eta2_dejd 

    dt = T / NStep

    X_all = np.zeros((NStep + 1, NPaths))
    for i in range(0, NPaths):
        X = np.zeros(NStep)
        X = np.insert(X, 0, X0)

        # simulate the number of jumps
        NoJumps = poisson.rvs(lambda_one * dt, size=NStep)  # or use equivalently: NoJumps = poissrnd(lambda*dt);
        DEJ = np.zeros(NStep)

        for j in range(0, NStep - 1):
            u = np.random.rand(1, NoJumps[j])
            DEJ[j] = np.sum((u < p) * np.log(np.random.rand(1, NoJumps[j])) * (1 / eta_p) - (u >= p) * np.log(
                np.random.rand(1, NoJumps[j])) * (-1 / eta_m))

        vector = mu * dt + DEJ + norm.rvs(0, sigma * np.sqrt(dt), size=NStep)

        X[1:len(X)] = X0 + np.cumsum(vector, axis=0)
        # X = np.reshape(X, (NStep+1, 1))

        X_all[:, i] = X

    return X_all
