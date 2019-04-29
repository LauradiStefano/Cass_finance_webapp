import os
from compute import find_parameters, compute_shimko_table, compute_index_underlying_cdf, \
    compute_index_underlying_distribution, compute_returns_cdf, kolmogorov_smirnov_test
from compute import create_implied_volatility_plot, create_plot_index_underlying_distribution, \
    create_plot_return_underlying_distribution, create_plot_price_cdf, create_plot_return_cdf
from flask import render_template, request, redirect, url_for
from forms import ComputeForm
from db_models import db, User, Compute
from flask_login import LoginManager, current_user, \
    login_user, logout_user, login_required
from app import app
import json
import numpy as np
from sqlalchemy import desc

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(user_id)


@app.route('/', methods=['GET', 'POST'])
def index():
    user = current_user
    form = ComputeForm(request.form)

    a0 = None
    a1 = None
    a2 = None
    strike = None
    implied_volatility = None
    volatility = None

    st = None
    pdf = None
    pdf_returns = None
    area_prices = None
    expected_price = None
    sigma2_price = None
    skewness_prices = None
    kurtosis_prices = None
    skewness_prices_log_n = None
    kurtosis_prices_log_n = None
    area_returns = None
    m1_returns = None
    m2_returns = None
    skewness_log_returns = None
    kurtosis_log_returns = None
    pdf_bench_log_prices = None
    pdf_bench_norm_returns = None
    ret_t = None
    skewness_normal = None
    kurtosis_normal = None
    cdf_prices = None
    cdf_returns = None
    cdf_bench_log_prices = None
    cdf_bench_norm_returns = None
    statistic_prices = None
    statistic_returns = None
    pvalue_prices = None
    pvalue_returns = None

    plot_implied_volatility = None
    plot_index_distribution = None
    plot_return_distribution = None
    plot_index_cdf = None
    plot_return_cdf = None

    if request.method == "POST":
        if form.validate():
            a0, a1, a2, strike, implied_volatility, volatility = \
                find_parameters(form.strike_min.data, form.strike_atm.data, form.strike_max.data,
                                form.volatility_min.data, form.volatility_atm.data, form.volatility_max.data)

            pdf_returns, area_prices, expected_price, sigma2_price, skewness_prices, kurtosis_prices, \
            skewness_prices_log_n, kurtosis_prices_log_n, area_returns, m1_returns, m2_returns, \
            skewness_log_returns, kurtosis_log_returns, pdf_bench_log_prices, pdf_bench_norm_returns, ret_t, \
            skewness_normal, kurtosis_normal, std_deviation_log_ret, sigma2, mu = \
                compute_shimko_table(a0, a1, a2, form.price.data, form.risk_free.data, form.div_yield.data,
                                     form.time.data, form.strike_min.data, form.strike_max.data)

            statistic_prices, pvalue_prices, statistic_returns, pvalue_returns = \
                kolmogorov_smirnov_test(a0, a1, a2, form.price.data, form.risk_free.data, form.div_yield.data,
                                        form.time.data, form.strike_min.data, form.strike_max.data, expected_price,
                                        sigma2, ret_t, mu, m1_returns, std_deviation_log_ret)

            plot_implied_volatility = create_implied_volatility_plot(strike, implied_volatility, form.price.data,
                                                                     form.strike_min.data, form.strike_atm.data,
                                                                     form.strike_max.data, volatility, a0, a1, a2)

            plot_return_distribution = create_plot_return_underlying_distribution(ret_t, pdf_returns,
                                                                                  pdf_bench_norm_returns)

            if '0' in form.plot_choice.data:
                st, pdf, pdf_bench_log_prices = \
                    compute_index_underlying_distribution(a0, a1, a2, form.price.data, form.risk_free.data,
                                                          form.div_yield.data, form.time.data, form.strike_min.data,
                                                          form.strike_max.data, expected_price, sigma2, mu)

                plot_index_distribution = create_plot_index_underlying_distribution(st, pdf, pdf_bench_log_prices,
                                                                                    form.price.data,
                                                                                    form.strike_min.data,
                                                                                    form.strike_max.data)
            if '1' in form.plot_choice.data:
                cdf_prices, cdf_bench_log_prices, st = \
                    compute_index_underlying_cdf(a0, a1, a2, form.price.data, form.risk_free.data, form.div_yield.data,
                                                 form.time.data, form.strike_min.data, form.strike_max.data,
                                                 expected_price, sigma2, mu)

                plot_index_cdf = create_plot_price_cdf(st, cdf_prices, cdf_bench_log_prices, form.strike_min.data,
                                                       form.strike_max.data)

            if '2' in form.plot_choice.data:
                ret_t, cdf_returns, cdf_bench_norm_returns = \
                    compute_returns_cdf(a0, a1, a2, form.price.data, form.risk_free.data, form.div_yield.data,
                                        form.time.data, form.strike_min.data, form.strike_max.data, m1_returns,
                                        std_deviation_log_ret, ret_t)

                plot_return_cdf = create_plot_return_cdf(ret_t, cdf_returns, cdf_bench_norm_returns)

        if user.is_authenticated:  # store data in db
            object = Compute()
            form.populate_obj(object)

            # json.dumps return a array string
            # json.loads convert from string to array

            object.a0 = a0
            object.a1 = a1
            object.a2 = a2
            object.strike = json.dumps(strike.tolist())
            object.implied_volatility = json.dumps(implied_volatility)
            object.strike_min = form.strike_min.data
            object.strike_atm = form.strike_atm.data
            object.strike_max = form.strike_max.data
            object.volatility = json.dumps(volatility)
            object.pdf_returns = json.dumps(pdf_returns)
            object.area_prices = area_prices
            object.expected_prices = expected_price
            object.sigma2_price = sigma2_price
            object.skewness_prices = skewness_prices
            object.kurtosis_prices = kurtosis_prices
            object.skewness_prices_log_n = skewness_prices_log_n
            object.kurtosis_prices_log_n = kurtosis_prices_log_n
            object.area_returns = area_returns
            object.m1_returns = m1_returns
            object.m2_returns = m2_returns
            object.skewness_log_returns = skewness_log_returns
            object.kurtosis_log_returns = kurtosis_log_returns
            object.pdf_bench_norm_returns = json.dumps(pdf_bench_norm_returns)
            object.price = form.price.data
            object.ret_t = json.dumps(ret_t.tolist())
            object.skewness_normal = skewness_normal
            object.kurtosis_normal = kurtosis_normal
            object.statistic_prices = statistic_prices
            object.statistic_returns = statistic_returns
            object.pvalue_prices = pvalue_prices
            object.pvalue_returns = pvalue_returns

            if st is not None:
                object.st = json.dumps(st.tolist())
                object.pdf = json.dumps(pdf)
                object.pdf_bench_log_prices = json.dumps(pdf_bench_log_prices)
                object.cdf_prices = json.dumps(cdf_prices)
                object.cdf_returns = json.dumps(cdf_returns)
                object.cdf_bench_log_prices = json.dumps(cdf_bench_log_prices)
                object.cdf_bench_norm_returns = json.dumps(cdf_bench_norm_returns)

            object.plot_choice = json.dumps(form.plot_choice.data)

            object.user = user
            db.session.add(object)
            db.session.commit()
    else:
        if user.is_authenticated:  # user authenticated, store the data
            if user.Compute.count() > 0:
                instance = user.Compute.order_by(desc('id')).first()  # decreasing order db, take the last data saved
                form = populate_form_from_instance(instance)

                a0 = instance.a0
                a1 = instance.a1
                a2 = instance.a2
                strike = np.array(json.loads(instance.strike))
                implied_volatility = json.loads(instance.implied_volatility)
                strike_min = instance.strike_min
                strike_atm = instance.strike_atm
                strike_max = instance.strike_max
                volatility = json.loads(instance.volatility)
                pdf_returns = json.loads(instance.pdf_returns)
                area_prices = instance.area_prices
                expected_price = instance.expected_price
                sigma2_price = instance.sigma2_price
                skewness_prices = instance.skewness_prices
                kurtosis_prices = instance.kurtosis_prices
                skewness_prices_log_n = instance.skewness_prices_log_n
                kurtosis_prices_log_n = instance.kurtosis_prices_log_n
                area_returns = instance.area_returns
                m1_returns = instance.m1_returns
                m2_returns = instance.m2_returns
                skewness_log_returns = instance.skewness_log_returns
                kurtosis_log_returns = instance.kurtosis_log_returns
                pdf_bench_norm_returns = json.loads(instance.pdf_bench_norm_returns)
                price = instance.price
                ret_t = np.array(json.loads(instance.ret_t))
                skewness_normal = instance.skewness_normal
                kurtosis_normal = instance.kurtosis_normal
                statistic_prices = instance.statistic_prices
                statistic_returns = instance.statistic_returns
                pvalue_prices = instance.pvalue_prices
                pvalue_returns = instance.pvalue_returns

                plot_choice = json.loads(instance.plot_choice)

                if instance.st is not None:

                    st = np.array(json.loads(instance.st))
                    pdf = json.loads(instance.pdf)
                    pdf_bench_log_prices = json.loads(instance.pdf_bench_log_prices)
                    cdf_prices = json.loads(instance.cdf_prices)
                    cdf_returns = json.loads(instance.cdf_returns)
                    cdf_bench_norm_returns = json.loads(instance.cdf_bench_norm_returns)
                    cdf_bench_log_prices = json.loads(instance.cdf_bench_log_prices)

                    if '0' in plot_choice:
                        plot_index_distribution = create_plot_index_underlying_distribution(st, pdf,
                                                                                            pdf_bench_log_prices,
                                                                                            price, strike_min,
                                                                                            strike_max)

                    if '1' in plot_choice:
                        plot_index_cdf = create_plot_price_cdf(st, cdf_prices, cdf_bench_log_prices, strike_min,
                                                               strike_max)

                    if '2' in plot_choice:
                        plot_return_cdf = create_plot_return_cdf(ret_t, cdf_returns, cdf_bench_norm_returns)

                plot_implied_volatility = create_implied_volatility_plot(strike, implied_volatility, price, strike_min,
                                                                         strike_atm, strike_max, volatility, a0, a1, a2)

                plot_return_distribution = create_plot_return_underlying_distribution(ret_t, pdf_returns,
                                                                                      pdf_bench_norm_returns)

    a0 = round(a0, 8) if a0 is not None else None
    a1 = round(a1, 8) if a1 is not None else None
    a2 = round(a2, 10) if a2 is not None else None

    area_prices = round(area_prices, 4) if area_prices is not None else None
    expected_price = round(expected_price, 4) if expected_price is not None else None
    sigma2_price = round(sigma2_price, 4) if sigma2_price is not None else None
    skewness_prices = round(skewness_prices, 4) if skewness_prices is not None else None
    kurtosis_prices = round(kurtosis_prices, 4) if kurtosis_prices is not None else None
    skewness_prices_log_n = round(skewness_prices_log_n, 4) if skewness_prices_log_n is not None else None
    kurtosis_prices_log_n = round(kurtosis_prices_log_n, 4) if kurtosis_prices_log_n is not None else None
    area_returns = round(area_returns, 4) if area_returns is not None else None
    m1_returns = round(m1_returns, 4) if m1_returns is not None else None
    m2_returns = round(m2_returns, 4) if m2_returns is not None else None
    skewness_log_returns = round(skewness_log_returns, 4) if skewness_log_returns is not None else None
    kurtosis_log_returns = round(kurtosis_log_returns, 4) if kurtosis_log_returns is not None else None
    skewness_normal = round(skewness_normal, 4) if skewness_normal is not None else None
    kurtosis_normal = round(kurtosis_normal, 4) if kurtosis_normal is not None else None
    statistic_prices = round(statistic_prices, 4) if statistic_prices is not None else None
    statistic_returns = round(statistic_returns, 4) if statistic_returns is not None else None
    pvalue_prices = round(pvalue_prices, 4) if pvalue_prices is not None else None
    pvalue_returns = round(pvalue_returns, 4) if pvalue_returns is not None else None

    return render_template("view_bootstrap.html", form=form, a0=a0, a1=a1, a2=a2, area_prices=area_prices,
                           expected_price=expected_price, sigma2_price=sigma2_price, skewness_prices=skewness_prices,
                           kurtosis_prices=kurtosis_prices, skewness_prices_log_n=skewness_prices_log_n,
                           kurtosis_prices_log_n=kurtosis_prices_log_n, area_returns=area_returns,
                           m1_returns=m1_returns, m2_returns=m2_returns, skewness_log_returns=skewness_log_returns,
                           kurtosis_log_returns=kurtosis_log_returns, skewness_normal=skewness_normal,
                           kurtosis_normal=kurtosis_normal, statistic_prices=statistic_prices,
                           statistic_returns=statistic_returns, pvalue_prices=pvalue_prices,
                           pvalue_returns=pvalue_returns, user=user, plot_implied_volatility=plot_implied_volatility,
                           plot_index_distribution=plot_index_distribution, plot_index_cdf=plot_index_cdf,
                           plot_return_distribution=plot_return_distribution, plot_return_cdf=plot_return_cdf)


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
            a0 = instance.a0
            a1 = instance.a1
            a2 = instance.a2
            strike = json.loads(instance.strike)
            implied_volatility = json.loads(instance.implied_volatility)
            strike_min = instance.strike_min
            strike_atm = instance.strike_atm
            strike_max = instance.strike_max
            volatility = json.loads(instance.volatility)
            pdf_returns = json.loads(instance.pdf_returns)
            area_prices = instance.area_prices
            expected_prices = instance.expected_price
            sigma2_price = instance.sigma2_price
            skewness_prices = instance.skewness_prices
            kurtosis_prices = instance.kurtosis_prices
            skewness_prices_log_n = instance.skewness_prices_log_n
            kurtosis_prices_log_n = instance.kurtosis_prices_log_n
            area_returns = instance.area_returns
            m1_returns = instance.m1_returns
            m2_returns = instance.m2_returns
            skewness_log_returns = instance.skewness_log_returns
            kurtosis_log_returns = instance.kurtosis_log_returns
            pdf_bench_norm_returns = json.loads(instance.pdf_bench_norm_returns)
            price = instance.price
            ret_t = json.loads(instance.ret_t)
            skewness_normal = instance.skewness_normal
            kurtosis_normal = instance.kurtosis_normal
            statistic_prices = instance.statistic_prices
            statistic_returns = instance.statistic_returns
            pvalue_prices = instance.pvalue_prices
            pvalue_returns = instance.pvalue_returns

            plot_choice = json.loads(instance.plot_choice)

            plot_index_distribution = None
            plot_index_cdf = None
            plot_return_cdf = None

            if instance.st is not None:

                st = np.array(json.loads(instance.st))
                pdf = json.loads(instance.pdf)
                pdf_bench_log_prices = json.loads(instance.pdf_bench_log_prices)
                cdf_prices = json.loads(instance.cdf_prices)
                cdf_returns = json.loads(instance.cdf_returns)
                cdf_bench_norm_returns = json.loads(instance.cdf_bench_norm_returns)
                cdf_bench_log_prices = json.loads(instance.cdf_bench_log_prices)

                if '0' in plot_choice:
                    plot_index_distribution = create_plot_index_underlying_distribution(st, pdf, pdf_bench_log_prices,
                                                                                        price, strike_min, strike_max)
                if '1' in plot_choice:
                    plot_index_cdf = create_plot_price_cdf(st, cdf_prices, cdf_bench_log_prices, strike_min, strike_max)

                if '2' in plot_choice:
                    plot_return_cdf = create_plot_return_cdf(ret_t, cdf_returns, cdf_bench_norm_returns)

            plot_implied_volatility = create_implied_volatility_plot(strike, implied_volatility, price, strike_min,
                                                                     strike_atm, strike_max, volatility, a0, a1, a2)

            plot_return_distribution = create_plot_return_underlying_distribution(ret_t, pdf_returns,
                                                                                  pdf_bench_norm_returns)
            a0 = round(a0, 8) if a0 is not None else None
            a1 = round(a1, 8) if a1 is not None else None
            a2 = round(a2, 10) if a2 is not None else None

            data.append({'form': form, 'id': id, 'a0': a0, 'a1': a1, 'a2': a2, 'area_prices': area_prices,
                         'expected_prices': expected_prices, 'sigma2_price': sigma2_price,
                         'skewness_prices': skewness_prices, 'kurtosis_prices': kurtosis_prices,
                         'skewness_prices_log_n': skewness_prices_log_n, 'kurtosis_prices_log_n': kurtosis_prices_log_n,
                         'area_returns': area_returns, 'm1_returns': m1_returns, 'm2_returns': m2_returns,
                         'skewness_log_returns': skewness_log_returns, 'kurtosis_log_returns': kurtosis_log_returns,
                         'ret_t': ret_t, 'skewness_normal': skewness_normal, 'statistic_prices': statistic_prices,
                         'statistic_returns': statistic_returns, 'pvalue_prices': pvalue_prices,
                         'pvalue_returns': pvalue_returns, 'kurtosis_normal': kurtosis_normal,
                         'plot_implied_volatility': plot_implied_volatility,
                         'plot_index_distribution': plot_index_distribution, 'plot_return_cdf': plot_return_cdf,
                         'plot_return_distribution': plot_return_distribution, 'plot_index_cdf': plot_index_cdf})

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
