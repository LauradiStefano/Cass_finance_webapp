# -*- coding: utf-8 -*-
"""
Created on Fri May  3 09:56:26 2019

@author: Diego
"""
import bokeh.plotting as bp
from bokeh.models import HoverTool
from bokeh.plotting import ColumnDataSource

from asian_option.get_MJD_option import mjd_option
from asian_option.get_cev_option import cev_option
from asian_option.get_dejd_option import dejd_option
from asian_option.get_exp_gaussian_option import exp_gaussian_option
from asian_option.get_gbm_option import gbm_option
from asian_option.get_heston_option import heston_option
from asian_option.get_option_CGMY import CGMY_option
from asian_option.get_option_meixner import meixner_option
from asian_option.get_option_nig import nig_option
from asian_option.get_vg_option import vg_option


def compute_values(type_choice, s0, strike, time, risk_free, N, sigma_gaussian, sigma_vg, theta_vg, kappa_vg, v0,
                   alpha_heston, beta_heston, gamma, rho, a_nig, b_nig, delta_nig, C, G, M, Y, a_meixner, b_meixner,
                   delta_meixner, sigma_mjd, lam_mjd, mews, sigmas, sigma_dejd, lam_dejd, rho_dejd, eta1, eta2,
                   beta_cev, epsilon_exp, k1_exp, sigma_exp, price_exp, strike_exp, risk_free_exp, time_exp, N_exp,
                   lmax_exp, lmin_exp, Nfft, lmax, lmin, delta, tolerance):
    Nfft = 2 ** Nfft
    N = int(N)
    type_choice = int(type_choice)
    risk_free = risk_free / 100

    if type_choice == 0:  # GBM
        ptrue, strike_exp_lcr, ptrue_strike, lam, lower_bound = gbm_option(s0, strike, time, risk_free, N,
                                                                           sigma_gaussian, Nfft, lmax, lmin, delta,
                                                                           tolerance)
        ptrue_strike = ptrue_strike[0]

    elif type_choice == 1:  # VG
        ptrue, strike_exp_lcr, ptrue_strike, lam, lower_bound = \
            vg_option(s0, strike, time, risk_free, N, sigma_vg, theta_vg, kappa_vg, Nfft, lmax, lmin, delta, tolerance)
        ptrue_strike = ptrue_strike[0]

    elif type_choice == 2:  # Heston
        ptrue, strike_exp_lcr, ptrue_strike, lam, lower_bound = \
            heston_option(s0, strike, v0, time, risk_free, N, alpha_heston, beta_heston, gamma, rho, Nfft, lmax, lmin,
                          delta, tolerance)
        ptrue_strike = ptrue_strike[0]

    elif type_choice == 3:  # NIG
        ptrue, strike_exp_lcr, ptrue_strike, lam, lower_bound = \
            nig_option(s0, strike, time, risk_free, N, a_nig, b_nig, delta_nig, Nfft, lmax, lmin, delta, tolerance)
        ptrue_strike = ptrue_strike[0]

    elif type_choice == 4:  # CGMY
        ptrue, strike_exp_lcr, ptrue_strike, lam, lower_bound = \
            CGMY_option(s0, strike, time, risk_free, N, C, G, M, Y, Nfft, lmax, lmin, delta, tolerance)
        ptrue_strike = ptrue_strike[0]

    elif type_choice == 5:  # Meixner
        ptrue, strike_exp_lcr, ptrue_strike, lam, lower_bound = \
            meixner_option(s0, strike, time, risk_free, N, a_meixner, b_meixner, delta_meixner, Nfft, lmax, lmin,
                           delta, tolerance)

        ptrue_strike = ptrue_strike[0]

    elif type_choice == 6:  # MJD
        ptrue, strike_exp_lcr, ptrue_strike, lam, lower_bound = \
            mjd_option(s0, strike, time, risk_free, N, sigma_mjd, lam_mjd, mews, sigmas, Nfft, lmax, lmin, delta,
                       tolerance)

        ptrue_strike = ptrue_strike[0]

    elif type_choice == 7:  # DEJD
        ptrue, strike_exp_lcr, ptrue_strike, lam, lower_bound = \
            dejd_option(s0, strike, time, risk_free, N, sigma_dejd, lam_dejd, rho_dejd, eta1, eta2, Nfft, lmax, lmin,
                        delta, tolerance)

        ptrue_strike = ptrue_strike[0]

    elif type_choice == 8:  # CEV

        ptrue, strike_exp_lcr, ptrue_strike, lam, lower_bound = cev_option(s0, strike, time, risk_free, N, beta_cev,
                                                                           Nfft, lmax, lmin, delta, tolerance)
        ptrue_strike = ptrue_strike[0]
        strike_exp_lcr = strike_exp_lcr[0]

    else:  # type choice == 9 Ou exp gaussian model

        risk_free_exp = risk_free_exp / 100
        ptrue, strike_exp_lcr, ptrue_strike, lam, lower_bound = \
            exp_gaussian_option(price_exp, strike_exp, time_exp, risk_free_exp, N_exp, epsilon_exp, k1_exp, sigma_exp,
                                Nfft, lmax_exp, lmin_exp, delta,
                                tolerance)

        # ptrue_strike = ptrue_strike[0]

    return ptrue, strike_exp_lcr, ptrue_strike, lam, lower_bound


def create_plot_lower_bound(lam, lower_bound):
    data = ColumnDataSource(data=dict(
        lam=lam,
        lower_bound=lower_bound
    ))

    hover_lower_bound = HoverTool(attachment="above", names=['lower bound'],
                                  tooltips=[("Lambda", "@lam"), ("Lower Bound", "@lower_bound")])
    max_range = []
    for i in range(0,len(lower_bound)):
        if lower_bound[i]>0.001:
            max_range.append(lower_bound[i])

    max_range = len(max_range)

    # x_range = [(strike - (strike - strike_exp_lcr)) * 0.75, (strike + (strike - strike_exp_lcr)) * 1.25]
    x_range = [min(lam), lam[max_range]]
    y_range = [0, max(lower_bound) *1.05]
    fig = bp.figure(tools=['save, pan, box_zoom, reset, crosshair', hover_lower_bound], x_range=x_range,
                    y_range=y_range, sizing_mode='scale_both', toolbar_location="right", x_axis_label='Strike',
                    y_axis_label='Lower Bound')

    fig.line(x='lam', y='lower_bound', source=data, legend_label="Lower Bound Function", color="#0095B6", alpha=0.9,
             line_width=4, name='lower bound')

    fig.legend.location = "top_right"
    fig.toolbar.active_drag = None

    from bokeh.embed import components
    script, div = components(fig)

    return script, div
