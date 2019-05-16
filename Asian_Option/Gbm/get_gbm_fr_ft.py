# -*- coding: utf-8 -*-
"""
Created on Mon May  6 18:34:28 2019

@author: Diego
"""
import numpy as np
import math

def fr_fourier_transform(x,a):
    
    m = len(x)
    
    #first fft
    vect_one = x*np.exp(-math.pi*1j*a*np.arange(0, m)**2)
    vect_two = np.concatenate((vect_one, np.zeros(m)))
    first_fft = np.fft.fft(vect_two)# correto
    
    #Second fft
    vect_third = np.exp(math.pi*1j*a*np.arange(0, m)**2)
    vect_fourth =  np.exp(math.pi*1j*a*np.arange(-m, 0)**2)
    second_fft = np.fft.fft(np.concatenate((vect_third, vect_fourth)))
    
    #ifyz
    ifyz =( np.fft.ifft(first_fft*second_fft))
    
    #f
    
    f =np.exp(-math.pi*1j*a*np.arange(0, m)**2)*ifyz[0:m,]
    
    return f

