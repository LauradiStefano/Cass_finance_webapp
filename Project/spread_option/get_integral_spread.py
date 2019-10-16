# -*- coding: utf-8 -*-
"""
Created on Fri May 10 11:26:57 2019

@author: Diego
"""
import math

import numpy as np
import scipy.integrate as integrate
from spread_option.get_fc_spread import fc_spread


def integral_spread(K, S1, S2, q1, q2, T, rf, a, b, d, parameter):
    integral = integrate.quad(
        lambda g: np.real(np.exp(-1j * g * b) * fc_spread(K, S1, S2, q1, q2, T, rf, g, a, d, parameter)), 0, 5000)
    res = (np.exp(-d * b - rf * T) / math.pi) * integral[0]
    return res
