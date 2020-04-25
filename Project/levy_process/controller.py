import csv
import io
import json

import numpy as np
from flask import redirect, url_for, Response
from sqlalchemy import desc

from db_models import db
from db_models import levy_process as compute
from levy_process.compute import cos_pdf_underlying_asset, create_plot_return_underlying_distribution, \
    compute_option_prices, compute_implied_volatility, create_implied_volatility_plot, select_parameters
from levy_process.forms import ComputeForm


def controller_levy_process(user, request):
    form = ComputeForm(request.form)

    pdf_underlying_asset = None
    strike = None
    implied_volatility = None
    option_prices = None

    mean = None
    variance = None
    skewness = None
    kurtosis = None
    number_of_strike = 0

    sim_id = None

    plot_implied_volatility = None
    plot_return_underlying_distribution = None

    if request.method == "POST":
        if form.validate():
            parameters = select_parameters(form.type_choice.data, form.mu.data, form.sigma_normal.data,
                                           form.sigma_vg.data, form.kappa_vg.data, form.theta_vg.data,
                                           form.sigma_nig.data, form.kappa_nig.data, form.theta_nig.data, form.c.data,
                                           form.g.data, form.m.data, form.y.data)
            pdf_underlying_asset, underlying_prices, mean, variance, skewness, kurtosis, norm_pdf = \
                cos_pdf_underlying_asset(form.type_choice.data, parameters, form.time.data)

            option_prices, strike = \
                compute_option_prices(form.type_choice.data, form.call_put.data, form.price.data, form.strike_min.data,
                                      form.strike_max.data, form.risk_free.data, form.dividend_yield.data,
                                      form.time.data, parameters)

            implied_volatility = \
                compute_implied_volatility(option_prices, form.call_put.data, form.price.data, strike, form.time.data,
                                           form.risk_free.data, form.dividend_yield.data)

            number_of_strike = len(strike)

            plot_return_underlying_distribution = \
                create_plot_return_underlying_distribution(underlying_prices, pdf_underlying_asset, norm_pdf)

            plot_implied_volatility = create_implied_volatility_plot(strike, implied_volatility, form.price.data)

            if user.is_authenticated:  # store data in db
                object = compute()
                form.populate_obj(object)

                # json.dumps return a array string
                # json.loads convert from string to array

                object.pdf_underlying_asset = json.dumps(pdf_underlying_asset)
                object.underlying_prices = json.dumps(underlying_prices.tolist())
                object.price = form.price.data
                object.strike = json.dumps(strike.tolist())
                object.implied_volatility = json.dumps(implied_volatility)
                object.norm_pdf = json.dumps(norm_pdf.tolist())
                object.mean = mean
                object.variance = variance
                object.skewness = skewness
                object.kurtosis = kurtosis
                object.option_prices = json.dumps(option_prices)
                object.number_of_strike = json.dumps(number_of_strike)

                object.user = user
                db.session.add(object)
                db.session.commit()
                sim_id = object.id
    else:
        if user.is_authenticated:  # user authenticated, store the data
            if user.compute_levy_process.count() > 0:
                instance = user.compute_levy_process.order_by(desc('id')).first()
                form = populate_form_from_instance(instance)

                sim_id = instance.id
                pdf_underlying_asset = json.loads(instance.pdf_underlying_asset)
                underlying_prices = np.array(json.loads(instance.underlying_prices))
                price = instance.price
                strike = np.array(json.loads(instance.strike))
                implied_volatility = json.loads(instance.implied_volatility)
                norm_pdf = np.array(json.loads(instance.norm_pdf))
                mean = instance.mean
                variance = instance.variance
                skewness = instance.skewness
                kurtosis = instance.kurtosis
                option_prices = json.loads(instance.option_prices)
                number_of_strike = json.loads(instance.number_of_strike)

                plot_return_underlying_distribution = \
                    create_plot_return_underlying_distribution(underlying_prices, pdf_underlying_asset, norm_pdf)

                plot_implied_volatility = create_implied_volatility_plot(strike, implied_volatility, price)

    mean = round(mean, 4) if mean is not None else None
    variance = round(variance, 4) if variance is not None else None
    skewness = round(skewness, 4) if skewness is not None else None
    kurtosis = round(kurtosis, 4) if kurtosis is not None else None
    implied_volatility = [round(x, 6) for x in implied_volatility] if implied_volatility is not None else None
    option_prices = [round(x, 6) for x in option_prices] if option_prices is not None else None

    pdf_underlying_asset = [round(x, 6) for x in pdf_underlying_asset] if pdf_underlying_asset is not None else None

    return {'form': form, 'user': user, 'plot_return_underlying_distribution': plot_return_underlying_distribution,
            'plot_implied_volatility': plot_implied_volatility, 'mean': mean, 'variance': variance,
            'skewness': skewness, 'kurtosis': kurtosis, 'number_of_strike': number_of_strike, 'strike': strike,
            'option_prices': option_prices, 'implied_volatility': implied_volatility,
            'pdf_underlying_asset': pdf_underlying_asset, 'sim_id': sim_id}


def populate_form_from_instance(instance):
    """Repopulate form with previous values"""
    form = ComputeForm()
    for field in form:
        field.data = getattr(instance, field.name, None)  # get a value or, if it doesn't exist, a default value
    return form


def controller_old_levy_process(user):
    data = []
    if user.is_authenticated():
        instances = user.compute_levy_process.order_by(desc('id')).all()
        for instance in instances:
            form = populate_form_from_instance(instance)

            # page old.html, store the date and the plot (previous simulation)

            id = instance.id
            pdf_underlying_asset = json.loads(instance.pdf_underlying_asset)
            underlying_prices = np.array(json.loads(instance.underlying_prices))
            price = instance.price
            strike = np.array(json.loads(instance.strike))
            implied_volatility = json.loads(instance.implied_volatility)
            norm_pdf = np.array(json.loads(instance.norm_pdf))
            mean = instance.mean
            variance = instance.variance
            skewness = instance.skewness
            kurtosis = instance.kurtosis
            option_prices = json.loads(instance.option_prices)
            number_of_strike = json.loads(instance.number_of_strike)

            plot_return_underlying_distribution = \
                create_plot_return_underlying_distribution(underlying_prices, pdf_underlying_asset, norm_pdf)

            plot_implied_volatility = create_implied_volatility_plot(strike, implied_volatility, price)

            mean = round(mean, 4) if mean is not None else None
            variance = round(variance, 4) if variance is not None else None
            skewness = round(skewness, 4) if skewness is not None else None
            kurtosis = round(kurtosis, 4) if kurtosis is not None else None

            data.append({'form': form, 'id': id,
                         'plot_return_underlying_distribution': plot_return_underlying_distribution,
                         'plot_implied_volatility': plot_implied_volatility, 'mean': mean, 'variance': variance,
                         'skewness': skewness, 'kurtosis': kurtosis})

    return {'data': data}


def delete_levy_process_simulation(user, id):
    id = int(id)
    if user.is_authenticated():
        if id == -1:
            user.compute_levy_process.delete()
        else:
            try:
                instance = user.compute_levy_process.filter_by(id=id).first()
                db.session.delete(instance)
            except:
                pass

        db.session.commit()
    return redirect(url_for('old_levy_process'))


def controller_levy_process_data(user, id):
    id = int(id)
    if user.is_authenticated:
        csvfile = io.StringIO()
        instance = user.compute_levy_process.filter_by(id=id).first()

        pdf_values = json.loads(instance.pdf_underlying_asset)

        fieldnames = ['Pdf Asset']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for value in pdf_values:
            writer.writerow({'Pdf Asset': value})

        return Response(csvfile.getvalue(), mimetype="text/csv",
                        headers={"Content-disposition": "attachment; filename=levy_data.csv"})

    else:
        return redirect(url_for('levy_process'))
