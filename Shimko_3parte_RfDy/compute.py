# -*- coding: utf-8 -*-
"""
Created on Fri Mar  8 10:03:36 2019

@author: Diego
"""

from shimkofun import ImpliedCDFPrices_FullRange, ImpliedPDFPrices_FullRange, ImpliedCDFReturns_FullRange, \
    ImpliedPDFReturns_FullRange, find_SD_B, find_parameters, get_lognormal_fit
from getbs import find_vol
from shimkofun import get_implied_parameters_lognormal
import numpy as np
import bokeh.plotting as plt
from bokeh.plotting import ColumnDataSource
from bokeh.models import HoverTool
from scipy import integrate
import math
from scipy.stats import norm, lognorm
import os
import pandas as pd


def upload_input(filename=None):
    data = pd.read_excel(os.path.join('uploads/', filename))
    x = []

    for i in range(0, len(data)):
        series = data.loc[i]
        array = np.array(series)

        if array[1] == 0:
            data.drop(data.index[i])
        else:
            x.append(np.array(data.loc[i]))

    call_market = []
    strike_data = []
    put_market = []
    u = x[0]
    time = u[4]

    for i in range(0, len(x)):
        y = x[i]
        strike_data.append(y[0])
        put_market.append(y[2])
        call_market.append(y[1])

    return filename, strike_data, call_market, put_market, time


def volatility_term_structure(s0, call_put_flag, time, call_market, put_market, strike_data, risk_free, div_yield):

    call_put_flag = int(call_put_flag)

    risk_free = risk_free / 100
    div_yield = div_yield / 100
    strike_min = int(strike_data[0])
    strike_max = int(strike_data[-1])
    step_k = 0.5
    SD = s0 * math.exp(-div_yield * time)
    B = math.exp(-risk_free * time)

    """
    Newton Method find implied volatily through B&S Formula
    if cp_flag==1 target_value is going to be C_market prices
    else P_market prices
    """
    if call_put_flag == 1:  # call = 1
        target_value = call_market
    elif call_put_flag == 0:
        target_value = put_market  # put = 0
    else:
        delta_k_s0 = np.array(strike_data) - float(s0)
        negative = delta_k_s0 < 0
        positive = delta_k_s0 > 0

        all_call_market = negative * call_market
        all_put_market = positive * put_market
        both_call_put = list(all_call_market + all_put_market)
        target_value = both_call_put

    volatility = find_vol(target_value, call_put_flag, s0, strike_data, time, risk_free, div_yield)  # annual volatility
    volatility_time = np.array(volatility * math.sqrt(time))  # output plot implied

    """
    Given implied volatility and strikes the paper considers the volatility structures
    as a parabola of best_squares_fit with parameters a0,a1,a2
    volatility(x,t)=a0(t)+a1(t)*k+a2(t)*k^2
    Show the implied volatility structure (vs strikes)
    """

    parameters = find_parameters(strike_data, volatility_time)
    a0 = parameters[0]
    a1 = parameters[1]
    a2 = parameters[2]
    r2 = parameters[3]

    implied_vol_t_k = lambda k: a0 + a1 * k + a2 * k ** 2

    strike_plot = np.arange(strike_min, strike_max, step_k)
    implied_volatility = np.array([implied_vol_t_k(i) for i in strike_plot])

    return a0, a1, a2, strike_plot, implied_volatility, strike_min, strike_max, volatility_time, r2


def compute_shimko_table(a0, a1, a2, s0, risk_free, div_yield, time, strike_min, strike_max):

    step_k = 0.5

    """
    Comupute the moments of prices and logret
    """
    risk_free = risk_free / 100
    div_yield = div_yield / 100
    SD = s0 * math.exp(-div_yield * time)
    B = math.exp(-risk_free * time)

    x_fit_lgn = get_lognormal_fit(a0, a1, a2, SD, B, strike_min, strike_max)

    """
    Estimate the PDF &  CDF of the underlying asset price at maturity
    """
    pdf_prices = lambda k: ImpliedPDFPrices_FullRange(a0, a1, a2, SD, B, k, strike_min, strike_max, x_fit_lgn)

    # chart pdf e normpdf returns

    pdf_returns = lambda kret: ImpliedPDFReturns_FullRange(a0, a1, a2, SD, B, kret, strike_min, strike_max, x_fit_lgn)
    st = np.arange(strike_min * 0.75, strike_max * 1.5, step_k)  # output per grafico

    # ret_t = np.log(st / SD)  # output grafico 3

    # Table moments

    up_factor = 20
    area_prices = integrate.quad(lambda k: pdf_prices(k), 0, strike_max * up_factor)  # Table Ceq Moment
    m1 = integrate.quad(lambda k: k * pdf_prices(k) / area_prices[0], 0, strike_max * up_factor)
    m2 = integrate.quad(lambda k: (k - m1[0]) ** 2 * pdf_prices(k) / area_prices[0], 0, strike_max * up_factor)
    m3 = integrate.quad(lambda k: (k - m1[0]) ** 3 * pdf_prices(k) / area_prices[0], 0, strike_max * up_factor)
    m4 = integrate.quad(lambda k: (k - m1[0]) ** 4 * pdf_prices(k) / area_prices[0], 0, strike_max * up_factor)
    expected_price = m1[0]  # Table Ceq Moment
    sigma2_price = m2[0]  # Table Ceq Moment
    std_deviation_price = m2[0] ** 0.5
    skew_prices = m3[0] / (m2[0] ** 0.5) ** 3  # Table Ceq Moment
    kurt_prices = m4[0] / (m2[0] ** 0.5) ** 4  # Table Ceq Moment

    # Fitted Lognormal

    q_shimko = std_deviation_price / expected_price
    skew_prices_logn = 3 * q_shimko + q_shimko ** 3  # Table Lognormal Moment
    kurt_prices_logn = 3 + 16 * q_shimko ** 2 + 15 * q_shimko ** 4 + 6 * q_shimko ** 6 + q_shimko ** 8

    implied_parameters_lognormal = get_implied_parameters_lognormal(expected_price / SD, (m2[0] + m1[0] ** 2) / SD ** 2)
    mu = implied_parameters_lognormal[0]
    sigma2 = implied_parameters_lognormal[1]

    # exp_sg2=math.exp(sigma2)
    # skew_prices_logn=(exp_sg2+2)*(math.sqrt(exp_sg2-1))
    # kurt_prices_logn=math.exp(4*sigma2)+2*math.exp(3*sigma2)+3*exp(2*sigma2)-6
    ret_min = mu - 9 * sigma2 ** 0.5
    ret_max = mu + 9 * sigma2 ** 0.5
    step_ret = 0.01
    ret_t = np.arange(ret_min * 0.75, ret_max * 1.5, step_ret)
    # ret_t = np.log(st / SD)  # output grafico 3
    pdf_ret = [float(pdf_returns(x)) for x in ret_t]  # output grafico3

    area_ret = integrate.quad(lambda k: pdf_returns(k), ret_min, ret_max)  # Table logReturns moment
    m1_ret = integrate.quad(lambda k: k * pdf_returns(k) / area_ret[0], ret_min, ret_max)  # Table logReturns moment
    m2_ret = integrate.quad(lambda k: (k - m1_ret[0]) ** 2 * pdf_returns(k) / area_ret[0], ret_min,
                            ret_max)  # Table LogReturns moment
    m3_ret = integrate.quad(lambda k: (k - m1_ret[0]) ** 3 * pdf_returns(k) / area_ret[0], ret_min, ret_max)
    m4_ret = integrate.quad(lambda k: (k - m1_ret[0]) ** 4 * pdf_returns(k) / area_ret[0], ret_min, ret_max)
    std_deviation_log_ret = m2_ret[0] ** 0.5
    skew_log_ret = m3_ret[0] / (m2_ret[0] ** 0.5) ** 3  # Table LogReturns Moment
    kurt_log_ret = m4_ret[0] / (m2_ret[0] ** 0.5) ** 4  # Table LogReturns Moment

    pdf_bench_log_prices = lambda k: lognorm.pdf(k, sigma2 ** 0.5, mu, m1[0])
    pdf_bench_norm_returns = lambda k: norm.pdf(k, m1_ret[0], std_deviation_log_ret)
    area_ret_norm = integrate.quad(lambda k: pdf_bench_norm_returns(k), ret_min, ret_max)  # Table logReturns moment

    m3_ret_norm = integrate.quad(lambda k: (k - m1_ret[0]) ** 3 * pdf_bench_norm_returns(k), ret_min, ret_max)
    m4_ret_norm = integrate.quad(lambda k: (k - m1_ret[0]) ** 4 * pdf_bench_norm_returns(k), ret_min, ret_max)
    skew_norm = abs(m3_ret_norm[0] / (std_deviation_log_ret) ** 3)  # Table LogReturns Moment
    kurt_norm = m4_ret_norm[0] / (std_deviation_log_ret) ** 4

    pdf_bench_norm_returns = [float(pdf_bench_norm_returns(x)) for x in ret_t]  # aggiungere all'output

    return pdf_ret, area_prices[0], expected_price, sigma2_price, skew_prices, kurt_prices, skew_prices_logn, \
           kurt_prices_logn, area_ret[0], m1_ret[0], m2_ret[0], skew_log_ret, kurt_log_ret, \
           pdf_bench_norm_returns, ret_t, skew_norm, kurt_norm, mu, std_deviation_log_ret, sigma2


def create_implied_volatility_plot(strike_plot, implied_volatility, s0, strike_min, strike_max, strike_data,
                                   volatility_time):

    tools = "save, box_zoom, pan, reset"

    # strike = [str(Strike) for Strike in strike]
    # impliedVolatility = [str(impVol) for impVol in impliedVolatility]

    delta_k_s0 = np.array(strike_data) - float(s0)
    negative = delta_k_s0 < 0
    positive = delta_k_s0 > 0
    strike_call = (strike_data * negative)
    strike_call = np.array([elem for elem in strike_call if elem != 0])
    volatility_t_call = volatility_time * negative
    volatility_t_call = np.array([elem for elem in volatility_t_call if elem != 0])

    strike_put = strike_data * positive
    strike_put = np.array([elem for elem in strike_put if elem != 0])
    volatility_t_put = volatility_time * positive
    volatility_t_put = np.array([elem for elem in volatility_t_put if elem != 0])

    data_line = ColumnDataSource(data=dict(
        strike=strike_plot,
        implied_volatility=implied_volatility
    ))

    data_circle_call = ColumnDataSource(data=dict(
        strike_call=strike_call,
        volatility_t_call=volatility_t_call,
    ))

    data_circle_put = ColumnDataSource(data=dict(
        strike_put=strike_put,
        volatility_t_put=volatility_t_put,
    ))

    x_range = [strike_min, strike_max + 10]
    y_range = [0, max(volatility_time) + 0.02]
    p = plt.figure(x_range=x_range, y_range=y_range, title="Implied volatility profile", plot_height=450,
                   tools=tools, toolbar_location="left", x_axis_label='Exercise price',
                   y_axis_label='Volatility x root time')

    p.line(x='strike', y='implied_volatility', source=data_line, color="#0095B6", legend='Volatility Structure',
           line_width=4, alpha=0.8)

    p.square(x=s0, y=0, source=data_line, legend='Price', color="#050402", size=8)

    p.circle(x='strike_call', y='volatility_t_call', source=data_circle_call, color="#D21F1B",
             legend='Implied Volatility of Market Call Option Price',
             size=6)
    p.circle(x='strike_put', y='volatility_t_put', source=data_circle_put, color="#120A8F",
             legend='Implied Volatility of Market Put Option Price',
             size=6)

    p.add_tools(HoverTool(
        tooltips=[
            ('strike', '@strike'),
            ('implied volatility', '@impliedVolatility'),
        ],
        mode='hline'
    ))

    p.toolbar.active_drag = None
    p.legend.location = "bottom_left"
    p.legend.orientation = "vertical"

    from bokeh.embed import components
    script, div = components(p)
    return script, div


def create_plot_return_underlying_distribution(ret_t, pdf_ret, pdf_bench_norm_returns):
    tools = "save, pan, box_zoom, reset"
    ret_t = [round(st, 2) for st in ret_t]
    pdf_ret = [round(pdfret, 10) for pdfret in pdf_ret]
    pdf_bench_norm_returns = [round(pdf_benchNorm, 10) for pdf_benchNorm in pdf_bench_norm_returns]

    data = ColumnDataSource(data=dict(
        returns_t=ret_t,
        pdf_ret=pdf_ret,
        pdf_bench_norm_returns=pdf_bench_norm_returns
    ))

    # tooltips = [("returnsT", "@returnsT"),
    #             ("PdfRet", "@Pdfret"),
    #             ("Pdf Bench Norm", "@Pdf_BenchNorm_Returns")
    #             ]

    x_range = [min(ret_t) * 0.9, max(ret_t) * 1.1]
    y_range = [0, max(pdf_ret) * 1.10]
    p = plt.figure(x_range=x_range, y_range=y_range, title="Implied CEQ returns distribution", plot_height=450,
                   toolbar_location="right", tools=tools, x_axis_label='Log Returns',
                   y_axis_label='Probability Density')

    p.line(x='returns_t', y='pdf_ret', source=data, legend="CEQ distribution", color="#0095B6", alpha=0.9, line_width=4)
    p.line(x='returns_t', y='pdf_bench_norm_returns', source=data, legend="Benchmark Normal", color="#D21F1B",
           alpha=0.6, line_width=4)

    p.legend.location = "top_right"
    p.toolbar.active_drag = None
    p.legend.click_policy = "hide"

    from bokeh.embed import components
    script, div = components(p)

    return script, div


def compute_underlying_distribution(a0, a1, a2, s0, risk_free, div_yield, time, strike_min, strike_max, expected_price,
                                    sigma2, mu):

    risk_free = risk_free / 100
    div_yield = div_yield / 100
    step_k = 0.5
    SD = s0 * math.exp(-div_yield * time)
    B = math.exp(-risk_free * time)

    x_fit_lgn = get_lognormal_fit(a0, a1, a2, SD, B, strike_min, strike_max)

    pdf_prices = lambda k: ImpliedPDFPrices_FullRange(a0, a1, a2, SD, B, k, strike_min, strike_max, x_fit_lgn)
    st = np.arange(strike_min * 0.75, strike_max * 1.5, step_k)  # output per grafico
    pdf = [float(pdf_prices(x)) for x in st]  # output grafico2

    pdf_bench_log_prices = lambda k: lognorm.pdf(k, sigma2 ** 0.5, mu, expected_price)
    pdf_bench_log_prices = [float(pdf_bench_log_prices(x)) for x in st]

    return st, pdf, pdf_bench_log_prices


def create_plot_index_underlying_distribution(st, pdf, pdf_bench_log_prices, s0, strike_min, strike_max):

    tools = "save, pan, box_zoom, reset"
    st = [round(s, 2) for s in st]
    # ST = [str(s) for s in ST]
    pdf = [round(pf, 10) for pf in pdf]
    # Pdf = [str(pf) for pf in Pdf]
    # Pdf_BenchLog_Prices = [round(pdf_bench, 10) for pdf_bench in Pdf_BenchLog_Prices]

    # Pdf_BenchLog_Prices = [str(Pbp) for Pbp in Pdf_BenchLog_Prices]

    data = ColumnDataSource(data=dict(
        strike=st,
        pdf=pdf,
        pdf_bench_log_prices=pdf_bench_log_prices
    ))

    # hover = HoverTool(
    #     tooltips=[
    #         ('strike', '$strike'),
    #         ('Pdf', '$Pdf'),
    #         ('Pdf Bench Log Prices', '$Pdf_BenchLog_Prices')
    #     ]
    # )
    # tooltips = [("strike", "@strike"),
    #             ("Pdf", "@Pdf"),
    #             ("Pdf Bench Log Prices", "@Pdf_BenchLog_Prices"),
    #             ("S0", "@S0")
    #             ]

    x_range = [strike_min * 0.125, strike_max * 2]
    y_range = [0, max(pdf) * 1.10]
    p = plt.figure(x_range=x_range, y_range=y_range, title="Implied CEQ index distribution", plot_height=400,
                   toolbar_location="left", tools=tools, x_axis_label='Index Value', y_axis_label='Probability Density')

    p.line(x='strike', y='pdf', source=data, legend="CEQ distribution", color="#0095B6", alpha=0.9, line_width=4)

    p.line(x='strike', y='pdf_bench_log_prices', source=data, legend="Benchmark LogNormal", color="#D21F1B",
           alpha=0.6, line_width=4)
    p.square(x=s0, y=0, source=data, legend="Price Today", color="#050402", size=8)

    p.legend.location = "top_right"
    p.toolbar.active_drag = None
    p.legend.click_policy = "hide"

    from bokeh.embed import components
    script, div = components(p)

    return script, div


def compute_underlying_cdf(a0, a1, a2, s0, risk_free, div_yield, time, strike_min, strike_max, expected_price, sigma2,
                           mu):

    step_k = 0.5
    risk_free = risk_free / 100
    div_yield = div_yield / 100
    SD = s0 * math.exp(-div_yield * time)
    B = math.exp(-risk_free * time)

    x_fit_lgn = get_lognormal_fit(a0, a1, a2, SD, B, strike_min, strike_max)

    st = np.arange(strike_min * 0.75, strike_max * 1.5, step_k)  # output per grafico
    cdf_prices = lambda k: ImpliedCDFPrices_FullRange(a0, a1, a2, SD, B, k, strike_min, strike_max, x_fit_lgn)
    cdf_prices = [float(cdf_prices(x)) for x in st]
    cdf_bench_log_prices = lambda k: lognorm.cdf(k, sigma2 ** 0.5, mu, expected_price)
    cdf_bench_log_prices = [float(cdf_bench_log_prices(x)) for x in st]  # vs st

    return cdf_prices, cdf_bench_log_prices, st


def create_plot_price_cdf(st, cdf_prices, cdf_bench_log_prices, strike_min, strike_max):

    tools = "save, pan, box_zoom, reset"
    # ST = [round(st, 2) for st in ST]
    # CdfPrices = [round(cdfpr, 10) for cdfpr in CdfPrices]
    # Cdf_BenchLog_Prices = [round(cdf_benchLog, 10) for cdf_benchLog in Cdf_BenchLog_Prices]

    data = ColumnDataSource(data=dict(
        st=st,
        cdf_prices=cdf_prices,
        cdf_bench_log_prices=cdf_bench_log_prices
    ))

    # tooltips = [("returnsT", "@returnsT"),
    #             ("PdfRet", "@Pdfret")
    #             ]

    x_range = [strike_min * 0.125, strike_max * 2]
    y_range = [0, 1.1]
    p = plt.figure(x_range=x_range, y_range=y_range, title="Implied CEQ prices CDF", plot_height=400,
                   toolbar_location="left",
                   tools=tools, x_axis_label='Index Value', y_axis_label='Cumulative Probability')
    p.line(x='st', y='cdf_prices', source=data, legend="CEQ distribution", color="#0095B6", alpha=0.9,
           line_width=4)
    p.line(x='st', y='cdf_bench_log_prices', source=data, legend="Benchmark LogNormal", color="#D21F1B", alpha=0.6,
           line_width=4)

    p.legend.location = "bottom_right"
    p.toolbar.active_drag = None
    p.legend.click_policy = "hide"

    from bokeh.embed import components
    script, div = components(p)

    return script, div


def compute_returns_cdf(a0, a1, a2, s0, risk_free, div_yield, time, strike_min, strike_max, m1_ret,
                        std_deviation_log_ret, ret_t):

    step_k = 0.5
    risk_free = risk_free / 100
    div_yield = div_yield / 100
    SD = s0 * math.exp(-div_yield * time)
    B = math.exp(-risk_free * time)

    x_fit_lgn = get_lognormal_fit(a0, a1, a2, SD, B, strike_min, strike_max)

    cdf_returns = lambda kret: ImpliedCDFReturns_FullRange(a0, a1, a2, SD, B, kret, strike_min, strike_max, x_fit_lgn)

    cdf_returns = [float(cdf_returns(x)) for x in ret_t]
    cdf_bench_norm_returns = lambda k: norm.cdf(k, m1_ret, std_deviation_log_ret)
    cdf_bench_norm_returns = [float(cdf_bench_norm_returns(x)) for x in ret_t]

    return ret_t, cdf_returns, cdf_bench_norm_returns


def create_plot_return_cdf(ret_t, cdf_returns, cdf_bench_norm_returns):

    tools = "save, pan, box_zoom, reset"
    # retT = [round(st, 2) for st in retT]
    # CdfReturns = [round(cdfret, 10) for cdfret in CdfReturns]
    # Cdf_BenchNorm_Returns = [round(cdf_benchNorm, 10) for cdf_benchNorm in Cdf_BenchNorm_Returns]

    data = ColumnDataSource(data=dict(
        returns_t=ret_t,
        cdf_returns=cdf_returns,
        cdf_bench_norm_returns=cdf_bench_norm_returns
    ))

    # tooltips = [("returnsT", "@returnsT"),
    #             ("PdfRet", "@Pdfret"),
    #             ("Pdf Bench Norm", "@Pdf_BenchNorm_Returns")
    #             ]

    x_range = [min(ret_t) * 0.9, max(ret_t) * 1.1]
    y_range = [0, 1.1]
    p = plt.figure(x_range=x_range, y_range=y_range, title="Implied CEQ returns CDF", plot_height=400,
                   toolbar_location="right", tools=tools, x_axis_label='Log Returns',
                   y_axis_label='Cumulative Probability')

    p.line(x='returns_t', y='cdf_returns', source=data, legend="CEQ distribution", color="#0095B6", alpha=0.9,
           line_width=4)
    p.line(x='returns_t', y='cdf_bench_norm_returns', source=data, legend="Benchmark Normal", color="#D21F1B",
           alpha=0.6, line_width=4)

    p.legend.location = "bottom_right"
    p.toolbar.active_drag = None
    p.legend.click_policy = "hide"

    from bokeh.embed import components
    script, div = components(p)

    return script, div
