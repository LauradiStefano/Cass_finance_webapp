# -*- coding: utf-8 -*-
"""
Created on Thu Mar 21 17:43:59 2019

@author: Diego
"""
import math


# %cumulants of Levy processes
# %function [c1, c2, c3, c4]=LProc_cumulants(xxx,type_choice,dt)


def get_cumulants(parameters, type_choice, dt):
    type_choice = int(type_choice)

    if type_choice == 1:
        c1, c2, c3, c4 = Norm_cum(parameters, dt)
    elif type_choice == 2:
        c1, c2, c3, c4 = VG_cum(parameters, dt)
    elif type_choice == 3:
        c1, c2, c3, c4 = NIG_cum(parameters, dt)
    else:  # type_choice == 4:
        c1, c2, c3, c4 = CGMY_cum(parameters, dt)

    return c1, c2, c3, c4


def Norm_cum(parameters, dt):
    mu = parameters[0]
    sigma = parameters[1]
    c1 = mu * dt
    c2 = sigma ** 2 * dt
    c3 = 0
    c4 = 0
    return c1, c2, c3, c4


def VG_cum(parameters, dt):
    mu = parameters[0]
    sigma = parameters[1]
    theta = parameters[2]
    kappa = parameters[3]
    c1 = (mu + theta) * dt
    c2 = (sigma ** 2 + theta ** 2 * kappa) * dt
    c3 = kappa * (3 * sigma ** 2 * theta + 2 * theta ** 3 * kappa) * dt
    c4 = 3 * kappa * (sigma ** 4 + 2 * theta ** 4 * kappa ** 2 + 4 * sigma ** 2 * theta ** 2 * kappa) * dt

    return c1, c2, c3, c4


def NIG_cum(parameters, dt):
    mu = parameters[0]
    sigma = parameters[1]
    theta = parameters[2]
    kappa = parameters[3]
    c1 = (mu + theta) * dt
    c2 = (sigma ** 2 + theta ** 2 * kappa) * dt
    c3 = 3 * theta * kappa * (sigma ** 2 + theta ** 2 * kappa) * dt
    c4 = 3 * kappa * (sigma ** 4 + 5 * theta ** 4 * kappa ** 2 + 6 * sigma ** 2 * theta ** 2 * kappa) * dt

    return c1, c2, c3, c4


def CGMY_cum(parameters, dt):
    mu = parameters[0]
    C = parameters[1]
    G = parameters[2]
    M = parameters[3]
    Y = parameters[4]
    c1 = mu * dt + C * math.gamma(1 - Y) * (M ** (Y - 1) - G ** (Y - 1)) * dt
    c2 = C * math.gamma(2 - Y) * (M ** (Y - 2) + G ** (Y - 2)) * dt
    c3 = C * math.gamma(3 - Y) * (M ** (Y - 3) - G ** (Y - 3)) * dt
    c4 = C * math.gamma(4 - Y) * (M ** (Y - 4) + G ** (Y - 4)) * dt

    return c1, c2, c3, c4
