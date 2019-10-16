from flask import redirect, url_for
from sqlalchemy import desc

from db_models import db
from db_models import spread_option as compute
from spread_option.forms import ComputeForm
from spread_option.compute import price_spread_option


def controller_spread_option(user, request):
    form = ComputeForm(request.form)
    spread_option_price = None
    if request.method == "POST":
        if form.validate():
            spread_option_price = price_spread_option(form.risk_free.data, form.time.data, form.price_1.data,
                                                      form.price_2.data, form.dividend_yield_1,
                                                      form.dividend_yield_2.data, form.strike.data, form.dump.data,
                                                      form.volatility_1.data, form.volatility_2.data, form.rho.data)

        if user.is_authenticated:  # store data in db
            object = compute()
            form.populate_obj(object)

            object.spread_option_price = spread_option_price

            object.user = user
            db.session.add(object)
            db.session.commit()

    else:
        if user.is_authenticated:  # user authenticated, store the data
            if user.compute_heston_method.count() > 0:
                instance = user.compute_heston_method.order_by(desc('id')).first()
                form = populate_form_from_instance(instance)

                spread_option_price = instance.spread_option_price

    spread_option_price = round(spread_option_price, 6) if spread_option_price is not None else None

    return {'form': form, 'user': user, 'spread_option_price': spread_option_price}


def populate_form_from_instance(instance):
    """Repopulate form with previous values"""
    form = ComputeForm()
    for field in form:
        field.data = getattr(instance, field.name)
    return form


def controller_old_spread_option(user):
    data = []
    if user.is_authenticated():
        instances = user.compute_heston_method.order_by(desc('id')).all()
        for instance in instances:
            form = populate_form_from_instance(instance)

            # page old.html, store the date and the plot (previous simulation)

            id = instance.id
            spread_option_price = instance.spread_option_price

            spread_option_price = round(spread_option_price, 6) if spread_option_price is not None else None

            data.append({'form': form, 'id': id, 'spread_option_price':spread_option_price})

    return {'data': data}


def delete_spread_option_simulation(user, id):
    id = int(id)
    if user.is_authenticated():
        if id == -1:
            user.compute_spread_option.delete()
        else:
            try:
                instance = user.compute_spread_option.filter_by(id=id).first()
                db.session.delete(instance)
            except:
                pass

        db.session.commit()
    return redirect(url_for('old_spread_option'))
