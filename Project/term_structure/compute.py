# -*- coding: utf-8 -*-
"""
Created on Tue Sep 10 15:17:49 2019

@author: Diego
"""

import os

import numpy as np
import pandas as pd
from scipy import optimize
from scipy.optimize import least_squares
import numpy as np
import bokeh.plotting as bp
from bokeh.plotting import ColumnDataSource
from bokeh.models import HoverTool
from bokeh.layouts import row, column
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import Slider, TextInput
from bokeh.plotting import figure

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


def fitting_method(model, x0, data, flag1, flag2):
    ttm = (data["Maturity"].tolist())
    market_discount_factor = (data["Discount Factor"].tolist())

    if model == 1:

        if flag1 == 0:

            res_1 = least_squares(lambda y: fit_df_Vasicek(y, data, flag1, flag2), x0)
            param = res_1.x
            discount_factor = get_df_Vasicek(param, ttm)

        else:

            param = optimize.fmin(lambda y: fit_df_Vasicek(y, data, flag1, flag2), x0)
            discount_factor = get_df_Vasicek(param, ttm)

    elif model == 2:

        if flag1 == 0:

            res_1 = least_squares(lambda y: fit_df_CIR(y, data, flag1, flag2), x0)
            param = res_1.x
            discount_factor = get_df_CIR(param, ttm)

        else:

            param = optimize.fmin(lambda y: fit_df_CIR(y, data, flag1, flag2), x0)
            discount_factor = get_df_CIR(param, ttm)

    elif model == 3:

        if flag1 == 0:

            res_1 = least_squares(lambda y: fit_df_NelsonSiegel(y, data, flag1, flag2), x0)
            param = res_1.x
            discount_factor = get_df_NelsonSiegel(param, ttm)

        else:

            param = optimize.fmin(lambda y: fit_df_NelsonSiegel(y, data, flag1, flag2), x0)
            discount_factor = get_df_NelsonSiegel(param, ttm)

    else:

        if flag1 == 0:

            res_1 = least_squares(lambda y: fit_df_Svensson(y, data, flag1, flag2), x0)
            param = res_1.x
            discount_factor = get_df_Svensson(param, ttm)

        else:

            param = optimize.fmin(lambda y: fit_df_Svensson(y, data, flag1, flag2), x0)
            discount_factor = get_df_Svensson(param, ttm)

    model_discount_factor = discount_factor

    model_spot_rate = -np.log(model_discount_factor) / ttm
    market_spot_rate = -np.log(market_discount_factor) / ttm

    discount_factor_model_error = (model_discount_factor - market_discount_factor) ** 2
    spot_rate_model_error = (model_spot_rate - market_spot_rate) ** 2

    return market_discount_factor, market_spot_rate, model_discount_factor, model_spot_rate, \
        discount_factor_model_error, spot_rate_model_error, param, ttm



def discount_factor_term_structure(ttm, market_discount_factor, model_discount_factor):



    data_market_discount_factor = ColumnDataSource(data=dict(
        ttm=ttm,
        market_discount_factor=market_discount_factor
    ))

    data_model_discount_factor = ColumnDataSource(data=dict(
        ttm=ttm,
        model_discount_factor=model_discount_factor
    ))



#    hover_market = HoverTool(attachment="below", names=['market discount factor'],
#                             tooltips=[("Maturity", "@ttm"), ("market_discount_factor", "@market_discount_factor")])
#
#    hover_model = HoverTool(attachment="above", names=['model discount factor'], tooltips=[("Maturity", "@ttm"),
#                            ("Model discount factor", "@model_discount_factor")])

   

    x_range = [min(ttm), max(ttm)]
    y_range = [min(model_discount_factor), max(model_discount_factor)]

    fig = bp.figure(tools=['save, pan, box_zoom, reset, crosshair'], x_range = x_range, y_range = y_range, title="Discount Factor Term Structure", plot_height=450,
                    toolbar_location="left", x_axis_label='Time', y_axis_label='Discount Factor')

    fig.line(x='ttm', y='model_discount_factor', source=data_model_discount_factor, color="#0095B6",
             legend='Model Discount Factor Term Structure', line_width=4, alpha=0.8, name='Model discount term structure')


    
    fig.circle(x='ttm', y='market_discount_factor', source=data_market_discount_factor, color="#D21F1B",
                legend='Market Discount Factor', size=6, name='Market discount factor')


    fig.toolbar.active_drag = None
    fig.legend.location = "bottom_left"
    fig.legend.orientation = "vertical"

    from bokeh.embed import components
    script, div = components(fig)

    return script, div
    
   

def interest_rate_term_structure(ttm, market_spot_rate, model_spot_rate):



    data_market_spot_rate = ColumnDataSource(data=dict(
        ttm=ttm,
        market_spot_rate=market_spot_rate
    ))

    data_model_spot_rate = ColumnDataSource(data=dict(
        ttm=ttm,
        model_spot_rate=model_spot_rate
    ))



#    hover_market = HoverTool(attachment="below", names=['market spot rate'],
#                             tooltips=[("Maturity", "@ttm"), ("market_spot_rate", "@market_spot_rate")])
#
#    hover_model = HoverTool(attachment="above", names=['model spot rate'], tooltips=[("Maturity", "@ttm"),
#                            ("Model spot rater", "@model_spot_rate")])

   

    x_range = [min(ttm), max(ttm)]
    y_range = [min(model_spot_rate), max(model_spot_rate)]

    fig = bp.figure(tools=['save, pan, box_zoom, reset, crosshair'], x_range = x_range, y_range = y_range, title="Spot Rate Term Structure", plot_height=450,
                    toolbar_location="left", x_axis_label='Time', y_axis_label='Spot Rate')

    fig.line(x='ttm', y='model_spot_rate', source=data_model_spot_rate, color="#0095B6",
             legend='Model Spot Rate Term Structure', line_width=4, alpha=0.8, name='Model spot rate term structure')


    
    fig.circle(x='ttm', y='market_spot_rate', source=data_market_spot_rate, color="#D21F1B",
                legend='Market spot rate', size=6, name='Market spot rate')


    fig.toolbar.active_drag = None
    fig.legend.location = "bottom_left"
    fig.legend.orientation = "vertical"

    from bokeh.embed import components
    script, div = components(fig)

    return script, div




def plot_error_interest_rate(ttm, spot_rate_model_error):
    
    # tools = "save, box_zoom, crosshair, reset"
    # labels = ["model_error"]
    # colors = ["#0095B6"]

    x = list(range(0, len(spot_rate_model_error)+1))


    # data = ColumnDataSource(data=dict(
    #      x = x,
    #      spot_rate_model_error = spot_rate_model_error
    #     ))

    #  tooltips = [
    #      ("time", "@ttm"),
    #      ("spot rate model_error", "@spot_rate_model_error")
    #  ]
    
    # p = plt.figure(x_range=x, title=" Capital Share & Interest Share", plot_height=300, toolbar_location="left",
    #                tools=tools, tooltips=tooltips, x_axis_label='Number of rates', y_axis_label='Amount')
    #  # add a line renderer with legend and line thickness
    # p.vbar(x= x,  width=0.5, bottom=0, top=spot_rate_model_error, color="#CAB2D6")

   

    # p.toolbar.active_drag = None
    # p.legend.orientation = "horizontal"
    # p.legend.location = "top_left"

    p = bp.figure(plot_width=450, plot_height=450)
    p.vbar(x = x, width=0.5, bottom=0, top=spot_rate_model_error, color="#0095B6")


    from bokeh.embed import components
    script, div = components(p)

    return script, div

    


def plot_error_discount_factor(ttm, discount_factor_model_error):
    
    # tools = "save, box_zoom, crosshair, reset"
    # labels = ["model_error"]
    # colors = ["#0095B6"]

    x = list(range(0, len(discount_factor_model_error)+1))


    # data = ColumnDataSource(data=dict(
    #      x = x,
    #      spot_rate_model_error = spot_rate_model_error
    #     ))

    #  tooltips = [
    #      ("time", "@ttm"),
    #      ("spot rate model_error", "@spot_rate_model_error")
    #  ]
    
    # p = plt.figure(x_range=x, title=" Capital Share & Interest Share", plot_height=300, toolbar_location="left",
    #                tools=tools, tooltips=tooltips, x_axis_label='Number of rates', y_axis_label='Amount')
    #  # add a line renderer with legend and line thickness
    # p.vbar(x= x,  width=0.5, bottom=0, top=spot_rate_model_error, color="#CAB2D6")

   

    # p.toolbar.active_drag = None
    # p.legend.orientation = "horizontal"
    # p.legend.location = "top_left"

    p = bp.figure(plot_width=450, plot_height=450)
    p.vbar(x = x, width=0.5, bottom=0, top=discount_factor_model_error, color="#0095B6")


    from bokeh.embed import components
    script, div = components(p)

    return script, div

