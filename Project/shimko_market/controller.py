import csv
import io
import json
import os

import numpy as np
from flask import redirect, url_for, Response
from sqlalchemy import desc
from werkzeug.utils import secure_filename

from app import allowed_file
from app import app
from db_models import db
from db_models import shimko_market_model as compute
from shimko_market.compute import create_implied_volatility_plot, create_plot_return_underlying_distribution, \
    create_plot_index_underlying_distribution, create_plot_price_cdf, create_plot_return_cdf, upload_input, \
    volatility_term_structure, compute_shimko_table, compute_underlying_distribution, \
    compute_underlying_cdf, compute_returns_cdf, kolmogorov_smirnov_test
from shimko_market.forms import ComputeForm


def controller_shimko_market(user, request):
    form = ComputeForm(request.form)

    file_data = None
    strike_data = None
    put_market = None
    call_market = None
    strike_plot = None
    implied_volatility = None
    strike_min = None
    strike_max = None
    volatility_time = None

    a0 = None
    a1 = None
    a2 = None
    st = None
    pdf = None
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
    pdf_returns = None
    pdf_bench_log_prices = None
    pdf_bench_norm_returns = None
    r2 = None
    skewness_normal = None
    kurtosis_normal = None
    cdf_prices = None
    cdf_returns = None
    cdf_bench_log_prices = None
    cdf_bench_norm_returns = None
    returns_t = None
    statistic_prices = None
    statistic_returns = None
    pvalue_prices = None
    pvalue_returns = None
    risk_free = None
    div_yield = None

    compute_not_allowed = False

    sim_id = None

    plot_implied_volatility = None
    plot_index_distribution = None
    plot_return_distribution = None
    plot_index_cdf = None
    plot_return_cdf = None

    if request.method == "POST":
        if user.is_authenticated:
            if form.validate() and request.files:
                file = request.files[form.file_data.name]

                if file and allowed_file(file.filename):
                    file_data = secure_filename(file.filename)
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], file_data))

                strike_data, call_market, put_market, time = upload_input(file_data)

                a0, a1, a2, strike_plot, implied_volatility, strike_min, strike_max, div_yield, risk_free, volatility_time, r2 \
                    = volatility_term_structure(form.price.data, form.call_put_flag.data, time, call_market, put_market,
                                                strike_data, form.risk_dividend.data, form.risk_free.data,
                                                form.div_yield.data)

                pdf_returns, area_prices, expected_price, sigma2_price, skewness_prices, kurtosis_prices, \
                skewness_prices_log_n, kurtosis_prices_log_n, area_returns, m1_returns, m2_returns, skewness_log_returns, \
                kurtosis_log_returns, pdf_bench_norm_returns, returns_t, skewness_normal, kurtosis_normal, mu, \
                std_deviation_log_ret, sigma2 = \
                    compute_shimko_table(a0, a1, a2, form.price.data, risk_free, div_yield, time, strike_min,
                                         strike_max)

                statistic_prices, pvalue_prices, statistic_returns, pvalue_returns = \
                    kolmogorov_smirnov_test(a0, a1, a2, form.price.data, risk_free, div_yield, time, strike_min,
                                            strike_max,
                                            expected_price, sigma2, returns_t, mu, m1_returns, std_deviation_log_ret)

                plot_implied_volatility = create_implied_volatility_plot(form.call_put_flag.data, strike_plot,
                                                                         implied_volatility, form.price.data,
                                                                         strike_min, strike_max, strike_data,
                                                                         volatility_time)

                plot_return_distribution = create_plot_return_underlying_distribution(returns_t, pdf_returns,
                                                                                      pdf_bench_norm_returns)

                if form.risk_dividend.data == '1':  # interest rate and div yield are implicitly calculated
                    risk_free = risk_free * 100
                    div_yield = div_yield * 100

                    risk_free = round(risk_free, 4) if risk_free is not None else None
                    div_yield = round(div_yield, 4) if div_yield is not None else None
                else:
                    risk_free = form.risk_free.data
                    div_yield = form.div_yield.data

                if '0' in form.plot_choice.data:
                    st, pdf, pdf_bench_log_prices = compute_underlying_distribution(a0, a1, a2, form.price.data,
                                                                                    risk_free,
                                                                                    div_yield, time, strike_min,
                                                                                    strike_max,
                                                                                    expected_price, sigma2, mu)

                    plot_index_distribution = create_plot_index_underlying_distribution(st, pdf, pdf_bench_log_prices,
                                                                                        form.price.data, strike_min,
                                                                                        strike_max)

                if '1' in form.plot_choice.data:
                    cdf_prices, cdf_bench_log_prices, st = compute_underlying_cdf(a0, a1, a2, form.price.data,
                                                                                  risk_free,
                                                                                  div_yield, time, strike_min,
                                                                                  strike_max,
                                                                                  expected_price, sigma2, mu)

                    plot_index_cdf = create_plot_price_cdf(st, cdf_prices, cdf_bench_log_prices, strike_min, strike_max)

                if '2' in form.plot_choice.data:
                    returns_t, cdf_returns, cdf_bench_norm_returns = compute_returns_cdf(a0, a1, a2, form.price.data,
                                                                                         risk_free,
                                                                                         div_yield, time, strike_min,
                                                                                         strike_max, m1_returns,
                                                                                         std_deviation_log_ret,
                                                                                         returns_t)

                    plot_return_cdf = create_plot_return_cdf(returns_t, cdf_returns, cdf_bench_norm_returns)

                if user.is_authenticated:  # store data in db
                    object = compute()
                    form.populate_obj(object)

                    # json.dumps return a array string
                    # json.loads convert from string to array

                    object.strike_data = json.dumps(list(map(int, strike_data)))
                    # map(TIPO, VET)is a function to convert in "TIPO" all elements of VET
                    # list converts the returned object to list
                    # convert the strike elements in integer and to have a list

                    object.put_market = json.dumps(put_market)
                    object.call_market = json.dumps(call_market)
                    object.a0 = a0
                    object.a1 = a1
                    object.a2 = a2
                    object.strike_plot = json.dumps(strike_plot.tolist())
                    object.implied_volatility = json.dumps(implied_volatility.tolist())
                    object.strike_min = strike_min
                    object.strike_max = strike_max
                    object.volatility_time = json.dumps(volatility_time.tolist())
                    object.pdf_returns = json.dumps(pdf_returns)
                    object.area_prices = area_prices
                    object.expected_price = expected_price
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
                    object.r2 = r2
                    object.returns_t = json.dumps(returns_t.tolist())
                    object.skewness_normal = skewness_normal
                    object.kurtosis_normal = kurtosis_normal
                    object.statistic_prices = statistic_prices
                    object.statistic_returns = statistic_returns
                    object.pvalue_prices = pvalue_prices
                    object.pvalue_returns = pvalue_returns
                    object.price = form.price.data
                    object.call_put_flag = form.call_put_flag.data
                    object.risk_dividend = form.risk_dividend.data
                    object.risk_free = risk_free
                    object.div_yield = div_yield

                    if st is not None:  # user chooses the plot
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
                    sim_id = object.id
        else:
            compute_not_allowed = True
    else:
        if user.is_authenticated:  # user authenticated, store the data

            if user.compute_shimko_market.count() > 0:
                instance = user.compute_shimko_market.order_by(
                    desc('id')).first()  # decreasing order db, take the last data saved
                form = populate_form_from_instance(instance)

                sim_id = instance.id
                strike_data = json.loads(instance.strike_data)
                a0 = instance.a0
                a1 = instance.a1
                a2 = instance.a2
                strike_plot = np.array(json.loads(instance.strike_plot))
                implied_volatility = np.array(json.loads(instance.implied_volatility))
                strike_min = instance.strike_min
                strike_max = instance.strike_max
                volatility_time = np.array(json.loads(instance.volatility_time))
                price = instance.price
                call_put_flag = instance.call_put_flag
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
                r2 = instance.r2
                returns_t = np.array(json.loads(instance.returns_t))
                skewness_normal = instance.skewness_normal
                kurtosis_normal = instance.kurtosis_normal
                statistic_prices = instance.statistic_prices
                statistic_returns = instance.statistic_returns
                pvalue_prices = instance.pvalue_prices
                pvalue_returns = instance.pvalue_returns
                plot_choice = json.loads(instance.plot_choice)
                risk_dividend = instance.risk_dividend
                risk_free = instance.risk_free
                div_yield = instance.div_yield

                if risk_dividend == '1':
                    risk_free = round(risk_free, 4) if risk_free is not None else None
                    div_yield = round(div_yield, 4) if div_yield is not None else None

                if instance.st is not None:
                    st = np.array(json.loads(instance.st))
                    pdf = json.loads(instance.pdf)
                    pdf_bench_log_prices = json.loads(instance.pdf_bench_log_prices)
                    cdf_prices = json.loads(instance.cdf_prices)
                    cdf_returns = json.loads(instance.cdf_returns)
                    cdf_bench_log_prices = json.loads(instance.cdf_bench_log_prices)
                    cdf_bench_norm_returns = json.loads(instance.cdf_bench_norm_returns)

                    if '0' in plot_choice:
                        plot_index_distribution = \
                            create_plot_index_underlying_distribution(st, pdf, pdf_bench_log_prices, price, strike_min,
                                                                      strike_max)
                    if '1' in plot_choice:
                        plot_index_cdf = create_plot_price_cdf(st, cdf_prices, cdf_bench_log_prices, strike_min,
                                                               strike_max)

                    if '2' in plot_choice:
                        plot_return_cdf = create_plot_return_cdf(returns_t, cdf_returns, cdf_bench_norm_returns)

                plot_implied_volatility = create_implied_volatility_plot(call_put_flag, strike_plot, implied_volatility,
                                                                         price,
                                                                         strike_min, strike_max, strike_data,
                                                                         volatility_time)

                plot_return_distribution = create_plot_return_underlying_distribution(returns_t, pdf_returns,
                                                                                      pdf_bench_norm_returns)

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
    statistic_prices = round(statistic_prices, 4) if statistic_prices is not None else None
    statistic_returns = round(statistic_returns, 4) if statistic_returns is not None else None
    pvalue_prices = round(pvalue_prices, 4) if pvalue_prices is not None else None
    pvalue_returns = round(pvalue_returns, 4) if pvalue_returns is not None else None

    return {'form': form, 'user': user, 'a0': a0, 'a1': a1, 'a2': a2,
            'area_prices': area_prices, 'expected_price': expected_price, 'sigma2_price': sigma2_price,
            'skewness_prices': skewness_prices, 'kurtosis_prices': kurtosis_prices,
            'skewness_prices_log_n': skewness_prices_log_n, 'kurtosis_prices_log_n': kurtosis_prices_log_n,
            'area_returns': area_returns, 'm1_returns': m1_returns, 'm2_returns': m2_returns,
            'skewness_log_returns': skewness_log_returns, 'kurtosis_log_returns': kurtosis_log_returns,
            'r2': r2, 'skewness_normal': skewness_normal, 'kurtosis_normal': kurtosis_normal,
            'statistic_prices': statistic_prices, 'statistic_returns': statistic_returns,
            'pvalue_prices': pvalue_prices, 'pvalue_returns': pvalue_returns,
            'plot_implied_volatility': plot_implied_volatility, 'div_yield': div_yield, 'risk_free': risk_free,
            'plot_index_distribution': plot_index_distribution, 'plot_return_cdf': plot_return_cdf,
            'plot_return_distribution': plot_return_distribution, 'plot_index_cdf': plot_index_cdf,
            'compute_not_allowed': compute_not_allowed, 'sim_id': sim_id}


def populate_form_from_instance(instance):
    """Repopulate form with previous values"""
    form = ComputeForm()
    for field in form:
        field.data = getattr(instance, field.name, None)  # get a value or, if it doesn't exist, a default value
    return form


def controller_old_shimko_market(user):
    data = []
    if user.is_authenticated():
        instances = user.compute_shimko_market.order_by(desc('id')).all()
        for instance in instances:
            form = populate_form_from_instance(instance)

            # page old.html, store the date and the plot (previous simulation)

            id = instance.id
            strike_data = json.loads(instance.strike_data)
            a0 = instance.a0
            a1 = instance.a1
            a2 = instance.a2
            strike_plot = np.array(json.loads(instance.strike_plot))
            implied_volatility = np.array(json.loads(instance.implied_volatility))
            strike_min = instance.strike_min
            strike_max = instance.strike_max
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
            call_put_flag = instance.call_put_flag
            volatility_time = np.array(json.loads(instance.volatility_time))
            r2 = instance.r2
            returns_t = np.array(json.loads(instance.returns_t))
            skewness_normal = instance.skewness_normal
            kurtosis_normal = instance.kurtosis_normal
            statistic_prices = instance.statistic_prices
            statistic_returns = instance.statistic_returns
            pvalue_prices = instance.pvalue_prices
            pvalue_returns = instance.pvalue_returns
            risk_dividend = instance.risk_dividend

            plot_choice = json.loads(instance.plot_choice)

            plot_index_distribution = None
            plot_index_cdf = None
            plot_return_cdf = None
            risk_free = instance.risk_free
            div_yield = instance.div_yield

            if risk_dividend == '1':
                risk_free = round(risk_free, 4) if risk_free is not None else None
                div_yield = round(div_yield, 4) if div_yield is not None else None

            if instance.st is not None:

                st = np.array(json.loads(instance.st))
                pdf = json.loads(instance.pdf)
                pdf_bench_log_prices = json.loads(instance.pdf_bench_log_prices)
                cdf_prices = json.loads(instance.cdf_prices)
                cdf_returns = json.loads(instance.cdf_returns)
                cdf_bench_log_prices = json.loads(instance.cdf_bench_log_prices)
                cdf_bench_norm_returns = json.loads(instance.cdf_bench_norm_returns)

                if '0' in plot_choice:
                    plot_index_distribution = create_plot_index_underlying_distribution(st, pdf, pdf_bench_log_prices,
                                                                                        price, strike_min, strike_max)
                if '1' in plot_choice:
                    plot_index_cdf = create_plot_price_cdf(st, cdf_prices, cdf_bench_log_prices, strike_min, strike_max)

                if '2' in plot_choice:
                    plot_return_cdf = create_plot_return_cdf(returns_t, cdf_returns, cdf_bench_norm_returns)

            plot_implied_volatility = create_implied_volatility_plot(call_put_flag, strike_plot, implied_volatility,
                                                                     price, strike_min,
                                                                     strike_max, strike_data, volatility_time)

            plot_return_distribution = create_plot_return_underlying_distribution(returns_t, pdf_returns,
                                                                                  pdf_bench_norm_returns)

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
            statistic_prices = round(statistic_prices, 4) if statistic_prices is not None else None
            statistic_returns = round(statistic_returns, 4) if statistic_returns is not None else None
            pvalue_prices = round(pvalue_prices, 4) if pvalue_prices is not None else None
            pvalue_returns = round(pvalue_returns, 4) if pvalue_returns is not None else None

            data.append({'form': form, 'id': id, 'a0': a0, 'a1': a1, 'a2': a2,
                         'area_prices': area_prices, 'expected_price': expected_price, 'sigma2_price': sigma2_price,
                         'skewness_prices': skewness_prices, 'kurtosis_prices': kurtosis_prices,
                         'skewness_prices_log_n': skewness_prices_log_n, 'kurtosis_prices_log_n': kurtosis_prices_log_n,
                         'area_returns': area_returns, 'm1_returns': m1_returns, 'm2_returns': m2_returns,
                         'skewness_log_returns': skewness_log_returns, 'kurtosis_log_returns': kurtosis_log_returns,
                         'r2': r2, 'statistic_prices': statistic_prices, 'statistic_returns': statistic_returns,
                         'pvalue_prices': pvalue_prices, 'pvalue_returns': pvalue_returns,
                         'skewness_normal': skewness_normal, 'kurtosis_normal': kurtosis_normal,
                         'plot_implied_volatility': plot_implied_volatility, 'risk_free': risk_free,
                         'plot_index_distribution': plot_index_distribution, 'div_yield': div_yield,
                         'plot_return_distribution': plot_return_distribution, 'plot_index_cdf': plot_index_cdf,
                         'plot_return_cdf': plot_return_cdf})

    return {'data': data}


def delete_shimko_market_simulation(user, id):
    id = int(id)
    if user.is_authenticated():
        if id == -1:
            user.compute_shimko_market.delete()
        else:
            try:
                instance = user.compute_shimko_market.filter_by(id=id).first()
                db.session.delete(instance)
            except:
                pass

        db.session.commit()
    return redirect(url_for('old_shimko_market'))


def controller_shimko_market_data(user, id):
    id = int(id)
    if user.is_authenticated:
        csvfile = io.StringIO()
        instance = user.compute_shimko_market.filter_by(id=id).first()

        pdf_returns_values = json.loads(instance.pdf_returns)

        values_array = [pdf_returns_values]
        fieldnames = ['Pdf Returns']

        plot_choice = json.loads(instance.plot_choice)

        if '0' in plot_choice:
            pdf_values = json.loads(instance.pdf)
            values_array.append(pdf_values)
            fieldnames.append('Pdf Prices')

        if '1' in plot_choice:
            cdf_prices_values = json.loads(instance.cdf_prices)
            values_array.append(cdf_prices_values)
            fieldnames.append('Cdf Prices')

        if '2' in plot_choice:
            cdf_returns_values = json.loads(instance.cdf_returns)
            values_array.append(cdf_returns_values)
            fieldnames.append('Cdf Returns')

        writer = csv.writer(csvfile)
        writer.writerow(fieldnames)
        for value in zip(*values_array):
            writer.writerow(value)

        return Response(csvfile.getvalue(), mimetype="text/csv",
                        headers={"Content-disposition": "attachment; filename=shimko_market_data.csv"})

    else:
        return redirect(url_for('shimko_market'))
