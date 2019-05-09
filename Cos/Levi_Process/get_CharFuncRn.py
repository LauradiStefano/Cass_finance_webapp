# -*- coding: utf-8 -*-
"""
Created on Fri Mar 22 11:35:48 2019

@author: Diego
"""

from get_CharFunc import CharFunc
import numpy as np
import cmath


def CharFuncRN(parameters, type_choice, u, dt, rf, q1):
    drift = (rf - q1) - cmath.log(CharFunc(np.insert(parameters[1:], 0, 0), type_choice, -1j, 1))



    ret = np.exp(1j * u * drift * dt) * CharFunc(np.insert(parameters[1:], 0, 0), type_choice, u, dt)


    return ret
