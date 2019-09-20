import json
import os

from flask import url_for, redirect
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

    file_name = None
    market_discount_factor = None
    market_spot_rate = None
    model_discount_factor = None
    model_spot_rate = None
    discount_factor_model_error = None
    spot_rate_model_error = None
    parameters = None
    time = None
    number_of_time = 0

    plot_discount_factor_term_structure = None
    plot_interest_rate_term_structure = None
    plot_error_discount_factor = None
    plot_error_interest_rate = None

    if request.method == "POST":
        if form.validate():
            file = request.files[form.file_name.name]

            if file and allowed_file(file.filename):
                file_name = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], file_name))

            file_name = upload_input(file_name)

            variables = create_objective_vector(form.model_choice.data, form.kappa_vasicek.data,
                                                form.theta_vasicek.data, form.sigma_vasicek.data, form.rho_vasicek.data,
                                                form.kappa_cir.data, form.theta_cir.data, form.sigma_cir.data,
                                                form.rho_cir.data, form.beta0_nelson.data, form.beta1_nelson.data,
                                                form.beta2_nelson.data, form.tau_nelson.data, form.beta0_svensson.data,
                                                form.beta1_svensson.data, form.beta2_svensson.data,
                                                form.beta3_svensson.data, form.tau1_svensson.data,
                                                form.tau2_svensson.data)

            market_discount_factor, market_spot_rate, model_discount_factor, model_spot_rate, \
            discount_factor_model_error, spot_rate_model_error, parameters, time = \
                fitting_method(form.model_choice.data, variables, file_name, form.discount_factor.data,
                               form.least_fmin.data)

            number_of_time = len(time)
            # number_of_parameters = len(parameters)

            plot_discount_factor_term_structure = \
                create_plot_discount_factor_term_structure(time, market_discount_factor, model_discount_factor)
            plot_interest_rate_term_structure = \
                create_plot_interest_rate_term_structure(time, market_spot_rate, model_spot_rate)
            plot_error_discount_factor = create_plot_error_discount_factor(discount_factor_model_error)
            plot_error_interest_rate = create_plot_error_interest_rate(spot_rate_model_error)

        if user.is_authenticated:  # store data in db
            object = compute()
            form.populate_obj(object)

            object.parameters = json.dumps(parameters)
            object.time = json.dumps(time)
            object.market_discount_factor = json.dumps(market_discount_factor)
            object.model_discount_factor = json.dumps(model_discount_factor)
            object.market_spot_rate = json.dumps(market_spot_rate)
            object.model_spot_rate = json.dumps(model_spot_rate)
            object.discount_factor_model_error = json.dumps(discount_factor_model_error)
            object.spot_rate_model_error = json.dumps(spot_rate_model_error)
            object.number_of_time = json.dumps(number_of_time)

            object.user = user
            db.session.add(object)
            db.session.commit()

    else:

        if user.is_authenticated:  # user authenticated, store the data
            if user.compute_term_structure.count() > 0:
                instance = user.compute_term_structure.order_by(
                    desc('id')).first()  # decreasing order db, take the last data saved
                form = populate_form_from_instance(instance)

                parameters = json.loads(instance.parameters)
                time = json.loads(instance.time)
                market_discount_factor = json.loads(instance.market_discount_factor)
                model_discount_factor = json.loads(instance.model_discount_factor)
                market_spot_rate = json.loads(instance.market_spot_rate)
                model_spot_rate = json.loads(instance.model_spot_rate)
                discount_factor_model_error = json.loads(instance.discount_factor_model_error)
                spot_rate_model_error = json.loads(instance.spot_rate_model_error)
                number_of_time = json.loads(instance.number_of_time)

                plot_discount_factor_term_structure = \
                    create_plot_discount_factor_term_structure(time, market_discount_factor, model_discount_factor)
                plot_interest_rate_term_structure = \
                    create_plot_interest_rate_term_structure(time, market_spot_rate, model_spot_rate)
                plot_error_discount_factor = create_plot_error_discount_factor(discount_factor_model_error)
                plot_error_interest_rate = create_plot_error_interest_rate(spot_rate_model_error)

    time = [round(x, 4) for x in time] if time is not None else None
    market_discount_factor = [round(x, 4) for x in
                              market_discount_factor] if market_discount_factor is not None else None
    model_discount_factor = [round(x, 4) for x in model_discount_factor] if model_discount_factor is not None else None
    market_spot_rate = [round(x, 4) for x in market_spot_rate] if market_spot_rate is not None else None
    model_spot_rate = [round(x, 4) for x in model_spot_rate] if model_spot_rate is not None else None

    return {'form': form, 'user': user, 'parameters': parameters, 'time': time,
            'market_discount_factor': market_discount_factor, 'model_discount_factor': model_discount_factor,
            'market_spot_rate': market_spot_rate, 'model_spot_rate': model_spot_rate, 'number_of_time': number_of_time,
            'plot_discount_factor_term_structure': plot_discount_factor_term_structure,
            'plot_interest_rate_term_structure': plot_interest_rate_term_structure,
            'plot_error_discount_factor': plot_error_discount_factor,
            'plot_error_interest_rate': plot_error_interest_rate}


def populate_form_from_instance(instance):
    """Repopulate form with previous values"""
    form = ComputeForm()
    for field in form:
        field.data = getattr(instance, field.name)
    return form


def controller_old_term_structure(user):
    data = []

    if user.is_authenticated():
        instances = user.compute_term_structure.order_by(desc('id')).all()
        for instance in instances:
            form = populate_form_from_instance(instance)

            # page old.html, store the date and the plot (previous simulation)

            id = instance.id
            parameters = json.loads(instance.parameters)
            time = json.loads(instance.time)
            market_discount_factor = json.loads(instance.market_discount_factor)
            model_discount_factor = json.loads(instance.model_discount_factor)
            market_spot_rate = json.loads(instance.market_spot_rate)
            model_spot_rate = json.loads(instance.model_spot_rate)
            discount_factor_model_error = json.loads(instance.discount_factor_model_error)
            spot_rate_model_error = json.loads(instance.spot_rate_model_error)

            plot_discount_factor_term_structure = \
                create_plot_discount_factor_term_structure(time, market_discount_factor, model_discount_factor)
            plot_interest_rate_term_structure = \
                create_plot_interest_rate_term_structure(time, market_spot_rate, model_spot_rate)
            plot_error_discount_factor = create_plot_error_discount_factor(discount_factor_model_error)
            plot_error_interest_rate = create_plot_error_interest_rate(spot_rate_model_error)

            data.append({'form': form, 'id': id, 'parameters': parameters,
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
                instance = user.compute_term_strucuture.filter_by(id=id).first()
                db.session.delete(instance)
            except:
                pass

        db.session.commit()
    return redirect(url_for('old_term_structure'))
