# -*- coding: utf-8 -*-
"""
Created on Tue Sep 10 15:17:49 2019

@author: Diego
"""

import pandas as pd
import numpy as np
import os

from scipy import optimize
from scipy.optimize import least_squares
from fit_df_Vasicek import fit_df_Vasicek
from fit_df_Svensson import fit_df_Svensson
from fit_df_NelsonSiegel import fit_df_NelsonSiegel
from fit_df_CIR import fit_df_CIR  
from get_df_Vasicek import get_df_Vasicek
from get_df_Svensson import get_df_Svensson
from get_df_NelsonSiegel import get_df_NelsonSiegel
from get_df_CIR import get_df_CIR

def upload_input(filename=None):
    data = pd.read_excel(os.path.join('uploads/', filename))

return data
    

def fitting_method(model, x0, data, flag1, flag2):
    
    ttm = (data["Maturity"].tolist())
    market_discount_factor = (data["Discount Factor"].tolist())
    
    if model == 1:
 
        if flag1 ==0:
        
            res_1 = least_squares(lambda y : fit_df_Vasicek(y,data,flag1,flag2), x0 )
            param = res_1.x
            discount_factor = get_df_Vasicek(param, ttm)

        else:
        
            param = optimize.fmin(lambda y : fit_df_Vasicek(y,data,flag1,flag2),x0)
            discount_factor = get_df_Vasicek(param, ttm)


    elif model == 2:
 
        if flag1 ==0:
            
            res_1 = least_squares(lambda y : fit_df_CIR(y,data,flag1,flag2), x0 )
            param = res_1.x
            discount_factor = get_df_CIR(param, ttm)
    
        else:
            
            param = optimize.fmin(lambda y : fit_df_CIR 
                                    (y,data,flag1,flag2),x0)
            
            discount_factor = get_df_CIR(param, ttm)
        

    elif model == 3:
 
        if flag1 ==0:
            
            res_1 = least_squares(lambda y : fit_df_NelsonSiegel(y,data,flag1,flag2), x0 )
            param = res_1.x
            discount_factor = get_df_NelsonSiegel(param, ttm)
    
        else:
            
            param = optimize.fmin(lambda y : fit_df_NelsonSiegel
                                    (y,data,flag1,flag2),x0)
            
            discount_factor = get_df_NelsonSiegel(param, ttm)
        
    else :
    
        if flag1 ==0:
    
            res_1 = least_squares(lambda y : fit_df_Svensson(y,data,flag1,flag2), x0 )
            param = res_1.x
            discount_factor = get_df_Svensson(param, ttm)

        else: 
    
            param = optimize.fmin(lambda y : fit_df_Svensson
                            (y,data,flag1,flag2),x0)
    
            discount_factor = get_df_Svensson(param, ttm)
            

    model_discount_factor = discount_factor

    model_spot_rate = -np.log(model_discount_factor)/ttm
    market_spot_rate = -np.log(market_discount_factor)/ttm
    
    discount_factor_model_error = (model_discount_factor - market_discount_factor)**2
    spot_rate_model_error = (model_spot_rate - market_spot_rate )**2
    
    
    return market_discount_factor, market_spot_rate, model_discount_factor, model_spot_rate, discount_factor_model_error, spot_rate_model_error, param
