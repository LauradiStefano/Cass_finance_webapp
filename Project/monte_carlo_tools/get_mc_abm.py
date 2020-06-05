# -*- coding: utf-8 -*-
"""
Created on Wed May 13 14:41:55 2020

@author: Diego
"""

import numpy as np


def get_mc_abm(X0, mu, sigma, T, Nstep, Npaths):
    # Assign the number of simulated paths (nsimul)
    nsimul = Npaths

    # Time to maturity (expiry)
    expiry = T

    # number of steps (nsteps)
    nsteps = Nstep

    # time step (dt) and observation times (timestep):
    dt = expiry / nsteps
    ##timestep = [0:dt:expiry]'

    # Simulate increments ABM dX:
    dX = mu * dt + sigma * np.random.randn(nsteps, nsimul) * dt ** 0.5

    # Simulate ABM process: cumulate increments
    first_row = np.array([X0 * np.ones(nsimul)])
    second_component = X0 + np.cumsum(dX, axis=0)
    X = np.concatenate((first_row, second_component), axis=0)

    return X
