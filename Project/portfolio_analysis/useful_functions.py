# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 20:42:55 2019

@author: Diego
"""
import numpy as np
import random

def sumweigth(x):
    return np.sum(x) - 1


def expret(x, m, target):
    ''' 
    Compute the excess expected return e of a portfolio given the mean vector
    '''
    return np.dot(x.T, m) - target


def variance(x, Sigma):
    ''' 
    Compute the variance of a portfolio given the covariance matrix
    '''
    return np.dot(x.T, np.dot(Sigma, x))


def rand_weights(n):
    ''' Produces n random weights that sum to 1 '''
    k = np.random.rand(n)
    return k / sum(k)

def rand_weights_zero_one(n, max):
    done = False
    while not done:
        k = [random.uniform(-100, 100) for _ in range(0,n)]
        somma = abs(np.sum(k))
        value = k /somma
        
        #value= random.uniform(-1, 1)
        condition = all(flag<max for flag in value)
        if condition == True and sum(value)>0: #value[0]<max and value[1]<max and value[2]<max and sum(value)>0:
            done=True
        else:
            None
    return value


def random_portfolio(returns, weights_max, short_selling):
    ''' 
    Returns the mean and standard deviation of returns for a random portfolio
    '''

    p = np.asmatrix(np.mean(returns, axis=1))  # mean of each assets

    if short_selling == 1:
        w = np.asmatrix(rand_weights_zero_one(returns.shape[0], weights_max))#random weight for each assets
    else:
        w = np.asmatrix(rand_weights(returns.shape[0]))


    C = np.asmatrix(np.cov(returns))  # variance/covariance matrix

    mu = w * p.T  # portfolio mean
    sigma = np.sqrt(w * C * w.T)  # portfolio variance

    # This recursion reduces outliers to keep plots pretty
    if sigma > 2:
        return random_portfolio(returns)  # ripeto la procedura per evitare risultati estremi(eliminabile nel miocaso)
    return mu, sigma
