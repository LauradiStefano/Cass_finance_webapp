# -*- coding: utf-8 -*-
"""
Created on Fri May  3 09:56:26 2019

@author: Diego
"""
import bokeh.plotting as bp
from bokeh.models import HoverTool
from bokeh.plotting import ColumnDataSource

from get_gbm_option import gbm_option
from get_heston_option import heston_option
from get_option_CGMY import CGMY_option
from get_option_nig import nig_option
from get_vg_option import vg_option


def compute_values(type_choice, s0, strike, time, risk_free, N, sigma_gaussian, sigma_vg, theta, kappa, v0,
                   alpha_heston, beta_heston, eta, rho, alpha_nig, beta_nig, delta_nig, C, G, M, Y, Nfft, lmax, lmin,
                   delta, umax):
    Nfft = 2 ** Nfft
    N = int(N)
    type_choice = int(type_choice)
    risk_free = risk_free / 100

    if type_choice == 0:
        ptrue, strike_exp_lcr, ptrue_strike, lam, lower_bound = gbm_option(s0, strike, time, risk_free, N,
                                                                           sigma_gaussian, Nfft, lmax, lmin, delta,
                                                                           umax)
        ptrue_strike = ptrue_strike[0]

    elif type_choice == 1:
        ptrue, strike_exp_lcr, ptrue_strike, lam, lower_bound = vg_option(s0, strike, time, risk_free, N, sigma_vg,
                                                                          theta, kappa, Nfft, lmax, lmin, delta, umax)
        ptrue_strike = ptrue_strike[0]

    elif type_choice == 2:

        ptrue, strike_exp_lcr, ptrue_strike, lam, lower_bound = heston_option(s0, strike, v0, time, risk_free, N,
                                                                              alpha_heston, beta_heston, eta, rho, Nfft,
                                                                              lmax, lmin, delta, umax)
        ptrue_strike = ptrue_strike[0]

    elif type_choice == 3:
        ptrue, strike_exp_lcr, ptrue_strike, lam, lower_bound = nig_option(s0, strike, time, risk_free, N, alpha_nig,
                                                                           beta_nig, delta_nig, Nfft, lmax, lmin, delta,
                                                                           umax)
        ptrue_strike = ptrue_strike[0]


    else:
        ptrue, strike_exp_lcr, ptrue_strike, lam, lower_bound = CGMY_option(s0, strike, time, risk_free, N, C, G, M, Y,
                                                                            Nfft, lmax, lmin, delta,
                                                                            umax)

        ptrue_strike = ptrue_strike[0]

    return ptrue, strike_exp_lcr, ptrue_strike, lam, lower_bound


def create_plot_lower_bound(lam, lower_bound, strike, strike_exp_lcr):
    data = ColumnDataSource(data=dict(
        lam=lam,
        lower_bound=lower_bound
    ))

    hover_lower_bound = HoverTool(attachment="left", names=['lower bound'],
                                  tooltips=[("Lambda", "@lam"), ("Lower Bound", "@lower_bound")])

    x_range = [(strike - (strike - strike_exp_lcr)) * 0.75, (strike + (strike - strike_exp_lcr)) * 1.25]
    y_range = [0, max(lower_bound) * 1.10]
    fig = bp.figure(tools=['save, pan, box_zoom, reset, crosshair', hover_lower_bound], x_range=x_range,
                    y_range=y_range, title="Asian Option Lower Bound", plot_height=450,
                    toolbar_location="left", x_axis_label='Lambda', y_axis_label='Lower Bound')

    fig.line(x='lam', y='lower_bound', source=data, legend="Lower Bound Function", color="#0095B6", alpha=0.9,
             line_width=4, name='lower bound')

    fig.square(x=strike_exp_lcr, y=0, source=data, legend='Optimal Strike', color="#D21F1B", size=9)
    fig.square(x=strike, y=0, source=data, legend='Strike', color="#050402", size=7)

    fig.legend.location = "top_right"
    fig.toolbar.active_drag = None

    from bokeh.embed import components
    script, div = components(fig)

    return script, div
