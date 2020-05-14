# -*- coding: utf-8 -*-
"""
Created on Mon May  4 17:08:56 2020

@author: Diego
"""
import os
import datetime as dt
import numpy as np
import pandas as pd
import pandas_datareader.data as web

from bokeh.models import ColumnDataSource
from bokeh.palettes import Spectral6
from bokeh.plotting import figure
from bokeh.transform import factor_cmap


def import_dataset_file_excel(filename, price_or_return):
    data = pd.read_excel(os.path.join('uploads/', filename))
    if price_or_return == 1:
        tickers = list(data.columns.values)
        data_array = []

        for i in range(0, len(data)):
            data_array.append((np.array(data.loc[i])))

        prices = np.vstack(data_array)

        log_returns = []
        for i in range(0, len(prices) - 1):
            log_return = np.log(prices[i + 1] / prices[i])
            log_returns.append(log_return)

        returns = np.vstack(log_returns)

    else:
        tickers = list(data.columns.values)
        data_array = []
        for i in range(0, len(data)):
            data_array.append((np.array(data.loc[i])))

        returns = np.vstack(data_array)

    covariance_matrix = np.cov(returns.T)
    D, A = np.linalg.eig(covariance_matrix)

    autovect = A
    evalues = sorted(D, reverse=True)

    return evalues, autovect


# Permette di calcolare la matrice varianza covarianza importando i prezzi di chiusura da Yahoo

def import_dataset_tickers(tickers, start_day, start_month, start_year, end_day, end_month, end_year):
    start = dt.datetime(start_year, start_month, start_day)
    end = dt.datetime(end_year, end_month, end_day)

    data = pd.DataFrame()
    for i in range(0, len(tickers)):
        df = web.DataReader(tickers[i], 'yahoo', start, end)
        price = df['Adj Close']

        data.insert(i, tickers[i], price, True)

    data = data.reset_index()
    # dates = data['Date'].tolist()
    del data['Date']
    tickers = list(data.columns.values)

    data_array = []
    for i in range(0, len(data)):
        data_array.append((np.array(data.loc[i])))

    prices = np.vstack(data_array)

    log_returns = []
    for i in range(0, len(prices) - 1):
        log_return = np.log(prices[i + 1] / prices[i])
        log_returns.append(log_return)

    log_returns = np.vstack(log_returns)
    covariance_matrix = np.cov(log_returns.T)

    D, A = np.linalg.eig(covariance_matrix)

    evalues = D
    autovect = A

    return evalues, autovect


# def funzione che permette di calcolare gli evalues nel terzo caso di import


def create_plot_variance_component(evalues):
    len_tickers = len(evalues)
    tickers = [str(i) for i in range(len_tickers)]
    percentage = evalues / sum(evalues) * 100

    data = ColumnDataSource(data=dict(
        tickers=tickers,
        percentage=percentage))

    fig = figure(x_range=tickers, plot_height=350, toolbar_location=None,
                 title="Percentage Variance explained by each Component")
    fig.xaxis.axis_label = 'Ticker'
    fig.yaxis.axis_label = 'Percentage'
    fig.vbar(x='tickers', top='percentage', width=0.9, source=data, legend_field="tickers",
             line_color='white', fill_color=factor_cmap('tickers', palette=Spectral6, factors=tickers))

    fig.xgrid.grid_line_color = None
    fig.y_range.start = 0
    fig.y_range.end = 140
    fig.legend.orientation = "horizontal"
    fig.legend.location = "top_center"

    from bokeh.embed import components
    script, div = components(fig)

    return script, div


def create_plot_cumulative_component(evalues):
    len_tickers = len(evalues)
    tickers = [str(i) for i in range(len_tickers)]
    percentage = np.cumsum(evalues / sum(evalues) * 100)

    source = ColumnDataSource(data=dict(tickers=tickers, percentage=percentage))

    fig = figure(x_range=tickers, plot_height=350, toolbar_location=None,
                 title="Cumulative Percentage Variance Explained")
    fig.xaxis.axis_label = 'Ticker'
    fig.yaxis.axis_label = 'Percentage'

    fig.vbar(x='tickers', top='percentage', width=0.9, source=source, legend_field="tickers",
             line_color='white', fill_color=factor_cmap('tickers', palette=Spectral6, factors=tickers))

    fig.xgrid.grid_line_color = None
    fig.y_range.start = 0
    fig.y_range.end = 140
    fig.legend.orientation = "horizontal"
    fig.legend.location = "top_center"
    # fig.toolbar.active_drag = None
    # fig.legend.location = "bottom_right"

    from bokeh.embed import components
    script, div = components(fig)

    return script, div


def create_plot_one_loadings(autovect):
    pca_one = autovect[:, 0]

    tickers = [str(i) for i in range(len(pca_one))]

    source = ColumnDataSource(data=dict(
        tickers=tickers, pca_one=pca_one
    ))

    fig = figure(x_range=tickers, plot_height=350, toolbar_location=None, title="Loadings with respect the 1 st PC")
    fig.xaxis.axis_label = 'Ticker'
    fig.yaxis.axis_label = 'Percentage'

    fig.vbar(x='tickers', top='pca_one', width=0.9, source=source, legend_field="tickers",
             line_color='white', fill_color=factor_cmap('tickers', palette=Spectral6, factors=tickers))

    fig.xgrid.grid_line_color = None
    fig.y_range.start = -1
    fig.y_range.end = 1
    fig.legend.orientation = "horizontal"
    fig.legend.location = "top_center"
    # fig.toolbar.active_drag = None
    # fig.legend.location = "bottom_right"

    from bokeh.embed import components
    script, div = components(fig)

    return script, div


def create_plot_two_loadings(autovect):
    pca_one = autovect[:, 1]

    tickers = [str(i) for i in range(len(pca_one))]

    source = ColumnDataSource(data=dict(
        tickers=tickers, pca_one=pca_one
    ))

    fig = figure(x_range=tickers, plot_height=350, toolbar_location=None, title="Loadings with respect the 1 st PC")
    fig.xaxis.axis_label = 'Ticker'
    fig.yaxis.axis_label = 'Percentage'

    fig.vbar(x='tickers', top='pca_one', width=0.9, source=source, legend_field="tickers",
             line_color='white', fill_color=factor_cmap('tickers', palette=Spectral6, factors=tickers))

    fig.xgrid.grid_line_color = None
    fig.y_range.start = -1
    fig.y_range.end = 1
    fig.legend.orientation = "horizontal"
    fig.legend.location = "top_center"
    # fig.toolbar.active_drag = None
    # fig.legend.location = "bottom_right"

    from bokeh.embed import components
    script, div = components(fig)

    return script, div