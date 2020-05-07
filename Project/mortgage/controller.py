import csv
import io
import json
import os

import numpy as np
from flask import url_for, redirect, Response
from sqlalchemy import desc
from werkzeug.utils import secure_filename

from app import allowed_file, app
from db_models import db
from db_models import portfolio_analysis as compute
from portfolio_analysis.compute import upload_input, compute_efficient_frontier, create_plot_efficient_frontier, \
    create_plot_efficient_weights
from mortgage.forms import ComputeForm


def controller_mortgage(user, request):
    form = ComputeForm(request.form)

    residual_debt = None
    capital_share = None
    interest_share = None
    debt_share = None
    dates = None

    number_of_rates = 0

    plot_capital_interest_share = None
    plot_debt_share = None

    if request.method == "POST":
        if form.validate() and request.files:

            returns, n_assets, tickers = upload_input(file_data)

            standard_deviations, means, efficient_means, efficient_std, efficient_weights = \
                compute_efficient_frontier(returns, n_assets, form.n_portfolio.data)

            plot_efficient_frontier = \
                create_plot_efficient_frontier(returns, standard_deviations, means, efficient_means,
                                               efficient_std)
            plot_efficient_weights = create_plot_efficient_weights(efficient_means, efficient_weights, tickers)

            if user.is_authenticated:  # store data in db
                object = compute()
                form.populate_obj(object)

                object.dates = json.dumps(dates)
                object.residual_debt = json.dumps(residual_debt)
                object.capital_share = json.dumps(capital_share)
                object.interest_share = json.dumps(interest_share)
                object.debt_share = json.dumps(debt_share)
                object.number_of_rates = json.dumps(number_of_rates)

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

                plot_efficient_frontier = \
                    create_plot_efficient_frontier(returns, standard_deviations, means, efficient_means,
                                                   efficient_std)
                plot_efficient_weights = create_plot_efficient_weights(efficient_means, efficient_weights, tickers)

    return {'form': form, 'user': user, 'dates': dates, 'residual_debt': residual_debt, 'capital_share': capital_share,
            'interest_share': interest_share, 'debt_share': debt_share, 'number_of_rates': number_of_rates,
            'plot_capital_interest_share': plot_capital_interest_share,
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
            residual_debt = json.loads(instance.residual_debt)
            capital_share = json.loads(instance.capital_share)
            interest_share = json.loads(instance.interest_share)
            debt_share = json.loads(instance.debt_share)

            plot_capital_interest_share = \
                create_plot_efficient_frontier(returns, standard_deviations, means, efficient_means,
                                               efficient_std)
            plot_debt_share = create_plot_efficient_weights(efficient_means, efficient_weights, tickers)

            data.append({'form': form, 'id': id, 'plot_capital_interest_share': plot_capital_interest_share,
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
