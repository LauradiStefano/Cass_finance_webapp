# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 23:48:26 2019

@author: Diego
"""

import os

import bokeh.plotting as bp
import numpy as np
import pandas as pd
from bokeh.models import HoverTool
from bokeh.palettes import brewer
from bokeh.plotting import *
from scipy.optimize import minimize

from portfolio_analysis.useful_functions import sumweigth, expret, variance, random_portfolio


def upload_input(filename=None):
    data = pd.read_excel(os.path.join('uploads/', filename))

    tickers = list(data.columns.values)
    data_array = []

    for i in range(0, len(data)):
        data_array.append((np.array(data.loc[i])))

    prices = np.vstack(data_array)

    log_returns = []
    for i in range(0, len(prices) - 1):
        log_return = np.log(prices[i + 1] / prices[i])
        log_returns.append(log_return)

    return_vec = np.vstack(log_returns)
    return_vec = np.ndarray.transpose(return_vec)
    n_assets = len(tickers)

    return return_vec, n_assets, tickers


def compute_efficient_frontier(return_vec, n_assets, n_portfolios):
    n_portf_eff = int(n_portfolios / 10)

    means, stds = np.column_stack([
        random_portfolio(return_vec)
        for _ in
        range(n_portfolios)])  # compute different number of means and variances for number of random portfolio computed

    Sigma = np.cov(return_vec)
    MeanV = np.mean(return_vec, axis=1)
    x0 = np.ones(n_assets) / n_assets

    # COMPUTE BOUNDS OF WEIGHTS
    bnds = tuple(np.c_[np.zeros((n_assets, 1)), np.ones((n_assets, 1))])

    con1 = ({'type': 'eq', 'fun': sumweigth})
    con = ([con1])
    res = minimize(variance, x0, args=(Sigma,), method='SLSQP', options={'xtol': 1e-8, 'disp': True}, constraints=con,
                   bounds=bnds)
    mintarget = expret(res.x, MeanV, 0)
    maxtarget = np.max(MeanV)

    target = np.linspace(mintarget, maxtarget, n_portf_eff)

    mintarget = expret(res.x, MeanV, 0)

    feff = np.array([[res.fun], [mintarget]])
    feffweights = np.array(res.x)

    j = 0
    for extarget in target:
        con2 = ({'type': 'eq', 'fun': expret, 'args': (MeanV, extarget,)})
        con = ([con1, con2])
        x0 = res.x
        res = minimize(variance, x0, args=(Sigma,), method='SLSQP', options={'xtol': 1e-8, 'disp': True},
                       constraints=con, bounds=bnds)
        feff = np.c_[feff, [[res.fun], [extarget]]]
        feffweights = np.r_[feffweights, res.x]

        j = j + 1

    # DELETE THE FIRST SOLUTION
    feff = feff[:, 1:n_portf_eff + 1]
    feffweights = feffweights[n_assets:, ]
    feffweights = feffweights.reshape(n_portf_eff, n_assets)

    EFstds = feff[0, :] ** 0.5
    EFmeans = feff[1, :]

    standard_deviations = stds  # deviazioni standard portafogli randomici
    ef_standard_deviations = EFstds  # deviazioni standard dei portafogli efficienti
    ef_means = EFmeans  # valori attesi dei portafogli efficienti

    return standard_deviations, means, ef_means, ef_standard_deviations, feffweights


def create_plot_efficient_frontier(return_vec, standard_deviations, means, ef_means, ef_standard_deviations):
    ticker_means = np.mean(return_vec, axis=1)
    ticker_standard_deviations = np.std(return_vec, axis=1)

    data_efficient = ColumnDataSource(data=dict(
        ef_means=ef_means,
        ef_standard_deviations=ef_standard_deviations))

    data_randomize = ColumnDataSource(data=dict(
        means=means,
        standard_deviations=standard_deviations))

    data_ticker = ColumnDataSource(data=dict(
        ticker_means=ticker_means,
        ticker_standard_deviations=ticker_standard_deviations))

    hover_data_efficient = HoverTool(attachment="above", names=['efficient portfolios'],
                                     tooltips=[("Eff Std", "@ef_standard_deviations"),
                                               ("Eff Means", "@ef_means")])

    hover_data_randomize = HoverTool(attachment="below", names=['data random'],
                                     tooltips=[("Std", "@standard_deviations"), ("Means", "@means")])

    hover_data_ticker = HoverTool(attachment="below", names=['data ticker'],
                                  tooltips=[("Ticker Std", "@ticker_standard_deviations"),
                                            ("Ticker Mean", "@ticker_means")])

    y_range = [min(min(ticker_means), min(means), min(ef_means)) * 1.05,
               max(max(ticker_means), max(means), max(ef_means)) * 1.05]
    x_range = [min(min(ticker_standard_deviations), min(ef_standard_deviations), min(standard_deviations)) * 0.95,
               max(max(ticker_standard_deviations), max(ef_standard_deviations), max(standard_deviations)) * 1.05]

    fig = bp.figure(
        tools=['save, pan, box_zoom, reset, crosshair', hover_data_efficient, hover_data_randomize, hover_data_ticker],
        x_range=x_range, y_range=y_range, sizing_mode='scale_both', toolbar_location="right",
        x_axis_label='Standard Deviation', y_axis_label=' Mean')

    fig.circle(x='standard_deviations', y='means', source=data_randomize, legend="Random Port",
               color="#0095B6", size=5, name='data random')

    fig.circle(x='ef_standard_deviations', y='ef_means', source=data_efficient, legend="Efficient Port",
               color="#2F2F2F", size=6, name='efficient portfolios')

    fig.circle(x='ticker_standard_deviations', y='ticker_means', source=data_ticker,
               legend="Mean and Std Single Asset", color="#D21F1B", size=6, alpha=0.7, name='data ticker')

    fig.toolbar.active_drag = None
    fig.legend.location = "bottom_left"
    fig.legend.click_policy = "hide"

    from bokeh.embed import components
    script, div = components(fig)

    return script, div


def create_plot_efficient_weights(ef_means, feffweights, tickers):
    # N = len(ef_means)
    # feffweights = eff_weights
    df = pd.DataFrame(feffweights, columns=tickers)

    # df = pd.DataFrame(feffweights).add_prefix('y')
    df.index = ef_means

    df_top = df.cumsum(axis=1)
    # df_bottom = df_top.shift(axis=1).fillna({'y0': 0})[::-1]
    df_bottom = df_top.shift(axis=1).fillna({tickers[0]: 0})[::-1]

    df_stack = pd.concat([df_bottom, df_top], ignore_index=True)

    areas = df_stack
    x2 = np.hstack((df.index[::-1], df.index))

    colors = brewer['Blues'][areas.shape[1]]

    x_range = [min(ef_means), max(ef_means)]
    y_range = [0, 1]

    fig = bp.figure(tools=['save, pan, box_zoom, reset, crosshair'], x_range=x_range, y_range=y_range,
                    sizing_mode='scale_both', toolbar_location="right", x_axis_label='Portfolio Returns',
                    y_axis_label='Efficient Weights')

    fig.grid.minor_grid_line_color = '#eeeeee'

    # names = ["y%d" % i for i in range(N)]

    for a, area in enumerate(areas):
        fig.patch(x2, areas[area], color=colors[a], legend=area, alpha=0.8, line_color=None)

    fig.toolbar.active_drag = None
    fig.legend.location = "bottom_left"
    fig.legend.click_policy = "hide"

    from bokeh.embed import components
    script, div = components(fig)

    return script, div
