import json

import numpy as np
from flask import redirect, url_for
from sqlalchemy import desc

from db_models import db
from db_models import heston_method as compute
from heston_method.compute import heston_pdf_and_volatility, create_plot_return_underlying_distribution, \
    create_implied_volatility_plot
from heston_method.forms import ComputeForm


def controller_heston_method(user, request):
    form = ComputeForm(request.form)

    returns = None
    heston_pdf = None
    strike = None
    implied_volatility = None
    option_prices = None
    number_of_strike = 0
    norm_pdf = None
    mean = None
    variance = None
    skewness = None
    kurtosis = None

    plot_implied_volatility = None
    plot_return_underlying_distribution = None

    if request.method == "POST":
        if form.validate():
            heston_pdf, returns, implied_volatility, strike, option_prices, mean, variance, skewness, kurtosis, \
                norm_pdf = heston_pdf_and_volatility(form.price.data, form.strike_min.data, form.strike_max.data,
                                                     form.time.data, form.volatility_t0.data, form.chi.data,
                                                     form.lam.data, form.rho.data, form.volatility_hat.data,
                                                     form.mu.data, form.risk_free.data, form.dividend_yield.data,
                                                     form.call_put.data)

            number_of_strike = len(strike)

            plot_return_underlying_distribution = \
                create_plot_return_underlying_distribution(returns, heston_pdf, norm_pdf)

            plot_implied_volatility = create_implied_volatility_plot(strike, implied_volatility, form.price.data)

        if user.is_authenticated:  # store data in db
            object = compute()
            form.populate_obj(object)

            # json.dumps return a array string
            # json.loads convert from string to array

            object.heston_pdf = json.dumps(heston_pdf)
            object.returns = json.dumps(returns.tolist())
            object.price = form.price.data
            object.strike = json.dumps(strike.tolist())
            object.implied_volatility = json.dumps(implied_volatility)
            object.option_prices = json.dumps(option_prices)
            object.number_of_strike = json.dumps(number_of_strike)
            object.norm_pdf = json.dumps(norm_pdf.tolist())
            object.mean = mean
            object.variance = variance
            object.skewness = skewness
            object.kurtosis = kurtosis

            object.user = user
            db.session.add(object)
            db.session.commit()
    else:
        if user.is_authenticated:  # user authenticated, store the data
            if user.compute_heston_method.count() > 0:
                instance = user.compute_heston_method.order_by(desc('id')).first()
                form = populate_form_from_instance(instance)

                heston_pdf = json.loads(instance.heston_pdf)
                returns = np.array(json.loads(instance.returns))
                price = instance.price
                strike = np.array(json.loads(instance.strike))
                implied_volatility = json.loads(instance.implied_volatility)
                option_prices = json.loads(instance.option_prices)
                number_of_strike = json.loads(instance.number_of_strike)
                norm_pdf = np.array(json.loads(instance.norm_pdf))
                mean = instance.mean
                variance = instance.variance
                skewness = instance.skewness
                kurtosis = instance.kurtosis

                plot_return_underlying_distribution = \
                    create_plot_return_underlying_distribution(returns, heston_pdf, norm_pdf)

                plot_implied_volatility = create_implied_volatility_plot(strike, implied_volatility, price)

    implied_volatility = [round(x, 4) for x in implied_volatility] if implied_volatility is not None else None
    option_prices = [round(x, 4) for x in option_prices] if option_prices is not None else None
    mean = round(mean, 4) if mean is not None else None
    variance = round(variance, 4) if variance is not None else None
    skewness = round(skewness, 4) if skewness is not None else None
    kurtosis = round(kurtosis, 4) if kurtosis is not None else None

    return {'form': form, 'user': user, 'plot_return_underlying_distribution': plot_return_underlying_distribution,
            'plot_implied_volatility': plot_implied_volatility, 'strike': strike, 'number_of_strike': number_of_strike,
            'implied_volatility': implied_volatility, 'option_prices': option_prices, 'mean': mean,
            'variance': variance, 'skewness': skewness, 'kurtosis': kurtosis}


def populate_form_from_instance(instance):
    """Repopulate form with previous values"""
    form = ComputeForm()
    for field in form:
        field.data = getattr(instance, field.name)
    return form


def controller_old_heston_method(user):
    data = []
    if user.is_authenticated():
        instances = user.compute_heston_method.order_by(desc('id')).all()
        for instance in instances:
            form = populate_form_from_instance(instance)

            # page old.html, store the date and the plot (previous simulation)

            id = instance.id
            heston_pdf = json.loads(instance.heston_pdf)
            returns = np.array(json.loads(instance.returns))
            price = instance.price
            strike = np.array(json.loads(instance.strike))
            implied_volatility = json.loads(instance.implied_volatility)
            option_prices = json.loads(instance.option_prices)
            number_of_strike = json.loads(instance.number_of_strike)
            norm_pdf = np.array(json.loads(instance.norm_pdf))
            mean = instance.mean
            variance = instance.variance
            skewness = instance.skewness
            kurtosis = instance.kurtosis

            plot_return_underlying_distribution = \
                create_plot_return_underlying_distribution(returns, heston_pdf, norm_pdf)

            plot_implied_volatility = create_implied_volatility_plot(strike, implied_volatility, price)

            # implied_volatility = [round(x, 4) for x in implied_volatility] if implied_volatility is not None else None
            # option_prices = [round(x, 4) for x in option_prices] if option_prices is not None else None
            mean = round(mean, 4) if mean is not None else None
            variance = round(variance, 4) if variance is not None else None
            skewness = round(skewness, 4) if skewness is not None else None
            kurtosis = round(kurtosis, 4) if kurtosis is not None else None

            data.append({'form': form, 'id': id,
                         'plot_return_underlying_distribution': plot_return_underlying_distribution,
                         'plot_implied_volatility': plot_implied_volatility, 'strike': strike,
                         'implied_volatility': implied_volatility, 'option_prices': option_prices,
                         'number_of_strike': number_of_strike, 'mean': mean, 'variance': variance, 'skewness': skewness,
                         'kurtosis': kurtosis})

    return {'data': data}


def delete_post(user, id):
    id = int(id)
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
