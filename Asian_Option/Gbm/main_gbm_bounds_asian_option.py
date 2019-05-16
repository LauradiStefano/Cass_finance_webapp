# -*- coding: utf-8 -*-
"""
Created on Fri May  3 09:56:26 2019

@author: Diego
"""
import bokeh.plotting as bp
from bokeh.models import HoverTool
from bokeh.plotting import ColumnDataSource

from get_gbm_option import gbm_option


# s0 = 100
# N = 50
# strike = 100
# risk_free = 0.04
# sigma = 0.3
# time = 1


# S0= 100
# n =50
# N=n
# K=100
# r = 0.04
# sigma = 0.3
# T = 1

def compute_values(s0, strike, time, risk_free, N, sigma):
    N = int(N)
    risk_free = risk_free / 100
    ptrue, strike_exp_lcr, ptrue_strike, lam, lower_bound = gbm_option(s0, strike, time, risk_free, N, sigma)
    ptrue_strike = ptrue_strike[0]
    return ptrue, strike_exp_lcr, ptrue_strike, lam, lower_bound


def create_plot_lower_bound(lam, lower_bound, strike, strike_exp_lcr):
    data = ColumnDataSource(data=dict(
        lam=lam,
        lower_bound=lower_bound
    ))

    hover_lower_bound = HoverTool(attachment="left", names=['lower bound'],
                                  tooltips=[("Lambda", "@lam"), ("Lower Bound", "@lower_bound")])

    x_range = [min(lam), max(lam) * 0.5]
    y_range = [0, max(lower_bound) * 1.10]
    fig = bp.figure(tools=['save, pan, box_zoom, reset, crosshair', hover_lower_bound], x_range=x_range,
                    y_range=y_range,
                    title="Asian Option Lower Bound", plot_height=450,
                    toolbar_location="left", x_axis_label='Lambda', y_axis_label='Lower Bound')

    fig.line(x='lam', y='lower_bound', source=data, legend="Lower Bound Function", color="#0095B6", alpha=0.9,
             line_width=4, name='lower bound')

    fig.circle(x=strike_exp_lcr, y=0, source=data, legend='Optimal Strike', color="#D21F1B", size=5)
    fig.circle(x=strike, y=0, source=data, legend='Strike', color="#050402", size=3)

    fig.legend.location = "top_right"
    fig.toolbar.active_drag = None

    from bokeh.embed import components
    script, div = components(fig)

    return script, div
