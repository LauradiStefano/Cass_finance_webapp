# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 16:15:08 2019

@author: Diego
"""
import math

import numpy as np

from get_heston_bounds import compute_heston_bounds
from get_heston_charfn import heston_charfn

def get_pdf_cos(Tt, v0, chi, lam, rho, v_hat, mu):
    N = 1000

    a,b=compute_heston_bounds(mu, Tt, v0, chi, lam, rho, v_hat)
    x=np.linspace(a,b,N)
    CharFn = heston_charfn(np.arange(0,N,1)*math.pi/(b-a), Tt, v0, chi, lam, rho, v_hat, mu)
    COSpdf=[]
    
    for j in range(0,len(x)):
        if x[j]<a or x[j] >b:
            COSpdf.append(0)
        else:
            rangeN=np.arange(0,N,1)*math.pi/(b-a)
            V = (2/(b-a))*np.cos((x[j]-a)*rangeN)
            
            complexNumber=np.sum(CharFn*V*np.exp(1j*rangeN*(-a)))-0.5*CharFn[0]*V[0]
            COSpdf.append(complexNumber.real)

    return COSpdf

#    CharFn=CharFunc(param,type,(0:N-1)*pi/(b-a),T);
#
# %truncate the pdf outside the bounds
# for j=1:length(x)
#    if x(j)<a || x(j) >b
#        COS_pdf(j)=0;
#    else
#        V = (2/(b-a))*cos((x(j)-a)*(0:N-1)*pi/(b-a));
#        COS_pdf(j)=real(sum(CharFn.*V.*exp(1i*(0:N-1)*pi*(-a)/(b-a)))-0.5*CharFn(1)*V(1));
#    end
# end
