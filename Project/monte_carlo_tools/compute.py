# -*- coding: utf-8 -*-
"""
Created on Wed May 13 14:38:52 2020

@author: Diego De Bortoli
"""
from monte_carlo_tools.get_mc_abm import get_mc_abm
from monte_carlo_tools.get_mc_cir import get_mc_cir
from monte_carlo_tools.get_mc_heston import get_mc_heston
from monte_carlo_tools.get_mc_gmr import get_mc_gmr
from monte_carlo_tools.get_mc_garch import get_mc_garch
from monte_carlo_tools.get_mc_mjd import get_mc_mjd
from monte_carlo_tools.get_mc_dedj import get_mc_dedj
from monte_carlo_tools.get_mc_vg import get_mc_vg

from monte_carlo_tools.get_moments import get_moments
from scipy.stats import skew, kurtosis
from bokeh.plotting import ColumnDataSource
from bokeh.models import HoverTool
from bokeh.layouts import gridplot
from bokeh.palettes import Spectral11
from bokeh.models import BoxAnnotation

import bokeh.plotting as bp
import numpy as np
import itertools

"""Run  main_montecarlo_tool the output are 3 html page containing different plots
    
    1 - fix steps, nsimulations, time horizon and the model line 33
    2 - Insert model parameters and compute simulated paths line 44
    3 - Compute moments and quatiles line 113
    4 - Compute plot  3 different in html page line 118

"""


# form.price_abm.data, form.price_gbm.data,
# form.price_cir.data, form.price_mrg.data, form.price_heston.data

def get_simutalted_path_and_moments(T, NStep, NPaths, model, mu_abm, sigma_abm, mu_cir, alpha_cir, sigma_cir, mu_dejd,
                                    sigma_dejd, lambda_dejd, p_dejd, eta1_dejd, eta2_dejd, mu_ewma, v0_ewma, omega_ewma,
                                    alpha_ewma, beta_ewma, asymm_ewma, mu_garch, v0_garch, omega_garch, alpha_garch,
                                    beta_garch, asymm_garch, mu_gbm, sigma_gbm, mu_heston, v0_heston, alpha_heston,
                                    beta_heston, eta_heston, rho_heston, mu_mjd, sigma_mjd, lambda_mjd, mu_jumps_mjd,
                                    sg_jumps_mjd, mu_gmr, alpha_gmr, sigma_gmr, theta_vg, sigma_vg, kappa_vg,
                                    price_abm, price_cir, price_dejd, price_ewma, price_garch, price_gbm, price_heston,
                                    price_mjd, price_mrg, price_vg):
    """1 - Fix steps, nsimulations, time horizon and the model"""
    # T=5
    # NStep=50
    # NPaths=1000

    # NBins = 130
    timestep = np.linspace(0, T, NStep + 1)
    # NBins=max([min([NBins, round(NPaths**0.5)]),10])
    # model = 5  # 0-abm  1-gbm  2-cir  3-mrg  4-heston

    """2 - Insert model parameters and compute simulated paths"""

    model = int(model)
    # Arithmetic Brownian Motion
    if model == 0:
        # X0 = 100
        # mu_abm = 0
        # sigma_abm = 0.2
        parameters = [mu_abm, sigma_abm]

        X = get_mc_abm(price_abm, mu_abm, sigma_abm, T, NStep, NPaths)
        # mean = np.mean(X[-1,:])
        # std = np.std(X[-1,:])
        X0 = price_abm

    # Cox Ingersson Ross
    elif model == 1:
        # X0 = 0.1
        # alpha_cir = 1
        # mu_cir = 0.05
        # sigma_cir = 0.1
        parameters = [alpha_cir, mu_cir, sigma_cir]

        X = get_mc_cir(price_cir, alpha_cir, mu_cir, sigma_cir, T, NStep, NPaths)
        # mean = np.mean(X[-1,:])
        # std = np.std(X[-1,:])
        X0 = price_cir

    # DEJD
    elif model == 2:
        # mu_dejd = 0.01
        # sigma_dejd = 0.2
        # lambda_dejd = 0.1
        # p_dejd = 0.2
        # eta1_dejd = 12
        # eta2_dejd = 23
        parameters = [mu_dejd, sigma_dejd, lambda_dejd, p_dejd, eta1_dejd, eta2_dejd]
        # X0 = 0
        X = get_mc_dedj(price_dejd, mu_dejd, sigma_dejd, lambda_dejd, p_dejd, eta1_dejd, eta2_dejd, T, NStep, NPaths)
        # mean = np.mean(X[-1,:])
        # std = np.std(X[-1,:])
        X0 = price_dejd

    # EWMA
    elif model == 3:
        # v0_ewma = 0.2**2/250
        # mu_ewma = 0
        # omega_ewma = 0
        # alpha_ewma = 0.1
        # beta_ewma = 1-alpha_ewma
        # asymm_ewma = 0
        parameters = [mu_ewma, v0_ewma, omega_ewma, alpha_ewma, beta_ewma, asymm_ewma]
        # X0 = 0

        X = get_mc_garch(price_ewma, mu_ewma, v0_ewma, omega_ewma, alpha_ewma, beta_ewma,
                         asymm_ewma, T, NStep, NPaths)
        # mean = np.mean(X[-1,:])
        # std = np.std(X[-1,:])
        X0 = price_ewma

    # GARCH
    elif model == 4:
        # v0_garch = 0.2**2/250
        # mu_garch = 0.0
        # alpha_garch = 0.1
        # beta_garch = 0.85
        # omega_garch = 5.7800*10**(-6)
        # asymm_garch = 0
        parameters = [mu_garch, v0_garch, omega_garch, alpha_garch, beta_garch, asymm_garch]
        # X0 = 0.0
        X = get_mc_garch(price_garch, mu_garch, v0_garch, omega_garch, alpha_garch, beta_garch,
                         asymm_garch, T, NStep, NPaths)
        # mean = np.mean(X[-1,:])
        # std = np.std(X[-1,:])
        X0 = price_garch

    # Geometric Brownian Motion
    elif model == 5:
        # X0 = 1
        # mu_gbm = 0.01
        # sigma_gbm = 0.2
        parameters = [mu_gbm, sigma_gbm]

        X = np.exp(get_mc_abm(np.log(price_gbm), mu_gbm - sigma_gbm * sigma_gbm / 2, sigma_gbm, T, NStep, NPaths))
        # mean = np.mean(X[-1,:])
        # std = np.std(X[-1,:])
        X0 = price_gbm

    # Heston Model
    elif model == 6:
        # X0 = 0.1
        # mu_heston = 0
        # v0_heston = 0.2**2
        # alpha_heston = 0.1
        # beta_heston = 0.25**2
        # eta_heston = 0.2
        # rho_heston = -0.8
        parameters = [v0_heston, mu_heston, alpha_heston, beta_heston, eta_heston, rho_heston]

        X = get_mc_heston(price_heston, v0_heston, mu_heston, alpha_heston, beta_heston, eta_heston, rho_heston, T,
                          NStep, NPaths)
        # mean = np.mean(X[-1,:])
        # std = np.std(X[-1,:])
        X0 = price_heston
    # print([mean, std])

    # MJD
    elif model == 7:
        # mu_mjd = 0.01
        # sigma_mjd = 0.1
        # lambda_mjd = 0.5
        # mu_jumps_mjd = -0.1
        # sg_jumps_mjd = 0.2
        parameters = [mu_mjd, sigma_mjd, lambda_mjd, mu_jumps_mjd, sg_jumps_mjd]
        # X0 = 0
        X = get_mc_mjd(price_mjd, mu_mjd, sigma_mjd, lambda_mjd, mu_jumps_mjd, sg_jumps_mjd, T, NStep, NPaths)
        # mean = np.mean(X[-1,:])
        # std = np.std(X[-1,:])
        X0 = price_mjd

    # Mean Reverting Gaussian
    elif model == 8:
        # X0 = 0.1
        # alpha_gmr = 1
        # mu_gmr = -0.05
        # sigma_gmr = 0.1
        parameters = [alpha_gmr, mu_gmr, sigma_gmr]

        X = get_mc_gmr(price_mrg, alpha_gmr, mu_gmr, sigma_gmr, T, NStep, NPaths)
        # mean = np.mean(X[-1,:])
        # std = np.std(X[-1,:])
        X0 = price_mrg

    # VG   
    else:  # model==9
        # theta_vg = -0.01
        # sigma_vg = 0.2
        # kappa_vg = 0.3
        parameters = [theta_vg, sigma_vg, kappa_vg]
        # X0=0.1
        X = get_mc_vg(price_vg, theta_vg, sigma_vg, kappa_vg, T, NStep, NPaths)
        X0 = price_vg

    simulated_paths = X
    """3 - Compute moments and quatiles"""
    moments, quantiles = get_moments(model, X0, parameters, T, NStep)

    return simulated_paths, moments, quantiles, timestep


def create_plot_simulated_paths(simulated_paths, timestep, NStep, NPaths, quantiles):
    x = []
    y = []
    for i in range(0, NStep):
        min_x = min(simulated_paths[i, :])
        x.append(min_x)
        max_y = max(simulated_paths[i, :])
        y.append(max_y)

    y_range = [min(x), max(y)]

    fig_simulated_1 = bp.figure(tools=['save, pan, box_zoom, reset, crosshair'], sizing_mode='scale_both',
                                y_range=y_range, x_axis_label='Time')
    colors = itertools.cycle(Spectral11)

    for i, color in zip(range(0, NPaths), colors):
        fig_simulated_1.line(timestep, simulated_paths[:, i], color=color)

    last_quantiles = quantiles[-1, :]
    confidence_interval = BoxAnnotation(bottom=last_quantiles[0], top=last_quantiles[1], fill_color='#0095B6',
                                        fill_alpha=0.1)
    fig_simulated_1.add_layout(confidence_interval)

    hhist, hedges = np.histogram(simulated_paths[-1, :], bins=20)
    # hzeros = np.zeros(len(hedges)-1)
    # hmax = max(hhist)*1.0
    # LINE_ARGS = dict(color="#3A5785", line_color=None)

    fig_simulated_2 = bp.figure(tools=['save, pan, box_zoom, reset, crosshair'], sizing_mode='scale_both',
                                x_axis_label='Frequency', y_range=y_range)

    fig_simulated_2.xgrid.grid_line_color = None
    fig_simulated_2.quad(left=0, bottom=hedges[:-1], top=hedges[1:], right=hhist, color="#ffffff", line_color="#0095B6")
    fig_simulated_2.add_layout(confidence_interval)

    figure = gridplot([[fig_simulated_1, fig_simulated_2]], sizing_mode='scale_both')

    from bokeh.embed import components
    script, div = components(figure)

    return script, div


def create_plot_moments(simulated_paths, moments, timestep):
    exp_value_simulated = np.mean(simulated_paths, axis=1)
    variance_simulated = np.var(simulated_paths, axis=1) ** 0.5
    skewness_simulated = skew(simulated_paths, axis=1)
    skewness_simulated[0] = 0
    kurtosis_simulated = kurtosis(simulated_paths, axis=1) + 3
    kurtosis_simulated[0] = 3

    exp_value_theoretical = moments[:, 0]
    variance_theoretical = moments[:, 1]
    skewness_theoretical = moments[:, 2]
    kurtosis_theoretical = moments[:, 3]

    data_exp_value = ColumnDataSource(data=dict(
        exp_value_theoretical=exp_value_theoretical,
        exp_value_simulated=exp_value_simulated,
        timestep=timestep))

    hover_exp_theoretical = HoverTool(attachment="above", names=['theoretical expected value'],
                                      tooltips=[("Theoretical Expected Value ", "@exp_value_theoretical"),
                                                ("Nstep", "@timestep")])

    hover_exp_simulated = HoverTool(attachment="below", names=['simulated expected value'],
                                    tooltips=[("Simulated Expected Value ", "@exp_value_simulated"),
                                              ("Nstep", "@timestep")])

    fig_exp_value = bp.figure(
        tools=['save, pan, box_zoom, reset, crosshair', hover_exp_theoretical, hover_exp_simulated],
        sizing_mode='scale_both', x_axis_label='Time', y_axis_label='Expected Value')

    fig_exp_value.line(x='timestep', y='exp_value_theoretical', source=data_exp_value,
                       legend_label="Theoretical Expected Value", color="#D21F1B", alpha=0.9, line_width=1,
                       name='theoretical expected value')

    fig_exp_value.line(x='timestep', y='exp_value_simulated', source=data_exp_value,
                       legend_label="Simulated Expected Value", color="#0095B6", alpha=0.9, line_width=1,
                       name='simulated expected value')

    fig_exp_value.legend.location = "bottom_left"
    fig_exp_value.toolbar.active_drag = None

    data_variance = ColumnDataSource(data=dict(
        variance_theoretical=variance_theoretical,
        variance_simulated=variance_simulated,
        timestep=timestep))

    hover_var_theoretical = HoverTool(attachment="above", names=['theoretical standard deviation'],
                                      tooltips=[("Theoretical Variance ", "@variance_theoretical"),
                                                ("Nstep", "@timestep")])

    hover_var_simulated = HoverTool(attachment="below", names=['simulated standard deviation'],
                                    tooltips=[("Simulated Variance ", "@variance_simulated"), ("Nstep", "@timestep")])

    fig_variance_value = bp.figure(
        tools=['save, pan, box_zoom, reset, crosshair', hover_var_theoretical, hover_var_simulated],
        sizing_mode='scale_both', x_axis_label='Time', y_axis_label=' Standard Deviation')

    fig_variance_value.line(x='timestep', y='variance_theoretical', source=data_variance,
                            legend_label="Theoretical Standard Deviation", color="#D21F1B", alpha=0.9, line_width=1,
                            name='theoretical standard deviation')

    fig_variance_value.line(x='timestep', y='variance_simulated', source=data_variance,
                            legend_label="Simulated Standard Deviation", color="#0095B6", alpha=0.9, line_width=1,
                            name='simulated standard deviation')

    fig_variance_value.legend.location = "bottom_right"
    fig_variance_value.toolbar.active_drag = None

    data_skewness = ColumnDataSource(data=dict(
        skewness_theoretical=skewness_theoretical,
        skewness_simulated=skewness_simulated,
        timestep=timestep))

    hover_skew_theoretical = HoverTool(attachment="above", names=['theoretical skewness'],
                                       tooltips=[("Theoretical Skewness ", "@skewness_theoretical"),
                                                 ("Nstep", "@timestep")])

    hover_skew_simulated = HoverTool(attachment="below", names=['simulated skewness'],
                                     tooltips=[("Simulated Skewness ", "@skewness_simulated"), ("Nstep", "@timestep")])

    fig_skewness_value = bp.figure(
        tools=['save, pan, box_zoom, reset, crosshair', hover_skew_theoretical, hover_skew_simulated],
        sizing_mode='scale_both', x_axis_label='Time', y_axis_label='Skewness')

    fig_skewness_value.line(x='timestep', y='skewness_theoretical', source=data_skewness,
                            legend_label="Theoretical Skewness", color="#D21F1B", alpha=0.9, line_width=1,
                            name='theoretical skewness')

    fig_skewness_value.line(x='timestep', y='skewness_simulated', source=data_skewness,
                            legend_label="Simulated Skewness", color="#0095B6", alpha=0.9, line_width=1,
                            name='simulated skewness')

    fig_skewness_value.legend.location = "top_right"
    fig_skewness_value.toolbar.active_drag = None

    data_kurtosis = ColumnDataSource(data=dict(
        kurtosis_theoretical=kurtosis_theoretical,
        kurtosis_simulated=kurtosis_simulated,
        timestep=timestep))

    hover_kurt_theoretical = HoverTool(attachment="above", names=['theoretical kurtosis'],
                                       tooltips=[("Theoretical Kurtosis ", "@kurtosis_theoretical"),
                                                 ("Nstep", "@timestep")])

    hover_kurt_simulated = HoverTool(attachment="below", names=['simulated kurtosis'],
                                     tooltips=[("Simulated Kurtosis ", "@kurtosis_simulated"), ("Nstep", "@timestep")])

    fig_kurtosis_value = bp.figure(
        tools=['save, pan, box_zoom, reset, crosshair', hover_kurt_theoretical, hover_kurt_simulated],
        sizing_mode='scale_both', x_axis_label='Time', y_axis_label='Kurtosis')

    fig_kurtosis_value.line(x='timestep', y='kurtosis_theoretical', source=data_kurtosis,
                            legend_label="Theoretical Kurtosis", color="#D21F1B", alpha=0.9, line_width=1,
                            name='theoretical kurtosis')

    fig_kurtosis_value.line(x='timestep', y='kurtosis_simulated', source=data_kurtosis,
                            legend_label="Simulated Kurtosis", color="#0095B6", alpha=0.9, line_width=1,
                            name='simulated kurtosis')

    fig_kurtosis_value.legend.location = "bottom_right"
    fig_kurtosis_value.toolbar.active_drag = None

    figure = gridplot([[fig_exp_value, fig_variance_value], [fig_skewness_value, fig_kurtosis_value]],
                      sizing_mode='scale_both')

    from bokeh.embed import components
    script, div = components(figure)
    return script, div


def create_plot_histogram(simulated_paths, NStep):
    t1 = int(NStep / 4)
    t2 = int(NStep / 2)
    t3 = NStep

    min_x = np.quantile(simulated_paths[-1, :], 0.01)
    max_x = np.quantile(simulated_paths[-1, :], 0.99)
    hhist, hedges = np.histogram(simulated_paths[t1, :], density=True, bins=100)

    x_range = [min_x, max_x]

    fig_hist_1 = bp.figure(title='Simulated distribution after ' + str(t1) + ' steps',
                           tools=['save, pan, box_zoom, reset, crosshair'], sizing_mode='scale_both',
                           y_axis_location="right", x_range=x_range)

    fig_hist_1.xaxis.axis_label = "X"
    fig_hist_1.xgrid.grid_line_color = None
    fig_hist_1.quad(bottom=0, left=hedges[:-1], right=hedges[1:], top=hhist, color="#0095B6", line_color="#ffffff")

    hhist, hedges = np.histogram(simulated_paths[t2, :], density=True, bins=100)

    fig_hist_2 = bp.figure(title='Simulated distribution after ' + str(t2) + ' steps',
                           tools=['save, pan, box_zoom, reset, crosshair'], sizing_mode='scale_both',
                           y_axis_location="right", x_range=x_range)

    fig_hist_2.xaxis.axis_label = "X"
    fig_hist_2.xgrid.grid_line_color = None
    fig_hist_2.quad(bottom=0, left=hedges[:-1], right=hedges[1:], top=hhist, color="#0095B6", line_color="#ffffff")

    hhist, hedges = np.histogram(simulated_paths[t3, :], density=True, bins=100)

    fig_hist_3 = bp.figure(title='Simulated distribution after ' + str(t3) + ' steps',
                           tools=['save, pan, box_zoom, reset, crosshair'], sizing_mode='scale_both',
                           y_axis_location="right", x_range=x_range)

    fig_hist_3.xaxis.axis_label = "X"
    fig_hist_3.xgrid.grid_line_color = None
    fig_hist_3.quad(bottom=0, left=hedges[:-1], right=hedges[1:], top=hhist, color="#0095B6", line_color="#ffffff")

    figure = gridplot([[fig_hist_1, fig_hist_2], [fig_hist_3]], sizing_mode='scale_both')

    from bokeh.embed import components
    script, div = components(figure)

    return script, div
