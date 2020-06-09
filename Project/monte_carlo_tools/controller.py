import csv
import io
import json

import numpy as np
from flask import redirect, url_for, Response
from sqlalchemy import desc

from db_models import db
from db_models import monte_carlo_tools as compute
from monte_carlo_tools.compute import get_simutalted_path_and_moments, create_plot_simulated_paths, create_plot_moments, \
    create_plot_histogram
from monte_carlo_tools.forms import ComputeForm


def controller_monte_carlo_tools(user, request):
    form = ComputeForm(request.form)

    sim_id = None

    plot_simulated_paths = None

    plot_moments = None

    plot_histogram = None

    if request.method == "POST":
        if form.validate():
            simulated_paths, moments, quantiles, timestep = \
                get_simutalted_path_and_moments(form.time.data, form.number_step.data, form.number_paths.data,
                                                form.model_choice.data, form.price.data, form.mu_abm.data,
                                                form.sigma_abm.data, form.mu_gbm.data, form.sigma_gbm.data,
                                                form.alpha_cir.data, form.mu_cir.data, form.sigma_cir.data,
                                                form.alpha_mrg.data, form.mu_mrg.data, form.sigma_mrg.data,
                                                form.mu_heston.data, form.volatility_t0_heston.data,
                                                form.alpha_heston.data, form.beta_heston.data, form.eta_heston.data,
                                                form.rho_heston.data)

            plot_simulated_paths = create_plot_simulated_paths(simulated_paths, timestep, form.number_step.data,
                                                               form.number_paths.data, quantiles)

            plot_moments = create_plot_moments(simulated_paths, moments, timestep)

            plot_histogram = create_plot_histogram(simulated_paths, form.number_step.data)

            if user.is_authenticated:  # store data in db
                object = compute()
                form.populate_obj(object)

                # json.dumps return a array string
                # json.loads convert from string to array

                object.simulated_paths = json.dumps(simulated_paths.tolist())
                object.timestep = json.dumps(timestep.tolist())
                object.quantiles = json.dumps(quantiles.tolist())
                object.moments = json.dumps(moments.tolist())

                object.user = user
                db.session.add(object)
                db.session.commit()
                sim_id = object.id
    else:
        if user.is_authenticated:  # user authenticated, store the data
            if user.compute_monte_carlo_tools.count() > 0:
                instance = user.compute_monte_carlo_tools.order_by(desc('id')).first()
                form = populate_form_from_instance(instance)

                sim_id = instance.id
                simulated_paths = np.array(json.loads(instance.simulated_paths))
                timestep = np.array(json.loads(instance.timestep))
                quantiles = np.array(json.loads(instance.quantiles))
                moments = np.array(json.loads(instance.moments))

                plot_simulated_paths = create_plot_simulated_paths(simulated_paths, timestep, form.number_step.data,
                                                                   form.number_paths.data, quantiles)

                plot_moments = create_plot_moments(simulated_paths, moments, timestep)

                plot_histogram = create_plot_histogram(simulated_paths, form.number_step.data)

    return {'form': form, 'user': user, 'plot_simulated_paths': plot_simulated_paths, 'plot_moments': plot_moments,
            'plot_histogram': plot_histogram, 'sim_id': sim_id}


def populate_form_from_instance(instance):
    """Repopulate form with previous values"""
    form = ComputeForm()
    for field in form:
        field.data = getattr(instance, field.name, None)  # get a value or, if it doesn't exist, a default value
    return form


def controller_old_monte_carlo_tools(user):
    data = []
    if user.is_authenticated():
        instances = user.compute_monte_carlo_tools.order_by(desc('id')).all()
        for instance in instances:
            form = populate_form_from_instance(instance)

            # page old.html, store the date and the plot (previous simulation)

            id = instance.id
            simulated_paths = np.array(json.loads(instance.simulated_paths))
            timestep = np.array(json.loads(instance.timestep))
            quantiles = np.array(json.loads(instance.quantiles))
            moments = np.array(json.loads(instance.moments))

            plot_simulated_paths = create_plot_simulated_paths(simulated_paths, timestep, form.number_step.data,
                                                               form.number_paths.data, quantiles)

            plot_moments = create_plot_moments(simulated_paths, moments, timestep)

            plot_histogram = create_plot_histogram(simulated_paths, form.number_step.data)

            data.append(
                {'form': form, 'id': id, 'plot_simulated_paths': plot_simulated_paths, 'plot_moments': plot_moments,
                 'plot_histogram': plot_histogram})

    return {'data': data}


def delete_monte_carlo_tools_simulation(user, id):
    id = int(id)
    if user.is_authenticated():
        if id == -1:
            user.compute_monte_carlo_tools.delete()
        else:
            try:
                instance = user.compute_monte_carlo_tools.filter_by(id=id).first()
                db.session.delete(instance)
            except:
                pass

        db.session.commit()
    return redirect(url_for('old_monte_carlo_tools'))


def controller_monte_carlo_tools_paths_data(user, id):
    id = int(id)
    if user.is_authenticated:
        csvfile = io.StringIO()
        instance = user.compute_monte_carlo_tools.filter_by(id=id).first()

        timestep_values = np.array(json.loads(instance.timestep))

        simulated_paths_values = np.array(json.loads(instance.simulated_paths))

        fieldnames = ['Time Step', 'Simulated Paths']

        writer = csv.writer(csvfile)
        writer.writerow(fieldnames)
        for value in zip(timestep_values, simulated_paths_values.tolist()):
            writer.writerow(value)

        return Response(csvfile.getvalue(), mimetype="text/csv",
                        headers={"Content-disposition": "attachment; filename=pro.csv"})

    else:
        return redirect(url_for('monte_carlo_tools'))
