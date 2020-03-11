# -*- coding: utf-8 -*-
"""
Created on Fri Nov  1 20:10:49 2019

@author: Diego
"""

import datetime as dt
import os

import numpy as np
import pandas as pd
import pandas_datareader.data as web
import scipy.stats


def import_dataset_file_excel(filename):
    data = pd.read_excel(os.path.join('uploads/', filename))
    del data['Time']

    return data


def import_dataset_tickers(tickers, start_day, start_month, start_year, end_day, end_month, end_year):
    start = dt.datetime(start_year, start_month, start_day)
    end = dt.datetime(end_year, end_month, end_day)

    data = pd.DataFrame()
    nature = type(tickers)

    # questo è da fare su controller
    if nature == str:
        tickers = [tickers]
    # for i in range(0, len(tickers)):
    for i in range(0, len(tickers)):
        df = web.DataReader(tickers[i], 'yahoo', start, end)
        price = df['Adj Close']
        # price = np.vstack(adj_close)
        data.insert(i, tickers[i], price, True)

    data = data.reset_index()
    del data['Date']

    return data


def compute_table(data):
    # dates = (data["Time"].tolist())

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
    # m = ['Mean']
    # sg = ['Standard Deviation']
    # sg2= ['Variance']
    # sk = ['Skewness']
    # ku = ['Kurtosis']
    # minr = ['Min log returns']
    # maxr = ['Max log returns']

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
 
    n_observations = []

    for i in range(0, len(tickers)):
        observations = len(log_returns[:, i])
        n_observations.append(observations)


    mean = m
    volatility = sg
    variance = sg2
    skewness = sk
    kurtosis = ku
    min_return = minr
    max_return = maxr
    print("type",type(m))
    return mean, volatility, variance, skewness, kurtosis, min_return, max_return, jb_statistic, p_value, tickers #,n_observations
