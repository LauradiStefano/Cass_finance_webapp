import datetime
import calendar
from bokeh.models import HoverTool
from bokeh.plotting import ColumnDataSource
import bokeh.plotting as bp


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

