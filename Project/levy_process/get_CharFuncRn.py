# -*- coding: utf-8 -*-
"""
Created on Fri Mar 22 11:35:48 2019

@author: Diego
"""

import cmath

import numpy as np

from levy_process.get_CharFunc import CharFunc


def CharFuncRN(parameters, type_choice, u, dt, rf, q1):
    drift = (rf - q1) - cmath.log(CharFunc(np.insert(parameters[1:], 0, 0), type_choice, -1j, 1))

    ret = np.exp(1j * u * drift * dt) * CharFunc(np.insert(parameters[1:], 0, 0), type_choice, u, dt)

    return ret
