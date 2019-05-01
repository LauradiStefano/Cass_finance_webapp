# -*- coding: utf-8 -*-
"""
Created on Fri Apr  5 15:14:27 2019

@author: Diego
"""
import numpy as np
import math
from get_CharFunc import CharFunc
from get_COS_bounds import get_COS_bounds


# opzione sullo spot
def get_cos_prices(type, L, N, CallPut, S0, K, r, q, Tt, param):
    price = []
    if Tt == 0:
        price = (max(CallPut * (S0 - K), 0))

    else:

        param[0] = 0
        omega = np.log(CharFunc(param, type, -1j, 1))
        # np.concatenate((np.array([(0)]),np.array([param])),axis=None)

        mu = r - q - np.real(omega)

        param[0] = mu
        paramrn = param
        # np.concatenate((np.array([(mu)]),np.array([param])),axis=None)

        a, b = get_COS_bounds(paramrn, type, Tt, L)

    if CallPut == 1:  # call

        V = ((2 / (b - a)) * (chiFO(0, b, N, a, b) - psiFO(0, b, N, a, b)))

    else:  # CallPut == 0  # put

        V = -(2 / (b - a)) * (chiFO(a, 0, N, a, b) - psiFO(a, 0, N, a, b))

    CharFn = (CharFunc(paramrn, type, np.arange(0, N, 1) * math.pi / (b - a), Tt))
    Cfv = np.matrix(CharFn * V)  # corretto

    for j in range(0, len(K)):
        k = np.log(S0 / K[j]) - a
        Exp_term = np.matrix(np.exp(1j * math.pi * (k) * np.arange(0, N, 1) / (b - a)))  # corretto

        real_term = np.real(np.dot(Exp_term, Cfv.getT()) - 0.5 * Exp_term[0, 0] * Cfv[
            0, 0])  # corretto il secondo termine della sottrazione

        price.append(float(K[j] * math.exp(-r * Tt) * real_term))  # transpose CFV

    return price


# Fourier-cosine series coefficients of the terminal payoff function
def chiFO(c, d, N, a, b):
    rangeN = np.arange(0, N, 1)

    rangeN_c = rangeN * math.pi * (c - a) / (b - a)
    rangeN_d = rangeN * math.pi * (d - a) / (b - a)

    chi = (1 / (1 + (rangeN * math.pi / (b - a)) ** 2)) * (
            np.cos(rangeN_d) * math.exp(d) - np.cos(rangeN_c) * math.exp(c) + (rangeN * math.pi / (b - a)) * np.sin(
        rangeN_d) * math.exp(d) - (rangeN * math.pi / (b - a)) * np.sin(rangeN_c) * math.exp(c))

    return chi


def psiFO(c, d, N, a, b):
    rangeN = np.arange(0, N, 1)
    rangeN_c = rangeN * math.pi * (c - a) / (b - a)
    rangeN_d = rangeN * math.pi * (d - a) / (b - a)
    psi = []
    psi.append(d - c)
    for i in range(1, N):
        psi.append((math.sin(rangeN_d[i]) - math.sin(rangeN_c[i])) * (b - a) / (rangeN[i] * math.pi))

    return psi

# %opzione sullo spot
# function [price] = myPlainVanillaPrice(type, L, N, CallPut, S0, K, r, q, Tt, param)
#
#
#
# NR=size(S0,1)%righe
# NC=size(S0,2)%colonne
# price=zeros(NR,NC) 
#
# for j=1:NR
#    T=Tt(j,1)
#    
#    if T==0
#        price(NR,:)=max(CallPut*(S0(NR,:)-K),0)
#    else
#        omega=log(CharFunc([0 param],type,-1i,1))
#        mu=r-q-omega
#        
#        paramrn=[mu param]
#
#        [a, b]=get_COS_bounds(paramrn,type,T,L)
#    
#    if CallPut == 1 % call
#    
#        V = (2/(b-a))*(chiFO(0,b,N,a,b)-psiFO(0,b,N,a,b))
#    elseif CallPut == -1 % put
#        V = -(2/(b-a))*(chiFO(a,0,N,a,b)-psiFO(a,0,N,a,b))
#    end
#
#        CharFn = CharFunc(paramrn,type,(0:N-1)*pi/(b-a),T)
#
#        CFV=CharFn.*V
#        
#        Exp_term=exp(1i*pi*(log(S0(j,:)'./K)-a).*(0:N-1)/(b-a))
#        price(j,:) = K*exp(-r*T)*real(Exp_term*CFV.'-0.5*Exp_term(1)*CFV(1))'
#    end
# end
#
# end
#
# % Fourier-cosine series coefficients of the terminal payoff function
# function ret=chiFO(N,a,b)
#
# rangeN=(0:N-1)
#
# rangeN_c=rangeN*pi*(c-a)/(b-a)
# rangeN_d=rangeN*pi*(d-a)/(b-a)
#
# chi = (1./(1+(rangeN*pi/(b-a)).^2)).*(cos(rangeN_d)*exp(d)-cos(rangeN_c)*exp(c)+...
#    (rangeN*pi/(b-a)).*sin(rangeN_d)*exp(d)-(rangeN*pi/(b-a)).*sin(rangeN_c)*exp(c))
# ret=chi
# end
#
# function ret=psiFO(c,d,N,a,b)
#
# rangeN=(1:N-1)
# rangeN_c=rangeN*pi*(c-a)/(b-a)
# rangeN_d=rangeN*pi*(d-a)/(b-a)
#
# psi(1) = d-c
# psi(2:N) = (sin(rangeN_d)-sin(rangeN_c))*(b-a)./(rangeN*pi)
# ret=psi
# end
