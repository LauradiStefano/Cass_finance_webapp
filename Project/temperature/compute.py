# -*- coding: utf-8 -*-
"""
Created on Wed Apr  8 14:03:23 2020

@author: Diego
"""
from bokeh.plotting import figure

import datetime
import pandas as pd
import numpy as np
import math
import os
from scipy.optimize import curve_fit
from statistics import mean


# from get_seasnp_corrected import get_seasnp_corrected
# from statsmodels.tsa.arima_model import ARIMA

def import_dataset_file_excel(filename):
    sheet_name = 'Datinofeb'
    data = pd.read_excel(os.path.join('uploads/', filename, sheet_name=sheet_name))
    return data


def compute_parametric_function(data):
    Old_Snow_Y = (data["Year"].tolist())
    Old_Snow_M = (data["Month"].tolist())
    Old_Snow_D = (data["Day"].tolist())
    Old_Snow_Level = (data["snow data"].tolist())
    Old_Temp_Level = (data["temp"].tolist())

    nm = 0
    Start_Day = 305  # 1st of Nov
    Start_Month = Old_Snow_M[Start_Day]

    Temp_Level = Old_Temp_Level[Start_Day - 1:len(Old_Temp_Level)]

    Temp_Level = [float(i) * 0.1 for i in Temp_Level]
    LogTemp = Temp_Level;

    Snow_Y = Old_Snow_Y[Start_Day - 1:len(Old_Temp_Level)]
    Snow_M = Old_Snow_M[Start_Day - 1:len(Old_Temp_Level)]
    Snow_D = Old_Snow_D[Start_Day - 1:len(Old_Temp_Level)]

    Dates_LogLevel = []
    for i in range(0, len(Snow_Y)):
        Dates_LogLevel.append(datetime.datetime(Snow_Y[i], Snow_M[i], Snow_D[i]))
        # t_dates = (Dates_LogLevel-Dates_LogLevel(1))/365;

    t_dates = []
    for i in range(0, len(Dates_LogLevel)):
        delta = ((Dates_LogLevel[i] - Dates_LogLevel[0]))
        delta = delta.days
        t_dates.append(delta / 365)

    temp_3_9_A = lambda t, a1, a2, a3, a4, omega: a1 + a2 * t + a3 * np.sin(omega * t) + a4 * np.cos(omega * t)
    temp_3_9 = lambda t, a1, a2, a3, a4: a1 + a2 * t + a3 * np.sin(2 * math.pi * t) + a4 * np.cos(2 * math.pi * t)

    popt, pcov = curve_fit(temp_3_9, t_dates, LogTemp, [mean(LogTemp), -0.46, 149.66, -75.69])
    t_date = np.array(t_dates)
    t_dates = np.asarray(t_dates)
    trend_temp_par = temp_3_9_A(t_dates, popt[0], popt[1], popt[2], popt[3], 2 * math.pi)
    R_temp_par = LogTemp - trend_temp_par

    return LogTemp, trend_temp_par


def plot_parametric_function(LogTemp, trend_temp_par):
    x = [i for i in range(len(LogTemp))]
    y = [trend_temp_par[i] for i in x]
    # LogTemp = [ LogTemp(i) for i in len(LogTemp)]

    x_range = [0, 1460]
    y_range = [min([min(y) - 1, min(LogTemp) - 1]), max([max(y) + 1, max(LogTemp) + 1])]
    # p1 = figure(x_range=x_range ,y_range=y_range, title='Temperature seasonality component', tools=TOOLS)
    fig = figure(tools=['save, pan, box_zoom, reset, crosshair'], x_range=x_range,
                 y_range=y_range, sizing_mode='scale_both', toolbar_location="right", x_axis_label='Days',
                 y_axis_label="Λt", title="A Temperature seasonality component")
    fig.line(x, y, line_color="blue", line_width=2)
    fig.circle(x, LogTemp, line_color="blue", line_alpha=0.5, fill_color="yellow", fill_alpha=0.7)

    from bokeh.embed import components
    script, div = components(fig)

    return fig, div
