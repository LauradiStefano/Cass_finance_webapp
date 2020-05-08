import datetime
import calendar
from bokeh.plotting import ColumnDataSource
import bokeh.plotting as bp
from bokeh.core.properties import value
from bokeh.models import HoverTool


def mortgage_compute(capital, rate, years, frequency):
    frequency = int(frequency)
    percentage_rate = rate / 100
    number_of_rates = int(years) * frequency

    # compute rate
    im = (1 + percentage_rate) ** (1 / frequency) - 1
    annuity = (1 - (1 + im) ** (-number_of_rates)) / im
    rate_value = capital / annuity  # constant rate

    residual_debt = []
    capital_share = []
    interest_share = []
    debt_share = []

    residual_debt.append(capital)
    capital_share.append(0)
    interest_share.append(0)
    debt_share.append(0)

    for j in range(1, int(number_of_rates + 1)):  # number_of_rates+1 excluded
        interest_share.append(im * residual_debt[j - 1])
        capital_share.append(rate_value - interest_share[j])
        residual_debt.append(residual_debt[j - 1] - capital_share[j])
        debt_share.append(debt_share[j - 1] + capital_share[j])

    residual_debt = [round(x, 4) for x in residual_debt]
    capital_share = [round(x, 4) for x in capital_share]
    interest_share = [round(x, 4) for x in interest_share]
    debt_share = [round(x, 4) for x in debt_share]
    rate_value = round(rate_value, 4)
    dates = [d.strftime("%d/%m/%y") for d in generate_date(frequency, number_of_rates)]

    return rate_value, dates, residual_debt, capital_share, interest_share, debt_share


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
    x = [str(v) for v in range(len(dates))]
    labels = ["capital_share", "interest_share"]
    colors = ["#0095B6", "#D21F1B"]

    data = ColumnDataSource(data=dict(
        x=x,
        dates=dates,
        capital_share=capital_share,
        interest_share=interest_share
    ))
    hover_share = HoverTool(attachment="above", names=['share'],
                            tooltips=[("Date", "@dates"), ("Capital Share", "@capital_share"),
                                      ("Interest Share", "@interest_share")])

    fig = bp.figure(tools=['save, pan, box_zoom, reset, crosshair', hover_share], x_range=x,
                    sizing_mode='scale_both', toolbar_location="right", x_axis_label='Number of rates',
                    y_axis_label='Amount')

    fig.vbar_stack(labels, x='x', width=0.9, alpha=0.8, color=colors, source=data,
                   legend_label='Capital Share Interest Share', name='share')

    fig.legend.orientation = "horizontal"
    fig.legend.location = "bottom_center"
    fig.toolbar.active_drag = None

    from bokeh.embed import components
    script, div = components(fig)

    return script, div


def create_debt_plot(dates, debt_share):
    x = [str(v) for v in range(len(dates))]
    labels = ["debt_share"]
    colors = ["#0095B6"]

    data = ColumnDataSource(data=dict(
        x=x,
        dates=dates,
        debt_share=debt_share
    ))

    hover_share = HoverTool(attachment="above", names=['debt share'],
                            tooltips=[("Date", "@dates"), ("Debt Share", "@debt_share")])

    fig = bp.figure(tools=['save, pan, box_zoom, reset, crosshair', hover_share], x_range=x,
                    sizing_mode='scale_both', toolbar_location="right", x_axis_label='Number of rates',
                    y_axis_label='Amount')

    fig.vbar_stack(labels, x='x', width=0.9, alpha=0.8, color=colors, source=data, legend_label="Debt Share",
                   name='debt share')

    fig.legend.location = "top_left"
    fig.toolbar.active_drag = None

    from bokeh.embed import components
    script, div = components(fig)

    return script, div
