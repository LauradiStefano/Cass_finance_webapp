import csv
import io
import json

import numpy as np
from flask import url_for, redirect, Response
from sqlalchemy import desc

from db_models import db
from db_models import shimko_theoretical_model as compute
from shimko_theoretical.compute import create_implied_volatility_plot, create_plot_index_underlying_distribution, \
    create_plot_return_underlying_distribution, create_plot_price_cdf, create_plot_return_cdf, \
    find_parameters, compute_shimko_table, compute_index_underlying_cdf, \
    compute_index_underlying_distribution, compute_returns_cdf, kolmogorov_smirnov_test
from shimko_theoretical.forms import ComputeForm


def controller_shimko_theoretical(user, request):
    form = ComputeForm(request.form)

    a0 = None
    a1 = None
    a2 = None

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

    sim_id = None

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
                object = compute()
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
                sim_id = object.id
    else:
        if user.is_authenticated:  # user authenticated, store the data
            if user.compute_shimko_theoretical.count() > 0:
                instance = user.compute_shimko_theoretical.order_by(
                    desc('id')).first()  # decreasing order db, take the last data saved
                form = populate_form_from_instance(instance)

                sim_id = instance.id
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
                        plot_index_distribution = \
                            create_plot_index_underlying_distribution(st, pdf, pdf_bench_log_prices, price, strike_min,
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

    pdf_returns = [round(x, 6) for x in pdf_returns] if pdf_returns is not None else None
    pdf = [round(x, 6) for x in pdf] if pdf is not None else None
    cdf_returns = [round(x, 6) for x in cdf_returns] if cdf_returns is not None else None
    cdf_prices = [round(x, 6) for x in cdf_prices] if cdf_prices is not None else None

    return {'form': form, 'user': user, 'a0': a0, 'a1': a1, 'a2': a2, 'area_prices': area_prices,
            'expected_price': expected_price, 'sigma2_price': sigma2_price, 'skewness_prices': skewness_prices,
            'kurtosis_prices': kurtosis_prices, 'skewness_prices_log_n': skewness_prices_log_n,
            'kurtosis_prices_log_n': kurtosis_prices_log_n, 'area_returns': area_returns, 'm1_returns': m1_returns,
            'm2_returns': m2_returns, 'skewness_log_returns': skewness_log_returns,
            'kurtosis_log_returns': kurtosis_log_returns, 'skewness_normal': skewness_normal,
            'kurtosis_normal': kurtosis_normal, 'statistic_prices': statistic_prices,
            'statistic_returns': statistic_returns, 'pvalue_prices': pvalue_prices, 'pvalue_returns': pvalue_returns,
            'pdf_returns': pdf_returns, 'pdf': pdf, 'cdf_returns': cdf_returns, 'cdf_prices': cdf_prices,
            'plot_implied_volatility': plot_implied_volatility, 'plot_index_distribution': plot_index_distribution,
            'plot_index_cdf': plot_index_cdf, 'plot_return_distribution': plot_return_distribution,
            'plot_return_cdf': plot_return_cdf, 'sim_id': sim_id}


def populate_form_from_instance(instance):
    """Repopulate form with previous values"""
    form = ComputeForm()
    for field in form:
        field.data = getattr(instance, field.name, None)  # get a value or, if it doesn't exist, a default value
    return form


def controller_old_shimko_theoretical(user):
    data = []
    if user.is_authenticated():
        instances = user.compute_shimko_theoretical.order_by(desc('id')).all()
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

            data.append({'form': form, 'id': id, 'a0': a0, 'a1': a1, 'a2': a2, 'area_prices': area_prices,
                         'expected_price': expected_price, 'sigma2_price': sigma2_price,
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

    return {'data': data}


def delete_shimko_theoretical_simulation(user, id):
    id = int(id)
    if user.is_authenticated():
        if id == -1:
            user.compute_shimko_theoretical.delete()
        else:
            try:
                instance = user.compute_shimko_theoretical.filter_by(id=id).first()
                db.session.delete(instance)
            except:
                pass

        db.session.commit()
    return redirect(url_for('old_shimko_theoretical'))


def controller_shimko_theoretical_data(user, id):
    id = int(id)
    if user.is_authenticated:
        csvfile = io.StringIO()
        instance = user.compute_shimko_theoretical.filter_by(id=id).first()

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
                        headers={"Content-disposition": "attachment; filename=shimko_theoretical_data.csv"})

    else:
        return redirect(url_for('shimko_theoretical'))
