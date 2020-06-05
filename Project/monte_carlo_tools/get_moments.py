# -*- coding: utf-8 -*-
"""
Created on Sun May 17 14:49:47 2020

@author: Diego
"""
from scipy.stats import norm, lognorm, ncx2
from monte_carlo_tools.heston_mom import get_heston_moment, Power
import numpy as np


def get_moments(model, X0, parameters, T, NStep):
    dt = T / NStep
    p = 0.01

    horizon = np.arange(0, T + dt, dt)
    if model == 1:  # ABM
        mu = parameters[0]
        sg = parameters[1]
        moments = np.zeros((len(horizon), 4))
        moments[:, 0] = X0 + mu * horizon  # mean
        moments[:, 1] = sg * horizon ** 0.5  # Standard deviation
        moments[:, 2] = np.full(shape=len(horizon), fill_value=0, dtype=np.int)  # skewness
        moments[:, 3] = np.full(shape=len(horizon), fill_value=3, dtype=np.int)  # kurt

        quantiles = np.zeros((len(horizon), 2))

        quantiles[:, 0] = norm.ppf(p, moments[:, 0], moments[:, 1])
        quantiles[:, 1] = norm.ppf(1 - p, moments[:, 0], moments[:, 1])



    elif model == 2:  # GBM
        mu = parameters[0]
        sg = parameters[1]
        momgbm = lambda n: (X0 ** n) * np.exp(n * (mu - 0.5 * sg * sg) * horizon + n * n * sg * sg * horizon / 2)

        moments = np.zeros((len(horizon), 4))
        moments[:, 0] = momgbm(1)  # mean
        moments[:, 1] = (momgbm(2) - momgbm(1) ** 2) ** 0.5  # Standard deviation
        moments[:, 2] = (momgbm(3) - 3 * momgbm(2) * momgbm(1) + 2 * momgbm(1) ** 3) / (moments[:, 1] ** 3)  # skewness
        moments[:, 3] = (momgbm(4) - 4 * momgbm(3) * momgbm(1) + 6 * momgbm(2) * momgbm(1) ** 2 - 3 * momgbm(
            1) ** 4) / moments[:, 1] ** 4  # excess kurtosis
        moments[0, 2] = 0
        moments[0, 3] = 3

        quantiles = np.zeros((len(horizon), 2))
        scale = np.exp(np.log(X0) + (mu - sg * sg / 2) * horizon)
        s = sg * horizon ** 0.5  # sigma
        quantiles[:, 0] = lognorm.ppf(p, s, loc=0, scale=scale)
        quantiles[:, 1] = lognorm.ppf(1 - p, s, loc=0, scale=scale)




    elif model == 4:  # GAUSSIAN MR
        alpha = parameters[0]
        mu = parameters[1]
        sg = parameters[2]

        moments = np.zeros((len(horizon), 4))
        moments[:, 0] = np.exp(-alpha * horizon) * X0 + (1 - np.exp(-alpha * horizon)) * mu  # mean
        moments[:, 1] = (sg * sg * (1 - np.exp(-2 * alpha * horizon)) / (2 * alpha)) ** 0.5  # mean
        moments[:, 2] = np.full(shape=len(horizon), fill_value=0, dtype=np.int)  # skewness
        moments[:, 3] = np.full(shape=len(horizon), fill_value=3, dtype=np.int)  # kurt

        quantiles = np.zeros((len(horizon), 2))
        quantiles[:, 0] = norm.ppf(0.05, moments[:, 0], moments[:, 1])
        quantiles[:, 1] = norm.ppf(0.95, moments[:, 0], moments[:, 1])



    elif model == 3:  # CIR - SR MR
        alpha = parameters[0]
        mu = parameters[1]
        sg = parameters[2]
        k = sg * sg * (1 - np.exp(-alpha * horizon)) / (4 * alpha)
        d = 4 * alpha * mu / sg ** 2
        lam = 4 * alpha * X0 / (sg * sg * (np.exp(alpha * horizon) - 1))

        moments = np.zeros((len(horizon), 4))
        moments[:, 0] = np.exp(-alpha * horizon) * X0 + (1 - np.exp(-alpha * horizon)) * mu  # mean
        moments[:, 1] = k * (2 * (d + 2 * lam)) ** 0.5  # std dev.
        moments[:, 2] = 2 ** (3 / 2) * (d + 3 * lam) / (d + 2 * lam) ** (3 / 2)
        moments[:, 3] = 3 + 12 * (d + 4 * lam) / (d + 2 * lam) ** 2

        quantiles = np.zeros((len(horizon), 2))
        quantiles[:, 0] = k * ncx2.ppf(0.05, d, lam)
        quantiles[:, 1] = k * ncx2.ppf(0.95, d, lam)

    else:  # Heston
        v0 = parameters[0]
        mu = parameters[1]
        alpha = parameters[2]
        beta = parameters[3]
        eta = parameters[4]
        rho = parameters[5]
        moments = get_heston_moment(X0, v0, mu, alpha, beta, eta, rho, horizon)
        moments[0, 2] = 0
        moments[0, 3] = 3

        quantiles = np.zeros((len(horizon), 2))
        quantiles[:, 0] = moments[:, 0] + 3 * moments[:, 1]
        quantiles[:, 1] = moments[:, 0] - 3 * moments[:, 1]

    return moments, quantiles

    # if model == 5: #CEV
    #     #TO BE DONE

    # if model == 6 :#HESTON SV
    #     v0 = parameters(1)
    #     mu = parameters(2) 
    #     alpha = parameters(3)
    #     beta = parameters(4) 
    #     eta = parameters(5) 
    #     rho = parameters(6)
    #     moments = get_mom_Heston(X0, v0, mu, alpha, beta, eta, rho, horizon)
    #     moments(1,3) = 0
    #     moments(1,4) = 3

    #     quantiles(:,1) = moments(:,1)+3*moments(:,2)
    #     quantiles(:,2) = moments(:,1)-3*moments(:,2)
