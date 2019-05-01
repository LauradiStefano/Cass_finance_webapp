# -*- coding: utf-8 -*-
"""
Created on Fri Mar 22 10:57:35 2019

@author: Diego
"""

import math
from get_cumulants_file import get_cumulants


def get_COS_bounds(parameters, type_choice, T, L):
    # Compute the relevant range in the cos method
    print('parameters',parameters)
    c1, c2, c3, c4 = get_cumulants(parameters, type_choice, T)

    xmin = c1 - L * math.sqrt(c2 + math.sqrt(c4))
    xmax = c1 + L * math.sqrt(c2 + math.sqrt(c4))

    return xmin, xmax

# [c1 c2 c3 c4]=get_cumulants(param,type_choice,T)
#
# xmin = c1-L*sqrt(c2+sqrt(c4)) 
# xmax = c1+L*sqrt(c2+sqrt(c4))
