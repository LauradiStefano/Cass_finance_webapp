import csv
import io
import json
import os

from flask import url_for, redirect, Response
from sqlalchemy import desc
from werkzeug.utils import secure_filename

from app import allowed_file, app
from db_models import db
from db_models import linear_interpolation_constant_forward as compute
from linear_interpolation_constant_forward.compute import upload_input, get_spot_rate_discount_factor, \
    create_plot_discount_factor_term_structure, create_plot_interest_rate_term_structure
from linear_interpolation_constant_forward.forms import ComputeForm


def controller_linear_interpolation_constant_forward(user, request):
    form = ComputeForm(request.form)

    file_data = None

    compute_not_allowed = False

    sim_id = None

    plot_discount_factor_term_structure = None
    plot_interest_rate_term_structure = None

    if request.method == "POST":
        if user.is_authenticated:
            if form.validate and request.files:
                file = request.files[form.file_data.name]

                if file and allowed_file(file.filename):
                    file_data = secure_filename(file.filename)
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], file_data))

                file_data = upload_input(file_data)

                model_discount_factor, model_spot_rate, market_spot_rate, market_discount_factor, date_db, \
                daily_time_plot, time_plot = get_spot_rate_discount_factor(file_data, form.model_choices.data)

                plot_discount_factor_term_structure = \
                    create_plot_discount_factor_term_structure(time_plot, market_discount_factor, daily_time_plot,
                                                               model_discount_factor)
                plot_interest_rate_term_structure = \
                    create_plot_interest_rate_term_structure(time_plot, market_spot_rate, daily_time_plot,
                                                             model_spot_rate)

                if user.is_authenticated:  # store data in db
                    object = compute()
                    form.populate_obj(object)

                    object.time_plot = json.dumps(time_plot)
                    object.daily_time_plot = json.dumps(daily_time_plot)
                    object.market_discount_factor = json.dumps(market_discount_factor)
                    object.model_discount_factor = json.dumps(model_discount_factor)
                    object.market_spot_rate = json.dumps(market_spot_rate)
                    object.model_spot_rate = json.dumps(model_spot_rate)
                    object.date_db = json.dumps(date_db)

                    object.user = user
                    db.session.add(object)
                    db.session.commit()
                    sim_id = object.id
        else:
            compute_not_allowed = True

    else:
        if user.is_authenticated:  # user authenticated, store the data
            if user.compute_linear_interpolation_constant_forward.count() > 0:
                instance = user.compute_linear_interpolation_constant_forward.order_by(
                    desc('id')).first()  # decreasing order db, take the last data saved
                form = populate_form_from_instance(instance)

                sim_id = instance.id

                time_plot = json.loads(instance.time_plot)
                daily_time_plot = json.loads(instance.daily_time_plot)
                market_discount_factor = json.loads(instance.market_discount_factor)
                model_discount_factor = json.loads(instance.model_discount_factor)
                market_spot_rate = json.loads(instance.market_spot_rate)
                model_spot_rate = json.loads(instance.model_spot_rate)

                plot_discount_factor_term_structure = \
                    create_plot_discount_factor_term_structure(time_plot, market_discount_factor, daily_time_plot,
                                                               model_discount_factor)
                plot_interest_rate_term_structure = \
                    create_plot_interest_rate_term_structure(time_plot, market_spot_rate, daily_time_plot,
                                                             model_spot_rate)

    return {'form': form, 'user': user,
            'plot_discount_factor_term_structure': plot_discount_factor_term_structure,
            'plot_interest_rate_term_structure': plot_interest_rate_term_structure,
            'compute_not_allowed': compute_not_allowed, 'sim_id': sim_id}


def populate_form_from_instance(instance):
    """Repopulate form with previous values"""
    form = ComputeForm()
    for field in form:
        field.data = getattr(instance, field.name, None)  # get a value or, if it doesn't exist, a default value
    return form


def controller_old_linear_interpolation_constant_forward(user):
    data = []

    if user.is_authenticated():
        instances = user.compute_linear_interpolation_constant_forward.order_by(desc('id')).all()
        for instance in instances:
            form = populate_form_from_instance(instance)

            # page old.html, store the date and the plot (previous simulation)

            id = instance.id
            time_plot = json.loads(instance.time_plot)
            daily_time_plot = json.loads(instance.daily_time_plot)
            market_discount_factor = json.loads(instance.market_discount_factor)
            model_discount_factor = json.loads(instance.model_discount_factor)
            market_spot_rate = json.loads(instance.market_spot_rate)
            model_spot_rate = json.loads(instance.model_spot_rate)

            plot_discount_factor_term_structure = \
                create_plot_discount_factor_term_structure(time_plot, market_discount_factor, daily_time_plot,
                                                           model_discount_factor)
            plot_interest_rate_term_structure = \
                create_plot_interest_rate_term_structure(time_plot, market_spot_rate, daily_time_plot,
                                                         model_spot_rate)

            data.append({'form': form, 'id': id,
                         'plot_discount_factor_term_structure': plot_discount_factor_term_structure,
                         'plot_interest_rate_term_structure': plot_interest_rate_term_structure})

    return {'data': data}


def delete_linear_interpolation_constant_forward_simulation(user, id):
    id = int(id)
    if user.is_authenticated():
        if id == -1:
            user.compute_linear_interpolation_constant_forward.delete()
        else:
            try:
                instance = user.compute_linear_interpolation_constant_forward.filter_by(id=id).first()
                db.session.delete(instance)
            except:
                pass

        db.session.commit()
    return redirect(url_for('old_linear_interpolation_constant_forward'))


def controller_linear_interpolation_constant_forward_data(user, id):
    id = int(id)
    if user.is_authenticated:
        csvfile = io.StringIO()
        instance = user.compute_linear_interpolation_constant_forward.filter_by(id=id).first()

        model_discount_factor_values = json.loads(instance.model_discount_factor)
        model_spot_rate_values = json.loads(instance.model_spot_rate)
        date_db_values = json.loads(instance.date_db)

        fieldnames = ['Maturity', 'Interpolation DF', 'Interpolation SR']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for value_1, value_2, value_3 \
                in zip(date_db_values, model_discount_factor_values, model_spot_rate_values):
            writer.writerow({'Maturity': value_1, 'Interpolation DF': value_2, 'Interpolation SR': value_3})

        return Response(csvfile.getvalue(), mimetype="text/csv",
                        headers={"Content-disposition": "attachment; filename=linear_constant_data.csv"})

    else:
        return redirect(url_for('linear_interpolation_contract_forward'))
