# -*- coding: utf-8 -*-
"""
Created on Mon Apr 29 16:45:45 2019

@author: Diego
"""
import math

def compute_heston_bounds(mu, Tt, v0, chi, lam, rho, v_hat):
    
    #First cumulant
    c1=mu*Tt + (1-math.exp(-lam*Tt))*((v_hat-v0)/(2*lam))-0.5*v_hat*Tt
    
    #Second cumulant
    first_row = chi*Tt*lam*math.exp(-lam*Tt)*(v0-v_hat)*(8*lam*rho-4*chi)
    second_row = lam*rho*chi*(1-math.exp(-lam*Tt))*(16*v_hat-8*v0)
    third_row = 2*v_hat*lam*Tt*(-4*lam*rho*chi+chi**2+4*lam**2)
    fourth_row = chi**2*((v_hat-2*v0)*math.exp(-2*lam*Tt)+v_hat*(6*math.exp(-lam*Tt)-7)+2*v0)
    fifth_row = 8*lam**2*(v0-v_hat)*(1-math.exp(-lam*Tt))
    c2=(1/(8*lam**3))*(first_row+second_row+third_row+fourth_row+fifth_row)
    
    a = c1-12*math.sqrt(abs(c2))
    b = c1+12*math.sqrt(abs(c2))
    
    return a,b