# -*- coding: utf-8 -*-
"""
Created on Wed Jul 31 17:46:28 2019

@author: Diego
"""
import numpy as np
from get_df_Svensson import get_df_Svensson
## fit_df_Svensson
# This function computes the SSE for the Svensson model.
##
def fit_df_Svensson(x,data,flag1,flag2):
## Input & Output arguments
#
# INPUTS
#
#   x: 4x1 Vector. Svensson parameters.
# 		   x(1)=beta0
# 		   x(2)=beta1 
# 		   x(3)=beta2
# 		   x(4)=beta3
# 		   x(5)=tau1
# 		   x(6)=tau2
#
#   data:  nTimesx2 Matrix. first column provides the ttm and the second column
# 		   Col1 = times to maturity (in years)
# 		   COl2 = arket discount factors
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
    #df =get_df_Svensson(x,T)

    
    beta0=x[0] 
    beta1=x[1] 
    beta2=x[2] 
    beta3=x[3] 
    tau1=x[4] 
    tau2=x[5]
    
    spot=beta0 + beta1 * (1 - np.exp(-T / tau1)) * tau1 / T+ beta2 * ((1 - np.exp(-T / tau1)) * tau1 / T - np.exp(-T / tau1))  + beta3 * ((1 - np.exp(-T / tau2)) * tau2 / T - np.exp(-T /tau2))
       
    if flag1==0:
       
        if flag2==0:
            spotmkt=-np.log(market_discount_factor)/T
            f=spotmkt-spot
        elif flag2==1:
            df = np.exp(-T*spot)
            f=market_discount_factor-df
        
        
    elif flag1==1:
       
        if beta0<=0 or beta0+beta1<=0 or tau1<=0 or tau2<=0 :
            f=10^15
        else :
           if flag2==0:
              spotmkt=-np.log(market_discount_factor)/T
              f=np.sum((spotmkt-spot)**2)
           elif flag2==1:
              df = np.exp(-T*spot)
              f=np.sum((market_discount_factor-df)**2)
                   
        
    return f
    
   

   