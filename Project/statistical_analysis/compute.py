# -*- coding: utf-8 -*-
"""
Created on Mon Oct 28 22:22:28 2019

@author: Diego
"""
import os

import numpy as np
import pandas as pd
import scipy.stats


def upload_input(filename=None):
    data = pd.read_excel(os.path.join('uploads/', filename))
    return data


def compute_table(data):
    # dates = (data["Time"].tolist())

    del data['Time']
    tickers = list(data.columns.values)
    # data =data.T
    data_array = []

    for i in range(0, len(data)):
        data_array.append((np.array(data.loc[i])))

    prices = np.vstack(data_array)

    log_returns = []
    for i in range(0, len(prices) - 1):
        log_return = np.log(prices[i + 1] / prices[i])
        log_returns.append(log_return)

    log_returns = np.vstack(log_returns)

    m = []
    sg = []
    sg2 = []
    sk = []
    ku = []
    minr = []
    maxr = []
    jarque_bera_test_statistic = []

    for i in range(0, len(log_returns[0])):
        m.append(np.mean(log_returns[:, i]))

        sg.append(np.std(log_returns[:, i]))
        sg2.append(np.var(log_returns[:, i]))
        sk.append(scipy.stats.skew(log_returns[:, i]))
        ku.append(scipy.stats.kurtosis(log_returns[:, i]))
        minr.append(min(log_returns[:, i]))
        maxr.append(max(log_returns[:, i]))

    if len(log_returns) >= 2000:
        jb_statistic = []
        p_value = []
        for i in range(0, len(log_returns[0])):
            jarque_bera_test_statistic.append(scipy.stats.jarque_bera(log_returns[:, i]))

        for i in range(0, len(tickers)):
            x = jarque_bera_test_statistic[i]
            jb_statistic.append(x[0])
            p_value.append(x[1])

    else:
        jb_statistic = None
        p_value = None

    mean = m
    volatility = sg
    variance = sg2
    skewness = sk
    kurtosis = ku
    min_return = minr
    max_return = maxr

    return mean, volatility, variance, skewness, kurtosis, min_return, max_return, jb_statistic, p_value, tickers
