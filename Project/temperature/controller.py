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
from db_models import temperature as compute
from temperature.compute import import_dataset_file_excel, compute_parametric_function, create_plot_parametric_function
from temperature.forms import ComputeForm


def controller_temperature(user, request):
    form = ComputeForm(request.form)

    file_data = None

    sim_id = None

    plot_parametric_function = None

    if request.method == "POST":
        if form.validate() and request.files:
            file = request.files[form.file_data.name]

            if file and allowed_file(file.filename):
                file_data = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], file_data))

            data = import_dataset_file_excel(file_data)

            log_temp, trend_temp_par, lambda_zero, lambda_one, lambda_two, lambda_three = compute_parametric_function(
                data)

            plot_parametric_function = \
                create_plot_parametric_function(log_temp, trend_temp_par)

            if user.is_authenticated:  # store data in db
                object = compute()
                form.populate_obj(object)

                object.log_temp = json.dumps(log_temp.tolist())
                object.trend_temp_par = json.dumps(trend_temp_par.tolist())

                object.user = user
                db.session.add(object)
                db.session.commit()
                sim_id = object.id

    else:
        if user.is_authenticated:  # user authenticated, store the data
            if user.compute_temperature.count() > 0:
                instance = user.compute_portfolio_analysis.order_by(
                    desc('id')).first()  # decreasing order db, take the last data saved
                form = populate_form_from_instance(instance)

                sim_id = instance.id
                log_temp = np.array(json.loads(instance.log_temp))
                trend_temp_par = np.array(json.loads(instance.trend_temp_par))

                plot_parametric_function = \
                    create_plot_parametric_function(log_temp, trend_temp_par)

    return {'form': form, 'user': user, 'plot_parametric_function': plot_parametric_function, 'sim_id': sim_id}


def populate_form_from_instance(instance):
    """Repopulate form with previous values"""
    form = ComputeForm()
    for field in form:
        field.data = getattr(instance, field.name, None)  # get a value or, if it doesn't exist, a default value
    return form


# def controller_old_portfolio_analysis(user):
#     data = []
#
#     if user.is_authenticated():
#         instances = user.compute_portfolio_analysis.order_by(desc('id')).all()
#         for instance in instances:
#             form = populate_form_from_instance(instance)
#
#             # page old.html, store the date and the plot (previous simulation)
#
#             id = instance.id
#             returns = np.array(json.loads(instance.returns))
#             standard_deviations = np.array(json.loads(instance.standard_deviations))
#             means = np.array(json.loads(instance.means))
#             efficient_means = np.array(json.loads(instance.efficient_means))
#             efficient_std = np.array(json.loads(instance.efficient_std))
#             efficient_weights = np.array(json.loads(instance.efficient_weights))
#             tickers = json.loads(instance.tickers)
#
#             plot_efficient_frontier = \
#                 create_plot_efficient_frontier(returns, standard_deviations, means, efficient_means,
#                                                efficient_std)
#             plot_efficient_weights = create_plot_efficient_weights(efficient_means, efficient_weights, tickers)
#
#             data.append({'form': form, 'id': id, 'plot_efficient_frontier': plot_efficient_frontier,
#                          'plot_efficient_weights': plot_efficient_weights})
#
#     return {'data': data}


def delete_portfolio_analysis_simulation(user, id):
    id = int(id)
    if user.is_authenticated():
        if id == -1:
            user.compute_portfolio_analysis.delete()
        else:
            try:
                instance = user.compute_portfolio_analysis.filter_by(id=id).first()
                db.session.delete(instance)
            except:
                pass

        db.session.commit()
    return redirect(url_for('old_portfolio_analysis'))


def controller_portfolio_analysis_data(user, id):
    id = int(id)
    if user.is_authenticated:
        csvfile = io.StringIO()
        instance = user.compute_portfolio_analysis.filter_by(id=id).first()

        efficient_weights_values = np.array(json.loads(instance.efficient_weights))
        tickers = json.loads(instance.tickers)

        writer = csv.writer(csvfile)

        writer.writerow(tickers)
        for value in efficient_weights_values:
            writer.writerow(value)

        return Response(csvfile.getvalue(), mimetype="text/csv",
                        headers={"Content-disposition": "attachment; filename=portfolio_data.csv"})

    else:
        return redirect(url_for('portfolio_analysis'))
