# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 23:48:26 2019

@author: Diego
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 22:02:29 2019

@author: Diego
"""

import bokeh.plotting as bp
import numpy as np
import pandas as pd
from bokeh.models import HoverTool
from bokeh.plotting import ColumnDataSource
from scipy.optimize import minimize

from portfolio_analysis.useful_functions import sumweigth, expret, variance, random_portfolio


# ------------------------------------------------------------------------------
# INPUTS
# n_portfolios = come valore di default va bene 100
# il file xlsx con tanti colonne quanti sono i titoli in portafoglio

# OUTPUT
# genera portafogli casuali con peso totale =1 (no vendite allo scoperto)
# calcola portafogli ottimali (numero di combinazioni calcolate n_portfolios/10)
# target minimo =0 (portafoglio efficente con media minore)
# target massimo = valore atteso massimo tra i singoli titoli(portafoglio efficiente con media maggiore)
# ------------------------------------------------------------------------------

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

    return return_vec, n_assets


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

    return return_vec, standard_deviations, means, ef_means, ef_standard_deviations


def plot_efficient_frontier(return_vec, standard_deviations, means, ef_means, ef_standard_deviations):
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

    hover_data_efficient = HoverTool(attachment="above", names=['efficient combination'],
                                     tooltips=[("ef_standard_deviations", "@ef_standard_deviations"),
                                               ("ef_means", "@ef_means")])

    hover_data_randomize = HoverTool(attachment="below", names=['model spot rate'],
                                     tooltips=[("standard_deviations", "@standard_deviations"), ("means", "@means")])

    hover_data_ticker = HoverTool(attachment="below", names=['model spot rate'],
                                  tooltips=[("ticker_standard_deviations", "@ticker_standard_deviations"),
                                            ("ticker_means", "@ticker_means")])

    y_range = [min(ticker_means), max(ticker_means)]
    x_range = [min(ef_standard_deviations) - min(ef_standard_deviations) * 0.05, max(ticker_standard_deviations)]

    fig = bp.figure(
        tools=['save, pan, box_zoom, reset, crosshair', hover_data_efficient, hover_data_randomize, hover_data_ticker],
        x_range=x_range, y_range=y_range, sizing_mode='scale_both', toolbar_location="right",
        x_axis_label='Standard Deviation', y_axis_label=' Mean')

    fig.circle(x='ef_standard_deviations', y='ef_means', source=data_efficient, color="orange",
               legend='Efficient Portfolios', size=6, name='efficient portfolios')

    fig.circle(x='standard_deviations', y='means', source=data_randomize, color="green",
               legend='Random Generated Portfolios', size=6,
               name='Random Generated Portfolios')

    fig.circle(x='ticker_standard_deviations', y='ticker_means', source=data_ticker, color="blue",
               legend='Mean amd standard deviation single asset', size=6,
               name='Mean and Standard Deviation (single asset)')

    fig.toolbar.active_drag = None
    fig.legend.location = "bottom_right"

    from bokeh.embed import components
    script, div = components(fig)

    return script
