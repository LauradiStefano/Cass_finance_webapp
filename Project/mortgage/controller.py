import json

from flask import url_for, redirect, Response
from sqlalchemy import desc
from db_models import db
from db_models import mortgage as compute
from mortgage.compute import mortgage_compute, create_capital_interest_plot, create_debt_plot
from mortgage.forms import ComputeForm


def controller_mortgage(user, request):
    form = ComputeForm(request.form)

    residual_debt = None
    capital_share = None
    interest_share = None
    debt_share = None
    dates = None
    rate_value = None

    number_of_rates = 0

    plot_capital_interest_share = None
    plot_debt_share = None

    if request.method == "POST":
        if form.validate():

            rate_value, dates, residual_debt, capital_share, interest_share, debt_share = \
                mortgage_compute(form.capital_amount.data, form.interest_rate.data, form.loan_term.data,
                                 form.frequency.data)

            number_of_rates = len(dates)

            plot_capital_interest_share = \
                create_capital_interest_plot(dates, capital_share, interest_share)
            plot_debt_share = create_debt_plot(dates, debt_share)

            if user.is_authenticated:  # store data in db
                object = compute()
                form.populate_obj(object)

                object.dates = json.dumps(dates)
                object.residual_debt = json.dumps(residual_debt)
                object.capital_share = json.dumps(capital_share)
                object.interest_share = json.dumps(interest_share)
                object.debt_share = json.dumps(debt_share)
                object.number_of_rates = json.dumps(number_of_rates)
                object.rate_value = rate_value

                object.user = user
                db.session.add(object)
                db.session.commit()
    else:
        if user.is_authenticated:  # user authenticated, store the data
            if user.compute_mortgage.count() > 0:
                instance = user.compute_mortgage.order_by(
                    desc('id')).first()  # decreasing order db, take the last data saved
                form = populate_form_from_instance(instance)

                dates = json.loads(instance.dates)
                residual_debt = json.loads(instance.residual_debt)
                capital_share = json.loads(instance.capital_share)
                interest_share = json.loads(instance.interest_share)
                debt_share = json.loads(instance.debt_share)
                number_of_rates = json.loads(instance.number_of_rates)
                rate_value = instance.rate_value

                plot_capital_interest_share = \
                    create_capital_interest_plot(dates, capital_share, interest_share)
                plot_debt_share = create_debt_plot(dates, debt_share)

    rate_value = round(rate_value, 4) if rate_value is not None else None

    return {'form': form, 'user': user, 'dates': dates, 'residual_debt': residual_debt, 'capital_share': capital_share,
            'interest_share': interest_share, 'debt_share': debt_share, 'number_of_rates': number_of_rates,
            'rate_value': rate_value, 'plot_capital_interest_share': plot_capital_interest_share,
            'plot_debt_share': plot_debt_share}


def populate_form_from_instance(instance):
    """Repopulate form with previous values"""
    form = ComputeForm()
    for field in form:
        field.data = getattr(instance, field.name, None)  # get a value or, if it doesn't exist, a default value
    return form


def controller_old_mortgage(user):
    data = []

    if user.is_authenticated():
        instances = user.compute_mortgage.order_by(desc('id')).all()
        for instance in instances:
            form = populate_form_from_instance(instance)

            # page old.html, store the date and the plot (previous simulation)

            id = instance.id
            dates = json.loads(instance.dates)
            capital_share = json.loads(instance.capital_share)
            interest_share = json.loads(instance.interest_share)
            debt_share = json.loads(instance.debt_share)
            rate_value = instance.rate_value

            plot_capital_interest_share = \
                create_capital_interest_plot(dates, capital_share, interest_share)
            plot_debt_share = create_debt_plot(dates, debt_share)

            rate_value = round(rate_value, 4) if rate_value is not None else None

            data.append({'form': form, 'id': id, 'rate_value': rate_value,
                         'plot_capital_interest_share': plot_capital_interest_share,
                         'plot_debt_share': plot_debt_share})

    return {'data': data}


def delete_mortgage_simulation(user, id):
    id = int(id)
    if user.is_authenticated():
        if id == -1:
            user.compute_mortgage.delete()
        else:
            try:
                instance = user.compute_mortgage.filter_by(id=id).first()
                db.session.delete(instance)
            except:
                pass

        db.session.commit()
    return redirect(url_for('old_mortgage'))

# def controller_portfolio_analysis_data(user, id):
#     id = int(id)
#     if user.is_authenticated:
#         csvfile = io.StringIO()
#         instance = user.compute_portfolio_analysis.filter_by(id=id).first()
#
#         efficient_weights_values = np.array(json.loads(instance.efficient_weights))
#         tickers = json.loads(instance.tickers)
#
#         writer = csv.writer(csvfile)
#
#         writer.writerow(tickers)
#         for value in efficient_weights_values:
#             writer.writerow(value)
#
#         return Response(csvfile.getvalue(), mimetype="text/csv",
#                         headers={"Content-disposition": "attachment; filename=portfolio_data.csv"})
#
#     else:
#         return redirect(url_for('portfolio_analysis'))
