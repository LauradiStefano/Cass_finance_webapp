# -*- coding: utf-8 -*-
"""
Created on Mon Jul 22 10:57:25 2019

@author: Diego
"""
import numpy as np


# get_df_NelsonSiegel
# This function computes the Nelson-Siegel discount factors.


def get_df_NelsonSiegel(x, ttm):
    ttm = np.array(ttm)

    # Read in

    beta0 = x[0]
    beta1 = x[1]
    beta2 = x[2]
    tau1 = x[3]

    # Compute the spot rates

    spot = beta0 + beta1 * (1 - np.exp(-ttm / tau1)) * tau1 / ttm + beta2 * (
            (1 - np.exp(-ttm / tau1)) * tau1 / ttm - np.exp(-ttm / tau1))

    # Compute the discount factors

    df = np.exp(-spot * ttm)

    if ttm[0] == 0:
        df[0] = 1

    return df
