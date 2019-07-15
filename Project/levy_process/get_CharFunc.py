# -*- coding: utf-8 -*-
"""
Created on Fri Mar 22 11:10:58 2019

@author: Diego
"""
import math

import numpy as np


def CharFunc(parameters, type_choice, u, dt):
    type_choice = int(type_choice)

    if type_choice == 0:
        CharFn = NormCF(parameters, u, dt)
    elif type_choice == 1:
        CharFn = VGCF(parameters, u, dt)
    elif type_choice == 2:
        CharFn = NIGCF(parameters, u, dt)
    else:  # type_choice == 3
        CharFn = CGMYCF(parameters, u, dt)

    ret = CharFn

    return ret


def NormCF(parameters, u, dt):
    mu = parameters[0]
    sigma = parameters[1]
    output = np.exp(dt * (1j * u * mu - 0.5 * sigma ** 2 * u ** 2))

    return output


def VGCF(parameters, u, dt):
    mu = parameters[0]
    sigma = parameters[1]
    theta = parameters[2]
    kappa = parameters[3]
    output = np.exp(1j * u * mu * dt) * (1 - 1j * u * theta * kappa + 0.5 * u ** 2 * sigma ** 2 * kappa) ** (
            -dt / kappa)

    return output


def NIGCF(parameters, u, dt):
    mu = parameters[0]
    sigma = parameters[1]
    theta = parameters[2]
    kappa = parameters[3]
    output = np.exp(
        1j * u * mu * dt + dt / kappa * (1 - np.sqrt(1 + u ** 2 * sigma ** 2 * kappa - 2 * 1j * u * theta * kappa)))

    return output


def CGMYCF(parameters, u, dt):
    mu = parameters[0]
    C = parameters[1]
    G = parameters[2]
    M = parameters[3]
    Y = parameters[4]
    output = np.exp(
        1j * u * mu * dt + C * math.gamma(-Y) * dt * ((M - 1j * u) ** Y - M ** Y + (G + 1j * u) ** Y - G ** Y))

    return output
