# -*- coding: utf-8 -*-
"""
Created on Fri May 10 11:20:16 2019

@author: Diego
"""
from spread_option.get_gbm_char_fn import gbm_char_fn


def fc_gen(S1, S2, q1, q2, rf, T, g1, g2, parameter):
    fc = gbm_char_fn(S1, S2, q1, q2, parameter, T, rf, g1, g2)

    return fc
