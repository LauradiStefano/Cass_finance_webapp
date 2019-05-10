# -*- coding: utf-8 -*-
"""
Created on Thu May  9 10:22:01 2019

@author: Diego
"""
import math


def compute_moments(type_choice, parameters):
    type_choice = int(type_choice)

    if type_choice == 1:
        mean = parameters[0]
        variance = parameters[1] ** 2
        skewness = 0
        kurtosis = 3

    elif type_choice == 2:  # VG
        sigma = parameters[1]
        theta = parameters[2]
        kappa = parameters[3]

        mean = theta
        variance = sigma ** 2 + kappa * theta ** 2
        skew_nominatore = theta * kappa * (3 * sigma ** 2 + 2 * kappa * theta ** 2)
        skew_denominatore = (theta + kappa * theta) ** (3 / 2)
        skewness = skew_nominatore / skew_denominatore
        kurtosis = 3 * (1 + 2 * kappa - kappa * sigma ** 4 * (sigma ** 2 + kappa * theta ** 2) ** (-2))

    elif type_choice == 3:  # NIG

        sigma = parameters[1]
        theta = parameters[2]
        kappa = parameters[3]

        mean = sigma * theta / math.sqrt(kappa ** 2 - theta ** 2)
        variance = kappa ** 2 * sigma * (kappa ** 2 - theta ** 2) ** (-3 / 2)
        skewness = 3 * theta * kappa ** (-1) * sigma ** (-0.5) * (kappa ** 2 - theta ** 2) ** (-1 / 4)
        kurtosis = 3 * (1 + (kappa ** 2 + 4 * theta ** 2) / (sigma * kappa ** 2 * math.sqrt(kappa ** 2 - theta ** 2)))

    else:  # type_choice == 4 CGMY
        C = parameters[1];
        G = parameters[2];
        M = parameters[3];
        Y = parameters[4]

        mean = C * (M ** (Y - 1) - G ** (Y - 1)) * math.gamma(1 - Y)
        variance = C * (M ** (Y - 2) + G ** (Y - 2)) * math.gamma(2 - Y)
        skewness_numerator = C * (M ** (Y - 3) - G ** (Y - 3)) * math.gamma(3 - Y)
        skewness_denominator = (C * (M ** (Y - 2) + G ** (Y - 2)) * math.gamma(2 - Y)) ** (3 / 2)
        skewness = skewness_numerator / skewness_denominator
        kurtosis_numerator = C * (M ** (Y - 4) + G ** (Y - 4)) * math.gamma(4 - Y)
        kurtosis_denominator = (C * (M ** (Y - 2) + G ** (Y - 2)) * math.gamma(2 - Y)) ** 2
        kurtosis = 3 + (kurtosis_numerator / kurtosis_denominator)

    return mean, variance, skewness, kurtosis
