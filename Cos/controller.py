import os
from compute import cos_pdf_underlying_asset, create_plot_return_underlying_distribution, compute_option_prices, \
    compute_implied_volatilites, create_implied_volatility_plot, select_parameters
from flask import render_template, request, redirect, url_for
from forms import ComputeForm
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

    pdf_underlying_asset = None
    underlying_prices = None
    strike = None
    implied_volatility = None

    plot_implied_volatility = None
    plot_return_underlying_distribution = None

    if request.method == "POST":
        if form.validate():
            parameters = select_parameters(form.type_choice.data, form.mu.data, form.sigma.data, form.kappa.data,
                                           form.theta.data, form.c.data, form.g.data, form.m.data, form.y.data)
            pdf_underlying_asset, underlying_prices = \
                cos_pdf_underlying_asset(form.type_choice.data, parameters, form.time.data)

            option_prices, strike = \
                compute_option_prices(form.type_choice.data, form.call_put.data, form.price.data, form.strike_min.data,
                                      form.strike_max.data, form.risk_free.data, form.dividend_yield.data,
                                      form.time.data, parameters)

            implied_volatility = \
                compute_implied_volatilites(option_prices, form.call_put.data, form.price.data, strike, form.time.data,
                                            form.risk_free.data, form.dividend_yield.data)

            plot_return_underlying_distribution = \
                create_plot_return_underlying_distribution(underlying_prices, pdf_underlying_asset, form.price.data)

            plot_implied_volatility = create_implied_volatility_plot(strike, implied_volatility, form.price.data)

        if user.is_authenticated:  # store data in db
            object = Compute()
            form.populate_obj(object)

            # json.dumps return a array string
            # json.loads convert from string to array

            object.pdf_underlying_asset = json.dumps(pdf_underlying_asset)
            object.underlying_prices = json.dumps(underlying_prices)
            object.price = form.price.data
            object.strike = json.dumps(strike)
            object.implied_volatility = json.dumps(implied_volatility)

            object.user = user
            db.session.add(object)
            db.session.commit()
    else:
        if user.is_authenticated:  # user authenticated, store the data
            if user.Compute.count() > 0:
                instance = user.Compute.order_by(desc('id')).first()
                form = populate_form_from_instance(instance)

                pdf_underlying_asset = json.loads(instance.pdf_underlying_asset)
                underlying_prices = json.loads(instance.underlying_prices)
                price = instance.price
                strike = json.loads(instance.strikes)
                implied_volatility = json.loads(instance.implied_volatilities)

                plot_return_underlying_distribution = create_plot_return_underlying_distribution\
                    (underlying_prices, pdf_underlying_asset, price)

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
        instances = user.Compute.order_by('-id').all()
        for instance in instances:
            form = populate_form_from_instance(instance)

            # page old.html, store the date and the plot (previous simulation)

            id = instance.id
            pdf_underlying_asset = json.loads(instance.pdf_underlying_asset)
            underlying_prices = json.loads(instance.underlying_prices)
            price = instance.price
            strike = json.loads(instance.strikes)
            implied_volatility = json.loads(instance.implied_volatilities)

            plot_return_underlying_distribution = (underlying_prices, pdf_underlying_asset, price)

            plot_implied_volatilities = create_implied_volatility_plot(strike, implied_volatility, price)

            data.append({'form': form, 'id': id,
                         'plot_return_underlying_distribution': plot_return_underlying_distribution,
                         'plot_implied_volatilities': plot_implied_volatilities})

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
