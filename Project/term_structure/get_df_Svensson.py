# -*- coding: utf-8 -*-
"""
Created on Mon Jul 22 10:49:00 2019

@author: Diego
"""
import numpy as np

# This function computes the Svensson discount factors.
##
def get_df_Svensson(x,ttm):
## Input & Output arguments
#
# INPUTS
#
#   x: 4x1 Vector. Svensson parameters.
# 		   x[0]=beta0
# 		   x[1]=beta1 
# 		   x[2]=beta2
# 		   x[3]=beta3
# 		   x[4]=tau1
# 		   x[5]=tau2
#
#   ttm:  nTimesx1 vector of time to maturities (in years) 
#
# OUTPUT
#
#   df:   nTimesx1 vector of discount factors
  
    ttm = np.array(ttm)
    ## Read in
    beta0=x[0]
    beta1=x[1]
    beta2=x[2]
    beta3=x[3]
    tau1=x[4]
    tau2=x[5]
    
    ## Compute the spot rates
    
    spot=beta0+beta1*(1-np.exp(-ttm/tau1))*tau1/ttm+beta2*((1-np.exp(-ttm/tau1))*tau1/ttm-np.exp(-ttm/tau1))+beta3*((1-np.exp(-ttm / tau2))*tau2/ttm-np.exp(-ttm/tau2))
    
    ## Compute the discount factors
    
    df=np.exp(-spot*ttm)
    
    if ttm[0]==0: # change inf result into 1 (python gives warning for inf)
        df[0]=1
        
    return df
