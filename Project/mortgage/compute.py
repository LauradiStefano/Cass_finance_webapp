import bokeh.plotting as plt
from bokeh.core.properties import value
import datetime
import calendar
from bokeh.models import HoverTool
from bokeh.plotting import ColumnDataSource
import bokeh.plotting as bp


def mortgage_compute(S, i, n, m):
    m = int(m)
    z = i / 100  # tasso percentuale
    nr = int(n) * m  # numero di rate totali

    # calcolo rata
    im = z / nr
    a = (1 - (1 + im) ** (-nr)) / im  # annuity
    R = S / a  # rata costante

    D = []
    C = []
    I = []
    E = []

    D.append(S)  # debito residuo
    C.append(0)  # quota capitale
    I.append(0)  # quota interessi
    E.append(0)  # quota debito

    for j in range(1, int(nr + 1)):  # nr+1 escluso
        I.append(im * D[j - 1])
        C.append(R - I[j])
        D.append(D[j - 1] - C[j])
        E.append(E[j - 1] + C[j])
    D = [round(x, 2) for x in D]
    C = [round(x, 2) for x in C]
    I = [round(x, 2) for x in I]
    E = [round(x, 2) for x in E]
    dates = generate_date(m, nr)

    return dates, D, C, I, E


def generate_date(frequency, nr):
    dates = []
    dates.append(datetime.date.today())
    interval = 12 // frequency

    for j in range(1, (nr + 1)):
        datefirst = dates[j - 1]
        month = datefirst.month - 1 + interval
        year = datefirst.year + month // 12
        month = month % 12 + 1
        day = min(datefirst.day, calendar.monthrange(year, month)[1])
        dates.append((datetime.date(year, month, day)))

    return dates


def create_capital_interest_plot(dates, capital_share, interest_share):
    dates = [str(x) for x in dates]

    data = ColumnDataSource(data=dict(
        dates=dates,
        capital_share=capital_share,
        interest_share=interest_share
    ))

    hover_capital_share = HoverTool(attachment="above", names=['capital share'],
                                    tooltips=[("Date", "@dates"), ("Capital Share", "@capital_share")])
    hover_interest_share = HoverTool(attachment="below", names=['interest share'],
                                     tooltips=[("Date", "@dates"), ("Interest Share", "@interest_share")])

    x_range = [min(dates), max(dates)]
    fig = bp.figure(tools=['save, pan, box_zoom, reset, crosshair', hover_capital_share, hover_interest_share],
                    x_range=x_range, sizing_mode='scale_both', toolbar_location="right", x_axis_label='Dates',
                    y_axis_label='Share')

    fig.vbar_stack(x='dates', y='capital_share', source=data, legend_label="Capital Share", color="#0095B6", alpha=0.9,
                   line_width=4, name='capital share')
    fig.vbar_stack(x='dates', y='interest_share', source=data, legend_label="Interest Share", color="#D21F1B",
                   alpha=0.9, line_width=4, name='capital share')

    fig.legend.location = "top_left"
    fig.toolbar.active_drag = None

    from bokeh.embed import components
    script, div = components(fig)

    return script, div


def create_debt_plot(dates, debt_share):
    dates = [str(x) for x in dates]

    data = ColumnDataSource(data=dict(
        dates=dates,
        debt_share=debt_share
    ))

    hover_debt_share = HoverTool(attachment="above", names=['debt share'],
                                    tooltips=[("Date", "@dates"), ("Debt Share", "@debt_share")])

    x_range = [min(dates), max(dates)]
    fig = bp.figure(tools=['save, pan, box_zoom, reset, crosshair', hover_debt_share],
                    x_range=x_range, sizing_mode='scale_both', toolbar_location="right", x_axis_label='Dates',
                    y_axis_label='Debt Share')

    fig.vbar_stack(x='dates', y='debt_share', source=data, legend_label="Debt Share", color="#0095B6", alpha=0.9,
                   line_width=4, name='debt share')

    fig.legend.location = "top_left"
    fig.toolbar.active_drag = None

    from bokeh.embed import components
    script, div = components(fig)

    return script, div

