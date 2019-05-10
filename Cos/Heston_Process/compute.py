# -*- coding: utf-8 -*-
"""
Created on Thu May  9 12:24:34 2019

@author: Diego
"""
import numpy as np
from get_heston_cos_pdf import get_pdf_cos
from get_heston_bounds import compute_heston_bounds
from get_heston_option_prices import get_cos_prices
from getbs import find_vol

#Inputs

#s0 = 100
#strike_min = s0*0.50
#strike_max = s0*1.50
#nk=50
#strikes= np.linspace ( strike_min , strike_max , nk )
#time = 1
#call_put = 1
#mu = 0
#v0 = 0.0175     #0.0175 
#v_hat = 0.0175   #0.0398  
#lam = 0.00000001 #1.5768 
#chi = 0.00000001 #0.5751       
#rho = 0.00000001 #-0.5711  
#risk_free = 0
#dividend_yield = 0
#N=1000

#Pdf Heston Model
def heston_pdf_and_volatility(s0, strike_min, strike_max, time, v0, chi, lam, rho, v_hat, mu, risk_free, dividend_yield, call_put  ):
    heston_pdf = get_pdf_cos(time, v0, chi, lam, rho, v_hat, mu )
    nk=50
    a,b = compute_heston_bounds(mu, time, v0, chi, lam, rho, v_hat)
    N = 1000
    returns = np.linspace(a,b,N)
    
    strike = np.linspace (strike_min, strike_max, nk )
    option_prices = get_cos_prices(mu,s0, strike, risk_free, dividend_yield, time, v0, chi, lam, rho, v_hat, call_put)
    
    
    volatility = find_vol(option_prices, call_put, s0, strike, time, risk_free, dividend_yield)
    
    return heston_pdf, returns, volatility, strike



 
 




