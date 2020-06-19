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
from db_models import principal_component_analysis as compute
from principal_component_analysis.compute import import_dataset_file_excel, import_dataset_tickers, \
    create_plot_variance_component, create_plot_cumulative_component, create_plot_one_loadings, create_plot_two_loadings
from principal_component_analysis.forms import ComputeForm


def controller_principal_component_analysis(user, request):
    form = ComputeForm(request.form)

    file_data = None

    sim_id = None

    plot_variance_component = None
    plot_cumulative_component = None
    plot_one_loadings = None
    plot_two_loadings = None

    if request.method == "POST":
        if form.validate():
            if form.method_choice.data == '0':
                if request.files:
                    file = request.files[form.file_data.name]

                    if file and allowed_file(file.filename):
                        file_data = secure_filename(file.filename)
                        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file_data))

                evalues, autovect, pc_terms = import_dataset_file_excel(file_data, form.asset_flag.data,
                                                                        form.matrix_flag.data)
            else:
                evalues, autovect, pc_terms = import_dataset_tickers(form.tickers_list.data, form.start_day.data,
                                                                     form.start_month.data, form.start_year.data,
                                                                     form.end_day.data, form.end_month.data,
                                                                     form.end_year.data, form.asset_flag.data,
                                                                     form.matrix_flag.data)

            plot_variance_component = create_plot_variance_component(evalues, form.explained_variance.data)

            plot_cumulative_component = create_plot_cumulative_component(evalues, form.explained_variance.data)

            plot_one_loadings = create_plot_one_loadings(autovect)

            plot_two_loadings = create_plot_two_loadings(autovect)

            if user.is_authenticated:  # store data in db
                object = compute()
                form.populate_obj(object)

                object.evalues = json.dumps(evalues.tolist())
                object.autovect = json.dumps(autovect.tolist())
                object.pc_terms = json.dumps(pc_terms)

                object.user = user
                db.session.add(object)
                db.session.commit()
                sim_id = object.id

    else:
        if user.is_authenticated:  # user authenticated, store the data
            if user.compute_principal_component_analysis.count() > 0:
                instance = user.compute_principal_component_analysis.order_by(
                    desc('id')).first()  # decreasing order db, take the last data saved
                form = populate_form_from_instance(instance)

                sim_id = instance.id
                evalues = np.array(json.loads(instance.evalues))
                autovect = np.array(json.loads(instance.autovect))

                plot_variance_component = create_plot_variance_component(evalues, form.explained_variance.data)

                plot_cumulative_component = create_plot_cumulative_component(evalues, form.explained_variance.data)

                plot_one_loadings = create_plot_one_loadings(autovect)

                plot_two_loadings = create_plot_two_loadings(autovect)

    return {'form': form, 'user': user, 'plot_variance_component': plot_variance_component,
            'plot_cumulative_component': plot_cumulative_component, 'plot_one_loadings': plot_one_loadings,
            'plot_two_loadings': plot_two_loadings, 'sim_id': sim_id}


def populate_form_from_instance(instance):
    """Repopulate form with previous values"""
    form = ComputeForm()
    for field in form:
        if not type(field.data) == list:  # dont't use the variables tickers_list
            field.data = getattr(instance, field.name, None)  # get a value or, if it doesn't exist, a default value

    return form


def controller_old_principal_component_analysis(user):
    data = []

    if user.is_authenticated():
        instances = user.compute_principal_component_analysis.order_by(desc('id')).all()
        for instance in instances:
            form = populate_form_from_instance(instance)

            # page old.html, store the date and the plot (previous simulation)

            id = instance.id
            evalues = np.array(json.loads(instance.evalues))
            autovect = np.array(json.loads(instance.autovect))

            plot_variance_component = create_plot_variance_component(evalues, form.explained_variance.data)

            plot_cumulative_component = create_plot_cumulative_component(evalues, form.explained_variance.data)

            plot_one_loadings = create_plot_one_loadings(autovect)

            plot_two_loadings = create_plot_two_loadings(autovect)

            data.append({'form': form, 'id': id, 'plot_variance_component': plot_variance_component,
                         'plot_cumulative_component': plot_cumulative_component, 'plot_one_loadings': plot_one_loadings,
                         'plot_two_loadings': plot_two_loadings})

    return {'data': data}


def delete_principal_component_analysis_simulation(user, id):
    id = int(id)
    if user.is_authenticated():
        if id == -1:
            user.compute_principal_component_analysis.delete()
        else:
            try:
                instance = user.compute_principal_component_analysis.filter_by(id=id).first()
                db.session.delete(instance)
            except:
                pass

        db.session.commit()
    return redirect(url_for('old_principal_component_analysis'))


def controller_principal_component_analysis_data(user, id):
    id = int(id)
    if user.is_authenticated:
        csvfile = io.StringIO()
        instance = user.compute_principal_component_analysis.filter_by(id=id).first()

        evalues_values = np.array(json.loads(instance.evalues))
        autovect_values = np.array(json.loads(instance.autovect))

        fieldnames = ['EigenValues', 'EigenVectors']

        writer = csv.writer(csvfile)
        writer.writerow(fieldnames)
        for value in zip(evalues_values, autovect_values):
            writer.writerow(value)

        return Response(csvfile.getvalue(), mimetype="text/csv",
                        headers={"Content-disposition": "attachment; filename=principal_component_data.csv"})

    else:
        return redirect(url_for('principal_component_analysis'))
