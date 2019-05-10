import os
from compute import heston_pdf_and_volatility, create_plot_return_underlying_distribution,\
    create_implied_volatility_plot
from flask import render_template, request, redirect, url_for
from forms import ComputeForm
import numpy as np
from db_models import db, User, Compute
from flask_login import LoginManager, current_user, \
    login_user, logout_user, login_required
from app import app
from sqlalchemy import desc
import json

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(user_id)


@app.route('/', methods=['GET', 'POST'])
def index():
    user = current_user
    form = ComputeForm(request.form)

    returns = None
    heston_pdf = None
    strike = None
    implied_volatility = None

    plot_implied_volatility = None
    plot_return_underlying_distribution = None

    if request.method == "POST":
        if form.validate():
            heston_pdf, returns, implied_volatility, strike = \
                heston_pdf_and_volatility(form.price.data, form.strike_min.data, form.strike_max.data, form.time.data,
                                          form.volatility_t0.data, form.chi.data, form.lam.data, form.rho.data,
                                          form.volatility_hat.data, form.mu.data, form.risk_free.data,
                                          form.dividend_yield.data, form.call_put.data)

            plot_return_underlying_distribution = \
                create_plot_return_underlying_distribution(returns, heston_pdf)

            plot_implied_volatility = create_implied_volatility_plot(strike, implied_volatility, form.price.data)

        if user.is_authenticated:  # store data in db
            object = Compute()
            form.populate_obj(object)

            # json.dumps return a array string
            # json.loads convert from string to array

            object.heston_pdf = json.dumps(heston_pdf)
            object.returns = json.dumps(returns.tolist())
            object.price = form.price.data
            object.strike = json.dumps(strike.tolist())
            object.implied_volatility = json.dumps(implied_volatility.tolist())

            object.user = user
            db.session.add(object)
            db.session.commit()
    else:
        if user.is_authenticated:  # user authenticated, store the data
            if user.Compute.count() > 0:
                instance = user.Compute.order_by(desc('id')).first()
                form = populate_form_from_instance(instance)

                heston_pdf = json.loads(instance.heston_pdf)
                returns = np.array(json.loads(instance.returns))
                price = instance.price
                strike = np.array(json.loads(instance.strike))
                implied_volatility = np.array(json.loads(instance.implied_volatility))

                plot_return_underlying_distribution = \
                    create_plot_return_underlying_distribution(returns, heston_pdf)

                plot_implied_volatility = create_implied_volatility_plot(strike, implied_volatility, price)

    return render_template("view_bootstrap.html", form=form, user=user,
                           plot_return_underlying_distribution=plot_return_underlying_distribution,
                           plot_implied_volatility=plot_implied_volatility)


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
            heston_pdf = json.loads(instance.heston_pdf)
            returns = np.array(json.loads(instance.returns))
            price = instance.price
            strike = np.array(json.loads(instance.strike))
            implied_volatility = np.array(json.loads(instance.implied_volatility))

            plot_return_underlying_distribution = \
                create_plot_return_underlying_distribution(returns, heston_pdf)

            plot_implied_volatility = create_implied_volatility_plot(strike, implied_volatility, price)

            data.append({'form': form, 'id': id,
                         'plot_return_underlying_distribution': plot_return_underlying_distribution,
                         'plot_implied_volatility': plot_implied_volatility })

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
