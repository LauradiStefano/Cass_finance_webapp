import json
import os

import numpy as np
from flask import render_template, request, redirect, url_for
from flask_login import LoginManager, current_user, \
    login_user, logout_user, login_required
from sqlalchemy import desc

from app import app
from db_models import db, User, Compute
from forms import ComputeForm
from main_gbm_bounds_asian_option import create_plot_lower_bound, compute_values

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(user_id)


@app.route('/', methods=['GET', 'POST'])
def index():
    user = current_user
    form = ComputeForm(request.form)

    lam = None
    lower_bound = None
    optimal_strike = None
    optimal_lower_bound = None
    lower_bound_strike = None

    plot_lower_bound = None

    if request.method == "POST":
        if form.validate():
            optimal_lower_bound, optimal_strike, lower_bound_strike, lam, lower_bound = \
                compute_values(form.price.data, form.strike.data, form.time.data, form.risk_free.data, form.step.data,
                               form.sigma.data)

            plot_lower_bound = create_plot_lower_bound(lam, lower_bound, form.strike.data, optimal_strike)

        if user.is_authenticated:  # store data in db
            object = Compute()
            form.populate_obj(object)

            # json.dumps return a array string
            # json.loads convert from string to array

            object.lam = json.dumps(lam)
            object.lower_bound = json.dumps(lower_bound)
            object.strike = form.strike.data
            object.optimal_strike = optimal_strike
            object.optimal_lower_bound = optimal_lower_bound
            object.lower_bound_strike = lower_bound_strike

            object.user = user
            db.session.add(object)
            db.session.commit()
    else:
        if user.is_authenticated:  # user authenticated, store the data
            if user.Compute.count() > 0:
                instance = user.Compute.order_by(desc('id')).first()
                form = populate_form_from_instance(instance)

                lam = json.loads(instance.lam)
                lower_bound = json.loads(instance.lower_bound)
                strike = instance.strike
                optimal_strike = instance.optimal_strike
                optimal_lower_bound = instance.optimal_lower_bound
                lower_bound_strike = instance.lower_bound_strike

                plot_lower_bound = \
                    create_plot_lower_bound(lam, lower_bound, strike, optimal_strike)

    optimal_strike = round(optimal_strike, 4) if optimal_strike is not None else None
    optimal_lower_bound = round(optimal_lower_bound, 4) if optimal_lower_bound is not None else None
    lower_bound_strike = round(lower_bound_strike, 4) if lower_bound is not None else None

    return render_template("view_bootstrap.html", form=form, user=user, optimal_strike=optimal_strike,
                           optimal_lower_bound=optimal_lower_bound, lower_bound_strike=lower_bound_strike,
                           plot_lower_bound=plot_lower_bound)


def populate_form_from_instance(instance):
    """Repopulate form with previous values"""
    form = ComputeForm()
    for field in form:
        field.data = getattr(instance, field.name)
    return form


@app.route('/reg', methods=['GET', 'POST'])
def create_login():
    from forms import RegistrationForm
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User()
        form.populate_obj(user)
        user.set_password(form.password.data)

        db.session.add(user)
        db.session.commit()

        login_user(user)
        return redirect(url_for('index'))
    return render_template("reg.html", form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    from forms import Loginform
    form = Loginform(request.form)
    if request.method == 'POST' and form.validate():
        user = form.get_user()
        login_user(user)
        return redirect(url_for('index'))
    return render_template("login.html", form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/old')
@login_required
def old():
    data = []
    user = current_user
    if user.is_authenticated():
        instances = user.Compute.order_by(desc('id')).all()
        for instance in instances:
            form = populate_form_from_instance(instance)

            # page old.html, store the date and the plot (previous simulation)

            id = instance.id
            lam = json.loads(instance.lam)
            lower_bound = json.loads(instance.lower_bound)
            strike = instance.strike
            optimal_strike = instance.optimal_strike
            optimal_lower_bound = instance.optimal_lower_bound
            lower_bound_strike = instance.lower_bound_strike

            plot_lower_bound = \
                create_plot_lower_bound(lam, lower_bound, strike, optimal_strike)

            optimal_strike = round(optimal_strike, 4) if optimal_strike is not None else None
            optimal_lower_bound = round(optimal_lower_bound, 4) if optimal_lower_bound is not None else None
            lower_bound_strike = round(lower_bound_strike, 4) if lower_bound is not None else None

            data.append({'form': form, 'id': id, 'optimal_strike': optimal_strike,
                         'optimal_lower_bound': optimal_lower_bound, 'strike': strike,
                         'lower_bound_strike': lower_bound_strike, 'plot_lower_bound': plot_lower_bound})

    return render_template("old.html", data=data)


@app.route('/delete/<id>', methods=['GET', 'POST'])
@login_required
def delete_post(id):
    id = int(id)
    user = current_user
    if user.is_authenticated():
        if id == -1:
            user.Compute.delete()
        else:
            try:
                instance = user.Compute.filter_by(id=id).first()
                db.session.delete(instance)
            except:
                pass

        db.session.commit()
    return redirect(url_for('old'))


if __name__ == '__main__':
    if not os.path.isfile(os.path.join(os.path.dirname(__file__), 'sqlite.db')):
        db.create_all()
    app.run(debug=True)
