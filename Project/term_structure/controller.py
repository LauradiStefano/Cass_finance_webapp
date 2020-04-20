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
from db_models import term_structure as compute
from term_structure.compute import upload_input, create_objective_vector, fitting_method, \
    create_plot_discount_factor_term_structure, \
    create_plot_interest_rate_term_structure, create_plot_error_discount_factor, create_plot_error_interest_rate
from term_structure.forms import ComputeForm


def controller_term_structure(user, request):
    form = ComputeForm(request.form)

    file_data = None
    market_discount_factor = None
    market_spot_rate = None
    model_discount_factor = None
    model_spot_rate = None
    discount_factor_model_error = None
    spot_rate_model_error = None
    parameters = None
    time = None
    name_param = None
    rmse_discount_factor = None
    rmse_spot_rate = None
    compute_not_allowed = False
    daily_discount_factor = None
    annual_basis_date = None
    daily_model_spot_rate = None
    dates = None

    number_of_time = 0

    sim_id = None

    plot_discount_factor_term_structure = None
    plot_interest_rate_term_structure = None
    plot_error_discount_factor = None
    plot_error_interest_rate = None

    if request.method == "POST":
        if user.is_authenticated:
            if form.validate() and request.files:
                file = request.files[form.file_data.name]

                if file and allowed_file(file.filename):
                    file_data = secure_filename(file.filename)
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], file_data))

                file_data = upload_input(file_data)

                variables = create_objective_vector(form.model_choice.data, form.kappa_vasicek.data,
                                                    form.theta_vasicek.data, form.sigma_vasicek.data,
                                                    form.rho_vasicek.data,
                                                    form.kappa_cir.data, form.theta_cir.data, form.sigma_cir.data,
                                                    form.rho_cir.data, form.beta0_nelson.data, form.beta1_nelson.data,
                                                    form.beta2_nelson.data, form.tau_nelson.data,
                                                    form.beta0_svensson.data,
                                                    form.beta1_svensson.data, form.beta2_svensson.data,
                                                    form.beta3_svensson.data, form.tau1_svensson.data,
                                                    form.tau2_svensson.data)

                market_discount_factor, market_spot_rate, model_discount_factor, model_spot_rate, \
                discount_factor_model_error, spot_rate_model_error, parameters, time, rmse_discount_factor, \
                rmse_spot_rate, daily_discount_factor, annual_basis_date, daily_model_spot_rate, dates = fitting_method(
                    form.model_choice.data, variables, file_data, form.least_fmin.data,
                    form.discount_factor.data)

                number_of_time = len(annual_basis_date)

                name_param = form.name_parameters[form.model_choice.data]

                plot_discount_factor_term_structure = \
                    create_plot_discount_factor_term_structure(time, market_discount_factor, model_discount_factor)
                plot_interest_rate_term_structure = \
                    create_plot_interest_rate_term_structure(time, market_spot_rate, model_spot_rate)
                plot_error_discount_factor = create_plot_error_discount_factor(discount_factor_model_error, time)
                plot_error_interest_rate = create_plot_error_interest_rate(spot_rate_model_error, time)

            if user.is_authenticated:  # store data in db
                object = compute()
                form.populate_obj(object)

                object.parameters = json.dumps(parameters.tolist())
                object.time = json.dumps(time)
                object.market_discount_factor = json.dumps(market_discount_factor)
                object.model_discount_factor = json.dumps(model_discount_factor.tolist())
                object.market_spot_rate = json.dumps(market_spot_rate.tolist())
                object.model_spot_rate = json.dumps(model_spot_rate.tolist())
                object.discount_factor_model_error = json.dumps(discount_factor_model_error.tolist())
                object.spot_rate_model_error = json.dumps(spot_rate_model_error.tolist())
                object.number_of_time = json.dumps(number_of_time)
                object.name_param = json.dumps(name_param)
                object.rmse_discount_factor = rmse_discount_factor
                object.daily_discount_factor = json.dumps(daily_discount_factor.tolist())
                object.annual_basis_date = json.dumps(annual_basis_date)
                object.daily_model_spot_rate = json.dumps(daily_model_spot_rate.tolist())
                object.dates = json.dumps(dates)

                object.user = user
                db.session.add(object)
                db.session.commit()
                sim_id = object.id
        else:
            compute_not_allowed = True

    else:
        if user.is_authenticated:  # user authenticated, store the data
            if user.compute_term_structure.count() > 0:
                instance = user.compute_term_structure.order_by(
                    desc('id')).first()  # decreasing order db, take the last data saved
                form = populate_form_from_instance(instance)

                sim_id = instance.id
                parameters = np.array(json.loads(instance.parameters))
                time = json.loads(instance.time)
                market_discount_factor = json.loads(instance.market_discount_factor)
                model_discount_factor = np.array(json.loads(instance.model_discount_factor))
                market_spot_rate = np.array(json.loads(instance.market_spot_rate))
                model_spot_rate = np.array(json.loads(instance.model_spot_rate))
                discount_factor_model_error = np.array(json.loads(instance.discount_factor_model_error))
                spot_rate_model_error = np.array(json.loads(instance.spot_rate_model_error))
                number_of_time = json.loads(instance.number_of_time)
                name_param = json.loads(instance.name_param)
                rmse_discount_factor = instance.rmse_discount_factor
                rmse_spot_rate = instance.rmse_spot_rate
                annual_basis_date = json.loads(instance.annual_basis_date)
                daily_discount_factor = np.array(json.loads(instance.daily_discount_factor))
                daily_model_spot_rate = np.array(json.loads(instance.daily_model_spot_rate))
                dates = json.loads(instance.dates)

                plot_discount_factor_term_structure = \
                    create_plot_discount_factor_term_structure(time, market_discount_factor, model_discount_factor)
                plot_interest_rate_term_structure = \
                    create_plot_interest_rate_term_structure(time, market_spot_rate, model_spot_rate)
                plot_error_discount_factor = create_plot_error_discount_factor(discount_factor_model_error, time)
                plot_error_interest_rate = create_plot_error_interest_rate(spot_rate_model_error, time)

    time = [round(x, 6) for x in time] if time is not None else None
    market_discount_factor = [round(x, 6) for x in
                              market_discount_factor] if market_discount_factor is not None else None
    model_discount_factor = [round(x, 6) for x in model_discount_factor] if model_discount_factor is not None else None
    market_spot_rate = [round(x, 6) for x in market_spot_rate] if market_spot_rate is not None else None
    model_spot_rate = [round(x, 6) for x in model_spot_rate] if model_spot_rate is not None else None
    parameters = [round(x, 4) for x in parameters] if parameters is not None else None

    discount_factor_model_error = [round(x, 6) for x in
                                   discount_factor_model_error] if discount_factor_model_error is not None else None
    spot_rate_model_error = [round(x, 6) for x in spot_rate_model_error] if spot_rate_model_error is not None else None

    annual_basis_date = [round(x, 6) for x in annual_basis_date] if annual_basis_date is not None else None
    daily_discount_factor = [round(x, 6) for x in daily_discount_factor] if daily_discount_factor is not None else None
    daily_model_spot_rate = [round(x, 6) for x in daily_model_spot_rate] if daily_model_spot_rate is not None else None

    rmse_discount_factor = round(rmse_discount_factor, 4) if rmse_discount_factor is not None else None
    rmse_spot_rate = round(rmse_spot_rate, 4) if rmse_spot_rate is not None else None

    return {'form': form, 'user': user, 'parameters': parameters, 'time': time, 'name_param': name_param,
            'market_discount_factor': market_discount_factor, 'model_discount_factor': model_discount_factor,
            'market_spot_rate': market_spot_rate, 'model_spot_rate': model_spot_rate, 'number_of_time': number_of_time,
            'rmse_discount_factor': rmse_discount_factor, 'rmse_spot_rate': rmse_spot_rate,
            'annual_basis_date': annual_basis_date, 'daily_model_spot_rate': daily_model_spot_rate,
            'daily_discount_factor': daily_discount_factor, 'discount_factor_model_error': discount_factor_model_error,
            'spot_rate_model_error': spot_rate_model_error, 'dates': dates,
            'plot_discount_factor_term_structure': plot_discount_factor_term_structure,
            'plot_interest_rate_term_structure': plot_interest_rate_term_structure,
            'plot_error_discount_factor': plot_error_discount_factor,
            'plot_error_interest_rate': plot_error_interest_rate, 'compute_not_allowed': compute_not_allowed,
            'sim_id': sim_id}


def populate_form_from_instance(instance):
    """Repopulate form with previous values"""
    form = ComputeForm()
    for field in form:
        field.data = getattr(instance, field.name, None)  # get a value or, if it doesn't exist, a default value
    return form


def controller_old_term_structure(user):
    data = []

    if user.is_authenticated():
        instances = user.compute_term_structure.order_by(desc('id')).all()
        for instance in instances:
            form = populate_form_from_instance(instance)

            # page old.html, store the date and the plot (previous simulation)

            id = instance.id
            parameters = np.array(json.loads(instance.parameters))
            time = json.loads(instance.time)
            market_discount_factor = json.loads(instance.market_discount_factor)
            model_discount_factor = np.array(json.loads(instance.model_discount_factor))
            market_spot_rate = np.array(json.loads(instance.market_spot_rate))
            model_spot_rate = np.array(json.loads(instance.model_spot_rate))
            discount_factor_model_error = np.array(json.loads(instance.discount_factor_model_error))
            spot_rate_model_error = np.array(json.loads(instance.spot_rate_model_error))
            name_param = json.loads(instance.name_param)
            rmse_discount_factor = instance.rmse_discount_factor
            rmse_spot_rate = instance.rmse_spot_rate

            plot_discount_factor_term_structure = \
                create_plot_discount_factor_term_structure(time, market_discount_factor, model_discount_factor)
            plot_interest_rate_term_structure = \
                create_plot_interest_rate_term_structure(time, market_spot_rate, model_spot_rate)
            plot_error_discount_factor = create_plot_error_discount_factor(discount_factor_model_error, time)
            plot_error_interest_rate = create_plot_error_interest_rate(spot_rate_model_error, time)

            parameters = [round(x, 6) for x in parameters] if parameters is not None else None
            rmse_discount_factor = round(rmse_discount_factor, 4) if rmse_discount_factor is not None else None
            rmse_spot_rate = round(rmse_spot_rate, 4) if rmse_spot_rate is not None else None

            data.append({'form': form, 'id': id, 'parameters': parameters, 'name_param': name_param,
                         'rmse_discount_factor': rmse_discount_factor, 'rmse_spot_rate': rmse_spot_rate,
                         'plot_discount_factor_term_structure': plot_discount_factor_term_structure,
                         'plot_interest_rate_term_structure': plot_interest_rate_term_structure,
                         'plot_error_discount_factor': plot_error_discount_factor,
                         'plot_error_interest_rate': plot_error_interest_rate})

    return {'data': data}


def delete_term_structure_simulation(user, id):
    id = int(id)
    if user.is_authenticated():
        if id == -1:
            user.compute_term_structure.delete()
        else:
            try:
                instance = user.compute_term_structure.filter_by(id=id).first()
                db.session.delete(instance)
            except:
                pass

        db.session.commit()
    return redirect(url_for('old_term_structure'))


def controller_term_structure_data(user, id):
    id = int(id)
    if user.is_authenticated:
        csvfile = io.StringIO()
        instance = user.compute_term_structure.filter_by(id=id).first()

        market_discount_factor_values = json.loads(instance.market_discount_factor)
        model_discount_factor_values = np.array(json.loads(instance.model_discount_factor))
        market_spot_rate_values = np.array(json.loads(instance.market_spot_rate))
        model_spot_rate_values = np.array(json.loads(instance.model_spot_rate))
        discount_factor_model_error_values = np.array(json.loads(instance.discount_factor_model_error))
        spot_rate_model_error_values = np.array(json.loads(instance.spot_rate_model_error))

        fieldnames = ['Market DF', 'Model DF', 'Market SR', 'Model SR', 'DF Error', 'SR Error']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for value_1, value_2, value_3, value_4, value_5, value_6 \
                in zip(market_discount_factor_values, model_discount_factor_values, market_spot_rate_values,
                       model_spot_rate_values, discount_factor_model_error_values, spot_rate_model_error_values):
            writer.writerow({'Market DF': value_1, 'Model DF': value_2, 'Market SR': value_3, 'Model SR': value_4,
                             'DF Error': value_5, 'SR Error': value_6})

        return Response(csvfile.getvalue(), mimetype="text/csv",
                        headers={"Content-disposition": "attachment; filename=term_data.csv"})

    else:
        return redirect(url_for('term_structure'))


def controller_term_structure_daily_data(user, id):
    id = int(id)
    if user.is_authenticated:
        csvfile = io.StringIO()
        instance = user.compute_term_structure.filter_by(id=id).first()

        dates_value = json.loads(instance.dates)
        annual_basis_date_value = json.loads(instance.annual_basis_date)
        daily_discount_factor_value = np.array(json.loads(instance.daily_discount_factor))
        daily_model_spot_rate_value = np.array(json.loads(instance.daily_model_spot_rate))

        fieldnames = ['Dates', 'Annual Basis Date', 'Daily DF', 'Daily SR']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for value_1, value_2, value_3, value_4, \
                in zip(dates_value, annual_basis_date_value, daily_discount_factor_value, daily_model_spot_rate_value):
            writer.writerow({'Dates': value_1, 'Annual Basis Date': value_2, 'Daily DF': value_3, 'Daily SR': value_4})

        return Response(csvfile.getvalue(), mimetype="text/csv",
                        headers={"Content-disposition": "attachment; filename=term_daily_data.csv"})

    else:
        return redirect(url_for('term_structure'))
