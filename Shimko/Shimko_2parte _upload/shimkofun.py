# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 22:24:27 2019

@author: Diego
"""
import math

import numpy as np
from scipy.optimize import fsolve
from scipy.stats import norm


def find_SD_B(K, C_market, P_market):
    C = np.array(C_market)
    P = np.array(P_market)
    z = C - P
    parameters = np.polyfit(K, z, 1, rcond=None, full=False, w=None, cov=False)

    #    B=parameters[0];
    #    SD=parameters[1];

    return parameters


def find_parameters(K, volt):
    parameters = np.polyfit(K, volt, 2, rcond=None, full=False, w=None, cov=False)

    A2 = parameters[0];
    A1 = parameters[1];
    A0 = parameters[2];
    volt_hat = A0 + A1 * np.array(K) + A2 * np.array(K) ** 2
    volt_mean = np.sum(volt_hat) / len(volt_hat)
    ESS = np.sum((volt_hat - volt_mean) ** 2)
    TSS = np.sum((volt - volt_mean) ** 2)
    R2 = ESS / TSS

    return A0, A1, A2, R2


def ImpliedPDFPrices(A0, A1, A2, Sd, B, k):
    ivoltk = A0 + A1 * k + A2 * k ** 2

    d1 = (math.log(Sd / (k * B)) + 0.5 * ivoltk * ivoltk) / ivoltk  # formula A2
    d2 = d1 - ivoltk  # formula A2

    d1k = -1 / (k * ivoltk) + (1 - d1 / ivoltk) * (A1 + 2 * A2 * k)
    d2k = d1k - (A1 + 2 * A2 * k)

    return -norm.pdf(d2) * (d2k - (A1 + 2 * A2 * k) * (1 - d2 * d2k) - 2 * A2 * k)


# def ImpliedPDFLogret(S0,k):
#   
#    volt=A0+A1*k+A2*k**2
#    
#    
#    d1=(math.log(Sd/(k*B))+0.5*volt*volt)/volt #formula A2
#    d2= d1-volt  #formula A2
#    
#    d1k= -1/(k*volt)+(1-d1/volt)*(A1+2*A2*k)
#    d2k= d1k-(A1+2*A2*k)
#    
#    return -(norm.pdf(d2)*(d2k-(A1+2*A2*k)*(1-d2*d2k)-2*A2*k))
#  
# def ImpliedCDFLogret(S0,k):
#    return ImpliedCDFPrices(S0*math.exp(k))


def ImpliedCDFPrices(A0, A1, A2, SD, B, k):
    volt = A0 + A1 * k + A2 * k ** 2

    d1 = (math.log(SD / (k * B)) + 0.5 * volt * volt) / volt;  # formula A2
    d2 = d1 - volt;
    cdf = 1 + k * norm.pdf(d2) * (A1 + 2 * A2 * k) - norm.cdf(d2)
    cdf = max(cdf, 0)
    cdf = min(cdf, 0.999999)
    return cdf;  # Formula:A8 paper


def ImpliedPDFPrices_FullRange(A0, A1, A2, SD, B, k, kmin, kmax, x_fit_lgn):
    #  x_fit_lgn=get_lognormal_kmin(A0,A1,A2,SD,B,kmin,kmax)
    mumin = x_fit_lgn[0]
    sgmin = x_fit_lgn[1]
    mumax = x_fit_lgn[2]
    sgmax = x_fit_lgn[3]
    cdfmin = ImpliedCDFPrices(A0, A1, A2, SD, B, kmin)
    cdfmax = ImpliedCDFPrices(A0, A1, A2, SD, B, kmax)

    if k < kmin:
        if cdfmin == 0:
            pdf = 0
        else:
            pdf = norm.pdf((math.log(k) - mumin) / sgmin) / (k * sgmin)
    elif k > kmax:
        if cdfmax == 1:
            pdf = 0
        else:
            pdf = norm.pdf((math.log(k) - mumax) / sgmax) / (k * sgmax)
    else:
        pdf = ImpliedPDFPrices(A0, A1, A2, SD, B, k)

    return pdf


def ImpliedCDFPrices_FullRange(A0, A1, A2, SD, B, k, kmin, kmax, x_fit_lgn):
    #  x_fit_lgn=get_lognormal_kmin(A0,A1,A2,SD,B,kmin,kmax)
    mumin = x_fit_lgn[0]
    sgmin = x_fit_lgn[1]
    mumax = x_fit_lgn[2]
    sgmax = x_fit_lgn[3]

    if k == 0:
        cdf = 0
        return cdf

    cdfmin = ImpliedCDFPrices(A0, A1, A2, SD, B, kmin)
    cdfmax = ImpliedCDFPrices(A0, A1, A2, SD, B, kmax)

    if k < kmin:
        if cdfmin == 0:
            cdf = 0
        else:
            cdf = norm.cdf((math.log(k) - mumin) / sgmin)

    elif k > kmax:
        if cdfmax == 1:
            cdf = 1
        else:
            cdf = norm.cdf((math.log(k) - mumax) / sgmax)
    else:
        cdf = ImpliedCDFPrices(A0, A1, A2, SD, B, k)

    return cdf


def ImpliedCDFReturns_FullRange(A0, A1, A2, SD, B, kret, kmin, kmax, x_fit_lgn):
    cdf = ImpliedCDFPrices_FullRange(A0, A1, A2, SD, B, SD * math.exp(kret), kmin, kmax, x_fit_lgn)
    return cdf


def ImpliedPDFReturns_FullRange(A0, A1, A2, SD, B, kret, kmin, kmax, x_fit_lgn):
    pdf = ImpliedPDFPrices_FullRange(A0, A1, A2, SD, B, SD * math.exp(kret), kmin, kmax, x_fit_lgn) * SD * math.exp(
        kret)
    return pdf


# def get_implied_moments_prices(A0,A1,A2,SD,B,kret,kmin,kmax,x_fit_lgn):


def bs(A0, A1, A2, SD, B, k):
    volt = A0 + A1 * k + A2 * k ** 2
    d1 = (math.log(SD / (k * B)) + 0.5 * volt * volt) / (volt);
    d2 = d1 - volt;
    return SD * norm.cdf(d1) - k * B * norm.cdf(d2)


def densF(A0, A1, A2, SD, B, k):
    eps = 10 ^ (-5)
    bs_deriv = lambda k: (bs(A0, A1, A2, SD, B, k + eps) - 2 * bs(A0, A1, A2, SD, B, k) + bs(A0, A1, A2, SD, B,
                                                                                             k - eps)) / (eps) ** 2;
    return bs_deriv(k) / B;


def get_lognormal_match(A0, A1, A2, SD, B, kmin, kmax, p):
    #    PdfKmin=ImpliedPDFPrices(A0,A1,A2,SD,B,kmin)
    #    CdfKmin=ImpliedCDFPrices(A0,A1,A2,SD,B,kmin)
    PdfKmax = ImpliedPDFPrices(A0, A1, A2, SD, B, kmax)
    CdfKmax = ImpliedCDFPrices(A0, A1, A2, SD, B, kmax)
    mumax, sgmax = p
    arg = (math.log(kmax) - mumax) / sgmax
    f1 = norm.cdf(arg) - CdfKmax

    f2 = norm.pdf(arg) / (kmax * sgmax) - PdfKmax
    return (f1, f2)


def get_lognormal_fit(A0, A1, A2, SD, B, kmin, kmax):
    PdfKmin = ImpliedPDFPrices(A0, A1, A2, SD, B, kmin)
    CdfKmin = ImpliedCDFPrices(A0, A1, A2, SD, B, kmin)
    PdfKmax = ImpliedPDFPrices(A0, A1, A2, SD, B, kmax)
    CdfKmax = ImpliedCDFPrices(A0, A1, A2, SD, B, kmax)

    sgkmin = lambda mu: (math.log(kmin) - mu) / norm.ppf(CdfKmin)
    sgkmax = lambda mu: (math.log(kmax) - mu) / norm.ppf(CdfKmax)

    fminmatch = lambda mu: norm.pdf((math.log(kmin) - mu) / sgkmin(mu)) / (sgkmin(mu) * kmin) - PdfKmin
    fmaxmatch = lambda mu: norm.pdf((math.log(kmax) - mu) / sgkmax(mu)) / (sgkmax(mu) * kmax) - PdfKmax

    mumin = fsolve(fminmatch, math.log(kmin) + 0.5)
    mumax = fsolve(fmaxmatch, math.log(kmax) - 0.5)
    sgmin = sgkmin(mumin)
    sgmax = sgkmax(mumax)

    #    my_fun=lambda p :get_lognormal_match(A0,A1,A2,SD,B,kmin,kmax,p)
    #    mumax, sgmax =  fsolve(my_fun, (mumax, sgmax))
    #
    #    my_fun=lambda p :get_lognormal_match(A0,A1,A2,SD,B,kmin,kmin,p)
    #    mumin, sgmin =  fsolve(my_fun, (mumin, sgmin))
    #

    #    return mumin,sgmin,mumax,sgmax
    return mumin, sgmin, mumax, sgmax


# Retrun parameters of the gaussian distribution given moments of lognormal
def get_implied_parameters_lognormal(M1, M2):
    A = np.array([[1, 0.5], [2, 2]])
    inv_A = np.linalg.inv(A)
    B = np.array([[math.log(M1)], [math.log(M2)]])
    Parameters = np.dot(inv_A, B)

    return Parameters
