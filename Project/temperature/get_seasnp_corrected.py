# -*- coding: utf-8 -*-
"""
Created on Tue Dec 24 11:44:18 2019

@author: Diego
"""
import numpy as np
import numpy.matlib as matlib

def get_seasnp_corrected(X_Level):
    
    #X_Level = LogTemp
    trend = []
    #trend = zeros(1,365);
    for i in range(0,365):
    #for i = 1:365 np.linspace(0,5,10)
        trend.append(np.mean(X_Level[np.linspace(i,len(X_Level),365)]))
        #trend(i) = mean(X_Level(i:365:end))#-mean(X_Level(i:364+i));
    
    
    
    trend = matlib.repmat(trend,np.ceil(len(X_Level)/365),1)
    detrend_X = X_Level-trend[range(0,len(X_Level))]

    
    #(trend',ceil(length(X_Level)/365),1);
    #detrend_X = X_Level-trend(1:length(X_Level));

    return detrend_X, trend