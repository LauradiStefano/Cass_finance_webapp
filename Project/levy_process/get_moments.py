# -*- coding: utf-8 -*-
"""
Created on Thu May  9 10:22:01 2019

@author: Diego
"""

import math


def Power(a,b):
    result = a**b
    
    return result

def compute_moments(type_choice, parameters, dt):
    type_choice = int(type_choice)

    if type_choice == 0:
        mean = parameters[0]*dt #corretto
        variance = (parameters[1]*math.sqrt(dt)) ** 2 #corretto
        skewness = 0
        kurtosis = 3
        
        m1 = mean
        m2 = mean**2 + variance
        m3 = mean**3+3*mean*variance #corretto
        m4 = mean**4+6*mean**2*variance+3*variance**2 #corretto
        
        mc1= m1
        mc2= variance
        mc3= 0
        mc4= 3*variance**2 #ricontrollo formula
        
        c1_x = mc1
        c2_x = mc2
        c3_x = mc3
        c4_x = mc4-3*mc2**2 #check cumulanti normale
        
        excess_kurtosis = c4_x/mc2**2

        
        
        
    elif type_choice == 1:  # VG #corretto
        mu = parameters[0]
        sigma = parameters[1]
        theta = parameters[2]
        kappa = parameters[3]
        
        
        c1_x = (mu+theta)*dt;
        c2_x = (sigma**2+theta**2*kappa)*dt;
        c3_x = kappa*(3*sigma**2*theta+2*theta**3*kappa)*dt;
        c4_x = 3*kappa*(sigma**4+2*theta**4*kappa**2+4*sigma**2*theta**2*kappa)*dt;
        
        m1 = c1_x
        m2 = c2_x + c1_x**2
        m3 = c3_x + 3*c2_x*c1_x + c3_x**3
        m4 = c4_x + 4*c3_x*c1_x + 3*c2_x**2+6*c2_x*c1_x**2 + c1_x**4
        
        mc1 = m1
        mc2 = m2-m1**2
        mc3 = 2*m1**3-3*m1*m2+m3
        mc4 = -3*m1**4+6*m1**2*m2-4*m1*m3+m4
        
        mean = mc1
        variance = mc2
        skewness=mc3/mc2**(3/2)
        kurtosis=mc4/mc2**2
        excess_kurtosis = c4_x/mc2**2
#            mean = theta
#            variance = sigma ** 2 + kappa * theta ** 2
#            skew_nominatore = theta * kappa * (3 * sigma ** 2 + 2 * kappa * theta ** 2)
#            skew_denominatore = (theta + kappa * theta) ** (3 / 2)
#            skewness = skew_nominatore / skew_denominatore
#            kurtosis = 3 * (1 + 2 * kappa - kappa * sigma ** 4 * (sigma ** 2 + kappa * theta ** 2) ** (-2))
    
    else :
        if type_choice == 2:  # NIG corretto
            
            mu=parameters[0] 
            sigma=parameters[1]
            theta=parameters[2]
            kappa=parameters[3];
    
            m1 = dt* (mu + theta) #correct
            m2 = dt* (sigma**2 + kappa*theta**2 + dt *(mu + theta)**2) #correct
            m3 = dt* (dt**2* (mu + theta)**3 + 3* kappa *theta *(sigma**2 + kappa* theta**2) + 3* dt *(mu + theta) *(sigma**2 + kappa *theta**2))
            m4 = dt *(3* kappa *sigma**4 + 18 *kappa**2 *sigma**2 *theta**2 + 15* kappa**3 *theta**4 + dt**3 *(mu + theta)**4 + 
                      12* dt* kappa *theta* (mu + theta)* (sigma**2 + kappa *theta**2) + 6 *dt**2*(mu + theta)**2*(sigma**2 + kappa*theta**2) + 
                      3 *dt* (sigma**2 + kappa* theta**2)**2)
    
        else:  # type_choice == 3 CGMY corretto
            mu = parameters[0]
            C = parameters[1]
            G = parameters[2]
            M = parameters[3]
            Y = parameters[4]
    
            m1 = dt*(mu+C*(Power(G,-1 + Y) - Power(M,-1 + Y))*Y*math.gamma(-Y)) # correct 
    
            m2 = (dt*(C*(Power(G,Y)*Power(M,2) + Power(G,2)*Power(M,Y))*(-1 + Y)*Y*math.gamma(-Y) + 
                      dt*Power(G*M*mu - C*(-(Power(G,Y)*M) + G*Power(M,Y))*Y*math.gamma(-Y),2)))/(Power(G,2)*Power(M,2)) # correct
            
            
            m3 = -(dt*((C*(-(Power(G,Y)*Power(M,3)) + Power(G,3)*Power(M,Y))*(-2 + Y)*(-1 + Y)*Y*math.gamma(-Y))/(Power(G,3)*Power(M,3)) - 
                       Power(dt,2)*Power(mu + C*(Power(G,-1 + Y) - Power(M,-1 + Y))*Y*math.gamma(-Y),3) + (3*C*dt*(Power(G,Y)*Power(M,2) +
                       Power(G,2)*Power(M,Y))*(-1 + Y)*Y*math.gamma(-Y)*(-(G*M*mu) + C*(-(Power(G,Y)*M) + G*Power(M,Y))*Y*math.gamma(-Y)))/(Power(G,3)*Power(M,3))))#recheck
            
            m4 = dt*((C*(Power(G,Y)*Power(M,4) + Power(G,4)*Power(M,Y))*(-3 + Y)*(-2 + Y)*(-1 + Y)*Y*math.gamma(-Y))/(Power(G,4)*Power(M,4)) + 
                     3*Power(C,2)*dt*Power(Power(G,-2 + Y) + Power(M,-2 + Y),2)*Power(-1 + Y,2)*Power(Y,2)*Power(math.gamma(-Y),2) + 
                     Power(dt,3)*Power(mu + C*(Power(G,-1 + Y) - Power(M,-1 + Y))*Y*math.gamma(-Y),4) + (6*C*Power(dt,2)*(Power(G,Y)*Power(M,2) +
                     Power(G,2)*Power(M,Y))*(-1 + Y)*Y*math.gamma(-Y)*Power(G*M*mu - C*(-(Power(G,Y)*M) + G*Power(M,Y))*Y*math.gamma(-Y),2))/
                     (Power(G,4)*Power(M,4)) + (4*C*dt*(-(Power(G,Y)*Power(M,3)) + Power(G,3)*Power(M,Y))*(-2 + Y)*(-1 + Y)*Y*math.gamma(-Y)*(-(G*M*mu) + 
                     C*(-(Power(G,Y)*M) + G*Power(M,Y))*Y*math.gamma(-Y)))/(Power(G,4)*Power(M,4))) 
        
        #Compute central moments
        mc1=m1
        mc2=m2-m1**2
        mc3=2*m1**3-3*m1*m2+m3
        mc4=-3*m1**4+6*m1**2*m2-4*m1*m3+m4
        
        c1_x = mc1
        c2_x = mc2
        c3_x = mc3
        c4_x = mc4-3*mc2**2
        #print(c1_x,c2_x,c3_x,c4_x)
        
        mean = mc1
        variance = mc2
        skewness=mc3/mc2**(3/2)
        kurtosis=mc4/mc2**2
        excess_kurtosis = c4_x/mc2**2

    return mean, variance, skewness, kurtosis # excess_kurtosis, m1, m2, m3, m4, mc1, mc2, mc3, mc4, c1_x, c2_x, c3_x, c4_x mean, variance, skewness, kurtosis, excess_kurtosis
