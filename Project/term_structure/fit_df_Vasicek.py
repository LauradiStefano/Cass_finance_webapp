# -*- coding: utf-8 -*-
"""
Created on Tue Jul 30 14:13:01 2019

@author: Diego
"""
import numpy as np
from term_structure.get_df_Vasicek import get_df_Vasicek

# fit_df_Vasicek
# This function computes the SSE for the Vasicek model. 


def fit_df_Vasicek(x, data, flag1, flag2):

    ## Compute the SSE

    T = np.array(data["Maturity"].tolist())

    df = get_df_Vasicek(x, T)  # input parameters and maturities : output Vasi
    market_discount_factor = np.array(data["Discount Factor"].tolist())

    if flag1 == 0:  # solve non linear least squares problems

        if flag2 == 0:  # spot rate

            spotmkt = -np.log(market_discount_factor) / T
            spot = -np.log(df) / T
            f = spotmkt - spot

        else:  # flag2 == 1  discount factor

            dfmkt = market_discount_factor
            f = dfmkt - df

    else:  # flag2 == 1

        if x[0] <= 0 or x[1] <= 0 or x[2] <= 0 or x[3] <= 0:
            f = 10 ^ 15

        else:

            if flag2 == 0:

                spotmkt = -np.log(market_discount_factor) / T
                spot = -np.log(df) / T
                f = np.sum((spotmkt - spot) ** 2)

            else:  # flag2 == 1

                f = np.sum((market_discount_factor - df) ** 2)

    return f
