# -*- coding: utf-8 -*-
"""
Created on Tue Jun 30 20:54:23 2020

@author: Diego
"""

import numpy as np


def get_mc_vg(X0, theta, sigma, kappa, T, NStep, NPaths):
    # theta = theta_vg
    # sigma = sigma_vg 
    # kappa = kappa_vg 

    dt = T / NStep

    dG = np.zeros((NStep, NPaths))
    matrix_incr_abm = np.zeros((NStep, NPaths))

    for i in range(0, NStep):
        # Simulate increments of vairance gamma process
        dG[i, :] = np.random.gamma(dt / kappa, kappa, NPaths)
        # Simulate incrementsd  of the abm on the Gamma clock scale

        matrix_incr_abm[i, :] = np.random.randn(NPaths)
        # Simulate vg process (uns cumulative sum of increments)

    dX = theta * dG + sigma * np.sqrt(dG) * matrix_incr_abm
    first_component = X0 * np.ones((1, NPaths))
    second_componet = X0 + np.cumsum(dX, axis=0)
    X_all = np.concatenate((first_component, second_componet), axis=0)

    return X_all
