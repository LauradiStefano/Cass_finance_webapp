# -*- coding: utf-8 -*-
"""
Created on Sun May 17 14:49:47 2020

@author: Diego
"""
from scipy.stats import norm, lognorm, ncx2
from monte_carlo_tools.heston_mom import get_heston_moment
from monte_carlo_tools.get_garch_moments import get_mom_GARCH11

import numpy as np


def get_moments(model, X0, parameters, T, NStep):
    dt = T / NStep
    p = 0.05

    horizon = np.arange(0, T + dt, dt)

    if model == 0:  # ABM
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

    elif model == 1:  # CIR
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

    elif model == 2:  # DEJD
        mu = parameters[0]
        sigma = parameters[1]
        lambda_dedj = parameters[2]
        p = parameters[3]
        eta1 = parameters[4]
        eta2 = parameters[5]

        moments = np.zeros((len(horizon), 4))
        moments[:, 0] = (mu + lambda_dedj * (p / eta1 - (1 - p) / eta2)) * horizon  # mean
        moments[:, 1] = ((sigma * sigma + lambda_dedj * (
                p / eta1 ** 2 + (1 - p) / eta2 ** 2)) * horizon) ** 0.5  # std. dev.
        num_skewness = 6 * lambda_dedj * (p / eta1 ** 3 - (1 - p) / eta2 ** 3) * horizon
        moments[:, 2] = num_skewness / moments[:, 1] ** (3)  # skewness
        num_kurtosis = 24 * lambda_dedj * (p / eta1 ** 4 + (1 - p) / eta2 ** 4) * horizon
        moments[:, 3] = 3 + num_kurtosis / moments[:, 1] ** (4)  # kurtosis
        moments[0, 2] = 0
        moments[0, 3] = 3

        quantiles = np.zeros((len(horizon), 2))
        quantiles[:, 0] = moments[:, 0] + 5 * moments[:, 1]
        quantiles[:, 1] = moments[:, 0] - 5 * moments[:, 1]

    elif model == 3:  # EWMA
        mu = parameters[0]
        v0 = parameters[1]
        omega = parameters[2]
        alpha = parameters[3]
        beta = parameters[4]
        asymm = 0
        moments = get_mom_GARCH11(X0, mu, v0, omega, alpha, beta, asymm, T, NStep)

        # moments = [X0, 0, 0 3 moments ]
        quantiles = np.zeros((len(horizon), 2))
        quantiles[:, 0] = moments[:, 0] + 5 * moments[:, 1]
        quantiles[:, 1] = moments[:, 0] - 5 * moments[:, 1]

    elif model == 4:  # GARCH
        mu = parameters[0]
        v0 = parameters[1]
        omega = parameters[2]
        alpha = parameters[3]
        beta = parameters[4]
        asymm = parameters[5]
        moments = get_mom_GARCH11(X0, mu, v0, omega, alpha, beta, asymm, T, NStep)
        quantiles = np.zeros((len(horizon), 2))

        # moments = [X0, 0, 0 3 moments ]
        quantiles[:, 0] = moments[:, 0] + 5 * moments[:, 1]
        quantiles[:, 1] = moments[:, 0] - 5 * moments[:, 1]

    elif model == 5:  # GBM
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

    elif model == 6:  # Heston
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

    elif model == 7:  # MJD
        mu = parameters[0]
        sigma = parameters[1]
        lambda_mjd = parameters[2]
        mu_jumps = parameters[3]
        sg_jumps = parameters[4]

        moments = np.zeros((len(horizon), 4))
        moments[:, 0] = (mu + lambda_mjd * mu_jumps) * horizon  # mean
        moments[:, 1] = ((sigma * sigma + lambda_mjd * (mu_jumps ** 2 + sg_jumps ** 2)) * horizon) ** 0.5  # std. dev.
        numsk = lambda_mjd * mu_jumps * (mu_jumps ** 2 + 3 * sg_jumps ** 2) * horizon
        moments[:, 2] = numsk / moments[:, 1] ** 3  # skewness
        numk = lambda_mjd * (mu_jumps ** 4 + 6 * mu_jumps ** 2 * sg_jumps ** 2 + 3 * sg_jumps ** 4) * horizon
        moments[:, 3] = 3 + numk / moments[:, 1] ** 4  # kurtosis

        moments[0, 2] = 0
        moments[0, 3] = 3

        quantiles = np.zeros((len(horizon), 2))
        quantiles[:, 0] = moments[:, 0] + 5 * moments[:, 1]
        quantiles[:, 1] = moments[:, 0] - 5 * moments[:, 1]

    elif model == 8:  # MRG
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

    else:  # VG
        theta = parameters[0]
        sigma = parameters[1]
        kappa = parameters[2]
        moments = np.zeros((len(horizon), 4))

        moments[:, 0] = (theta) * horizon  # mean
        moments[:, 1] = ((sigma * sigma + theta * theta * kappa) * horizon) ** 0.5  # std. dev.
        num_skewness = (3 * sigma * sigma + 2 * theta * theta * kappa) * theta * kappa * horizon
        moments[:, 2] = num_skewness / moments[:, 1] ** (3)  # skewness
        num_kurtosis = (3 * sigma ** 4 + 12 * sigma * sigma * theta * theta * kappa + 6 * theta ** 4 * kappa * kappa) * kappa * horizon
        moments[:, 3] = 3 + num_kurtosis / moments[:, 1] ** (4)  # kurtosis
        moments[0, 2] = 0
        moments[0, 3] = 3
        quantiles = np.zeros((len(horizon), 2))
        quantiles[:, 0] = moments[:, 0] + 5 * moments[:, 1]
        quantiles[:, 1] = moments[:, 0] - 5 * moments[:, 1]

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
