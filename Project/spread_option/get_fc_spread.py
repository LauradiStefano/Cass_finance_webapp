# -*- coding: utf-8 -*-
"""
Created on Fri May 10 11:23:33 2019

@author: Diego
"""

import numpy as np
from spread_option.get_fc_gen import fc_gen


def fc_spread(K, S1, S2, q1, q2, T, rf, g, a, delta, parameter):
    term1 = fc_gen(S1, S2, q1, q2, rf, T, g - 1j * delta - 1j, -a * (g - 1j * delta), parameter)

    term2 = fc_gen(S1, S2, q1, q2, rf, T, g - 1j * delta, -a * (g - 1j * delta) - 1j, parameter)

    term3 = K * fc_gen(S1, S2, q1, q2, rf, T, g - 1j * delta, -a * (g - 1j * delta), parameter)

    term4 = np.exp(1j * (g - 1j * delta) * np.log(fc_gen(S1, S2, q1, q2, rf, T, 0, -1j * a, parameter)))

    fc = (term1 - term2 - term3) * term4 / (1j * g + delta)

    return fc
