# -*- coding: utf-8 -*-
"""
Created on Sun May 31 14:26:43 2020

@author: Diego
"""
import numpy as np
from bokeh.plotting import figure, output_file, show
from bokeh.palettes import Spectral11

"""inputs
n of steps = NStep
simulated paths = X
"""


def get_histograms_plot(X, NStep):
    t1 = int(NStep / 4)
    t2 = int(NStep / 2)
    t3 = NStep

    """plot histogram in t1 case"""

    min_x = np.quantile(X[-1, :], 0.01)
    max_x = np.quantile(X[-1, :], 0.99)
    hhist, hedges = np.histogram(X[t1, :], density=True, bins=100)
    # hzeros = np.zeros(len(hedges)-1)
    # hmax = max(hhist)*1.1
    # LINE_ARGS = dict(color="#3A5785", line_color=None)

    p1 = figure(tools=['save, pan, box_zoom, reset, crosshair'], toolbar_location='right', sizing_mode='scale_both',
                y_axis_location="right", x_range=(min_x, max_x))
    p1.xaxis.axis_label = 'Obs X at step n' + str(t1)
    p1.xgrid.grid_line_color = None
    p1.quad(bottom=0, left=hedges[:-1], right=hedges[1:], top=hhist, color="#0095B6", line_color="#3A5785")

    """plot histogram in t2 case"""

    min_x = np.quantile(X[-1, :], 0.01)
    max_x = np.quantile(X[-1, :], 0.99)
    hhist, hedges = np.histogram(X[t2, :], density=True, bins=100)
    # hzeros = np.zeros(len(hedges)-1)
    # hmax = max(hhist)*1.1
    # LINE_ARGS = dict(color="#3A5785", line_color=None)

    p2 = figure(tools=['save, pan, box_zoom, reset, crosshair'], toolbar_location='right', sizing_mode='scale_both',
                y_axis_location="right", x_range=(min_x, max_x))
    p2.xaxis.axis_label = 'Obs X at step n' + str(t2)
    p2.xgrid.grid_line_color = None
    p2.quad(bottom=0, left=hedges[:-1], right=hedges[1:], top=hhist, color="#0095B6", line_color="#3A5785")

    """plot histogram in t3 case"""

    min_x = np.quantile(X[t3, :], 0.01)
    max_x = np.quantile(X[t3, :], 0.99)
    hhist, hedges = np.histogram(X[t3, :], density=True, bins=100)
    # hzeros = np.zeros(len(hedges)-1)
    # hmax = max(hhist)*1.1
    # LINE_ARGS = dict(color="#3A5785", line_color=None)

    p3 = figure(tools=['save, pan, box_zoom, reset, crosshair'], toolbar_location='right', sizing_mode='scale_both',
                y_axis_location="right", x_range=(min_x, max_x))
    p3.xaxis.axis_label = 'Obs X at step n' + str(t3)
    p3.xgrid.grid_line_color = None
    p3.quad(bottom=0, left=hedges[:-1], right=hedges[1:], top=hhist, color="#0095B6", line_color="#3A5785")

    return p1, p2, p3
