# -*- coding: utf-8 -*-
"""
Created on Thu Jun 25 10:59:38 2020

@author: Diego
"""
import numpy as np


def get_mc_garch(X0, mu, v0, omega, alpha, beta, asymm, T, NStep, NPaths):
    dt = T / NStep

    # Gaussian innovation
    epsilon = np.random.randn(NPaths, NStep)

    # Array of 1-period returns
    X_k = np.zeros((NPaths, NStep))
    var_garch = np.ones((NPaths, 1)) * v0
    # lambda_one = 1 - alpha

    for i in range(0, NStep):
        X_k[:, i] = mu * dt + epsilon[:, i] * var_garch.reshape(NPaths) ** 0.5
        var_garch = omega + beta * var_garch.reshape(NPaths) + alpha * (X_k[:, i] - mu * dt - asymm) ** 2

    first_component = X0 * np.ones((1, NPaths))
    second_component = X0 + np.cumsum(X_k, axis=1).T
    X_all = np.concatenate((first_component, second_component), axis=0)

    return X_all
