# -*- coding: utf-8 -*-
"""
Created on Thu May 28 23:35:38 2020

@author: Diego
"""

import numpy as np
from scipy.stats import skew, kurtosis
from bokeh.layouts import gridplot
from bokeh.plotting import figure, output_file, show, ColumnDataSource
from bokeh.models import HoverTool

"""inputs
moments matrix
simulated paths = X
timestep
"""


def get_moments_plot(X, moments, timestep):
    exp_value_emp = np.mean(X, axis=1)
    variance_emp = np.var(X, axis=1) ** 0.5
    skewness_emp = skew(X, axis=1)
    skewness_emp[0] = 0
    kurtosis_emp = kurtosis(X, axis=1) + 3
    kurtosis_emp[0] = 3

    exp_value_teo = moments[:, 0]
    variance_teo = moments[:, 1]
    skewness_teo = moments[:, 2]
    kurtosis_teo = moments[:, 3]

    """Plot exp value : teoretical vs empirical
    """

    data_expvalue = ColumnDataSource(data=dict(
        exp_value_teo=exp_value_teo,
        exp_value_emp=exp_value_emp,
        timestep=timestep))

    hover_exp_teo = HoverTool(attachment="above", names=['Theoretical Expected Value '],
                              tooltips=[("Theoretical Expected value ", "@exp_value_teo"), ("Nstep", "@timestep")])

    hover_exp_emp = HoverTool(attachment="above", names=['Empirical expected value'],
                              tooltips=[("Empirical Expected value ", "@exp_value_emp"), ("Nstep", "@timestep")])

    # x_range = [0, max(timestep)*1.05]
    # y_range = [min(), max(lower_bound) * 1.05]
    p1 = figure(tools=['save, pan, box_zoom, reset, crosshair', hover_exp_teo, hover_exp_emp],
                sizing_mode='scale_both', toolbar_location="right", x_axis_label='Time',
                y_axis_label='Expected Value')

    p1.line(x='timestep', y='exp_value_teo', source=data_expvalue, legend_label="Theoretical Expected Value",
            color="red", alpha=0.9,
            line_width=1, name='lower bound')

    p1.line(x='timestep', y='exp_value_emp', source=data_expvalue, legend_label="Empirical Expected Value",
            color="#0095B6", alpha=0.9,
            line_width=1, name='lower bound')

    p1.legend.location = "bottom_right"
    p1.toolbar.active_drag = None

    """Plot variance value : teoretical vs empirical
    """

    data_variance = ColumnDataSource(data=dict(
        variance_teo=variance_teo,
        variance_emp=variance_emp,
        timestep=timestep))

    hover_var_teo = HoverTool(attachment="above", names=['Theoretical  Standard Deviation '],
                              tooltips=[("Theoretical Variance ", "@variance_teo"), ("Nstep", "@timestep")])

    hover_var_emp = HoverTool(attachment="above", names=['Empirical  Standard Deviation'],
                              tooltips=[("Empirical Variance ", "@variance_emp"), ("Nstep", "@timestep")])

    # x_range = [0, max(timestep)*1.05]
    # y_range = [min(), max(lower_bound) * 1.05]
    p2 = figure(tools=['save, pan, box_zoom, reset, crosshair', hover_var_teo, hover_var_emp],
                sizing_mode='scale_both', toolbar_location="right", x_axis_label='Time',
                y_axis_label=' Standard Deviation')

    p2.line(x='timestep', y='variance_teo', source=data_variance, legend_label="Theoretical Standard Deviation",
            color="red", alpha=0.9,
            line_width=1, name='lower bound')

    p2.line(x='timestep', y='variance_teo', source=data_variance, legend_label="Empirical  Standard Deviation",
            color="#0095B6", alpha=0.9,
            line_width=1, name='lower bound')

    p2.legend.location = "bottom_right"
    p2.toolbar.active_drag = None

    """Plot skewness value : teoretical vs empirical
    """

    data_skewness = ColumnDataSource(data=dict(
        skewness_teo=skewness_teo,
        skewness_emp=skewness_emp,
        timestep=timestep))

    hover_skew_teo = HoverTool(attachment="above", names=['Theoretical Skewness '],
                               tooltips=[("Theoretical Skewness ", "@skewness_teo"), ("Nstep", "@timestep")])

    hover_skew_emp = HoverTool(attachment="above", names=['Empirical Skewness'],
                               tooltips=[("Empirical Skewness ", "@skewness_emp"), ("Nstep", "@timestep")])

    # x_range = [0, max(timestep)*1.05]
    # y_range = [min(), max(lower_bound) * 1.05]
    p3 = figure(tools=['save, pan, box_zoom, reset, crosshair', hover_skew_teo, hover_skew_emp],
                sizing_mode='scale_both', toolbar_location="right", x_axis_label='Time',
                y_axis_label='Skewness')

    p3.line(x='timestep', y='skewness_teo', source=data_skewness, legend_label="Theoretical Skewness", color="red",
            alpha=0.9,
            line_width=1, name='lower bound')

    p3.line(x='timestep', y='skewness_emp', source=data_skewness, legend_label="Empirical Skewness", color="#0095B6",
            alpha=0.9,
            line_width=1, name='lower bound')

    p3.legend.location = "bottom_right"
    p3.toolbar.active_drag = None

    """Plot kurtosis value : teoretical vs empirical
    """

    data_kurtosis = ColumnDataSource(data=dict(
        kurtosis_teo=kurtosis_teo,
        kurtosis_emp=kurtosis_emp,
        timestep=timestep))

    hover_kurt_teo = HoverTool(attachment="above", names=['Theoretical Kurtosis '],
                               tooltips=[("Theoretical Kurtosis ", "@kurtosis_teo"), ("Nstep", "@timestep")])

    hover_kurt_emp = HoverTool(attachment="above", names=['Empirical Kurtosis'],
                               tooltips=[("Empirical Kurtosis ", "@kurtosis_emp"), ("Nstep", "@timestep")])

    # x_range = [0, max(timestep)*1.05]
    # y_range = [min(), max(lower_bound) * 1.05]
    p4 = figure(tools=['save, pan, box_zoom, reset, crosshair', hover_kurt_teo, hover_kurt_emp],
                sizing_mode='scale_both', toolbar_location="right", x_axis_label='Time',
                y_axis_label='Kurtosis')

    p4.line(x='timestep', y='kurtosis_teo', source=data_kurtosis, legend_label="Theoretical Kurtosis", color="red",
            alpha=0.9,
            line_width=1, name='lower bound')

    p4.line(x='timestep', y='kurtosis_emp', source=data_kurtosis, legend_label="Empirical Kurtosis", color="#0095B6",
            alpha=0.9,
            line_width=1, name='lower bound')
    p4.legend.location = "bottom_right"
    p4.toolbar.active_drag = None

    return p1, p2, p3, p4

# open a browser
