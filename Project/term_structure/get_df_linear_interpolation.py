# -*- coding: utf-8 -*-
"""
Created on Mon Jul 22 11:04:35 2019

@author: Diego
"""
import numpy as np


# get_df_linear_interpolation
# This function returns the riskless discount factors corresponding
# to a given  vector of time to maturity (in years), by linear interpolation
# of the spot rates.


def get_df_linear_interpolation(data_df, time):

    # Compute discount factors

    if data_df[0, 0] == 0:
        data_df = np.delete(data_df, 0, axis=0)

    T = data_df[:, 0]
    log_value = -np.log(data_df[:, 1]) / T
    y = np.interp(time, T, log_value)  # np.delete(time, (0), axis=0)
    df = np.exp(-y * time)

    if time[0] == 0:
        df[0] = 1

    return df
