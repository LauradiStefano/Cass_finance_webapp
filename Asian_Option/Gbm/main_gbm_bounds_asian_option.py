# -*- coding: utf-8 -*-
"""
Created on Fri May  3 09:56:26 2019

@author: Diego
"""
import matplotlib.pyplot as plt
from get_gbm_charfn import gbm_charfn
import numpy as np
from get_gbm_phi import gbm_phi
import math
from get_gbm_option import gbm_option

s0= 100
N =50
strike=100
risk_free = 0.04
sigma = 0.3
time = 1

#S0= 100
#n =50
#N=n
#K=100
#r = 0.04
#sigma = 0.3
#T = 1

def  compute_values(s0, strike, time, risk_free, N, sigma):
    
    Ptrue, strike_Exp_lcr, Ptrue_strike, lam  = gbm_option(s0, strike, time, risk_free, N, sigma)
    Ptrue_strike=Ptrue_strike[0]
    return Ptrue, strike_Exp_lcr, Ptrue_strike, lam#plot





#output = gbm_phi(g1, g2, n, N, dt, sigma, r, S0)
#plt.figure(1)
#
## Pdf prices,Pdf logPrices 1
#
#plt.plot(u,output)
##plt.yscale('Pdf prices,Pdf logPrices')
#plt.title('term')
#plt.grid(True)


