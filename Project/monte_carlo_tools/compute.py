# -*- coding: utf-8 -*-
"""
Created on Wed May 13 14:38:52 2020

@author: Diego De Bortoli
"""
from monte_carlo_tools.get_mc_abm import get_mc_abm
from monte_carlo_tools.get_mc_cir import get_mc_cir
from monte_carlo_tools.get_mc_heston import get_mc_heston
from monte_carlo_tools.get_mc_gmr import get_mc_gmr
from monte_carlo_tools.get_moments import get_moments
from monte_carlo_tools.plot_simulated_paths import get_simulated_paths
from monte_carlo_tools.moments_plot import get_moments_plot
from monte_carlo_tools.histograms_plot import get_histograms_plot

# from bokeh.plotting import figure, output_file, show
# from bokeh.layouts import gridplot

import numpy as np

"""Run  main_montecarlo_tool the output are 3 html page containing different plots
    
    1 - fix steps, nsimulations, time horizon and the model line 33
    2 - Insert model parameters and compute simulated paths line 44
    3 - Compute moments and quatiles line 113
    4 - Compute plot  3 different in html page line 118

"""


def get_simutalted_path_and_moments(T, NStep, NPaths, model, X0, mu_abm, sigma_abm,
                                    mu_gbm, sigma_gbm, alpha_cir, mu_cir, sigma_cir,
                                    alpha_gmr, mu_gmr, sigma_gmr, mu_heston, v0_heston,
                                    alpha_heston, beta_heston, eta_heston, rho_heston):
    """1 - Fix steps, nsimulations, time horizon and the model"""
    # T=5
    # NStep=50
    # NPaths=1000

    # NBins = 130
    timestep = np.linspace(0, T, NStep + 1)
    # NBins=max([min([NBins, round(NPaths**0.5)]),10])
    # model = 5  # 0-abm  1-gbm  2-cir  3-mrg  4-heston

    """2 - Insert model parameters and compute simulated paths"""

    # Arithmetic Brownian Motion
    if model == 0:
        # X0 = 100
        # mu_abm = 0
        # sigma_abm = 0.2
        parameters = [mu_abm, sigma_abm]

        X = get_mc_abm(X0, mu_abm, sigma_abm, T, NStep, NPaths)
        # mean = np.mean(X[-1,:])
        # std = np.std(X[-1,:])

    # Geometric Brownian Motion
    elif model == 1:
        # X0 = 1
        # mu_gbm = 0.01
        # sigma_gbm = 0.2
        parameters = [mu_gbm, sigma_gbm]

        X = np.exp(get_mc_abm(np.log(X0), mu_gbm - sigma_gbm * sigma_gbm / 2, sigma_gbm, T, NStep, NPaths))
        # mean = np.mean(X[-1,:])
        # std = np.std(X[-1,:])

    # Cox Ingersson Ross

    elif model == 2:
        # X0 = 0.1
        # alpha_cir = 1
        # mu_cir = 0.05
        # sigma_cir = 0.1
        parameters = [alpha_cir, mu_cir, sigma_cir]

        X = get_mc_cir(X0, alpha_cir, mu_cir, sigma_cir, T, NStep, NPaths)
        # mean = np.mean(X[-1,:])
        # std = np.std(X[-1,:])

    # Mean Reverting Gaussian
    elif model == 3:
        # X0 = 0.1
        # alpha_gmr = 1
        # mu_gmr = -0.05
        # sigma_gmr = 0.1
        parameters = [alpha_gmr, mu_gmr, sigma_gmr]

        X = get_mc_gmr(X0, alpha_gmr, mu_gmr, sigma_gmr, T, NStep, NPaths)
        # mean = np.mean(X[-1,:])
        # std = np.std(X[-1,:])

    # Heston Model
    else:
        # X0 = 0.1
        # mu_heston = 0
        # v0_heston = 0.2**2
        # alpha_heston = 0.1
        # beta_heston = 0.25**2
        # eta_heston = 0.2
        # rho_heston = -0.8
        parameters = [v0_heston, mu_heston, alpha_heston, beta_heston, eta_heston, rho_heston]

        X = get_mc_heston(X0, v0_heston, mu_heston, alpha_heston, beta_heston, eta_heston, rho_heston, T, NStep, NPaths)
        # mean = np.mean(X[-1,:])
        # std = np.std(X[-1,:])

    # print([mean, std])
    simulated_paths = X
    """3 - Compute moments and quatiles"""
    moments, quantiles = get_moments(model, X0, parameters, T, NStep)

    return simulated_paths, moments, quantiles, timestep


"""4 - Compute plot  3 different in html page"""

"Plot simulated paths"


def create_plot_simulated_paths(simulated_paths, timestep, NStep, NPaths, quantiles):
    p1, p2 = get_simulated_paths(simulated_paths, timestep, NStep, NPaths, quantiles)
    plots = {'Paths': p1, 'Hist': p2}

    from bokeh.embed import components
    script, div = components(plots)

    return script, div


# output_file("legend.html", title="example")
# show(gridplot([p1, p2], ncols=2, plot_width=400, plot_height=400)) 


"Plot moments"


def create_plot_moments(simulated_paths, moments, timestep):
    p3, p4, p5, p6 = get_moments_plot(simulated_paths, moments, timestep)
    plots = {'exp_value': p3, 'st_dev': p4, 'skew': p5, 'kurt': p6}

    from bokeh.embed import components
    script, div = components(plots)
    return script, div


# output_file("moments.html", title="example")
# show(gridplot([p3, p4, p5, p6], ncols=2, plot_width=400, plot_height=400)) 


"plot histogram pdf"


def create_plot_histogram(simulated_paths, NStep):
    p7, p8, p9 = get_histograms_plot(simulated_paths, NStep)

    plots = {'hist_t1': p7, 'hist_t2': p8, 'hist_t3': p9}

    from bokeh.embed import components
    script, div = components(plots)

    return script, div
# output_file("legend.html", title="Simulated Density")
# show(gridplot([p7, p8, p9], ncols=2, plot_width=400, plot_height=400))
