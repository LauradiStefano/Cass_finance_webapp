# -*- coding: utf-8 -*-
"""
Created on Mon Aug  5 15:32:31 2019

@author: Diego
"""
import numpy as np

from term_structure.get_df_CIR import get_df_CIR


# fit_df_CIR
# This function computes the SSE for the CIR model. 

def fit_df_CIR(x, data, flag1, flag2):
    # Compute the SSE

    T = np.array(data["Maturity"].tolist())
    market_discount_factor = np.array(data["Discount Factor"].tolist())
    df = get_df_CIR(x, T)

    if flag1 == 0:

        if flag2 == 0:

            spotmkt = -np.log(market_discount_factor) / T
            spot = -np.log(df) / T
            f = spotmkt - spot

        else:  # flag2 == 1

            f = market_discount_factor - df

    else:  # flag1 == 1

        if x[0] <= 0 or x[1] <= 0 or x[2] <= 0 or x[3] <= 0:
            f = 10 ^ 15

        else:

            if flag2 == 0:

                spotmkt = -np.log(market_discount_factor) / T
                spot = -np.log(df) / T
                f = np.sum((spotmkt - spot) ** 2)

            else:  # flag2 == 1

                f = sum((market_discount_factor - df) ** 2)

    return f
