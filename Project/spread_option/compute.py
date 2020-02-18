# -*- coding: utf-8 -*-
"""
Created on Tue Oct 15 18:30:44 2019

@author: Diego
"""

import math

from spread_option.get_integral_spread import integral_spread


# dati e parametri

# definizione dati
# d = dump
# NC = grid
def price_spread_option(risk_free, time, price_1, price_2, dividend_yiled_1, dividend_yield_2, strike, d,
                        volatility_1, volatility_2, correlation):
    #
    #    risstrike_free = 0.1 ;T = 1;
    #
    #    price_1 = 100; price_2 = 96; dividend_yiled_1 = 0.05; dividend_yiled_2 = 0.05;
    #
    #    d=.75; NC = 1000; dk = 0.5;

    # calcolo prezzi frd
    risk_free = risk_free / 100
    dividend_yiled_1 = dividend_yiled_1 / 100
    dividend_yield_2 = dividend_yield_2 / 100
    F2 = price_2 * math.exp((risk_free - dividend_yield_2) * time)

    # GMB: vq maybe v1, v2, rho

    parameter = [volatility_1, volatility_2, correlation]

    # guess notazione Fusai (quadgstrike)

    alpha = F2 / (F2 + strike)

    k = math.log(F2 + strike)

    spread_option_price = integral_spread(strike, price_1, price_2, dividend_yiled_1, dividend_yield_2, time, risk_free,
                                          alpha, k, d, parameter)

    # valutazione Fusai ottimizzata (quadgstrike)
    # function = lambda x : -integral_spread(strike, price_1, price_2, dividend_yiled_1, dividend_yield_2,
    # time, risk_free, x[0], x[1], d, parameter)
    # opt_parameters= scipy.optimize.least_squares(function, [alpha, k])

    return spread_option_price
