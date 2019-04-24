import os
from compute import upload_input, volatility_term_structure, compute_shimko_table, compute_underlying_distribution, \
    compute_underlying_cdf, compute_returns_cdf
from compute import create_implied_volatility_plot, create_plot_return_underlying_distribution, \
    create_plot_index_underlying_distribution, create_plot_price_cdf, create_plot_return_cdf
from flask import render_template, request, redirect, url_for
from forms import ComputeForm
from db_models import db, User, Compute
from flask_login import LoginManager, current_user, \
    login_user, logout_user, login_required
from app import app
import json
import numpy as np
from werkzeug.utils import secure_filename
from app import allowed_file

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(user_id)


@app.route('/', methods=['GET', 'POST'])
def index():
    # form = ComputeForm(CombinedMultiDict((request.form, request.files)))
    form = ComputeForm(request.form)
    user = current_user

    file_name = None

    strike_data = None
    put_market = None
    call_market = None

    a0 = None
    a1 = None
    a2 = None
    strike_plot = None
    implied_volatility = None
    strike_min = None
    strike_max = None
    div_yield = None
    risk_free = None
    time = None

    st = None
    pdf = None
    pdf_returns = None
    area_prices = None
    expected_price = None
    sigma2_price = None
    mu = None
    std_deviation_log_ret = None
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
    price = None
    volatility_time = None
    r2 = None
    returns_t = None
    skewness_normal = None
    kurtosis_normal = None
    cdf_prices = None
    cdf_returns = None
    cdf_bench_log_prices = None
    cdf_bench_norm_returns = None
    sigma2 = None
    plot_choice = None

    plot_implied_volatility = None
    plot_index_distribution = None
    plot_return_distribution = None
    plot_index_cdf = None
    plot_return_cdf = None

    if request.method == "POST" and request.files and form.validate():

        file = request.files[form.file_name.name]
        if file and allowed_file(file.filename):
            file_name = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file_name))

        file_name, strike_data, call_market, put_market, time = upload_input(file_name)

        a0, a1, a2, strike_plot, implied_volatility, strike_min, strike_max, div_yield, risk_free, volatility_time, r2 \
            = volatility_term_structure(form.price.data, form.call_put_flag.data, time, call_market, put_market,
                                        strike_data)

        pdf_returns, area_prices, expected_price, sigma2_price, skewness_prices, kurtosis_prices, \
        skewness_prices_log_n, kurtosis_prices_log_n, area_returns, m1_returns, m2_returns, skewness_log_returns, \
        kurtosis_log_returns, pdf_bench_norm_returns, returns_t, skewness_normal, kurtosis_normal, mu, \
        std_deviation_log_ret, sigma2 = \
            compute_shimko_table(a0, a1, a2, form.price.data, risk_free, div_yield, time, strike_min, strike_max)

        plot_implied_volatility = create_implied_volatility_plot(strike_plot, implied_volatility, form.price.data,
                                                                 strike_min, strike_max, strike_data, volatility_time)

        plot_return_distribution = create_plot_return_underlying_distribution(returns_t, pdf_returns,
                                                                              pdf_bench_norm_returns)

        if '0' in form.plot_choice.data:
            st, pdf, pdf_bench_log_prices = compute_underlying_distribution(a0, a1, a2, form.price.data, risk_free,
                                                                            div_yield, time, strike_min, strike_max,
                                                                            expected_price, sigma2, mu)

            plot_index_distribution = create_plot_index_underlying_distribution(st, pdf, pdf_bench_log_prices,
                                                                                form.price.data, strike_min, strike_max)

        if '1' in form.plot_choice.data:
            cdf_prices, cdf_bench_log_prices, st = compute_underlying_cdf(a0, a1, a2, form.price.data, risk_free,
                                                                          div_yield, time, strike_min, strike_max,
                                                                          expected_price, sigma2, mu)

            plot_index_cdf = create_plot_price_cdf(st, cdf_prices, cdf_bench_log_prices, strike_min, strike_max)

        if '2' in form.plot_choice.data:
            returns_t, cdf_returns, cdf_bench_norm_returns = compute_returns_cdf(a0, a1, a2, form.price.data, risk_free,
                                                                                 div_yield, time, strike_min,
                                                                                 strike_max, m1_returns,
                                                                                 std_deviation_log_ret, returns_t)

            plot_return_cdf = create_plot_return_cdf(returns_t, cdf_returns, cdf_bench_norm_returns)

        if user.is_authenticated:
            object = Compute()
            form.populate_obj(object)

            # json.dumps restiuisce un stringa di array
            # json.loads converte da stringa ad array

            object.filename = file_name
            object.strike_data = json.dumps(strike_data)
            object.put_market = json.dumps(put_market)
            object.call_market = json.dumps(call_market)
            object.a0 = a0
            object.a1 = a1
            object.a2 = a2
            object.strike_plot = json.dumps(strike_plot.tolist())
            object.implied_volatility = json.dumps(implied_volatility.tolist())
            object.strike_min = strike_min
            object.strike_max = strike_max
            object.div_yield = div_yield
            object.risk_free = risk_free
            object.time = time

            if st is not None:
                object.st = json.dumps(st.tolist())
                object.pdf = json.dumps(pdf)
                object.pdf_returns = json.dumps(pdf_returns)
                object.area_prices = area_prices
                object.expected_price = expected_price
                object.sigma2_price = sigma2_price
                object.mu = mu
                object.std_deviation_log_ret = std_deviation_log_ret
                object.skewness_prices = skewness_prices
                object.kurtosis_prices = kurtosis_prices
                object.skewness_prices_log_n = skewness_prices_log_n
                object.kurtosis_prices_log_n = kurtosis_prices_log_n
                object.area_returns = area_returns
                object.m1_returns = m1_returns
                object.m2_returns = m2_returns
                object.skewness_log_returns = skewness_log_returns
                object.kurtosis_log_returns = kurtosis_log_returns
                object.pdf_bench_log_prices = json.dumps(pdf_bench_log_prices)
                object.pdf_bench_norm_returns = json.dumps(pdf_bench_norm_returns)
                object.price = form.price.data
                object.volatility_time = json.dumps(volatility_time.tolist())
                object.r2 = r2
                object.returns_t = json.dumps(returns_t.tolist())
                object.skewness_normal = skewness_normal
                object.kurtosis_normal = kurtosis_normal
                object.cdf_prices = json.dumps(cdf_prices)
                object.cdf_returns = json.dumps(cdf_returns)
                object.cdf_bench_log_prices = json.dumps(cdf_bench_log_prices)
                object.cdf_bench_norm_returns = json.dumps(cdf_bench_norm_returns)
                object.sigma2 = sigma2
                object.plot_choice = json.dumps(form.plot_choice.data)

                object.user = user
                db.session.add(object)
                db.session.commit()
    else:
        if user.is_authenticated:
            if user.Compute.count() > 0:
                instance = user.Compute.order_by('-id').first()
                form = populate_form_from_instance(instance)

                file_name = instance.file_name
                strike_data = json.loads(instance.strike_data)
                call_market = json.loads(instance.call_market)
                put_market = json.loads(instance.put_market)

                a0 = instance.a0
                a1 = instance.a1
                a2 = instance.a2
                strike_plot = np.array(json.loads(instance.strike_plot))
                implied_volatility = np.array(json.loads(instance.implied_volatility))
                strike_min = instance.strike_min
                strike_max = instance.strike_max
                div_yield = instance.div_yield
                risk_free = instance.risk_free
                time = instance.time

                st = np.array(json.loads(instance.st))
                pdf = json.loads(instance.pdf)
                pdf_returns = json.loads(instance.pdf_returns)
                area_prices = instance.area_prices
                expected_price = instance.expected_price
                sigma2_price = instance.sigma2_price
                mu = instance.mu
                std_deviation_log_ret = instance.std_deviation_log_ret
                skewness_prices = instance.skewness_prices
                kurtosis_prices = instance.kurtosis_prices
                skewness_prices_log_n = instance.skewness_prices_log_n
                kurtosis_prices_log_n = instance.kurtosis_prices_log_n
                area_returns = instance.area_returns
                m1_returns = instance.m1_returns
                m2_returns = instance.m2_returns
                skewness_log_returns = instance.skewness_log_returns
                kurtosis_log_returns = instance.kurtosis_log_returns
                pdf_bench_log_prices = json.loads(instance.pdf_bench_log_prices)
                pdf_bench_norm_returns = json.loads(instance.pdf_bench_norm_returns)
                price = instance.price
                volatility_time = np.array(json.loads(instance.volatility_time))
                r2 = instance.r2
                returns_t = np.array(json.loads(instance.returns_t))
                skewness_normal = instance.skewness_normal
                kurtosis_normal = instance.kurtosis_normal
                cdf_prices = json.loads(instance.cdf_prices)
                cdf_returns = json.loads(instance.cdf_returns)
                cdf_bench_log_prices = json.loads(instance.cdf_bench_log_prices)
                cdf_bench_norm_returns = json.loads(instance.cdf_bench_norm_returns)
                sigma2 = instance.sigma2
                plot_choice = json.loads(instance.plot_choice)

                plot_implied_volatility = create_implied_volatility_plot(strike_plot, implied_volatility, price,
                                                                         strike_min, strike_max, strike_data,
                                                                         volatility_time)

                plot_return_distribution = create_plot_return_underlying_distribution(returns_t, pdf_returns,
                                                                                      pdf_bench_norm_returns)

                if '0' in plot_choice:
                    plot_index_distribution = create_plot_index_underlying_distribution(st, pdf, pdf_bench_log_prices,
                                                                                        price, strike_min, strike_max)
                if '1' in plot_choice:
                    plot_index_cdf = create_plot_price_cdf(st, cdf_prices, cdf_bench_log_prices, strike_min, strike_max)

                if '2' in plot_choice:
                    plot_return_cdf = create_plot_return_cdf(returns_t, cdf_returns, cdf_bench_norm_returns)

    a0 = round(a0, 8) if a0 is not None else None
    a1 = round(a1, 8) if a1 is not None else None
    a2 = round(a2, 10) if a2 is not None else None
    r2 = round(r2, 8) if r2 is not None else None
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

    return render_template("view_bootstrap.html", form=form, user=user, file_name=file_name, k=strike_data,
                           put_market=put_market, call_market=call_market, a0=a0, a1=a1, a2=a2, strike=strike_plot,
                           implied_volatility=implied_volatility, strike_min=strike_min, strike_max=strike_max,
                           div_yield=div_yield, risk_free=risk_free, time=time, st=st, pdf=pdf, pdf_returns=pdf_returns,
                           area_prices=area_prices, expected_price=expected_price, sigma2_price=sigma2_price, mu=mu,
                           stand_deviation_log_ret=std_deviation_log_ret, skewness_prices=skewness_prices,
                           kurtosis_prices=kurtosis_prices, skewness_prices_log_n=skewness_prices_log_n,
                           kurtosis_prices_log_n=kurtosis_prices_log_n, area_returns=area_returns,
                           m1_returns=m1_returns, m2_returns=m2_returns, skewness_log_returns=skewness_log_returns,
                           kurtosis_log_returns=kurtosis_log_returns, pdf_bench_log_prices=pdf_bench_log_prices,
                           pdf_bench_norm_returns=pdf_bench_norm_returns, s0=price, vol_t=volatility_time, r2=r2,
                           returns_t=returns_t, skewness_normal=skewness_normal, cdf_prices=cdf_prices,
                           cdf_returns=cdf_returns, cdf_bench_log_prices=cdf_bench_log_prices,
                           cdf_bench_norm_returns=cdf_bench_norm_returns, kurtosis_normal=kurtosis_normal, sg2=sigma2,
                           plot_choice=plot_choice, plot_implied_volatility=plot_implied_volatility,
                           plot_index_distribution=plot_index_distribution,
                           plot_return_distribution=plot_return_distribution, plot_index_cdf=plot_index_cdf,
                           plot_return_cdf=plot_return_cdf)


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
    from forms import LoginForm
    form = LoginForm(request.form)
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

            id = instance.id
            file_name = instance.file_name
            strike_data = json.loads(instance.strike_data)
            call_market = json.loads(instance.call_market)
            put_market = json.loads(instance.put_market)

            a0 = instance.a0
            a1 = instance.a1
            a2 = instance.a2
            strike_plot = np.array(json.loads(instance.strike_plot))
            implied_volatility = np.array(json.loads(instance.implied_volatility))
            strike_min = instance.strike_min
            strike_max = instance.strike_max
            div_yield = instance.div_yield
            risk_free = instance.risk_free
            time = instance.time

            st = np.array(json.loads(instance.st))
            pdf = json.loads(instance.pdf)
            pdf_returns = json.loads(instance.pdf_returns)
            area_prices = instance.area_prices
            expected_price = instance.expected_price
            sigma2_price = instance.sigma2_price
            mu = instance.mu
            std_deviation_log_ret = instance.std_deviation_log_ret
            skewness_prices = instance.skewness_prices
            kurtosis_prices = instance.kurtosis_prices
            skewness_prices_log_n = instance.skewness_prices_log_n
            kurtosis_prices_log_n = instance.kurtosis_prices_log_n
            area_returns = instance.area_returns
            m1_returns = instance.m1_returns
            m2_returns = instance.m2_returns
            skewness_log_returns = instance.skewness_log_returns
            kurtosis_log_returns = instance.kurtosis_log_returns
            pdf_bench_log_prices = json.loads(instance.pdf_bench_log_prices)
            pdf_bench_norm_returns = json.loads(instance.pdf_bench_norm_returns)
            price = instance.price
            volatility_time = np.array(json.loads(instance.volatility_time))
            r2 = instance.r2
            returns_t = np.array(json.loads(instance.returns_t))
            skewness_normal = instance.skewness_normal
            kurtosis_normal = instance.kurtosis_normal
            cdf_prices = json.loads(instance.cdf_prices)
            cdf_returns = json.loads(instance.cdf_returns)
            cdf_bench_log_prices = json.loads(instance.cdf_bench_log_prices)
            cdf_bench_norm_returns = json.loads(instance.cdf_bench_norm_returns)
            sg2 = instance.sigma2
            plot_choice = json.loads(instance.plot_choice)

            plot_implied_volatility = create_implied_volatility_plot(strike_plot, implied_volatility, price, strike_min,
                                                                     strike_max, strike_data, volatility_time)

            plot_return_distribution = create_plot_return_underlying_distribution(returns_t, pdf_returns,
                                                                                  pdf_bench_norm_returns)

            plot_index_distribution = None
            plot_index_cdf = None
            plot_return_cdf = None

            if '0' in plot_choice:
                plot_index_distribution = create_plot_index_underlying_distribution(st, pdf, pdf_bench_log_prices,
                                                                                    price,
                                                                                    strike_min, strike_max)
            if '1' in plot_choice:
                plot_index_cdf = create_plot_price_cdf(st, cdf_prices, cdf_bench_log_prices, strike_min, strike_max)

            if '2' in plot_choice:
                plot_return_cdf = create_plot_return_cdf(returns_t, cdf_returns, cdf_bench_norm_returns)

            a0 = round(a0, 8) if a0 is not None else None
            a1 = round(a1, 8) if a1 is not None else None
            a2 = round(a2, 10) if a2 is not None else None
            r2 = round(r2, 8) if r2 is not None else None

            data.append({'form': form, 'id': id, 'file_name': file_name, 'strike_data': strike_data,
                         'call_market': call_market, 'put_market': put_market, 'a0': a0, 'a1': a1, 'a2': a2,
                         'strike_plot': strike_plot, 'implied_volatility': implied_volatility, 'strike_min': strike_min,
                         'strike_max': strike_max, 'div_yield': div_yield, 'risk_free': risk_free, 'time': time,
                         'st': st, 'pdf': pdf, 'pdf_returns': pdf_returns, 'area_prices': area_prices,
                         'expected_price': expected_price, 'sigma2_price': sigma2_price, 'mu': mu,
                         'std_deviation_log_ret': std_deviation_log_ret, 'skewness_prices': skewness_prices,
                         'kurtosis_prices': kurtosis_prices, 'skewness_prices_log_n': skewness_prices_log_n,
                         'kurtosis_prices_log_n': kurtosis_prices_log_n, 'area_returns': area_returns,
                         'm1_returns': m1_returns, 'm2_returns': m2_returns,
                         'skewness_log_returns': skewness_log_returns, 'kurtosis_log_returns': kurtosis_log_returns,
                         'pdf_bench_log_prices': pdf_bench_log_prices, 'pdf_bench_norm_returns': pdf_bench_norm_returns,
                         'price': price, 'volatility_time': volatility_time, 'r2': r2, 'returns_t': returns_t,
                         'skewness_normal': skewness_normal, 'kurtosis_normal': kurtosis_normal,
                         'cdf_prices': cdf_prices, 'cdf_returns': cdf_returns,
                         'cdf_bench_log_prices': cdf_bench_log_prices, 'cdf_bench_norm_returns': cdf_bench_norm_returns,
                         'sg2': sg2, 'plot_choice': plot_choice, 'plot_implied_volatility': plot_implied_volatility,
                         'plot_index_distribution': plot_index_distribution,
                         'plot_return_distribution': plot_return_distribution, 'plot_index_cdf': plot_index_cdf,
                         'plot_return_cdf': plot_return_cdf})

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
