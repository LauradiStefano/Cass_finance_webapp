# -*- coding: utf-8 -*-
"""
Created on Mon Jul 22 11:04:35 2019

@author: Diego
"""
from scipy.interpolate import interp1d
import numpy as np

## get_df_linear_interpolation
# This function returns the riskless discount factors corresponding
# to a given  vector of time to maturity (in years), by linear interpolation
# of the spot rates.

##

def get_df_linear_interpolation(data_df,time):

## Input & Output arguments
# 
# INPUTS
#
#   time: vector of time to maturity (in years)
#
#   data_df: nTimes×2 matrix of the term structure market table from the
#            boostrapping procedure 
#            -> Column 1 = nTimes×1 vector of market times (in years)
#            -> Column 2 = nTimes×1 vector of market discount factors
#
# OUPUT
#
#   df: discount factors by linear interpolation 

    
    ## Compute discount factors
    if data_df[0,0]==0:
        data_df = np.delete(data_df, (0), axis=0)
        
    
    T=data_df[:,0]
    log_value = -np.log(data_df[:,1])/T
    y=np.interp(time, T, log_value) #np.delete(time, (0), axis=0)
    df=np.exp(-y*time)
    
    if time[0]==0:
        df[0]=1

    return df