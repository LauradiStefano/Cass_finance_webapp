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
import bokeh.plotting as bp

from bokeh.models import ColumnDataSource, BoxAnnotation
from bokeh.palettes import Blues9
from bokeh.transform import factor_cmap


def import_dataset_file_excel(filename, price_or_return, cov_or_corr):
    data = pd.read_excel(os.path.join('uploads/', filename))
    price_or_return = int(price_or_return)
    tickers = list(data.columns.values)

    data_array = []
    for i in range(0, len(data)):
        data_array.append((np.array(data.loc[i])))
    prices = np.vstack(data_array)

    if price_or_return == 0:  # log returns
        log_returns = []
        for i in range(0, len(prices) - 1):
            log_return = np.log(prices[i + 1] / prices[i])
            log_returns.append(log_return)

        returns = np.vstack(log_returns)

    elif price_or_return == 1:  # percentage returns
        percentage_returns = []
        for i in range(0, len(prices) - 1):
            percentage_return = (prices[i + 1] - prices[i]) / prices[i]
            percentage_returns.append(percentage_return)

        returns = np.vstack(percentage_returns)

    elif price_or_return == 2:  # changes
        changes = []
        for i in range(0, len(prices) - 1):
            change = prices[i + 1] - prices[i]
            changes.append(change)
        returns = np.vstack(changes)

    else:

        returns = prices

    cov_or_corr = int(cov_or_corr)

    if cov_or_corr == 0:  # use covariance matrix
        covariance_matrix = np.cov(returns.T)
        D, A = np.linalg.eig(covariance_matrix)

    else:  # use corr coef
        correlation_matrix = np.corrcoef(returns.T)
        D, A = np.linalg.eig(correlation_matrix)

    autovect = A
    evalues = sorted(D, reverse=True)
    evalues = np.array(evalues)

    pc_terms = []
    for i in range(1, len(evalues) + 1):
        z = "pc" + str(i)
        pc_terms.append(z)

    # pc_terms = np.array(pc_terms)

    return evalues, autovect, pc_terms


# Permette di calcolare la matrice varianza covarianza importando i prezzi di chiusura da Yahoo

def import_dataset_tickers(tickers, start_day, start_month, start_year, end_day,
                           end_month, end_year, price_or_return, cov_or_corr):
    price_or_return = int(price_or_return)
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

    if price_or_return == 0:  # log returns
        log_returns = []
        for i in range(0, len(prices) - 1):
            log_return = np.log(prices[i + 1] / prices[i])
            log_returns.append(log_return)
        returns = np.vstack(log_returns)

    elif price_or_return == 1:  # percentage returns
        percentage_returns = []
        for i in range(0, len(prices) - 1):
            percentage_return = (prices[i + 1] - prices[i]) / prices[i]
            percentage_returns.append(percentage_return)
        returns = np.vstack(percentage_returns)

    elif price_or_return == 2:  # changes
        changes = []
        for i in range(0, len(prices) - 1):
            change = prices[i + 1] - prices[i]
            changes.append(change)

        returns = np.vstack(changes)

    else:  # prices
        returns = prices

    cov_or_corr = int(cov_or_corr)

    if cov_or_corr == 0:  # use covariance matrix
        covariance_matrix = np.cov(returns.T)
        D, A = np.linalg.eig(covariance_matrix)

    else:  # use corr coef
        correlation_matrix = np.corrcoef(returns.T)
        D, A = np.linalg.eig(correlation_matrix)

    evalues = sorted(D, reverse=True)
    evalues = np.array(evalues)
    autovect = A

    pc_terms = []
    for i in range(1, len(evalues) + 1):
        z = "pc" + str(i)
        pc_terms.append(z)

    # pc_terms = np.array(pc_terms)

    return evalues, autovect, pc_terms


# def funzione che permette di calcolare gli evalues nel terzo caso di import


def create_plot_variance_component(evalues, desired_explained_variance):
    len_tickers = len(evalues)
    tickers = [str(i) for i in range(len_tickers)]
    percentage = evalues / sum(evalues) * 100

    data = ColumnDataSource(data=dict(
        tickers=tickers,
        percentage=percentage))

    x_range = tickers
    y_range = [0, 140]

    fig = bp.figure(tools=['save, pan, box_zoom, reset, crosshair'], x_range=x_range, y_range=y_range,
                    sizing_mode='scale_both', toolbar_location="right", x_axis_label='Principal Component',
                    y_axis_label='Percentage')

    desired_variance = BoxAnnotation(bottom=0, top=desired_explained_variance * 100, fill_color='#0095B6',
                                     fill_alpha=0.1)
    fig.add_layout(desired_variance)

    fig.vbar(x='tickers', top='percentage', width=0.9, alpha=0.8, source=data, line_color='#FFFFFF')

    fig.xgrid.grid_line_color = None
    # fig.legend.orientation = "horizontal"
    # fig.legend.location = "top_left"
    fig.toolbar.active_drag = None

    from bokeh.embed import components
    script, div = components(fig)

    return script, div


def create_plot_cumulative_component(evalues, desired_explained_variance):
    len_tickers = len(evalues)
    tickers = [str(i) for i in range(len_tickers)]
    percentage = np.cumsum(evalues / sum(evalues) * 100)

    data = ColumnDataSource(data=dict(
        tickers=tickers,
        percentage=percentage
    ))

    x_range = tickers
    y_range = [0, 140]

    fig = bp.figure(tools=['save, pan, box_zoom, reset, crosshair'], x_range=x_range, y_range=y_range,
                    sizing_mode='scale_both', toolbar_location="right", x_axis_label='Principal Component',
                    y_axis_label='Percentage')

    fig.vbar(x='tickers', top='percentage', width=0.9, alpha=0.8, source=data, line_color='#FFFFFF')

    desired_variance = BoxAnnotation(bottom=0, top=desired_explained_variance * 100, fill_color='#0095B6',
                                     fill_alpha=0.1)
    fig.add_layout(desired_variance)

    fig.xgrid.grid_line_color = None
    fig.toolbar.active_drag = None

    from bokeh.embed import components
    script, div = components(fig)

    return script, div


def create_plot_one_loadings(autovect):
    pca_one = autovect[:, 0]

    tickers = [str(i) for i in range(len(pca_one))]

    data = ColumnDataSource(data=dict(
        tickers=tickers, pca_one=pca_one
    ))

    x_range = tickers
    y_range = [-1, 1]

    fig = bp.figure(tools=['save, pan, box_zoom, reset, crosshair'], x_range=x_range, y_range=y_range,
                    sizing_mode='scale_both', toolbar_location="right", x_axis_label='Asset',
                    y_axis_label='Loading')

    fig.vbar(x='tickers', top='pca_one', width=0.9, alpha=0.8, source=data, line_color='#FFFFFF')

    fig.xgrid.grid_line_color = None
    fig.toolbar.active_drag = None

    from bokeh.embed import components
    script, div = components(fig)

    return script, div


def create_plot_two_loadings(autovect):
    pca_one = autovect[:, 1]

    tickers = [str(i) for i in range(len(pca_one))]

    data = ColumnDataSource(data=dict(
        tickers=tickers, pca_one=pca_one
    ))

    x_range = tickers
    y_range = [-1, 1]

    fig = bp.figure(tools=['save, pan, box_zoom, reset, crosshair'], x_range=x_range, y_range=y_range,
                    sizing_mode='scale_both', toolbar_location="right", x_axis_label='Asset',
                    y_axis_label='Loading')

    fig.vbar(x='tickers', top='pca_one', width=0.9, alpha=0.8, source=data, line_color='#FFFFFF')

    fig.xgrid.grid_line_color = None
    fig.toolbar.active_drag = None

    from bokeh.embed import components
    script, div = components(fig)

    return script, div
