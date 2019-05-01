# -*- coding: utf-8 -*-
"""
Created on Tue Apr 16 09:49:53 2019

@author: Diego
"""
import numpy as np
from get_COS_bounds import get_COS_bounds
from get_pdf_cos import get_pdf_cos
from get_COSprices import get_cos_prices
from getbs import find_vol
import matplotlib.pyplot as plt
import bokeh.plotting as plt
from bokeh.plotting import ColumnDataSource

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
    if type_choice == 1:
        parameters = [mu, sigma]

    elif type_choice == 2 or type_choice == 3:
        parameters = [mu, sigma, kappa, theta]

    else:  # type_choice == 4
        parameters = [mu, c, g, m, y]

    return parameters


def cos_pdf_underlying_asset(type_choice, parameters, time):
    L = 10
    N = 10000
    a, b = get_COS_bounds(parameters, type_choice, time, L)
    underlying_prices = np.linspace(a, b, N)
    pdf_underlying_asset = get_pdf_cos(type_choice, underlying_prices, a, b, parameters, time, N)

    return pdf_underlying_asset, underlying_prices


# Plot Pdf underlying distribution


def create_plot_return_underlying_distribution(underlying_prices, pdf_underlying_asset, s0):
    data = ColumnDataSource(data=dict(
        underlying_prices=underlying_prices,
        pdf_underlying_asset=pdf_underlying_asset
    ))

    x_range = [min(underlying_prices), max(underlying_prices)]  # before x_range = [min(ret_t) - 0.5, max(ret_t) + 0.5]
    y_range = [0, max(pdf_underlying_asset) * 1.10]
    p = plt.figure(x_range=x_range, y_range=y_range, title="Pdf underlying asset", plot_height=450,
                   toolbar_location="right", x_axis_label='Prices', y_axis_label='Probability')

    p.line(x='underlying_prices', y='pdf_underlying_asset', source=data, legend="Pdf distribution", color="#0095B6",
           alpha=0.9, line_width=4)

    # p.square(x=S0, y=0, source=data,  legend="Log Price", color="#050402", size=8)

    p.legend.location = "top_right"
    p.toolbar.active_drag = None
    p.legend.click_policy = "hide"

    from bokeh.embed import components
    script, div = components(p)

    return script, div


# Compute option prices


def compute_option_prices(type_choice, call_put, s0, strike_min, strike_max, risk_free, dividend_yield, time,
                          parameters):
    # Compute option prices

    nk = 50

    strikes = np.linspace(strike_min, strike_max, nk)
    L = 10
    N = 10000
    option_prices = get_cos_prices(type_choice, L, N, call_put, s0, strikes, risk_free, dividend_yield, time,
                                   parameters)

    return option_prices, strikes


# Compute Implied Volatilities

def compute_implied_volatilites(option_prices, call_put, s0, strikes, time, risk_free, dividend_yield):
    target_value = option_prices
    implied_volatilities = find_vol(target_value, call_put, s0, strikes, time, risk_free, dividend_yield)

    return implied_volatilities


def create_implied_volatility_plot(strikes, implied_volatilities, s0):
    data = ColumnDataSource(data=dict(
        strikes=strikes,
        implied_volatilities=implied_volatilities
    ))

    x_range = [min(strikes) * 0.9, max(strikes) * 1.1]
    y_range = [min(implied_volatilities) * 0.9, max(implied_volatilities) * 1.1]
    p = plt.figure(x_range=x_range, y_range=y_range, title="Implied volatility profile", plot_height=400,
                   toolbar_location="left", x_axis_label='Exercise price',
                   y_axis_label='Volatility x root time')

    p.line(x='strike', y='implied_volatility', source=data, color="#0095B6", line_width=4, alpha=0.8)
    p.square(x=s0, y=0, source=data, legend='Price', color="#050402", size=8)
    # p.circle(x='strike_value', y='volatility', source=data, color="#D21F1B", legend='Implied Volatility', size=6)

    p.legend.orientation = "horizontal"
    p.legend.location = "bottom_right"
    p.toolbar.active_drag = None

    from bokeh.embed import components
    script, div = components(p)

    return script, div
