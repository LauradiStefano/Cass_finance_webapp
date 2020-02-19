import pandas as pd
import bokeh.plotting as bp
from bokeh.plotting import ColumnDataSource
from bokeh.models import HoverTool
from bokeh.io import curdoc
from bokeh.layouts import row, column
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import Slider, TextInput
from bokeh.plotting import figure
from bokeh.core.properties import value
import scipy.stats 
import math




def qq_plot(log_retruns):
    
    (x,empirical_distr), (slope, inter, cor) =scipy.stats.probplot(log_returns, dist="norm")#, plot=pylab)
    
    teoretical_quantiles = x
    #osmf = x.take([0, -1])  # endpoints
    normal_distr = slope * teoretical_quantiles + inter
    
    #normal_empirical = qq_plot_data[0]
    # teoretical_quantiles = normal_empirical[0]
    # empirical_distr = normal_empirical[1]
    
    
    data = ColumnDataSource(data=dict(
        teoretical_quantiles=teoretical_quantiles,
        normal_distr=normal_distr,
        empirical_distr=empirical_distr
    ))
    
    hover_normal = HoverTool(attachment="above", names=['Normal Distr'],
                             tooltips=[("teoretical quantiles", "@teoretical_quantiles"), ("Normal Distr", "@normal_distr")])
    
    hover_empirical = HoverTool(attachment="below", names=['model spot rate'],
                            tooltips=[("teoretical quantiles", "@teoretical_quantiles"), ("Empirical Distr", "@empirical_distr")])
    
    x_range = [min(teoretical_quantiles)-1, max(teoretical_quantiles) + 1]
    y_range = [min(empirical_distr)-0.02, max(empirical_distr) + 0.02]
    
    fig = bp.figure(tools=['save, pan, box_zoom, reset, crosshair', hover_empirical, hover_normal], x_range=x_range,
                    y_range=y_range, sizing_mode='scale_both', toolbar_location="right",
                    x_axis_label='Quantiles',
                    y_axis_label=' Distribution')
    
    fig.circle(x='teoretical_quantiles', y='empirical_distr', source=data, color="#0095B6", legend='Empirical Distribution',
            size=6, name='Normal Distribution')
    
    fig.line(x='teoretical_quantiles', y='normal_distr', source=data, color="#D21F1B", legend='Normal Distribution', line_width=4, alpha=0.8, name='Empirical Distr')
    
    
    fig.toolbar.active_drag = None
    fig.legend.location = "bottom_right"
    
    from bokeh.embed import components
    script, div = components(fig)
    
    
    return fig, div



