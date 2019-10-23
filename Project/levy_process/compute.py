# -*- coding: utf-8 -*-
"""
Created on Tue Apr 16 09:49:53 2019

@author: Diego
"""

import bokeh.plotting as bp
import numpy as np
from bokeh.models import HoverTool
from bokeh.plotting import ColumnDataSource
from scipy.stats import norm

from levy_process.get_COS_bounds import get_COS_bounds
from levy_process.get_COSprices import get_cos_prices
from levy_process.get_moments import compute_moments
from levy_process.get_pdf_cos import get_pdf_cos
from levy_process.getbs import find_vol


def select_parameters(type_choice, mu, sigma_normal, sigma_vg, kappa_vg, theta_vg, sigma_nig, kappa_nig, theta_nig, c,
                      g, m, y):
    type_choice = int(type_choice)
    if type_choice == 0:
        parameters = [mu, sigma_normal]

    elif type_choice == 1:
        parameters = [mu, sigma_vg, theta_vg, kappa_vg]

    elif type_choice == 2:
        parameters = [mu, sigma_nig, theta_nig, kappa_nig]

    else:  # type_choice == 3
        parameters = [mu, c, g, m, y]

    return parameters


def cos_pdf_underlying_asset(type_choice, parameters, time):
    L = 10
    N = 1000

    a, b = get_COS_bounds(parameters, type_choice, time, L)
    underlying_prices = np.linspace(a, b, N)
    pdf_underlying_asset = get_pdf_cos(type_choice, underlying_prices, a, b, parameters, time, N)

    mean, variance, skewness, kurtosis = compute_moments(type_choice, parameters, time)
    norm_pdf = norm.pdf(underlying_prices, mean, variance ** 0.5 )

    return pdf_underlying_asset, underlying_prices, mean, variance, skewness, kurtosis, norm_pdf


# Plot Pdf underlying distribution


def create_plot_return_underlying_distribution(underlying_prices, pdf_underlying_asset, norm_pdf):
    data = ColumnDataSource(data=dict(
        underlying_prices=underlying_prices,
        pdf_underlying_asset=pdf_underlying_asset,
        norm_pdf=norm_pdf
    ))

    hover_returns = HoverTool(attachment="above", names=['pdf ret'],
                              tooltips=[("Returns", "@underlying_prices"), ("Pdf", "@pdf_underlying_asset")])
    hover_norm_pdf = HoverTool(attachment="below", names=['pdf norm'],
                               tooltips=[("Returns", "@underlying_prices"), ("Pdf Norm", "@norm_pdf")])

    x_range = [min(underlying_prices), max(underlying_prices)]
    y_range = [0, max(max(norm_pdf),max(pdf_underlying_asset)) * 1.10]
    fig = bp.figure(tools=['save, pan, box_zoom, reset, crosshair', hover_returns, hover_norm_pdf], x_range=x_range,
                    y_range=y_range, sizing_mode='scale_both', toolbar_location="right", x_axis_label='Returns',
                    y_axis_label='Probability')

    fig.line(x='underlying_prices', y='pdf_underlying_asset', source=data, legend="Pdf distribution", color="#0095B6",
             alpha=0.9, line_width=4, name='pdf ret')
    fig.line(x='underlying_prices', y='norm_pdf', source=data, legend="Benchmark Normal", color="#D21F1B",
             alpha=0.6, line_width=3, name='pdf norm')

    fig.legend.location = "top_left"
    fig.toolbar.active_drag = None

    from bokeh.embed import components
    script, div = components(fig)

    return script, div


# Compute option prices


def compute_option_prices(type_choice, call_put, spot_price, strike_min, strike_max, risk_free, dividend_yield, time,
                          parameters):
    # Compute option prices
    risk_free = risk_free / 100
    dividend_yield = dividend_yield / 100
    nk = 1

    strike = np.arange(strike_min, strike_max + 1, nk)
    L = 10
    N = 1000

    option_prices = get_cos_prices(type_choice, L, N, call_put, spot_price, strike, risk_free, dividend_yield, time,
                                   parameters)
    return option_prices, strike


# Compute Implied Volatility

def compute_implied_volatility(option_prices, call_put, spot_price, strike, time, risk_free, dividend_yield):
    risk_free = risk_free / 100
    dividend_yield = dividend_yield / 100

    implied_volatility = find_vol(option_prices, call_put, spot_price, strike, time, risk_free, dividend_yield)
    return implied_volatility


def create_implied_volatility_plot(strike, implied_volatility, spot_price):
    data = ColumnDataSource(data=dict(
        strike=strike,
        implied_volatility=implied_volatility
    ))

    hover_implied = HoverTool(attachment="above", names=['implied vol'],
                              tooltips=[("Strike", "@strike"), ("Implied Vol", "@implied_volatility")])

    x_range = [min(strike) * 0.9, max(strike) * 1.1]
    y_range = [0, max(implied_volatility) * 1.75]
    fig = bp.figure(tools=['save, pan, box_zoom, reset, crosshair', hover_implied], x_range=x_range, y_range=y_range,
                    sizing_mode='scale_both', toolbar_location="right", x_axis_label='Exercise price',
                    y_axis_label='Volatility x root time')

    fig.line(x='strike', y='implied_volatility', source=data, legend='Implied volatility', color="#0095B6",
             line_width=4, alpha=0.8, name='implied vol')
    fig.square(x=spot_price, y=0, source=data, legend='Spot Price', color="#050402", size=8)

    fig.legend.orientation = "horizontal"
    fig.legend.location = "bottom_right"
    fig.toolbar.active_drag = None

    from bokeh.embed import components
    script, div = components(fig)

    return script, div
