# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 20:44:43 2019

@author: Diego
"""

import pandas as pd
import bokeh.plotting as bp
from bokeh.plotting import ColumnDataSource
from bokeh.models import HoverTool
from bokeh.io import curdoc
from bokeh.layouts import row, column
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import Slider, TextInput
from bokeh.plotting import figure
from bokeh.core.properties import value
import scipy.stats 
import math




def plot_log_returns(log_retruns,dates):
    
    
    
    del dates[0]
    data = ColumnDataSource(data=dict(
        dates=dates,
        log_returns=log_returns,
    ))
    
    hover_normal = HoverTool(attachment="above", names=['Normal Distr'],
                             tooltips=[("teoretical quantiles", "@dates"), ("Normal Distr", "@log_returns")])
    
    hover_empirical = HoverTool(attachment="below", names=['model spot rate'],
                            tooltips=[("teoretical quantiles", "@dates"), ("Empirical Distr", "@empirical_distr")])
    
    x_range = [min(dates), max(dates)]
    y_range = [min(log_returns)-0.01, max(log_returns) + 0.01]
    
    fig = bp.figure(tools=['save, pan, box_zoom, reset, crosshair', hover_empirical, hover_normal], x_range=x_range,
                    y_range=y_range, sizing_mode='scale_both', toolbar_location="right",
                    x_axis_label='Time',
                    y_axis_label=' Log Returns')

    
    fig.line(x='dates', y='log_returns', source=data, color="navy", legend='Log returns vs Dates', line_width=0.1, alpha=0.1, name='Log_Returns')
    
    
    fig.toolbar.active_drag = None
    fig.legend.location = "bottom_right"
    
    from bokeh.embed import components
    script, div = components(fig)
    
    
    return fig, div

