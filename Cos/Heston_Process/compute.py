# -*- coding: utf-8 -*-
"""
Created on Thu May  9 12:24:34 2019

@author: Diego
"""
import numpy as np
from get_heston_bounds import compute_heston_bounds
from get_heston_cos_pdf import get_pdf_cos
from get_heston_option_prices import get_cos_prices
from getbs import find_vol
from bokeh.models import HoverTool
from bokeh.plotting import ColumnDataSource
import bokeh.plotting as bp


# Inputs

# s0 = 100
# strike_min = 70
# strike_max = 130
# time = 1
# call_put = 1
# mu = 0
# v0 = 0.0175     #0.0175
# v_hat = 0.0175   #0.0398
# lam = 0.00000001 #1.5768
# chi = 0.00000001 #0.5751
# rho = 0.00000001 #-0.5711
# risk_free = 0
# dividend_yield = 0

# Pdf Heston Model
def heston_pdf_and_volatility(spot_price, strike_min, strike_max, time, v0, chi, lam, rho, v_hat, mu, risk_free,
                              dividend_yield, call_put):
    heston_pdf = get_pdf_cos(time, v0, chi, lam, rho, v_hat, mu)
    nk = 50
    a, b = compute_heston_bounds(mu, time, v0, chi, lam, rho, v_hat)
    N = 1000
    returns = np.linspace(a, b, N)

    strike = np.linspace(strike_min, strike_max, nk)
    option_prices = get_cos_prices(mu, spot_price, strike, risk_free, dividend_yield, time, v0, chi, lam, rho, v_hat,
                                   call_put)

    implied_volatility = find_vol(option_prices, call_put, spot_price, strike, time, risk_free, dividend_yield)

    return heston_pdf, returns, implied_volatility, strike


def create_plot_return_underlying_distribution(returns, heston_pdf):

    data = ColumnDataSource(data=dict(
        returns=returns,
        heston_pdf=heston_pdf
    ))

    hover_returns = HoverTool(attachment="left", names=['pdf ret'],
                              tooltips=[("Returns", "@returns"), ("Pdf", "@heston_pdf")])

    x_range = [min(returns), max(returns)]
    y_range = [0, max(heston_pdf) * 1.10]
    fig = bp.figure(tools=['save, pan, box_zoom, reset, crosshair', hover_returns], x_range=x_range, y_range=y_range,
                    title="Pdf underlying asset", plot_height=450,
                    toolbar_location="left", x_axis_label='Returns', y_axis_label='Probability')

    fig.line(x='returns', y='heston_pdf', source=data, legend="Pdf distribution", color="#0095B6", alpha=0.9,
             line_width=4, name='pdf ret')

    fig.legend.location = "top_right"
    fig.toolbar.active_drag = None

    from bokeh.embed import components
    script, div = components(fig)

    return script, div


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


