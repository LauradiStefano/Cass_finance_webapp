# -*- coding: utf-8 -*-
"""
Created on Tue Apr 16 09:49:53 2019

@author: Diego
"""

import numpy as np
from get_moments import compute_moments
from get_COS_bounds import get_COS_bounds
from get_pdf_cos import get_pdf_cos
from get_COSprices import get_cos_prices
from getbs import find_vol
import bokeh.plotting as bp
from bokeh.plotting import ColumnDataSource
from bokeh.models import HoverTool


# #Input
# u = 1
# type = 2
# call_put = 1
# time = 1
# s0 = 100
# strike_min = s0*0.65
# strike_max = s0*1.35
# nk=50
# strikes=np.linspace ( strike_min , strike_max , nk )
# dividend_yield = 0
# risk_free = 0.1
# mu = 0
# sigma = 0.1213
# theta=-0.2436 # if zero skew=0
# kappa=0.1689
# parameters = [ mu , sigma, theta , kappa  ]


def select_parameters(type_choice, mu, sigma, kappa, theta, c, g, m, y):
    type_choice = int(type_choice)
    if type_choice == 1:
        parameters = [mu, sigma]

    elif type_choice == 2 or type_choice == 3:
        parameters = [mu, sigma, kappa, theta]

    else:  # type_choice == 4
        parameters = [mu, c, g, m, y]

    return parameters


def cos_pdf_underlying_asset(type_choice, parameters, time):
    L = 6
    N = 500

    a, b = get_COS_bounds(parameters, type_choice, time, L)
    underlying_prices = np.linspace(a, b, N)
    pdf_underlying_asset = get_pdf_cos(type_choice, underlying_prices, a, b, parameters, time, N)
    
    mean, variance, skewness, kurtosis = compute_moments(type_choice, parameters)

    return pdf_underlying_asset, underlying_prices, mean, variance, skewness, kurtosis


# Plot Pdf underlying distribution


def create_plot_return_underlying_distribution(underlying_prices, pdf_underlying_asset):
    data = ColumnDataSource(data=dict(
        underlying_prices=underlying_prices,
        pdf_underlying_asset=pdf_underlying_asset
    ))

    hover_returns = HoverTool(attachment="left", names=['pdf ret'],
                              tooltips=[("Returns", "@underlying_prices"), ("Pdf", "@pdf_underlying_asset")])

    x_range = [min(underlying_prices), max(underlying_prices)]
    y_range = [0, max(pdf_underlying_asset) * 1.10]
    fig = bp.figure(tools=['save, pan, box_zoom, reset, crosshair', hover_returns], x_range=x_range, y_range=y_range,
                    title="Pdf underlying asset", plot_height=450,
                    toolbar_location="left", x_axis_label='Returns', y_axis_label='Probability')

    fig.line(x='underlying_prices', y='pdf_underlying_asset', source=data, legend="Pdf distribution", color="#0095B6",
             alpha=0.9, line_width=4, name='pdf ret')

    fig.legend.location = "top_right"
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
    nk = 50

    strike = np.linspace(strike_min, strike_max, nk)
    L = 10
    N = 1000

    option_prices = get_cos_prices(type_choice, L, N, call_put, spot_price, strike, risk_free, dividend_yield, time,
                                   parameters)
    return option_prices, strike


# Compute Implied Volatilities

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

    hover_implied = HoverTool(attachment="left", names=['implied vol'],
                              tooltips=[("Strike", "@strike"), ("Impl vol", "@implied_volatility")])

    x_range = [min(strike) * 0.9, max(strike) * 1.1]
    y_range = [0, max(implied_volatility) * 1.75]
    fig = bp.figure(tools=['save, pan, box_zoom, reset, crosshair', hover_implied], x_range=x_range, y_range=y_range,
                    title="Implied volatility profile", plot_height=450,
                    toolbar_location="right", x_axis_label='Exercise price', y_axis_label='Volatility x root time')

    fig.line(x='strike', y='implied_volatility', source=data, legend='Implied volatility', color="#0095B6",
             line_width=4, alpha=0.8, name='implied vol')
    fig.square(x=spot_price, y=0, source=data, legend='Spot Price', color="#050402", size=8)

    fig.legend.orientation = "horizontal"
    fig.legend.location = "bottom_right"
    fig.toolbar.active_drag = None

    from bokeh.embed import components
    script, div = components(fig)

    return script, div
