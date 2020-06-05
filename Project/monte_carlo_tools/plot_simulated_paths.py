# -*- coding: utf-8 -*-
"""
Created on Thu May 28 14:54:44 2020

@author: Diego
"""

import numpy as np

from bokeh.layouts import gridplot
from bokeh.palettes import Spectral11
from bokeh.plotting import figure, output_file, show
import itertools
from bokeh.models import BoxAnnotation, Toggle

""" inputs
def simulated_paths(timesteps, simulated_paths): #timesteps & X
timesteps = timesteps
matrix of simulated paths = X

"" Plot Simulated Paths
"""


def get_simulated_paths(X, timestep, NStep, NPaths, quantiles):
    x = []
    y = []
    for i in range(0, NStep):
        minn = min(X[i, :])
        x.append(minn)
        maxx = max(X[i, :])
        y.append(maxx)

    min_x = min(x)
    max_x = max(y)
    p1 = figure(title="Simulated Paths", tools="pan,wheel_zoom,box_zoom,reset,save,box_select", y_range=(min_x, max_x))
    p1.xaxis.axis_label = 'Time'
    colors = itertools.cycle(Spectral11)

    for i, color in zip(range(0, NPaths), colors):  # al posto di 51 NPaths
        p1.line(timestep, X[:, i], color=color)

    last_quantiles = quantiles[-1, :]
    green_box = BoxAnnotation(bottom=last_quantiles[0], top=last_quantiles[1], fill_color='green', fill_alpha=0.1)
    p1.add_layout(green_box)

    """Plot Histogram
    """
    hhist, hedges = np.histogram(X[-1, :], bins=20)
    # hzeros = np.zeros(len(hedges)-1)
    # hmax = max(hhist)*1.0
    # LINE_ARGS = dict(color="#3A5785", line_color=None)

    p2 = figure(toolbar_location=None, plot_width=p1.plot_width, y_axis_location="right", y_range=(min_x, max_x))
    p2.xaxis.axis_label = 'Frequency'
    p2.xgrid.grid_line_color = None
    # p2.background_fill_color = "#fafafa"
    p2.quad(left=0, bottom=hedges[:-1], top=hedges[1:], right=hhist, color="white", line_color="#3A5785")
    p2.add_layout(green_box)

    return p1, p2

# open a browser
