# -*- coding: utf-8 -*-
"""
Created on Fri Mar 22 11:35:48 2019

@author: Diego
"""

from get_CharFunc import CharFunc
import numpy as np
import cmath


def CharFuncRN(parameters, type, u, dt, rf, q1):
    drift = (rf - q1) - cmath.log(CharFunc(np.insert(parameters[1:], 0, 0), type, -1j, 1))

    # matlab code drift = (rf-q1)-log(CharFunc([0 xxx(2:end)],type,-1i, 1));

    ret = np.exp(1j * u * drift * dt) * CharFunc(np.insert(parameters[1:], 0, 0), type, u, dt)
    # matlab code ret=exp(1i*u*drift*dt).*CharFunc([0 xxx(2:end)],type,u,dt);
    # ret=CharFunc([drift xxx(2:end)],type,u,dt)

    return ret
