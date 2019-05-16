# -*- coding: utf-8 -*-
"""
Created on Fri May  3 09:52:17 2019

@author: Diego
"""
import numpy as np
import math 


def gbm_charfn(u, dt, sigma, r):
    
    output = np.exp(dt*(1j*(r-0.5*sigma**2)*u-0.5*sigma**2*u**2))
    

    return output
    

