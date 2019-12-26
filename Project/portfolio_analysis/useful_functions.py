# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 20:42:55 2019

@author: Diego
"""
import numpy as np


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


def random_portfolio(returns):
    ''' 
    Returns the mean and standard deviation of returns for a random portfolio
    '''

    p = np.asmatrix(np.mean(returns, axis=1))  # mean of each assets
    w = np.asmatrix(rand_weights(returns.shape[0]))  # random weight for each assets
    C = np.asmatrix(np.cov(returns))  # variance/covariance matrix

    mu = w * p.T  # portfolio mean
    sigma = np.sqrt(w * C * w.T)  # portfolio variance

    # This recursion reduces outliers to keep plots pretty
    if sigma > 2:
        return random_portfolio(returns)  # ripeto la procedura per evitare risultati estremi(eliminabile nel miocaso)
    return mu, sigma
