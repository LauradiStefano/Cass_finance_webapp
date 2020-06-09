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
    lambda_zero = None
    lambda_one = None
    lambda_two = None
    lambda_three = None

    sim_id = None

    plot_parametric_function = None

    if request.method == "POST":
        if form.validate and request.files:
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

                object.log_temp = json.dumps(log_temp)
                object.trend_temp_par = json.dumps(trend_temp_par.tolist())
                object.lambda_zero = lambda_zero
                object.lambda_one = lambda_one
                object.lambda_two = lambda_two
                object.lambda_three = lambda_three

                object.user = user
                db.session.add(object)
                db.session.commit()
                sim_id = object.id

    else:
        if user.is_authenticated:  # user authenticated, store the data
            if user.compute_temperature.count() > 0:
                instance = user.compute_temperature.order_by(
                    desc('id')).first()  # decreasing order db, take the last data saved
                form = populate_form_from_instance(instance)

                sim_id = instance.id
                log_temp = json.loads(instance.log_temp)
                trend_temp_par = np.array(json.loads(instance.trend_temp_par))
                lambda_zero = instance.lambda_zero
                lambda_one = instance.lambda_one
                lambda_two = instance.lambda_two
                lambda_three = instance.lambda_three

                plot_parametric_function = \
                    create_plot_parametric_function(log_temp, trend_temp_par)

    lambda_zero = round(lambda_zero, 6) if lambda_zero is not None else None
    lambda_one = round(lambda_one, 6) if lambda_one is not None else None
    lambda_two = round(lambda_two, 6) if lambda_two is not None else None
    lambda_three = round(lambda_three, 6) if lambda_three is not None else None

    return {'form': form, 'user': user, 'lambda_zero': lambda_zero, 'lambda_one': lambda_one, 'lambda_two': lambda_two,
            'lambda_three': lambda_three, 'plot_parametric_function': plot_parametric_function, 'sim_id': sim_id}


def populate_form_from_instance(instance):
    """Repopulate form with previous values"""
    form = ComputeForm()
    for field in form:
        field.data = getattr(instance, field.name, None)  # get a value or, if it doesn't exist, a default value
    return form


def controller_old_temperature(user):
    data = []

    if user.is_authenticated():
        instances = user.compute_temperature.order_by(desc('id')).all()
        for instance in instances:
            form = populate_form_from_instance(instance)

            # page old.html, store the date and the plot (previous simulation)

            id = instance.id
            log_temp = json.loads(instance.log_temp)
            trend_temp_par = np.array(json.loads(instance.trend_temp_par))
            lambda_zero = instance.lambda_zero
            lambda_one = instance.lambda_one
            lambda_two = instance.lambda_two
            lambda_three = instance.lambda_three

            plot_parametric_function = \
                create_plot_parametric_function(log_temp, trend_temp_par)

            lambda_zero = round(lambda_zero, 6) if lambda_zero is not None else None
            lambda_one = round(lambda_one, 6) if lambda_one is not None else None
            lambda_two = round(lambda_two, 6) if lambda_two is not None else None
            lambda_three = round(lambda_three, 6) if lambda_three is not None else None

            data.append(
                {'form': form, 'id': id, 'lambda_zero': lambda_zero, 'lambda_one': lambda_one, 'lambda_two': lambda_two,
                 'lambda_three': lambda_three, 'plot_parametric_function': plot_parametric_function})

    return {'data': data}


def delete_temperature_simulation(user, id):
    id = int(id)
    if user.is_authenticated():
        if id == -1:
            user.compute_temperature.delete()
        else:
            try:
                instance = user.compute_temperature.filter_by(id=id).first()
                db.session.delete(instance)
            except:
                pass

        db.session.commit()
    return redirect(url_for('old_temperature'))


def controller_temperature_data(user, id):
    id = int(id)
    if user.is_authenticated:
        csvfile = io.StringIO()
        instance = user.compute_temperature.filter_by(id=id).first()

        log_temp_values = json.loads(instance.log_temp)
        trend_temp_par_values = np.array(json.loads(instance.trend_temp_par))

        fieldnames = ['Log Temp', 'Trend Temp']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for value_1, value_2 in zip(log_temp_values, trend_temp_par_values):
            writer.writerow({'Log Temp': value_1, 'Trend Temp': value_2})

        return Response(csvfile.getvalue(), mimetype="text/csv",
                        headers={"Content-disposition": "attachment; filename=temperature_data.csv"})

    else:
        return redirect(url_for('temperature'))
