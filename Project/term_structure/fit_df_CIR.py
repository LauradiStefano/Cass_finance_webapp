# -*- coding: utf-8 -*-
"""
Created on Mon Aug  5 15:32:31 2019

@author: Diego
"""
import numpy as np
from get_df_CIR import get_df_CIR

# fit_df_CIR
# This function computes the SSE for the CIR model. 
##
def fit_df_CIR(x,data,flag1,flag2):
## Input & Output arguments
#
#  CIR model: dr(t)=k(theta-r(t))*dt+sigma*(r(t)^0.5*dW(t), r(0)=r0
#  Reference: Brigo-Mercurio, 2006, pag. 64-66
#
# INPUTS
#
#   x: 4x1 Vector. CIR Parameters.
# 		   x[0]=kappa
# 		   x[1]=theta 
# 		   x[2]=sigma
# 		   x[3]=r0
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
    df = get_df_CIR(x,T)
        
    if flag1==0 :
        
        if flag2==0:
              spotmkt=-np.log(market_discount_factor)/T
              spot=-np.log(df)/T
              f=spotmkt-spot
        elif flag2==1:
              
           f=market_discount_factor-df
          
        
    elif flag1==1:
        
        if x[0]<=0 or x[1]<=0 or x[2]<=0 or x[3]<=0 :
            f=10^15
        else :
           if flag2==0:
              spotmkt=-np.log(market_discount_factor)/T
              spot=-np.log(df)/T
              f=np.sum((spotmkt-spot)**2)
           elif flag2==1:
              
              f=sum((market_discount_factor-df)**2)
           
    return f