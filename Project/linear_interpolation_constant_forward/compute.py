# -*- coding: utf-8 -*-
"""
Created on Thu May 21 12:04:29 2020

@author: Diego De Bortoli
"""
from linear_interpolation_constant_forward.get_df_linear_interpolation import linear_interp
from linear_interpolation_constant_forward.get_constant_fwd import constant_fwd
from linear_interpolation_constant_forward.get_dates import list_of_daily_dates
from bokeh.plotting import figure
from bokeh.plotting import ColumnDataSource
from bokeh.models import HoverTool

import pandas as pd
import numpy as np
import os


def upload_input(filename=None):
    data = pd.read_excel(os.path.join('uploads/', filename))

    return data


def get_spot_rate_discount_factor(data, model_flag):
    time = (data["Maturity"].tolist())
    data_df = (data["Discount Factor"].tolist())
    dates, annualized = list_of_daily_dates(time)

    if data_df[0] == 0:
        data_df = data_df.remove(0)
        time = time.remove(0)

    if model_flag == '0':
        model_discount_factor, model_spot_rate, daily_time = linear_interp(data_df, time)

    if model_flag == '1':
        model_discount_factor, model_spot_rate, daily_time = constant_fwd(data_df, time)

    n = len(dates) - len(daily_time)
    dates = dates[:len(dates) - n]
    market_discount_factor = data_df
    market_spot_rate = -np.log(market_discount_factor) / np.array(time)
    market_spot_rate = list(market_spot_rate)

    if market_discount_factor[0] != 1:
        market_discount_factor.insert(0, 1)
        market_spot_rate.insert(0, 0)
        time.insert(0, 0)

    date_db = dates
    time_plot = time
    daily_time_plot = daily_time

    return model_discount_factor, model_spot_rate, market_spot_rate, market_discount_factor, date_db, daily_time_plot, time_plot


def create_plot_discount_factor_term_structure(time_plot, market_discount_factor, daily_time_plot,
                                               model_discount_factor):
    data_model = ColumnDataSource(data=dict(
        daily_time_plot=daily_time_plot,
        model_discount_factor=model_discount_factor,
    ))

    data_market = ColumnDataSource(data=dict(
        time_plot=time_plot,
        market_discount_factor=market_discount_factor,
    ))

    hover_market = HoverTool(attachment="above", names=['market discount factor'],
                             tooltips=[("TTM", "@time_plot"), ("Market Discount Factor", "@market_discount_factor")])

    hover_model = HoverTool(attachment="below", names=['model discount factor'],
                            tooltips=[("TTM", "@daily_time_plot"), ("Model Discount Factor", "@model_discount_factor")])

    x_range = [min(time_plot), max(time_plot) + 1]
    y_range = [min(model_discount_factor) * 0.9, max(model_discount_factor) * 1.1]

    fig = figure(tools=['save, pan, box_zoom, reset, crosshair', hover_market, hover_model], x_range=x_range,
                 y_range=y_range, sizing_mode='scale_both', toolbar_location="right",
                 x_axis_label='Time to Maturity', y_axis_label='Discount Factor')

    fig.line(x='daily_time_plot', y='model_discount_factor', source=data_model,
             legend_label='Interpolated Discount Factor Term Structure',
             color="#0095B6", line_width=4, alpha=0.9, name='interpolated discount factor')

    fig.circle(x='time_plot', y='market_discount_factor', source=data_market, color="#D21F1B",
               legend_label='Market Discount Factor', size=6, name='market discount factor')

    fig.toolbar.active_drag = None
    fig.legend.location = "top_right"

    from bokeh.embed import components
    script, div = components(fig)

    return script, div


def create_plot_interest_rate_term_structure(time_plot, market_discount_factor, daily_time_plot, model_discount_factor):
    data_model = ColumnDataSource(data=dict(
        daily_time_plot=daily_time_plot,
        model_discount_factor=model_discount_factor,
    ))

    data_market = ColumnDataSource(data=dict(
        time_plot=time_plot,
        market_discount_factor=market_discount_factor,
    ))

    hover_market = HoverTool(attachment="above", names=['market spot rate'],
                             tooltips=[("TTM", "@time_plot"), ("Market Spot Rate", "@market_discount_factor")])

    hover_model = HoverTool(attachment="below", names=['model spot rate'],
                            tooltips=[("TTM", "@daily_time_plot"),
                                      ("Interpolated Spot Rate", "@model_discount_factor")])

    x_range = [min(time_plot), max(time_plot) + 1]
    y_range = [min(market_discount_factor) * 0.9, max(market_discount_factor) * 1.1]

    fig = figure(tools=['save, pan, box_zoom, reset, crosshair', hover_market, hover_model], x_range=x_range,
                 y_range=y_range, sizing_mode='scale_both', toolbar_location="right",
                 x_axis_label='Time to Maturity', y_axis_label='Spot Rate')

    fig.line(x='daily_time_plot', y='model_discount_factor', source=data_model,
             legend_label='Interpolated Spot Rate Term Structure',
             color="#0095B6", line_width=4, alpha=0.9, name='interpolated spot rate')

    fig.circle(x='time_plot', y='market_discount_factor', source=data_market, color="#D21F1B",
               legend_label='Market Spot Rate', size=6, name='market spot rate')

    fig.toolbar.active_drag = None
    fig.legend.location = "top_right"

    from bokeh.embed import components
    script, div = components(fig)

    return script, div
