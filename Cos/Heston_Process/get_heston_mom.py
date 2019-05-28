# -*- coding: utf-8 -*-
"""
Created on Tue May 28 09:36:56 2019

@author: Diego
"""
import numpy as np

def Power(x,y):

    out=x**y
    
    return out

def momHeston(kappa, theta, sigma, rho, tau, r, S0, v0, central):

    # Heston parameters:
#    kappa  = variance mean reversion speed parameter
#    theta  = variance long-run level parameter
#    rho    = correlation between two Brownian motions
#    sigma  = volatility of variance
#    v0      = initial variance
#    S0      = initial stock price

#Log of the stock price.
    x0 = np.log(S0);

#powers of parameters
    x02=x0**2; x03=x0**3;
    v02=v0**2;
    r2=r**2; r3=r**3;
    sg2=sigma**2; sg3=sigma**3; sg4=sigma**4;
    k2=kappa**2; k3=kappa**3;
    k4=kappa**4; k5=kappa**5;
    k6=kappa**6; k7=kappa**7;
    th2=theta**2; th3=theta**3;
    tau2=tau**2; tau3=tau**3;
    rho2=rho**2; rho3=rho**3;



#First moment
    m1=x0+(r-theta/2)*tau+(theta-v0)*(1-np.exp(-kappa*tau))/(2*kappa);

#Second moment
    m2=(sg2*(theta - 2*v0) + 2*kappa*(theta - v0)**2 + \
      4*np.exp(kappa*tau)*(sg2*theta - kappa*(rho*sigma*(4*theta - 2*v0) + \
      (theta - v0)*(-(sg2*tau) + theta - v0)) + 
      k2*(theta - v0)*(2 - 2*r*tau - 2*rho*sigma*tau + tau*theta - 2*x0)) + \
      np.exp(2*kappa*tau)*(2*kappa*(sg2*tau*theta + rho*sigma*(8*theta - 4*v0) +(theta - v0)**2) + sg2*(-5*theta + 2*v0) + \
      2*k3*(4*(r*tau)**2 + (tau*theta)**2 - 4*r*tau*(tau*theta - 2*x0) - 4*tau*theta*(-1 + x0) + \
      4*(x0)**2) - 4*k2*(tau*th2 + 2*v0*(-1 + r*tau + x0) - theta*(-2 + 2*r*tau - 2*rho*sigma*tau + tau*v0 + 2*x0))))/(8.*np.exp(2*kappa*tau)*k3)

#Third moment
    m3=(-(sg4*(theta - 3*v0)) - 2*k2*(theta - v0)**3 - 3*kappa*sg2*(th2 - 3*theta*v0 + 2*v02) +  
         3*np.exp(kappa*tau)*(2*sg4*(-theta + v0) + kappa*sg2*\
         (-3*th2 + 4*rho*sigma*(2*theta - 3*v0) - 2*sg2*tau*(theta - 2*v0) + theta*v0 + 2*v02) - \
         2*k3*(theta - v0)**2*(4 - 2*r*tau - 4*rho*sigma*tau + tau*theta - 2*x0) + \
         k2*(4*rho*sg3*tau*(theta - 2*v0) + 2*(theta - v0)**3 + 8*rho*sigma \
         *(2*th2 - 3*theta*v0 + v02) + 
         sg2*(-5*tau*th2 - 4*v0*(-2 + r*tau + tau*v0 + x0) + 2*theta*(-2 + r*tau + 5*tau*v0 + x0)))) + \
         np.exp(3*kappa*tau)*(2*sg4*(11*theta - 3*v0) - \
         3*kappa*sg2*(2*sg2*tau*theta + 5*th2 + 4*rho*sigma*(10*theta - 3*v0) - 7*theta*v0 + 2*v02) +
         6*k4*(4*r2*tau2*(theta - v0) - 
         4*r*tau*(tau*th2 + theta*(2 + 2*rho*sigma*tau - tau*v0 - 2*x0) + 2*v0*(-1 + x0)) + 4*rho*sigma*tau*theta*(2 + tau*theta - 2*x0) +
         (theta - v0)*(tau2*th2 - 4*tau*theta*(-2 + x0) + 4*(-2 + x0)*x0)) + \
         2*k5*(8*r3*tau3 - tau3*th3 - 12*r2*tau2*(tau*theta - 2*x0) + \
         6*tau2*th2*(-2 + x0) - 12*tau*theta*(-2 + x0)*x0 + 8*x03 + \
         6*r*tau*(tau2*th2 - 4*tau*theta*(-1 + x0) + 4*x02)) + \
         k2*(36*rho*sg3*tau*theta + 2*(theta - v0)**3 + 24*rho*sigma*(2*th2 - 3*theta*v0 + v02) +
         3*sg2*(7*tau*th2 + 2*theta*(10 + 24*rho2 - 5*r*tau - 2*tau*v0 - 5*x0) + 4*v0*(-2 - 4*rho2 + r*tau + x0)))\
         - 6*k3*(8*rho2*sg2*tau*theta + \
         (sg2*tau*theta + (theta - v0)**2)*(4 - 2*r*tau + tau*theta - 2*x0) + \
         4*rho*sigma*(3*tau*th2 + 2*v0*(-1 + r*tau + x0) - 2*theta*(-2 + 2*r*tau + tau*v0 + 2*x0)))) -
         3*np.exp(2*kappa*tau)*(sg4*(5*theta + v0) + kappa*sg2*\
         (-32*rho*sigma*theta - 9*th2 + sg2*tau*(6*theta - 2*v0) + 11*theta*v0 - 2*v02) + \
         2*k2*(sg4*tau2*(theta - v0) + (theta - v0)**3 + 8*rho*sg3*tau*(-2*theta + v0) +
         8*rho*sigma*(2*th2 - 3*theta*v0 + v02) + \
         sg2*(tau*th2 - 2*v0*(4*rho2 + tau*v0) + theta*(8 + 24*rho2 - 4*r*tau + 3*tau*v0 - 4*x0))) +
         2*k4*(theta - v0)*(4*r2*tau2 + 4*rho2*sg2*tau2 + 8*tau*theta + \
         tau2*th2 - 4*rho*sigma*tau*(2 + tau*theta - 2*x0) - 8*x0 - 4*tau*theta*x0 + 4*x02 + \
         4*r*tau*(-2 + 2*rho*sigma*tau - tau*theta + 2*x0)) + \
         4*k3*(4*rho2*sg2*tau*(2*theta - v0) + \
         (theta - v0)*(sg2*tau - theta + v0)*(4 - 2*r*tau + tau*theta - 2*x0) + \
         2*rho*sigma*(-2*tau*th2 + v0*(2 - 2*r*tau + sg2*tau2 + tau*v0 - 2*x0) + \
         theta*(-4 + 4*r*tau - sg2*tau2 + 4*x0)))))/(16.*np.exp(3*kappa*tau)*k5);

#Fourth moment
    m4=(3*kappa*Power(sg2*(theta - 2*v0) + np.exp(2*kappa*tau)* \
       (8*k3*tau*theta - 8*k2*(theta + rho*sigma*tau*theta - v0) + sg2*(-5*theta + 2*v0) + \
        2*kappa*sigma*(8*rho*theta + sigma*tau*theta - 4*rho*v0)) + \
        4*np.exp(kappa*tau)*(sg2*theta - 2*k2*(-1 + rho*sigma*tau)*(theta - v0) + \
        kappa*sigma*(-4*rho*theta + sigma*tau*theta + 2*rho*v0 - sigma*tau*v0)),2) + \
        sg2*(3*sg4*(theta - 4*v0) + 24*np.exp(kappa*tau)*sg2*\
        (-2*k2*(-1 + rho*sigma*tau)*(theta - 3*v0) + sg2*(theta - 2*v0) + \
        kappa*sigma*(sigma*tau*(theta - 3*v0) + rho*(-4*theta + 10*v0))) + \
        3*np.exp(4*kappa*tau)*(64*k5*(1 + 4*rho2)*tau*theta + 4*kappa*sg3*(5*sigma*tau*theta + 8*rho*(22*theta - 5*v0)) +
        32*k3*sigma*(3*sigma*tau*theta + 12*rho2*sigma*tau*theta + 4*rho*(10*theta - 3*v0) + 8*rho3*(4*theta - v0)) + \
        sg4*(-93*theta + 20*v0) - 32*k2*sg2*\
        ((11 + 50*rho2 + 5*rho*sigma*tau)*theta - 3*(v0 + 4*rho2*v0)) - \
        32*k4*((5 + 24*rho2 + 12*rho*sigma*tau + 8*rho3*sigma*tau)*theta - 2*(v0 + 4*rho2*v0))) + \
        12*np.exp(2*kappa*tau)*(sg4*(7*theta - 4*v0) + \
        8*k4*(1 - 4*rho*sigma*tau + 2*rho2*sg2*tau2)*(theta - 2*v0) + \
        2*kappa*sg3*(-24*rho*theta + 5*sigma*tau*theta + 20*rho*v0 - 6*sigma*tau*v0) + \
        4*k2*sg2*((6 + 20*rho2 - 14*rho*sigma*tau + sg2*tau2)*theta - \
        2*(3 + 12*rho2 - 10*rho*sigma*tau + sg2*tau2)*v0) + \
        8*k3*sigma*(4*rho2*sigma*tau*(2*theta - 3*v0) + 3*sigma*tau*(theta - 2*v0) - \
        2*rho*((4 + sg2*tau2)*theta - 2*(3 + sg2*tau2)*v0))) - \
        8*np.exp(3*kappa*tau)*(16*k6*rho2*tau2*(-3 + rho*sigma*tau)*(theta - v0) - 3*sg4*(7*theta + 2*v0) - \
        6*k2*sg2*((15 + 80*rho2 - 35*rho*sigma*tau + 2*sg2*tau2)*theta + \
        (3 + 7*rho*sigma*tau - sg2*tau2)*v0) - \
        24*k5*tau*((2 - 4*rho*sigma*tau - 4*rho3*sigma*tau + rho2*(8 + sg2*tau2))*theta + \
        (-2 + 4*rho*sigma*tau + 2*rho3*sigma*tau - rho2*(4 + sg2*tau2))*v0) + \
        12*k4*((-4 + 24*rho3*sigma*tau - 3*sg2*tau2 + rho*sigma*tau*(32 + sg2*tau2) - \
        2*rho2*(12 + 7*sg2*tau2))*theta + \
        (-8*rho3*sigma*tau + 3*sg2*tau2 + 8*rho2*(1 + sg2*tau2) - \
        rho*sigma*tau*(16 + sg2*tau2))*v0) + 3*kappa*sg3*(sigma*tau*(-9*theta + v0) + 10*rho*(6*theta + v0)) + \
        2*k3*sigma*(48*rho3*(4*theta - v0) + 24*rho2*sigma*tau*(-10*theta + 3*v0) + \
        6*rho*((32 + 7*sg2*tau2)*theta - 4*sg2*tau2*v0) + \
        sigma*tau*((-54 - sg2*tau2)*theta + (18 + sg2*tau2)*v0)))) + \
        8*kappa*sigma*(-(sg3*(theta - 3*v0)) - 6*np.exp(kappa*tau)*sigma*\
        (-2*k2*(-1 + rho*sigma*tau)*(theta - 2*v0) + sg2*(theta - v0) + \
        kappa*sigma*(sigma*tau*(theta - 2*v0) + rho*(-4*theta + 6*v0))) + \
        2*np.exp(3*kappa*tau)*(24*k4*rho*tau*theta + sg3*(11*theta - 3*v0) - \
        3*kappa*sg2*(20*rho*theta + sigma*tau*theta - 6*rho*v0) - \
        12*k3*(4*rho*theta + sigma*tau*theta + 2*rho2*sigma*tau*theta - 2*rho*v0) + \
        6*k2*sigma*((5 + 12*rho2 + 3*rho*sigma*tau)*theta - 2*(v0 + 2*rho2*v0))) - \
        3*np.exp(2*kappa*tau)*(8*k4*rho*tau*(-2 + rho*sigma*tau)*(theta - v0) + sg3*(5*theta + v0) + \
        2*k2*sigma*((8 + 24*rho2 - 16*rho*sigma*tau + sg2*tau2)*theta - \
        (8*rho2 - 8*rho*sigma*tau + sg2*tau2)*v0) - 2*kappa*sg2*(16*rho*theta + sigma*tau*(-3*theta + v0)) + \
        8*k3*(2*sigma*tau*(theta - v0) + 2*rho2*sigma*tau*(2*theta - v0) + \
        rho*((-4 - sg2*tau2)*theta + (2 + sg2*tau2)*v0))))*\
        (-theta + v0 + np.exp(kappa*tau)*(theta - v0 + kappa*(2*r*tau - tau*theta + 2*x0))) + \
        12*k2*(sg2*(theta - 2*v0) + np.exp(2*kappa*tau)*\
        (8*k3*tau*theta - 8*k2*(theta + rho*sigma*tau*theta - v0) + sg2*(-5*theta + 2*v0) + \
        2*kappa*sigma*(8*rho*theta + sigma*tau*theta - 4*rho*v0)) + \
        4*np.exp(kappa*tau)*(sg2*theta - 2*k2*(-1 + rho*sigma*tau)*(theta - v0) + \
        kappa*sigma*(-4*rho*theta + sigma*tau*theta + 2*rho*v0 - sigma*tau*v0)))*\
        (-theta + v0 + np.exp(kappa*tau)*(theta - v0 + kappa*(2*r*tau - tau*theta + 2*x0)))**2 + \
        4*k3*(-theta + v0 + np.exp(kappa*tau)*(theta - v0 + kappa*(2*r*tau - tau*theta + 2*x0)))**4)/\
        (64.*np.exp(4*kappa*tau)*k7);
        
    if central==0:
        moments=[m1, m2, m3, m4]
        
    elif central==1:
        variance=(m2-m1**2);
        sk=(m3-3*m1*sd**2-m1**3)/sd**3;
        kur=(m4-4*m1*m3+6*m1**2*sd**2+3*m1**4)/sd**4;
        moments =[m1, sd, sk, kur]
        
    return m1, sd, sk, kurt
            

  