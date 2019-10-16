# -*- coding: utf-8 -*-
"""
Created on Fri May 10 11:15:26 2019

@author: Diego
"""
import math

import numpy as np


def gbm_char_fn(S1, S2, q1, q2, parameter, T, rf, u1, u2):
    v1 = parameter[0]
    v2 = parameter[1]
    rho = parameter[2]

    s1 = math.log(S1)

    s2 = math.log(S2)

    etafn1 = v1 ** 2 * u1 ** 2 + v2 ** 2 * u2 ** 2 + 2 * rho * v1 * v2 * u1 * u2

    etafn2 = (v1 ** 2 * u1 + v2 ** 2 * u2) * 1j

    etafn = -0.5 * (etafn1 + etafn2)

    tmp = 1j * u1 * s1 + 1j * u2 * s2 + etafn * T + u1 * (rf - q1) * T * 1j + u2 * (rf - q2) * T * 1j

    ret = np.exp(tmp)

    return ret
