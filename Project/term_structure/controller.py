import json

import numpy as np
from flask import url_for, redirect
from sqlalchemy import desc

from db_models import db
from term_structure.forms import ComputeForm


def controller_term_structure(user, request):
    form = ComputeForm(request.form)



    # if request.method == "POST":
    #     if form.validate():
    #
    #     if user.is_authenticated:  # store data in db
    #
    # else:
    #     if user.is_authenticated:  # user authenticated, store the data
    #         if user.compute_term_structure.count() > 0:
    #             instance = user.compute_term_structure.order_by(
    #                 desc('id')).first()  # decreasing order db, take the last data saved
    #             form = populate_form_from_instance(instance)

    return {'form': form, 'user': user}


def populate_form_from_instance(instance):
    """Repopulate form with previous values"""
    form = ComputeForm()
    for field in form:
        field.data = getattr(instance, field.name)
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
