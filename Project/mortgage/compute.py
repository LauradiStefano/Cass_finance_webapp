import datetime
import calendar
from bokeh.models import HoverTool
from bokeh.plotting import ColumnDataSource
import bokeh.plotting as plt


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
    tools = "save, box_zoom, crosshair, reset"
    x = [str(v) for v in range(len(dates))]
    labels = ["capital_share", "interest_share"]
    colors = ["#0095B6", "#D21F1B"]
    data = ColumnDataSource(data=dict(
        x=x,
        dates=dates,
        capital_share=capital_share,
        interest_share=interest_share
        ))
    tooltips = [
        ("date", "@dates"),
        ("capital share", "@capital_share"),
        ("interest share", "@interest_share")
    ]

    p = plt.figure(x_range=x, title=" Capital Share & Interest Share", plot_height=300, toolbar_location="left",
                   tools=tools, tooltips=tooltips, x_axis_label='Number of rates', y_axis_label='Amount')

    # add a line renderer with legend and line thickness
    p.vbar_stack(labels, x='x', width=0.9, color=colors, source=data)#legend=[value(x) for x in labels])

    p.toolbar.active_drag = None
    p.legend.orientation = "horizontal"
    p.legend.location = "bottom_center"

    from bokeh.embed import components
    script, div = components(p)

    return script, div


def create_debt_plot(dates, debt_share):
    tools = "save, box_zoom, crosshair, reset"
    x = [str(v) for v in range(len(dates))]
    labels = ["debt_share"]
    colors = ["#0095B6"]
    data = ColumnDataSource(data=dict(
        x=x,
        dates=dates,
        debt_share=debt_share
    ))

    tooltips = [
        ("date", "@dates"),
        ("debt share", "@debt_share")
    ]

    p = plt.figure(x_range=x, title="Debt Share", plot_height=300, toolbar_location="left", tools=tools,
                   tooltips=tooltips, x_axis_label='Number of rates', y_axis_label='Amount')
    # add a line renderer with legend and line thickness
    p.vbar_stack(labels, x='x', width=0.9, color=colors,
                 source=data)#, legend=[value(x) for x in labels]

    p.toolbar.active_drag = None
    p.legend.orientation = "horizontal"
    p.legend.location = "top_left"

    from bokeh.embed import components
    script, div = components(p)


    return script, div

