# -*- coding: utf-8 -*-
"""

@author: Diego De Bortoli
"""
import numpy as np
import pandas as pd


def linear_interp(data_df, time):
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

    cumulative_day_count = list(range(days[0], days[-1] + 1))
    daily_time = np.array(cumulative_day_count) / 365
    interest_rate = -np.log(data_df) / time
    spot_rate = np.interp(daily_time, time, interest_rate)  # np.delete(time, (0), axis=0)
    df = np.exp(-spot_rate * daily_time)
    df = list(df)
    daily_time = list(daily_time)
    spot_rate = list(spot_rate)
    if df[0] != 1:
        df.insert(0, 1)
        spot_rate.insert(0, 0)
        daily_time.insert(0, 0)

    return df, spot_rate, daily_time

# import matplotlib.pyplot as plt


# df_curve = plt.plot(cumulative_day_count, df, 'r--', days, data_df, 'bs')
# spot_curve = plt.plot(cumulative_day_count, spot_rate, 'r--')
