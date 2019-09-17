# -*- coding: utf-8 -*-
"""
Created on Tue Jul 30 14:15:37 2019

@author: Diego
"""
import numpy as np

## get_df_CIR
# This function computes the CIR discount factors.
##
def get_df_CIR(x,ttm) :
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
#   ttm:  nTimesx1 vector of time to maturities (in years) 
#
# OUTPUT
#
#   df:   nTimesx1 vector of discount factors
  
    
    ## Read in
    
# =============================================================================
#     kappa=x[0]
#     theta=x[1]
#     sg=x[2]
#     r0=x[3]  
# =============================================================================
    
    ## Compute the discount factors
    
    df=ZCB_CIR(x,ttm)
    
    if ttm[0]==0:
        df[0]=1
    
    return df




## NESTED FUNCTIONS

## Azcb_Cir
# This function computes the A term in the CIR zcb formula.

def Azcb_Cir(ttm,kappa,theta,sigma):

   ttm = np.array(ttm)
   phi1 = (kappa**2 + 2 * (sigma**2))**0.5
   phi2 = (phi1 + kappa )
   phi3 = 2 * kappa * theta / (sigma**2)

   num = 2 * phi1 * np.exp(phi2 * ttm / 2)
   den = phi2 * (np.exp(phi1 * ttm) - 1) + 2 * phi1
   res= (num / den)**phi3
   
   return res

## Bzcb_Cir
# This function computes the B term in the CIR zcb formula.

def Bzcb_Cir(ttm,kappa,sigma):
    
   ttm = np.array(ttm)

   phi1 = (kappa** 2 + 2 * (sigma**2))**0.5
   phi2 = (phi1 + kappa)
   arg = (np.exp(phi1 * ttm) - 1)
 
   res = 2 * arg / (phi2 * arg + 2 * phi1)
   
   return res

## ZCB_CIR
# This function computes the the CIR zcb price.

def ZCB_CIR(x,ttm):
    
    ttm = np.array(ttm)

    kappa=x[0]
    theta=x[1]
    sigma=x[2]
    r0=x[3]
   
    B= Bzcb_Cir(ttm,kappa,sigma)
    A= Azcb_Cir(ttm,kappa,theta,sigma)

    res = A * np.exp(-B * r0)
   
    return res
