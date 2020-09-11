import csv
import io
import json

import numpy as np
from flask import redirect, url_for, Response
from sqlalchemy import desc

from asian_option.compute import create_plot_lower_bound, compute_values
from asian_option.forms import ComputeForm
from db_models import asian_option as compute
from db_models import db


def controller_asian_option(user, request):
    form = ComputeForm(request.form)

    lam = None
    lower_bound = None
    optimal_strike = None
    optimal_lower_bound = None
    lower_bound_strike = None

    sim_id = None

    plot_lower_bound = None

    if request.method == "POST":
        if form.validate():
            optimal_lower_bound, optimal_strike, lower_bound_strike, lam, lower_bound = \
                compute_values(form.model_choice.data, form.price.data, form.strike.data, form.time.data,
                               form.risk_free.data, form.step.data, form.grid.data, form.upper_range.data,
                               form.lower_range.data, form.dump.data, form.tolerance.data, form.price_exp.data,
                               form.strike_exp.data, form.risk_free_exp.data, form.time_exp.data, form.step_exp.data,
                               form.upper_range_exp.data, form.lower_range_exp.data, form.beta_cev.data, form.c.data,
                               form.g.data, form.m.data, form.y.data, form.sigma_dejd.data, form.lam_dejd.data,
                               form.rho_dejd.data, form.eta1_dejd.data, form.eta2_dejd.data, form.epsilon_exp.data,
                               form.k1_exp.data, form.sigma_exp.data, form.sigma_gaussian.data, form.volatility_t0.data,
                               form.alpha_heston.data, form.beta_heston.data, form.gamma_heston.data,
                               form.rho_heston.data, form.a_meixner.data, form.b_meixner.data, form.delta_meixner.data,
                               form.sigma_mjd.data, form.lam_mjd.data, form.mu_x_mjd.data, form.sigma_x_mjd.data,
                               form.a_nig.data, form.b_nig.data, form.delta_nig.data, form.sigma_vg.data,
                               form.theta_vg.data, form.kappa_vg.data, )

            plot_lower_bound = create_plot_lower_bound(lam, lower_bound)

            if user.is_authenticated:  # store data in db
                object = compute()
                form.populate_obj(object)

                # json.dumps return a array string
                # json.loads convert from string to array

                object.lam = json.dumps(lam.tolist())
                object.lower_bound = json.dumps(lower_bound.tolist())
                object.optimal_strike = optimal_strike
                object.optimal_lower_bound = optimal_lower_bound
                object.lower_bound_strike = lower_bound_strike

                object.user = user
                db.session.add(object)
                db.session.commit()
                sim_id = object.id
    else:
        if user.is_authenticated:  # user authenticated, store the data
            if user.compute_asian_option.count() > 0:
                instance = user.compute_asian_option.order_by(desc('id')).first()
                form = populate_form_from_instance(instance)

                sim_id = instance.id
                lam = np.array(json.loads(instance.lam))
                lower_bound = np.array(json.loads(instance.lower_bound))
                optimal_strike = instance.optimal_strike
                optimal_lower_bound = instance.optimal_lower_bound
                lower_bound_strike = instance.lower_bound_strike

                plot_lower_bound = \
                    create_plot_lower_bound(lam, lower_bound)

    optimal_strike = round(optimal_strike, 4) if optimal_strike is not None else None
    optimal_lower_bound = round(optimal_lower_bound, 4) if optimal_lower_bound is not None else None
    lower_bound_strike = round(lower_bound_strike, 4) if lower_bound is not None else None
    lam = [round(x, 6) for x in lam] if lam is not None else None
    lower_bound = [round(x, 6) for x in lower_bound] if lower_bound is not None else None

    return {'form': form, 'user': user, 'optimal_strike': optimal_strike, 'optimal_lower_bound': optimal_lower_bound,
            'lower_bound_strike': lower_bound_strike, 'lam': lam, 'lower_bound': lower_bound,
            'plot_lower_bound': plot_lower_bound, 'sim_id': sim_id}


def populate_form_from_instance(instance):
    """Repopulate form with previous values"""
    form = ComputeForm()
    for field in form:
        field.data = getattr(instance, field.name, None)  # get a value or, if it doesn't exist, a default value
    return form


def controller_old_asian_option(user):
    data = []

    if user.is_authenticated():
        instances = user.compute_asian_option.order_by(desc('id')).all()
        for instance in instances:
            form = populate_form_from_instance(instance)

            # page old.html, store the date and the plot (previous simulation)

            id = instance.id
            lam = np.array(json.loads(instance.lam))
            lower_bound = np.array(json.loads(instance.lower_bound))
            optimal_strike = instance.optimal_strike
            optimal_lower_bound = instance.optimal_lower_bound
            lower_bound_strike = instance.lower_bound_strike

            plot_lower_bound = \
                create_plot_lower_bound(lam, lower_bound)

            optimal_strike = round(optimal_strike, 4) if optimal_strike is not None else None
            optimal_lower_bound = round(optimal_lower_bound, 4) if optimal_lower_bound is not None else None
            lower_bound_strike = round(lower_bound_strike, 4) if lower_bound is not None else None

            data.append({'form': form, 'id': id, 'optimal_strike': optimal_strike,
                         'optimal_lower_bound': optimal_lower_bound, 'lower_bound_strike': lower_bound_strike,
                         'plot_lower_bound': plot_lower_bound})

    return {'data': data}


def delete_asian_option_simulation(user, id):
    id = int(id)
    if user.is_authenticated():
        if id == -1:
            user.compute_asian_option.delete()
        else:
            try:
                instance = user.compute_asian_option.filter_by(id=id).first()
                db.session.delete(instance)
            except:
                pass

        db.session.commit()
    return redirect(url_for('old_asian_option'))


def controller_asian_option_data(user, id):
    id = int(id)
    if user.is_authenticated:
        csvfile = io.StringIO()
        instance = user.compute_asian_option.filter_by(id=id).first()

        lam_values = np.array(json.loads(instance.lam))
        lower_bound_values = np.array(json.loads(instance.lower_bound))

        fieldnames = ['Lam Asset', 'Lower Bound']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for value_1, value_2 in zip(lam_values, lower_bound_values):
            writer.writerow({'Lam Asset': value_1, 'Lower Bound': value_2})

        return Response(csvfile.getvalue(), mimetype="text/csv",
                        headers={"Content-disposition": "attachment; filename=asian_data.csv"})

    else:
        return redirect(url_for('asian_option'))
