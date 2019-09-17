# -*- coding: utf-8 -*-
"""
Created on Wed Jul 31 17:46:28 2019

@author: Diego
"""
import numpy as np

# fit_df_Svensson
# This function computes the SSE for the Svensson model.


def fit_df_Svensson(x, data, flag1, flag2):

    # Compute the SSE

    T = np.array(data["Maturity"].tolist())
    market_discount_factor = np.array(data["Discount Factor"].tolist())

    beta0 = x[0]
    beta1 = x[1]
    beta2 = x[2]
    beta3 = x[3]
    tau1 = x[4]
    tau2 = x[5]

    spot = beta0 + beta1 * (1 - np.exp(-T / tau1)) * tau1 / T + beta2 * (
                (1 - np.exp(-T / tau1)) * tau1 / T - np.exp(-T / tau1)) + beta3 * (
                       (1 - np.exp(-T / tau2)) * tau2 / T - np.exp(-T / tau2))

    if flag1 == 0:

        if flag2 == 0:

            spotmkt = -np.log(market_discount_factor) / T
            f = spotmkt - spot

        else:  # flag2 == 1

            df = np.exp(-T * spot)
            f = market_discount_factor - df

    else:  # flag2 == 1

        if beta0 <= 0 or beta0 + beta1 <= 0 or tau1 <= 0 or tau2 <= 0:
            f = 10 ^ 15

        else:

            if flag2 == 0:

                spotmkt = -np.log(market_discount_factor) / T
                f = np.sum((spotmkt - spot) ** 2)

            else:  # flag2 == 1

                df = np.exp(-T * spot)
                f = np.sum((market_discount_factor - df) ** 2)

    return f
