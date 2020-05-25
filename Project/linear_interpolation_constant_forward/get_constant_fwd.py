# -*- coding: utf-8 -*-
"""

@author: Diego De Bortoli
"""
import pandas as pd
import numpy as np


def constant_fwd(data_df, time):
    if data_df[0] == 0:
        data_df = data_df.remove(0)
        time = time.remove(0)

    days = []
    for i in range(0, len(time)):
        if time[i] >= 1:
            n_day_years = time[i] * 365
            # n_excess_day = (last_time - int(last_time))*365
            # n_day_from_today = int(round(n_day_years+n_excess_day,0))
            n_day_from_today = int(n_day_years)
            days.append(n_day_from_today)
        else:
            n_day_from_today = int(round(time[i] * 365, 0))
            days.append(n_day_from_today)

    delta_days = []
    for i in range(0, len(days) - 1):
        delta = days[i + 1] - days[i]
        delta_days.append(delta)

    daily_forward = []
    for i in range(0, len(delta_days)):
        df_fwd = (data_df[i + 1] / data_df[i]) ** (1 / delta_days[i])
        daily_forward.append(df_fwd)

    df_spot_all_period = [data_df[0]]
    for i in range(0, len(delta_days)):
        n_days_inrange = list(range(1, delta_days[i]))
        df_spot_one_period = data_df[i] * daily_forward[i] ** np.array(n_days_inrange)
        df_spot_all_period.extend(df_spot_one_period)
        df_spot_all_period.append(data_df[i + 1])

    cumulative_day_count = list(range(days[0], days[-1] + 1))
    daily_time = np.array(cumulative_day_count) / 365

    spot_rate = -np.log(df_spot_all_period) / (np.array(cumulative_day_count) / 365)
    spot_rate = list(spot_rate)
    daily_time = list(daily_time)
    df_spot_all_period = list(df_spot_all_period)

    if df_spot_all_period != 1:
        df_spot_all_period.insert(0, 1)
        spot_rate.insert(0, 0)
        daily_time.insert(0, 0)

    return df_spot_all_period, spot_rate, daily_time

# import matplotlib.pyplot as plt

# df_curve = plt.plot(cumulative_day_count, df_spot_all_period, 'r--', days, data_df, 'bs')
# spot_curve = plt.plot(cumulative_day_count, spot_rate)
