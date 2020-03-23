# -*- coding: utf-8 -*-
"""
Created on Fri Nov  1 20:10:49 2019

@author: Diego
"""

import datetime as dt
import os

import bokeh.plotting as bp
import numpy as np
import pandas as pd
import pandas_datareader.data as web
import scipy.stats
import scipy.stats
from bokeh.models import ColumnDataSource
from bokeh.models import HoverTool


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
    return mean, volatility, variance, skewness, kurtosis, min_return, max_return, jb_statistic, p_value, tickers, \
           n_observations, log_returns,


def create_histogram_distribution_plot(log_returns):
    hist, edges = np.histogram(log_returns, density=True, bins=100)
    m = np.mean(log_returns)
    sg = np.std(log_returns)
    log_returns.sort(reverse=False)
    normal_pdf = lambda x: scipy.stats.norm.pdf(x, m, sg)
    norm_pdf = [normal_pdf(i) for i in log_returns]  # aggiungere all'output

    # log_returns.sort(reverse = False)

    data = ColumnDataSource(data=dict(
        hist=hist,
        edges_left=edges[:-1],
        edges_right=edges[1:],
        log_returns=log_returns,
        norm_pdf=norm_pdf
    ))

    hover_histogram = HoverTool(attachment="above", names=['histogram'],
                                tooltips=[("Edges", "@edges"),
                                          ("Hist", "@histogram")])

    hover_theoretical = HoverTool(attachment="above", names=['discount factor'],
                                  tooltips=[("Log Returns", "@log returns"),
                                            ("Norm Pdf", "@norm pdf")])

    fig = bp.figure(tools=['save, pan, box_zoom, reset, crosshair', hover_histogram, hover_theoretical],
                    sizing_mode='scale_both', toolbar_location="right", x_axis_label='Series of Data',
                    y_axis_label='Model Error Discount Factor')

    fig.quad(top='hist', bottom=0, left='edges_left', right='edges_right', source=data,
             color="#0095B6", line_color="#ffffff", alpha=1, name='Histogram Log Returns')

    fig.line(x='log_returns', y='norm_pdf', source=data, color="#D21F1B", legend='Log returns PDF',
             line_width=1, alpha=1, name='Theoretical Distribution')

    fig.toolbar.active_drag = None

    from bokeh.embed import components
    script, div = components(fig)

    return script, div


def create_qq_plot(log_returns):
    (x, empirical_distr), (slope, inter, cor) = scipy.stats.probplot(log_returns, dist="norm")  # , plot=pylab)

    theoretical_quantiles = x
    # osmf = x.take([0, -1])  # endpoints
    normal_distr = slope * theoretical_quantiles + inter

    # normal_empirical = qq_plot_data[0]
    # teoretical_quantiles = normal_empirical[0]
    # empirical_distr = normal_empirical[1]

    data = ColumnDataSource(data=dict(
        theoretical_quantiles=theoretical_quantiles,
        normal_distr=normal_distr,
        empirical_distr=empirical_distr
    ))

    hover_normal = HoverTool(attachment="above", names=['Normal Distr'],
                             tooltips=[("Theoretical Quantiles", "@theoretical_quantiles"),
                                       ("Normal Distr", "@normal_distr")])

    hover_empirical = HoverTool(attachment="below", names=['model spot rate'],
                                tooltips=[("Theoretical Quantiles", "@theoretical_quantiles"),
                                          ("Empirical Distr", "@empirical_distr")])

    x_range = [min(theoretical_quantiles) - 1, max(theoretical_quantiles) + 1]
    y_range = [min(empirical_distr) - 0.02, max(empirical_distr) + 0.02]

    fig = bp.figure(tools=['save, pan, box_zoom, reset, crosshair', hover_empirical, hover_normal], x_range=x_range,
                    y_range=y_range, sizing_mode='scale_both', toolbar_location="right",
                    x_axis_label='Quantiles', y_axis_label=' Distribution')

    fig.circle(x='theoretical_quantiles', y='empirical_distr', source=data, color="#0095B6",
               legend='Empirical Distribution',
               size=6, name='Normal Distribution')

    fig.line(x='theoretical_quantiles', y='normal_distr', source=data, color="#D21F1B", legend='Normal Distribution',
             line_width=4, alpha=0.8, name='Empirical Distr')

    fig.toolbar.active_drag = None
    fig.legend.location = "bottom_right"

    from bokeh.embed import components
    script, div = components(fig)

    return fig, div


# def plot_log_returns(log_returns, dates):
#     del dates[0]
#     data = ColumnDataSource(data=dict(
#         dates=dates,
#         log_returns=log_returns,
#     ))
#
#     hover_normal = HoverTool(attachment="above", names=['Normal Distr'],
#                              tooltips=[("teoretical quantiles", "@dates"), ("Normal Distr", "@log_returns")])
#
#     hover_empirical = HoverTool(attachment="below", names=['model spot rate'],
#                                 tooltips=[("teoretical quantiles", "@dates"), ("Empirical Distr", "@empirical_distr")])
#
#     x_range = [min(dates), max(dates)]
#     y_range = [min(log_returns) - 0.01, max(log_returns) + 0.01]
#
#     fig = bp.figure(tools=['save, pan, box_zoom, reset, crosshair', hover_empirical, hover_normal], x_range=x_range,
#                     y_range=y_range, sizing_mode='scale_both', toolbar_location="right",
#                     x_axis_label='Time',
#                     y_axis_label=' Log Returns')
#
#     fig.line(x='dates', y='log_returns', source=data, color="navy", legend='Log returns vs Dates', line_width=0.1,
#              alpha=0.1, name='Log_Returns')
#
#     fig.toolbar.active_drag = None
#     fig.legend.location = "bottom_right"
#
#     from bokeh.embed import components
#     script, div = components(fig)
#
#     return fig, div
