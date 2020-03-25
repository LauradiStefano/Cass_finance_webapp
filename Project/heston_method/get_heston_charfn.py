# -*- coding: utf-8 -*-
"""
Created on Mon Apr 29 13:51:41 2019

@author: Diego

"""
import numpy as np


def heston_charfn(u, Tt, v0, chi, lam, rho, v_hat, mu):
    D = np.sqrt((lam - 1j * rho * chi * u) ** 2 + (u ** 2 + 1j * u) * chi ** 2)
    G = (lam - 1j * rho * chi * u - D) / (lam - 1j * rho * chi * u + D)

    # First term of product
    hest_1 = 1j * u * mu * Tt
    hest_2 = (v0 / chi ** 2) * ((1 - np.exp(-D * Tt)) / (1 - G * np.exp(-D * Tt)))
    hest_3 = lam - 1j * rho * chi * u - D

    heston_first_term = np.exp(hest_1 + hest_2 * hest_3)

    # Second term of product

    hest_4 = Tt * (lam - 1j * rho * chi * u - D)
    hest_5 = 2 * np.log((1 - G * np.exp(-D * Tt)) / (1 - G))

    heston_second_term = np.exp(((lam * v_hat) / chi ** 2) * (hest_4 - hest_5))

    heston_charfn = heston_first_term * heston_second_term

    return heston_charfn
