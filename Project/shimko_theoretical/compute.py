# -*- coding: utf-8 -*-
"""
Created on Fri Mar  8 10:03:36 2019

@author: Diego
"""

import math

import bokeh.plotting as bp
import numpy as np
from bokeh.layouts import column
from bokeh.models import CustomJS, Slider, HoverTool
from bokeh.plotting import ColumnDataSource
from scipy import integrate
from scipy.stats import norm, lognorm, ks_2samp

from shimko_theoretical.shimkofun import ImpliedCDFPrices_FullRange, ImpliedPDFPrices_FullRange, \
    ImpliedCDFReturns_FullRange, ImpliedPDFReturns_FullRange, get_implied_parameters_lognormal, get_lognormal_fit


def find_parameters(strike_min, strike_atm, strike_max, vol_min, vol_atm, vol_max):
    strike = [strike_min, strike_atm, strike_max]
    vol_min = vol_min / 100
    vol_atm = vol_atm / 100
    vol_max = vol_max / 100
    volatility = [vol_min, vol_atm, vol_max]

    parameters = np.polyfit(strike, volatility, 2, rcond=None, full=False, w=None, cov=False)

    a2 = parameters[0]
    a1 = parameters[1]
    a0 = parameters[2]

    f = lambda strike: a0 + a1 * strike + a2 * strike ** 2
    strike = np.arange(strike_min, strike_max, 0.1)
    implied_volatility = [f(i) for i in strike]

    return a0, a1, a2, strike, implied_volatility, volatility


def compute_shimko_table(a0, a1, a2, s0, risk_free, div_yield, time, strike_min, strike_max):
    step_k = 0.5

    risk_free = risk_free / 100
    div_yield = div_yield / 100

    SD = s0 * math.exp(-div_yield * time)
    B = math.exp(-risk_free * time)

    x_fit_lgn = get_lognormal_fit(a0, a1, a2, SD, B, strike_min, strike_max)

    """
        Estimate the PDF &  CDF of the underlying asset price at maturity
        """
    pdf_prices = lambda k: ImpliedPDFPrices_FullRange(a0, a1, a2, SD, B, k, strike_min, strike_max, x_fit_lgn)

    """
       Estimate the PDF &  CDF of the underlying asset Logret at maturity
       """
    pdf_returns = lambda kret: ImpliedPDFReturns_FullRange(a0, a1, a2, SD, B, kret, strike_min, strike_max, x_fit_lgn)

    """
        Comupute the moments of prices and logret
        """
    # table moments

    up_factor = 20

    area_prices = integrate.quad(lambda k: pdf_prices(k), 0, strike_max * up_factor)  # Table Ceq Moment
    m1 = integrate.quad(lambda k: k * pdf_prices(k) / area_prices[0], 0, strike_max * up_factor)
    m2 = integrate.quad(lambda k: (k - m1[0]) ** 2 * pdf_prices(k) / area_prices[0], 0, strike_max * up_factor)
    m3 = integrate.quad(lambda k: (k - m1[0]) ** 3 * pdf_prices(k) / area_prices[0], 0, strike_max * up_factor)
    m4 = integrate.quad(lambda k: (k - m1[0]) ** 4 * pdf_prices(k) / area_prices[0], 0, strike_max * up_factor)
    expected_price = m1[0]  # Table Ceq Moment
    sigma2_price = m2[0]  # Table Ceq Moment
    stand_deviation_prices = m2[0] ** 0.5
    skewness_prices = m3[0] / (m2[0] ** 0.5) ** 3  # Table Ceq Moment
    kurtosis_prices = m4[0] / (m2[0] ** 0.5) ** 4  # Table Ceq Moment

    # Fitted Lognormal
    q_shimko = stand_deviation_prices / expected_price
    skewness_prices_log_n = 3 * q_shimko + q_shimko ** 3  # Table Lognormal Moment
    kurtosis_prices_log_n = 3 + 16 * q_shimko ** 2 + 15 * q_shimko ** 4 + 6 * q_shimko ** 6 + q_shimko ** 8

    implied_parameters_lognormal = get_implied_parameters_lognormal(expected_price / SD, (m2[0] + m1[0] ** 2) / SD ** 2)
    mu = implied_parameters_lognormal[0]
    sigma2 = implied_parameters_lognormal[1] \
 \
        # exp_sg2=math.exp(sigma2)
    # skewness_prices_log_n=(exp_sg2+2)*(math.sqrt(exp_sg2-1))
    # kurtosis_prices_log_n=math.exp(4*sigma2)+2*math.exp(3*sigma2)+3*exp(2*sigma2)-6

    ret_min = mu - 9 * sigma2 ** 0.5
    ret_max = mu + 9 * sigma2 ** 0.5
    step_ret = 0.01
    ret_t = np.arange(ret_min * 0.65, ret_max * 0.65, step_ret)

    area_ret = integrate.quad(lambda k: pdf_returns(k), ret_min, ret_max)  # Table logReturns moment
    m1_returns = integrate.quad(lambda k: k * pdf_returns(k) / area_ret[0], ret_min, ret_max)
    m2_returns = integrate.quad(lambda k: (k - m1_returns[0]) ** 2 * pdf_returns(k) / area_ret[0], ret_min, ret_max)
    m3_returns = integrate.quad(lambda k: (k - m1_returns[0]) ** 3 * pdf_returns(k) / area_ret[0], ret_min, ret_max)
    m4_returns = integrate.quad(lambda k: (k - m1_returns[0]) ** 4 * pdf_returns(k) / area_ret[0], ret_min, ret_max)
    stand_deviation_log_ret = m2_returns[0] ** 0.5
    skew_log_ret = m3_returns[0] / (m2_returns[0] ** 0.5) ** 3  # Table LogReturns Moment
    kurt_log_ret = m4_returns[0] / (m2_returns[0] ** 0.5) ** 4  # Table LogReturns Moment

    pdf_bench_log_prices = lambda k: lognorm.pdf(k, sigma2 ** 0.5, mu, m1[0])

    pdf_bench_norm_returns = lambda k: norm.pdf(k, m1_returns[0], stand_deviation_log_ret)
    Area_Ret_Norm = integrate.quad(lambda k: pdf_bench_norm_returns(k), ret_min, ret_max)

    m3_ret_norm = integrate.quad(lambda k: (k - m1_returns[0]) ** 3 * pdf_bench_norm_returns(k), ret_min, ret_max)
    m4_ret_norm = integrate.quad(lambda k: (k - m1_returns[0]) ** 4 * pdf_bench_norm_returns(k), ret_min, ret_max)
    skew_norm = abs(m3_ret_norm[0] / (stand_deviation_log_ret ** 0.5) ** 3)  # Table LogReturns Moment
    kurt_norm = m4_ret_norm[0] / stand_deviation_log_ret ** 4
    pdf_returns = [float(pdf_returns(x)) for x in ret_t]  # output grafico3
    pdf_bench_norm_returns = [float(pdf_bench_norm_returns(x)) for x in ret_t]

    return pdf_returns, area_prices[0], expected_price, sigma2_price, skewness_prices, kurtosis_prices, \
           skewness_prices_log_n, kurtosis_prices_log_n, area_ret[0], m1_returns[0], m2_returns[0], skew_log_ret, \
           kurt_log_ret, pdf_bench_log_prices, pdf_bench_norm_returns, ret_t, skew_norm, kurt_norm, \
           stand_deviation_log_ret, sigma2, mu


def kolmogorov_smirnov_test(a0, a1, a2, s0, risk_free, div_yield, time, strike_min, strike_max, expected_price, sigma2,
                            ret_t, mu, m1_ret, std_deviation_log_ret):
    risk_free = risk_free / 100
    div_yield = div_yield / 100
    SD = s0 * math.exp(-div_yield * time)
    B = math.exp(-risk_free * time)
    step_k = 0.5

    # Test per i prices
    st = np.arange(strike_min * 0.75, strike_max * 1.25, step_k)  # output per grafico
    SD = s0 * math.exp(-div_yield * time)
    B = math.exp(-risk_free * time)
    x_fit_lgn = get_lognormal_fit(a0, a1, a2, SD, B, strike_min, strike_max)
    cdf_prices = lambda k: ImpliedCDFPrices_FullRange(a0, a1, a2, SD, B, k, strike_min, strike_max, x_fit_lgn)
    cdf_prices = [float(cdf_prices(x)) for x in st]
    cdf_bench_log_prices = lambda k: lognorm.cdf(k, sigma2 ** 0.5, mu, expected_price)
    cdf_bench_log_prices = [float(cdf_bench_log_prices(x)) for x in st]  # vs st
    kolmogorov_smirnov_prices = ks_2samp(cdf_prices, cdf_bench_log_prices)
    statistic_prices = kolmogorov_smirnov_prices[0]
    pvalue_prices = kolmogorov_smirnov_prices[1]

    # Test per i returns

    cdf_returns = lambda kret: ImpliedCDFReturns_FullRange(a0, a1, a2, SD, B, kret, strike_min, strike_max, x_fit_lgn)

    cdf_returns = [float(cdf_returns(x)) for x in ret_t]
    cdf_bench_norm_returns = lambda k: norm.cdf(k, m1_ret, std_deviation_log_ret)
    cdf_bench_norm_returns = [float(cdf_bench_norm_returns(x)) for x in ret_t]
    kolmogorov_smirnov_returns = ks_2samp(cdf_returns, cdf_bench_norm_returns)
    statistic_returns = kolmogorov_smirnov_returns[0]
    pvalue_returns = kolmogorov_smirnov_returns[1]

    return statistic_prices, pvalue_prices, statistic_returns, pvalue_returns


def create_implied_volatility_plot(strike, implied_volatility, s0, strike_min, strike_atm, strike_max, volatility, a0,
                                   a1, a2):
    strike = [round(st, 2) for st in strike]
    strike = [str(s) for s in strike]
    implied_volatility = [round(vol, 4) for vol in implied_volatility]

    data = ColumnDataSource(data=dict(
        strike=strike,
        implied_volatility=implied_volatility,
        strike_value=[strike_min, strike_atm, strike_max],
        volatility=volatility

    ))

    hover_implied_volatility = HoverTool(attachment="above", names=['implied vol'],
                                         tooltips=[("Strike", "@strike"), ("Implied vol", "@implied_volatility")])

    x_range = [strike_min, strike_max + 10]
    y_range = [0, max(implied_volatility) + 0.03]
    fig = bp.figure(tools=['save, pan, box_zoom, reset, crosshair', hover_implied_volatility], x_range=x_range,
                    y_range=y_range, plot_height=450, toolbar_location="right", x_axis_label='Exercise price',
                    y_axis_label='Volatility x root time')

    fig.line(x='strike', y='implied_volatility', source=data, color="#0095B6", line_width=4, alpha=0.8,
             name='implied vol')
    fig.square(x=s0, y=0, source=data, legend='Spot Price', color="#050402", size=8)
    fig.circle(x='strike_value', y='volatility', source=data, color="#D21F1B", legend='Implied Volatility', size=6)

    fig.legend.orientation = "horizontal"
    fig.legend.location = "bottom_left"
    fig.toolbar.active_drag = None

    callback = CustomJS(args=dict(source=data, a0=a0, a1=a1, a2=a2, strike_min=strike_min, strike_atm=strike_atm,
                                  strike_max=strike_max, y_range=fig.y_range), code="""
        var data = source.data;
        var vol_min = vol_min.value;
        var vol_atm = vol_atm.value;
        var vol_max = vol_max.value;
        var strike = data['strike'];
        var volatility = data['volatility'];
        var implied_volatility = data['implied_volatility'];
        
        var strike_matrix =([[1, strike_min, (Math.pow(strike_min,2))], [1, strike_atm, (Math.pow(strike_atm,2))], 
        [1, strike_max, (Math.pow(strike_max,2))]]);
        var inv_strike_matrix = math.inv(strike_matrix);
        volatility [0] = vol_min;
        volatility [1] = vol_atm;
        volatility [2] = vol_max;
        var parameters = math.multiply(inv_strike_matrix, math.transpose(volatility));
        a0=parameters[0];
        a1=parameters[1];
        a2=parameters[2];
        
        for (var i = 0; i < strike.length; i++) {
            implied_volatility[i] = a0 + a1 * strike[i] + a2 * Math.pow(strike[i], 2);
        }
        y_range.end = math.max(implied_volatility)+0.02;
        source.change.emit();
    """)

    vol_min_slider = Slider(start=0, end=0.5, value=volatility[0], step=.05, title="Min", callback=callback)
    callback.args["vol_min"] = vol_min_slider

    vol_atm_slider = Slider(start=0, end=0.5, value=volatility[1], step=.05, title="Atm", callback=callback)
    callback.args["vol_atm"] = vol_atm_slider

    vol_max_slider = Slider(start=0, end=0.5, value=volatility[2], step=.05, title="Max", callback=callback)
    callback.args["vol_max"] = vol_max_slider

    layout = column(
        fig,
        column(vol_min_slider, vol_atm_slider, vol_max_slider)
    )

    from bokeh.embed import components
    script, div = components(layout)
    return script, div


def create_plot_return_underlying_distribution(ret_t, pdf_ret, pdf_bench_norm_returns):
    ret_t = [round(st, 2) for st in ret_t]
    pdf_ret = [round(pdfret, 10) for pdfret in pdf_ret]
    pdf_bench_norm_returns = [round(pdf_benchNorm, 10) for pdf_benchNorm in pdf_bench_norm_returns]

    data = ColumnDataSource(data=dict(
        ret_t=ret_t,
        pdf_ret=pdf_ret,
        pdf_bench_norm_returns=pdf_bench_norm_returns
    ))

    x_range = [min(ret_t), max(ret_t)]
    y_range = [0, max(pdf_ret) * 1.10]
    hover_returns = HoverTool(attachment="left", names=['pdf ret'],
                              tooltips=[("Return", "@ret_t"), ("Pdf", "@pdf_ret")])

    hover_normal = HoverTool(attachment="right", names=['pdf norm'],
                             tooltips=[("Return", "@ret_t"), ("Benchmark Norm", "@pdf_bench_norm_returns")])

    fig = bp.figure(tools=['save, pan, box_zoom, reset, crosshair', hover_returns, hover_normal], x_range=x_range,
                    y_range=y_range, plot_height=450, toolbar_location="right", x_axis_label='Log Returns',
                    y_axis_label='Probability Density')

    fig.line(x='ret_t', y='pdf_ret', source=data, legend="CEQ distribution", color="#0095B6", alpha=0.9, line_width=4,
             name='pdf ret')

    fig.line(x='ret_t', y='pdf_bench_norm_returns', source=data, legend="Benchmark Normal", color="#D21F1B", alpha=0.6,
             line_width=4, name='pdf norm')

    fig.legend.location = "top_right"
    fig.toolbar.active_drag = None
    fig.legend.click_policy = "hide"

    from bokeh.embed import components
    script, div = components(fig)

    return script, div


def compute_index_underlying_distribution(a0, a1, a2, s0, risk_free, div_yield, time, strike_min, strike_max,
                                          expected_price, sigma2, mu):
    step_k = 0.5
    risk_free = risk_free / 100
    div_yield = div_yield / 100

    SD = s0 * math.exp(-div_yield * time)
    B = math.exp(-risk_free * time)

    x_fit_lgn = get_lognormal_fit(a0, a1, a2, SD, B, strike_min, strike_max)

    pdf_prices = lambda k: ImpliedPDFPrices_FullRange(a0, a1, a2, SD, B, k, strike_min, strike_max, x_fit_lgn)
    st = np.arange(strike_min * 0.8, strike_max * 1.2, step_k)  # output per grafico
    pdf = [float(pdf_prices(x)) for x in st]  # output grafico2

    pdf_bench_log_prices = lambda k: lognorm.pdf(k, sigma2 ** 0.5, mu, expected_price)
    pdf_bench_log_prices = [float(pdf_bench_log_prices(x)) for x in st]

    return st, pdf, pdf_bench_log_prices


def create_plot_index_underlying_distribution(st, pdf, pdf_bench_log_prices, s0, strike_min, strike_max):
    st = [round(st, 2) for st in st]
    pdf = [round(pdf, 10) for pdf in pdf]
    pdf_bench_log_prices = [round(pdf_bench, 10) for pdf_bench in pdf_bench_log_prices]

    data = ColumnDataSource(data=dict(
        st=st,
        pdf=pdf,
        pdf_bench_log_prices=pdf_bench_log_prices
    ))

    hover_pdf = HoverTool(attachment="left", names=['pdf prices'], tooltips=[("Strike", "@st"), ("Pdf", "@pdf")])

    hover_log_norm = HoverTool(attachment="right", names=['bench logNorm'],
                               tooltips=[("Strike", "@st"), ("Bench LogNorm", "@pdf_bench_log_prices")])

    x_range = [strike_min * 0.8, strike_max * 1.2]
    y_range = [0, max(pdf) * 1.10]
    fig = bp.figure(tools=['save, pan, box_zoom, reset, crosshair', hover_pdf, hover_log_norm], x_range=x_range,
                    y_range=y_range, plot_height=450, toolbar_location="right", x_axis_label='Index Value',
                    y_axis_label='Probability Density')

    fig.line(x='st', y='pdf', source=data, legend="CEQ distribution", color="#0095B6", alpha=0.9, line_width=4,
             name='pdf prices')

    fig.line(x='st', y='pdf_bench_log_prices', source=data, legend="Benchmark LogNormal", color="#D21F1B", alpha=0.6,
             line_width=4, name='bench logNorm')

    fig.square(x=s0, y=0, legend="Spot Price", color="#050402", size=8)

    fig.legend.location = "top_right"
    fig.toolbar.active_drag = None
    fig.legend.click_policy = "hide"

    from bokeh.embed import components
    script, div = components(fig)

    return script, div


def compute_index_underlying_cdf(a0, a1, a2, s0, risk_free, div_yield, time, strike_min, strike_max, expected_price,
                                 sigma2, mu):
    step_k = 0.5
    risk_free = risk_free / 100
    div_yield = div_yield / 100
    SD = s0 * math.exp(-div_yield * time)
    B = math.exp(-risk_free * time)

    x_fit_lgn = get_lognormal_fit(a0, a1, a2, SD, B, strike_min, strike_max)

    st = np.arange(strike_min * 0.75, strike_max * 1.25, step_k)  # output per grafico
    cdf_prices = lambda k: ImpliedCDFPrices_FullRange(a0, a1, a2, SD, B, k, strike_min, strike_max, x_fit_lgn)
    cdf_prices = [float(cdf_prices(x)) for x in st]
    cdf_bench_log_prices = lambda k: lognorm.cdf(k, sigma2 ** 0.5, mu, expected_price)
    cdf_bench_log_prices = [float(cdf_bench_log_prices(x)) for x in st]  # vs st

    return cdf_prices, cdf_bench_log_prices, st


def create_plot_price_cdf(st, cdf_prices, cdf_bench_log_prices, strike_min, strike_max):
    st = [round(s, 2) for s in st]

    data = ColumnDataSource(data=dict(
        st=st,
        cdf_prices=cdf_prices,
        cdf_bench_log_prices=cdf_bench_log_prices
    ))
    hover_cdf = HoverTool(attachment="left", names=['cdf'], tooltips=[("Strike", "@st"), ("Cdf", "@cdf_prices")])

    hover_log_norm = HoverTool(attachment="right", names=['bench logNorm'],
                               tooltips=[("Strike", "@st"), ("Bench LogNorm", "@cdf_bench_log_prices")])

    x_range = [strike_min * 0.8, strike_max * 1.2]
    y_range = [0, 1.1]
    fig = bp.figure(tools=['save, pan, box_zoom, reset, crosshair', hover_cdf, hover_log_norm], x_range=x_range,
                    y_range=y_range, plot_height=450, toolbar_location="right", x_axis_label='Index Value',
                    y_axis_label='Cumulative Probability')

    fig.line(x='st', y='cdf_prices', source=data, legend="CEQ distribution", color="#0095B6", alpha=0.9, line_width=4,
             name='cdf')

    fig.line(x='st', y='cdf_bench_log_prices', source=data, legend="Benchmark LogNormal", color="#D21F1B", alpha=0.6,
             line_width=4, name='bench logNorm')

    fig.legend.location = "bottom_right"
    fig.toolbar.active_drag = None
    fig.legend.click_policy = "hide"

    from bokeh.embed import components
    script, div = components(fig)

    return script, div


def compute_returns_cdf(a0, a1, a2, s0, risk_free, div_yield, time, strike_min, strike_max, m1_returns,
                        stand_deviation_log_ret, ret_t):
    risk_free = risk_free / 100
    div_yield = div_yield / 100
    SD = s0 * math.exp(-div_yield * time)
    B = math.exp(-risk_free * time)

    x_fit_lgn = get_lognormal_fit(a0, a1, a2, SD, B, strike_min, strike_max)

    cdf_returns = lambda kret: ImpliedCDFReturns_FullRange(a0, a1, a2, SD, B, kret, strike_min, strike_max,
                                                           x_fit_lgn)

    cdf_returns = [float(cdf_returns(x)) for x in ret_t]
    cdf_bench_norm_returns = lambda k: norm.cdf(k, m1_returns, stand_deviation_log_ret)
    cdf_bench_norm_returns = [float(cdf_bench_norm_returns(x)) for x in ret_t]

    return ret_t, cdf_returns, cdf_bench_norm_returns


def create_plot_return_cdf(ret_t, cdf_returns, cdf_bench_norm_returns):
    data = ColumnDataSource(data=dict(
        ret_t=ret_t,
        cdf_returns=cdf_returns,
        cdf_bench_norm_returns=cdf_bench_norm_returns
    ))

    hover_cdf = HoverTool(attachment="left", names=['cdf ret'],
                          tooltips=[("Strike", "@ret_t"), ("Cdf", "@cdf_returns")])

    hover_norm = HoverTool(attachment="right", names=['bench norm'],
                           tooltips=[("Strike", "@ret_t"), ("Bench Norm", "@cdf_bench_norm_returns")])

    x_range = [min(ret_t), max(ret_t)]
    y_range = [0, 1.1]
    fig = bp.figure(tools=['save, pan, box_zoom, reset, crosshair', hover_cdf, hover_norm], x_range=x_range,
                    y_range=y_range, plot_height=450, toolbar_location="right", x_axis_label='Log Returns',
                    y_axis_label='Cumulative Probability')

    fig.line(x='ret_t', y='cdf_returns', source=data, legend="CEQ distribution", color="#0095B6", alpha=0.9,
             line_width=4, name='cdf ret')

    fig.line(x='ret_t', y='cdf_bench_norm_returns', source=data, legend="Benchmark Normal", color="#D21F1B", alpha=0.6,
             line_width=4, name='bench norm')

    fig.legend.location = "bottom_right"
    fig.toolbar.active_drag = None
    fig.legend.click_policy = "hide"

    from bokeh.embed import components
    script, div = components(fig)

    return script, div
