# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 21:03:47 2019

@author: Diego
"""
import bokeh.plotting as bp
import numpy as np
import scipy.stats
from bokeh.models import ColumnDataSource
from bokeh.models import HoverTool


def create_histogram_distribution(log_returns):
    hist, edges = np.histogram(log_returns, density=True, bins=100)
    m = np.mean(log_returns)
    sg = np.std(log_returns)
    log_returns.sort(reverse=False)
    normal_pdf = lambda x: scipy.stats.norm.pdf(x, m, sg)
    norm_pdf = [normal_pdf(i) for i in log_returns]  # aggiungere all'output

    # log_returns.sort(reverse = False)

    data_hist = ColumnDataSource(data=dict(
        hist=hist,
        edges_left=edges[:-1],
        edges_right=edges[1:]))

    data_theoretical = ColumnDataSource(data=dict(
        log_returns=log_returns,
        norm_pdf=norm_pdf))

    hover_histogram = HoverTool(attachment="above", names=['histogram'],
                                tooltips=[("edges", "@edges"),
                                          ("hist", "@histogram")])

    hover_theoretical = HoverTool(attachment="above", names=['discount factor'],
                                  tooltips=[("log_returns", "@log returns"),
                                            ("norm_pdf", "@norm pdf")])

    fig = bp.figure(tools=['save, pan, box_zoom, reset, crosshair', hover_histogram, hover_theoretical],
                    sizing_mode='scale_both', toolbar_location="right", x_axis_label='Series of Data',
                    y_axis_label='Model Error Discount Factor')

    fig.quad(top='hist', bottom=0, left='edges_left', right='edges_right', source=data_hist,
             color="#0095B6", line_color="#ffffff", alpha=1, name='Histogram Log Returns')

    fig.line(x='log_returns', y='norm_pdf', source=data_theoretical, color="#D21F1B", legend='Log returns PDF',
             line_width=1, alpha=1, name='Theoretical Distribution')

    fig.toolbar.active_drag = None

    from bokeh.embed import components
    script, div = components(fig)

    return fig, div

# curdoc().add_root(row(p, width=800))
