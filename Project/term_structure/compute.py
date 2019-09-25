# -*- coding: utf-8 -*-
"""
Created on Tue Sep 10 15:17:49 2019

@author: Diego
"""

import os

import bokeh.plotting as bp
import numpy as np
import pandas as pd
from bokeh.models import HoverTool
from bokeh.plotting import ColumnDataSource
from scipy import optimize
from scipy.optimize import least_squares

from term_structure.fit_df_CIR import fit_df_CIR
from term_structure.fit_df_NelsonSiegel import fit_df_NelsonSiegel
from term_structure.fit_df_Svensson import fit_df_Svensson
from term_structure.fit_df_Vasicek import fit_df_Vasicek
from term_structure.get_df_CIR import get_df_CIR
from term_structure.get_df_NelsonSiegel import get_df_NelsonSiegel
from term_structure.get_df_Svensson import get_df_Svensson
from term_structure.get_df_Vasicek import get_df_Vasicek


def upload_input(filename=None):
    data = pd.read_excel(os.path.join('uploads/', filename))

    return data


def create_objective_vector(model, kappa_vasicek, theta_vasicek, sigma_vasicek, rho_vasicek, kappa_cir, theta_cir,
                            sigma_cir, rho_cir, beta0_nelson, beta1_nelson, beta2_nelson, tau_nelson, beta0_svensson,
                            beta1_svensson, beta2_svensson, beta3_svensson, tau1_svensson, tau2_svensson):
    model = int(model)

    if model == 0:
        x0 = [kappa_vasicek, theta_vasicek, sigma_vasicek, rho_vasicek]

    elif model == 1:
        x0 = [kappa_cir, theta_cir, sigma_cir, rho_cir]

    elif model == 2:
        x0 = [beta0_nelson, beta1_nelson, beta2_nelson, tau_nelson]

    else:  # model == 3
        x0 = [beta0_svensson, beta1_svensson, beta2_svensson, beta3_svensson, tau1_svensson, tau2_svensson]

    return x0


def fitting_method(model, x0, data, flag1, flag2):
    time = (data["Maturity"].tolist())
    market_discount_factor = (data["Discount Factor"].tolist())
    model = int(model)
    flag1 = int(flag1)
    flag2 = int(flag2)

    if model == 0:

        if flag1 == 0:

            res_1 = least_squares(lambda y: fit_df_Vasicek(y, data, flag1, flag2), x0)
            param = res_1.x
            discount_factor = get_df_Vasicek(param, time)

        else:

            param = optimize.fmin(lambda y: fit_df_Vasicek(y, data, flag1, flag2), x0)
            discount_factor = get_df_Vasicek(param, time)

    elif model == 1:

        if flag1 == 0:

            res_1 = least_squares(lambda y: fit_df_CIR(y, data, flag1, flag2), x0)
            param = res_1.x
            discount_factor = get_df_CIR(param, time)

        else:

            param = optimize.fmin(lambda y: fit_df_CIR(y, data, flag1, flag2), x0)
            discount_factor = get_df_CIR(param, time)

    elif model == 2:

        if flag1 == 0:

            res_1 = least_squares(lambda y: fit_df_NelsonSiegel(y, data, flag1, flag2), x0)
            param = res_1.x
            discount_factor = get_df_NelsonSiegel(param, time)

        else:

            param = optimize.fmin(lambda y: fit_df_NelsonSiegel(y, data, flag1, flag2), x0)
            discount_factor = get_df_NelsonSiegel(param, time)

    else:  # model == 3

        if flag1 == 0:

            res_1 = least_squares(lambda y: fit_df_Svensson(y, data, flag1, flag2), x0)
            param = res_1.x
            discount_factor = get_df_Svensson(param, time)

        else:

            param = optimize.fmin(lambda y: fit_df_Svensson(y, data, flag1, flag2), x0)
            discount_factor = get_df_Svensson(param, time)

    model_discount_factor = discount_factor

    model_spot_rate = -np.log(model_discount_factor) / time
    market_spot_rate = -np.log(market_discount_factor) / time

    discount_factor_model_error = (model_discount_factor - market_discount_factor) ** 2
    spot_rate_model_error = (model_spot_rate - market_spot_rate) ** 2

    return market_discount_factor, market_spot_rate, model_discount_factor, model_spot_rate, \
           discount_factor_model_error, spot_rate_model_error, param, time


def create_plot_discount_factor_term_structure(time, market_discount_factor, model_discount_factor):
    data = ColumnDataSource(data=dict(
        time=time,
        market_discount_factor=market_discount_factor,
        model_discount_factor=model_discount_factor
    ))

    hover_market = HoverTool(attachment="left", names=['market discount factor'],
                             tooltips=[("Maturity", "@time"), ("Market Discount Factor", "@market_discount_factor")])

    hover_model = HoverTool(attachment="right", names=['model discount factor'],
                            tooltips=[("Maturity", "@time"), ("Model Discount Factor", "@model_discount_factor")])

    x_range = [min(time), max(time) + 1]
    y_range = [min(model_discount_factor), max(model_discount_factor) + 0.2]

    fig = bp.figure(tools=['save, pan, box_zoom, reset, crosshair', hover_market, hover_model], x_range=x_range,
                    y_range=y_range, plot_height=500, toolbar_location="right", x_axis_label='Time',
                    y_axis_label='Discount Factor')

    fig.line(x='time', y='model_discount_factor', source=data, legend='Model Discount Factor Term Structure',
             color="#0095B6", line_width=4, alpha=0.9, name='model discount factor')

    fig.circle(x='time', y='market_discount_factor', source=data, color="#D21F1B", legend='Market Discount Factor',
               size=6, name='market discount factor')

    fig.toolbar.active_drag = None
    fig.legend.location = "top_right"

    from bokeh.embed import components
    script, div = components(fig)

    return script, div


def create_plot_interest_rate_term_structure(time, market_spot_rate, model_spot_rate):
    data = ColumnDataSource(data=dict(
        time=time,
        market_spot_rate=market_spot_rate,
        model_spot_rate=model_spot_rate
    ))

    hover_market = HoverTool(attachment="left", names=['market spot rate'],
                             tooltips=[("Maturity", "@time"), ("Market Spot Rate", "@market_spot_rate")])

    hover_model = HoverTool(attachment="right", names=['model spot rate'],
                            tooltips=[("Maturity", "@time"), ("Model Spot Rate", "@model_spot_rate")])

    x_range = [min(time), max(time) + 1]
    y_range = [min(model_spot_rate), max(model_spot_rate) + 0.002]

    fig = bp.figure(tools=['save, pan, box_zoom, reset, crosshair', hover_model, hover_market], x_range=x_range,
                    y_range=y_range, plot_height=500, toolbar_location="right", x_axis_label='Time',
                    y_axis_label='Spot Rate')

    fig.line(x='time', y='model_spot_rate', source=data, color="#0095B6", legend='Model Spot Rate Term Structure',
             line_width=4, alpha=0.8, name='model spot rate')

    fig.circle(x='time', y='market_spot_rate', source=data, color="#D21F1B", legend='Market spot rate', size=6,
               name='market spot rate')

    fig.toolbar.active_drag = None
    fig.legend.location = "bottom_right"

    from bokeh.embed import components
    script, div = components(fig)

    return script, div


def create_plot_error_interest_rate(spot_rate_model_error, time):
    edges = list(range(0, len(spot_rate_model_error) + 1))
    data = ColumnDataSource(data=dict(
        spot_rate_model_error=spot_rate_model_error,
        time=time,
        edges_left=edges[:-1],
        edges_right=edges[1:]
    ))

    hover_spot_rate = HoverTool(attachment="left", names=['spot rate'],
                                tooltips=[("Maturity", "@time"), ("Spot Rate Error", "@spot_rate_model_error")])

    fig = bp.figure(tools=['save, pan, box_zoom, reset, crosshair', hover_spot_rate],
                    plot_height=450, toolbar_location="right", x_axis_label='Series of Data',
                    y_axis_label='Model Error Spot Rate')

    fig.quad(top='spot_rate_model_error', bottom=0, left='edges_left', right='edges_right', source=data,
             legend="Spot Rate Model Error", color="#0095B6", line_color="#ffffff", alpha=0.9, name='spot rate')

    fig.toolbar.active_drag = None
    fig.legend.location = "top_left"

    from bokeh.embed import components
    script, div = components(fig)

    return script, div


def create_plot_error_discount_factor(discount_factor_model_error, time):
    edges = list(range(0, len(discount_factor_model_error) + 1))
    data = ColumnDataSource(data=dict(
        discount_factor_model_error=discount_factor_model_error,
        time=time,
        edges_left=edges[:-1],
        edges_right=edges[1:]
    ))

    hover_discount_factor = HoverTool(attachment="left", names=['discount factor'],
                                      tooltips=[("Maturity", "@time"),
                                                ("Discount Factor Error", "@discount_factor_model_error")])

    fig = bp.figure(tools=['save, pan, box_zoom, reset, crosshair', hover_discount_factor],
                    plot_height=450, toolbar_location="right", x_axis_label='Series of Data',
                    y_axis_label='Model Error Discount Factor')

    fig.quad(top='discount_factor_model_error', bottom=0, left='edges_left', right='edges_right', source=data,
             legend="Discount Factor Model Error", color="#0095B6", line_color="#ffffff", alpha=0.9,
             name='discount factor')

    fig.toolbar.active_drag = None
    fig.legend.location = "top_left"

    from bokeh.embed import components
    script, div = components(fig)

    return script, div
