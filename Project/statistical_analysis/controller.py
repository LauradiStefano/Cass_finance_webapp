import json
import os

import numpy as np
import pandas as pd
from flask import url_for, redirect
from sqlalchemy import desc
from werkzeug.utils import secure_filename

from app import allowed_file, app
from db_models import db
from db_models import statisitcal_analysis as compute
from statistical_analysis.compute import import_dataset_tickers, import_dataset_file_excel, compute_table, \
    create_histogram_distribution_plot, create_qq_plot, create_plot_log_returns, create_autocorrelation_function_plot
from statistical_analysis.forms import ComputeForm


def controller_statistical_analysis(user, request):
    form = ComputeForm(request.form)

    file_data = None
    mean = None
    volatility = None
    variance = None
    skewness = None
    kurtosis = None
    min_return = None
    max_return = None
    jb_test = None
    pvalue = None
    tickers = None
    n_observation = None
    log_returns = None
    dates = None

    plot_qq = None
    plot_histogram = None
    plot_log_returns = None
    plot_autocorrelation = None

    number_of_tickers = 0

    if request.method == "POST":
        if form.validate():
            if form.method_choice.data == '0':
                if request.files:
                    file = request.files[form.file_data.name]

                    if file and allowed_file(file.filename):
                        file_data = secure_filename(file.filename)
                        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file_data))

                file_data, dates = import_dataset_file_excel(file_data)

            else:  # form.method_choice.data == '1'

                file_data, dates = import_dataset_tickers(form.flist.data, form.start_day.data, form.start_month.data,
                                                          form.start_year.data, form.end_day.data, form.end_month.data,
                                                          form.end_year.data)

            mean, volatility, variance, skewness, kurtosis, min_return, max_return, jb_test, pvalue, tickers, \
            n_observation, log_returns = compute_table(file_data)

            plot_histogram = create_histogram_distribution_plot(log_returns)

            plot_qq = create_qq_plot(log_returns)

            plot_log_returns = create_plot_log_returns(log_returns, dates)

            plot_autocorrelation = create_autocorrelation_function_plot(log_returns)

            number_of_tickers = len(tickers)

        if user.is_authenticated:  # store data in db
            object = compute()
            form.populate_obj(object)

            object.mean = json.dumps(mean)
            object.volatility = json.dumps(volatility)
            object.variance = json.dumps(variance)
            object.skewness = json.dumps(skewness)
            object.kurtosis = json.dumps(kurtosis)
            object.min_return = json.dumps(min_return)
            object.max_return = json.dumps(max_return)
            object.jb_test = json.dumps(jb_test)
            object.pvalue = json.dumps(pvalue)
            object.tickers = json.dumps(tickers)
            object.number_of_tickers = number_of_tickers
            object.n_observation = json.dumps(n_observation)
            object.log_returns = json.dumps(log_returns.tolist())
            dates = list(map(str, dates))
            object.dates = json.dumps(dates)

            object.user = user
            db.session.add(object)
            db.session.commit()
    else:
        if user.is_authenticated and user.compute_statistical_analysis.count() > 0:
            # user authenticated, store the data
            instance = user.compute_statistical_analysis.order_by(
                desc('id')).first()  # decreasing order db, take the last data saved
            form = populate_form_from_instance(instance)

            mean = json.loads(instance.mean)
            volatility = json.loads(instance.volatility)
            variance = json.loads(instance.variance)
            skewness = json.loads(instance.skewness)
            kurtosis = json.loads(instance.kurtosis)
            min_return = json.loads(instance.min_return)
            max_return = json.loads(instance.max_return)
            jb_test = json.loads(instance.jb_test)
            pvalue = json.loads(instance.pvalue)
            tickers = json.loads(instance.tickers)
            number_of_tickers = instance.number_of_tickers
            n_observation = json.loads(instance.n_observation)
            log_returns = np.array(json.loads(instance.log_returns))
            dates = list(map(pd.Timestamp, json.loads(instance.dates)))

            plot_histogram = create_histogram_distribution_plot(log_returns)
            plot_qq = create_qq_plot(log_returns)
            plot_log_returns = create_plot_log_returns(log_returns, dates)
            plot_autocorrelation = create_autocorrelation_function_plot(log_returns)

    mean = [round(x, 6) for x in mean] if mean is not None else None
    volatility = [round(x, 6) for x in volatility] if volatility is not None else None
    variance = [round(x, 6) for x in variance] if variance is not None else None
    skewness = [round(x, 6) for x in skewness] if skewness is not None else None
    kurtosis = [round(x, 6) for x in kurtosis] if kurtosis is not None else None
    min_return = [round(x, 6) for x in min_return] if min_return is not None else None
    max_return = [round(x, 6) for x in max_return] if max_return is not None else None
    jb_test = [round(x, 2) for x in jb_test] if jb_test is not None else None
    pvalue = [round(x, 2) for x in pvalue] if pvalue is not None else None

    return {'form': form, 'user': user, 'min_return': min_return, 'mean': mean, 'volatility': volatility,
            'variance': variance, 'skewness': skewness, 'kurtosis': kurtosis, 'number_of_tickers': number_of_tickers,
            'max_return': max_return, 'jb_test': jb_test, 'pvalue': pvalue, 'tickers': tickers,
            'n_observation': n_observation, 'plot_histogram': plot_histogram, 'plot_qq': plot_qq,
            'plot_log_returns': plot_log_returns, 'plot_autocorrelation': plot_autocorrelation}


def populate_form_from_instance(instance):
    """Repopulate form with previous values"""
    form = ComputeForm()
    for field in form:
        if type(field.data) == list:
            field.data.pop()  # remove tickers name in field
            # for x in instance.tickers:
            #     field.data.append(x)
        else:
            field.data = getattr(instance, field.name, None)  # get a value or, if it doesn't exist, a default value

    return form


def controller_old_statistical_analysis(user):
    data = []

    if user.is_authenticated():
        instances = user.compute_statistical_analysis.order_by(desc('id')).all()
        for instance in instances:
            form = populate_form_from_instance(instance)

            # page old.html, store the date and the plot (previous simulation)

            id = instance.id
            mean = json.loads(instance.mean)
            volatility = json.loads(instance.volatility)
            variance = json.loads(instance.variance)
            skewness = json.loads(instance.skewness)
            kurtosis = json.loads(instance.kurtosis)
            min_return = json.loads(instance.min_return)
            max_return = json.loads(instance.max_return)
            jb_test = (json.loads(instance.jb_test))
            pvalue = json.loads(instance.pvalue)
            tickers = json.loads(instance.tickers)
            number_of_tickers = instance.number_of_tickers
            n_observation = json.loads(instance.n_observation)

            mean = [round(x, 6) for x in mean] if mean is not None else None
            volatility = [round(x, 6) for x in volatility] if volatility is not None else None
            variance = [round(x, 6) for x in variance] if variance is not None else None
            skewness = [round(x, 6) for x in skewness] if skewness is not None else None
            kurtosis = [round(x, 6) for x in kurtosis] if kurtosis is not None else None
            min_return = [round(x, 6) for x in min_return] if min_return is not None else None
            max_return = [round(x, 6) for x in max_return] if max_return is not None else None
            jb_test = [round(x, 2) for x in jb_test] if jb_test is not None else None
            pvalue = [round(x, 2) for x in pvalue] if pvalue is not None else None

            data.append({'form': form, 'id': id, 'mean': mean, 'volatility': volatility, 'variance': variance,
                         'skewness': skewness, 'kurtosis': kurtosis, 'min_return': min_return, 'max_return': max_return,
                         'jb_test': jb_test, 'pvalue': pvalue, 'tickers': tickers, 'n_observation': n_observation,
                         'number_of_tickers': number_of_tickers})

    return {'data': data}


def delete_statistical_analysis_simulation(user, id):
    id = int(id)
    if user.is_authenticated():
        if id == -1:
            user.compute_statistical_analysis.delete()
        else:
            try:
                instance = user.compute_statistical_analysis.filter_by(id=id).first()
                db.session.delete(instance)
            except:
                pass

        db.session.commit()
    return redirect(url_for('old_statistical_analysis'))

# def controller_plot_statistical_analysis(user, id, ticker):
#     data = []
#     plot_histogram = None
#
#     if user.is_authenticated():
#         instances = user.compute_statistical_analysis.order_by(desc('id')).all()
#         for instance in instances:
#             # page old.html, store the date and the plot (previous simulation)
#
#             id = instance.id
#             log_returns = json.loads(instance.log_returns)
#
#             plot_histogram = create_histogram_distribution_plot(log_returns)
#
#             plot_qq = create_qq_plot(log_returns)
#
#             data.append({'id': id, 'plot_histogram': plot_histogram, 'plot_qq': plot_qq})
#     return {'data': data}
