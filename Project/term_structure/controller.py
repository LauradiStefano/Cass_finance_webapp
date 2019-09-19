import json
import os

from flask import url_for, redirect
from sqlalchemy import desc
from werkzeug.utils import secure_filename

from app import allowed_file, app
from db_models import db
from db_models import term_structure as compute
from term_structure.compute import upload_input, fitting_method, create_plot_discount_factor_term_structure, \
    create_plot_interest_rate_term_structure, create_plot_error_discount_factor, create_plot_error_interest_rate
from term_structure.forms import ComputeForm


def controller_term_structure(user, request):
    form = ComputeForm(request.form)

    file_name = None
    variables = None
    market_discount_factor = None
    market_spot_rate = None
    model_discount_factor = None
    model_spot_rate = None
    discount_factor_model_error = None
    spot_rate_model_error = None
    parameters = None
    time = None

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

            market_discount_factor, market_spot_rate, model_discount_factor, model_spot_rate, \
                discount_factor_model_error, spot_rate_model_error, parameters, time = \
                fitting_method(form.model_choice.data, variables, file_name, form.discount_factor.data,
                               form.least_fmin.data)

            plot_discount_factor_term_structure = \
                create_plot_discount_factor_term_structure(time, market_discount_factor, model_discount_factor)
            plot_interest_rate_term_structure = \
                create_plot_interest_rate_term_structure(time, market_spot_rate, model_spot_rate)
            plot_error_discount_factor = create_plot_error_discount_factor(time, discount_factor_model_error)
            plot_error_interest_rate = create_plot_error_interest_rate(time, spot_rate_model_error)

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

                plot_discount_factor_term_structure = \
                    create_plot_discount_factor_term_structure(time, market_discount_factor, model_discount_factor)
                plot_interest_rate_term_structure = \
                    create_plot_interest_rate_term_structure(time, market_spot_rate, model_spot_rate)
                plot_error_discount_factor = create_plot_error_discount_factor(time, discount_factor_model_error)
                plot_error_interest_rate = create_plot_error_interest_rate(time, spot_rate_model_error)

    return {'form': form, 'user': user, 'parameters': parameters, 'time': time,
            'market_discount_factor': market_discount_factor, 'model_discount_factor': model_discount_factor,
            'market_spot_rate': market_spot_rate, 'model_spot_rate': model_spot_rate,
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
            plot_error_discount_factor = create_plot_error_discount_factor(time, discount_factor_model_error)
            plot_error_interest_rate = create_plot_error_interest_rate(time, spot_rate_model_error)

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
