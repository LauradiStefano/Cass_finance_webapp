import json
import os

import numpy as np
from flask import url_for, redirect
from sqlalchemy import desc
from werkzeug.utils import secure_filename

from app import allowed_file, app
from db_models import db
from db_models import portfolio_analysis as compute
from portfolio_analysis.compute import upload_input, compute_efficient_frontier, create_plot_efficient_frontier
from portfolio_analysis.forms import ComputeForm


def controller_portfolio_analysis(user, request):
    form = ComputeForm(request.form)

    returns = None
    file_data = None
    standard_deviations = None
    means = None
    efficient_means = None
    efficient_std = None
    plot_efficient_frontier = None

    if request.method == "POST":
        if form.validate() and request.files:
            file = request.files[form.file_data.name]

            if file and allowed_file(file.filename):
                file_data = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], file_data))

            returns, n_assets = upload_input(file_data)

            standard_deviations, means, efficient_means, efficient_std = \
                compute_efficient_frontier(returns, n_assets, form.n_portfolio.data)

            plot_efficient_frontier = \
                create_plot_efficient_frontier(returns, standard_deviations, means, efficient_means,
                                               efficient_std)

        if user.is_authenticated:  # store data in db
            object = compute()
            form.populate_obj(object)

            object.returns = json.dumps(returns.tolist())
            object.standard_deviations = json.dumps(standard_deviations)
            object.means = json.dumps(means)
            object.efficient_means = json.dumps(efficient_means.tolist())
            object.efficient_std = json.dumps(efficient_std.tolist())

            object.user = user
            db.session.add(object)
            db.session.commit()

    else:
        if user.is_authenticated:  # user authenticated, store the data
            if user.compute_portfolio_analysis.count() > 0:
                instance = user.compute_portfolio_analysis.order_by(
                    desc('id')).first()  # decreasing order db, take the last data saved
                form = populate_form_from_instance(instance)

                returns = np.array(json.loads(instance.returns))
                standard_deviations = json.loads(instance.standard_deviations)
                means = json.loads(instance.means)
                efficient_means = np.array(json.loads(instance.efficient_means))
                efficient_std = np.array(json.loads(instance.efficient_std))

                plot_efficient_frontier = \
                    create_plot_efficient_frontier(returns, standard_deviations, means, efficient_means,
                                                   efficient_std)

    return {'form': form, 'user': user, 'plot_efficient_frontier': plot_efficient_frontier}


def populate_form_from_instance(instance):
    """Repopulate form with previous values"""
    form = ComputeForm()
    for field in form:
        field.data = getattr(instance, field.name, None)  # get a value or, if it doesn't exist, a default value
    return form


def controller_old_portfolio_analysis(user):
    data = []

    if user.is_authenticated():
        instances = user.compute_portfolio_analysis.order_by(desc('id')).all()
        for instance in instances:
            form = populate_form_from_instance(instance)

            # page old.html, store the date and the plot (previous simulation)

            returns = np.array(json.loads(instance.returns))
            standard_deviations = json.loads(instance.standard_deviations)
            means = json.loads(instance.means)
            efficient_means = np.array(json.loads(instance.efficient_means))
            efficient_std = np.array(json.loads(instance.efficient_std))

            plot_efficient_frontier = \
                create_plot_efficient_frontier(returns, standard_deviations, means, efficient_means,
                                               efficient_std)

            data.append({'form': form, 'id': id, 'plot_efficient_frontier': plot_efficient_frontier})

    return {'data': data}


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
