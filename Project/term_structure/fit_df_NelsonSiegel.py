# -*- coding: utf-8 -*-
"""
Created on Wed Jul 31 18:09:44 2019

@author: Diego
"""
import numpy as np

## fit_df_NelsonSiegel
# This function computes the SSE for the Nelson-Siegel model.
##
def fit_df_NelsonSiegel(x,data,flag1,flag2):
## Input & Output arguments
#
# INPUTS
#
#   x: 4x1 Vector. Nelson-Siegel parameters.
# 		   x[0]=beta0
# 		   x[1]=beta1 
# 		   x[2]=beta2
# 		   x[3]=tau1
#
#   data:  nTimesx2 Matrix. first column provides the ttm and the second column
# 		   Col1 = times to maturity (in years)
# 		   COl2 = market discount factors
#
#   flag1: Scalar. Choose optimization procedure.
# 		   flag1 = 0 -> lsqnonlin
# 		   flag1 = 1 -> fminsearch  
#
#   flag2: Scalar. Choose objective function.
# 		   flag = 0 -> SSE between model and market spot rates
# 		   flag = 1 -> SSE between model and market discount factors
#
# OUTPUT
#
#   f:     SSE
    ## Compute the SSE
    
    T = np.array(data["Maturity"].tolist())
    market_discount_factor = np.array(data["Discount Factor"].tolist())

    beta0=x[0]
    beta1=x[1] 
    beta2=x[2]
    tau1=x[3]  
    
    spot = beta0 + beta1 * (1 - np.exp(-T / tau1)) * tau1 / T + beta2 * ((1 - np.exp(-T / tau1)) * tau1 / T - np.exp(-T / tau1))
   
    if flag1==0 :
 
        if flag2==0 :
            spotmkt=-np.log(market_discount_factor)/T
            f=spotmkt-spot
        elif flag2==1:
            df = np.exp(-T*spot)
            f=market_discount_factor-df
     
        
        
    elif flag1==1:
        
        if beta0<=0 or beta0+beta1<=0 or tau1<=0:
            f=10^15
        else: 
           if flag2==0:
              spotmkt=-np.log(market_discount_factor)/T
              f=np.sum((spotmkt-spot)**2)
           elif flag2==1:
              df = np.exp(-T*spot)
              f=np.sum((market_discount_factor-df)**2)

    return f