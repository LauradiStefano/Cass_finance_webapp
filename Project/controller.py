import os
from _socket import gethostname

from flask import render_template, request, redirect, url_for
from flask_login import LoginManager, current_user, \
    login_user, logout_user, login_required

from app import app
from asian_option.controller import controller_asian_option, controller_old_asian_option, \
    delete_asian_option_simulation, controller_asian_option_data
from db_models import db, User
from heston_method.controller import controller_heston_method, controller_old_heston_method, \
    delete_heston_method_simulation, controller_heston_method_data
from levy_process.controller import controller_levy_process, controller_old_levy_process, \
    delete_levy_process_simulation, controller_levy_process_data
from portfolio_analysis.controller import controller_portfolio_analysis, controller_old_portfolio_analysis, \
    delete_portfolio_analysis_simulation, controller_portfolio_analysis_data
from shimko_market.controller import controller_shimko_market, controller_old_shimko_market, \
    delete_shimko_market_simulation, controller_shimko_market_data
from shimko_theoretical.controller import controller_old_shimko_theoretical, controller_shimko_theoretical, \
    delete_shimko_theoretical_simulation, controller_shimko_theoretical_data
from spread_option.controller import controller_spread_option, controller_old_spread_option, \
    delete_spread_option_simulation
from statistical_analysis.controller import controller_statistical_analysis, controller_old_statistical_analysis, \
    delete_statistical_analysis_simulation, controller_statistical_analysis_prices_data, \
    controller_statistical_analysis_returns_data, controller_plot_statistical_analysis
from term_structure.controller import controller_term_structure, controller_old_term_structure, \
    delete_term_structure_simulation, controller_term_structure_data, controller_term_structure_daily_data

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(user_id)


@app.route('/', methods=['GET', 'POST'])
def index():
    just_registered = request.args.get('just_registered')
    return render_template("index.html", user=current_user, index=True, just_registered=just_registered)


@app.route('/implied_distribution_illustration', methods=['GET', 'POST'])
def shimko_theoretical():
    # ** = {'a':1, 'b':2} --> (a=1, b=2)
    template_variables = controller_shimko_theoretical(current_user, request)
    return render_template("implied_distribution_illustration.html", **template_variables, table_export=True)


@app.route('/implied_distribution_market_application', methods=['GET', 'POST'])
def shimko_market():
    # ** = {'a':1, 'b':2} --> (a=1, b=2)
    template_variables = controller_shimko_market(current_user, request)
    return render_template("implied_distribution_market_application.html", **template_variables, table_export=True)


@app.route('/plain_vanilla_levy_process', methods=['GET', 'POST'])
def levy_process():
    # ** = {'a':1, 'b':2} --> (a=1, b=2)
    template_variables = controller_levy_process(current_user, request)
    return render_template("plain_vanilla_levy_process.html", **template_variables, table_export=True)


@app.route('/plain_vanilla_heston_method', methods=['GET', 'POST'])
def heston_method():
    # ** = {'a':1, 'b':2} --> (a=1, b=2)
    template_variables = controller_heston_method(current_user, request)
    return render_template("plain_vanilla_heston_method.html", **template_variables, table_export=True)


@app.route('/asian_options', methods=['GET', 'POST'])
def asian_option():
    # ** = {'a':1, 'b':2} --> (a=1, b=2)
    template_variables = controller_asian_option(current_user, request)
    return render_template("asian_options.html", **template_variables)


@app.route('/term_structure', methods=['GET', 'POST'])
def term_structure():
    template_variables = controller_term_structure(current_user, request)
    return render_template("term_structure.html", **template_variables)


@app.route('/spread_option', methods=['GET', 'POST'])
def spread_option():
    template_variables = controller_spread_option(current_user, request)
    return render_template("spread_option.html", **template_variables)


@app.route('/return_data_statistics', methods=['GET', 'POST'])
def statistical_analysis():
    template_variables = controller_statistical_analysis(current_user, request)
    return render_template("return_data_statistics.html", **template_variables, table_export=True)


@app.route('/return_data_statistics/plot/<id>/<ticker>', methods=['GET', 'POST'])
@login_required
def plot_statistical_analysis(id, ticker):
    template_variables = controller_plot_statistical_analysis(current_user, id, ticker)
    return render_template("plot_return_data_statistics.html", **template_variables,
                           back_url=url_for('statistical_analysis'), second_page=True)


@app.route('/portfolio_construction', methods=['GET', 'POST'])
def portfolio_analysis():
    template_variables = controller_portfolio_analysis(current_user, request)
    return render_template("portfolio_construction.html", **template_variables)


@app.route('/implied_distribution_illustration/old')
@login_required
def old_shimko_theoretical():
    template_variables = controller_old_shimko_theoretical(current_user)
    return render_template("old_implied_distribution_illustration.html", **template_variables,
                           back_url=url_for('shimko_theoretical'),
                           old=True)


@app.route('/implied_distribution_market_application/old')
@login_required
def old_shimko_market():
    template_variables = controller_old_shimko_market(current_user)
    return render_template("old_implied_distribution_market_application.html", **template_variables,
                           back_url=url_for('shimko_market'), old=True)


@app.route('/plain_vanilla_levy_process/old')
@login_required
def old_levy_process():
    template_variables = controller_old_levy_process(current_user)
    return render_template("old_plain_vanilla_levy_process.html", **template_variables,
                           back_url=url_for('levy_process'), old=True)


@app.route('/plain_vanilla_heston_method/old')
@login_required
def old_heston_method():
    template_variables = controller_old_heston_method(current_user)
    return render_template("old_plain_vanilla_heston_method.html", **template_variables,
                           back_url=url_for('heston_method'), old=True)


@app.route('/asian_options/old')
@login_required
def old_asian_option():
    template_variables = controller_old_asian_option(current_user)
    return render_template("old_asian_options.html", **template_variables, back_url=url_for('asian_option'), old=True)


@app.route('/term_structure/old')
@login_required
def old_term_structure():
    template_variables = controller_old_term_structure(current_user)
    return render_template("old_term_structure.html", **template_variables, back_url=url_for('term_structure'),
                           old=True)


@app.route('/spread_option/old')
@login_required
def old_spread_option():
    template_variables = controller_old_spread_option(current_user)
    return render_template("old_spread_option.html", **template_variables, back_url=url_for('spread_option'),
                           old=True)


@app.route('/return_data_statistics/old')
@login_required
def old_statistical_analysis():
    template_variables = controller_old_statistical_analysis(current_user)
    return render_template("old_return_data_statistics.html", **template_variables,
                           back_url=url_for('statistical_analysis'), old=True)


@app.route('/portfolio_construction/old')
@login_required
def old_portfolio_analysis():
    template_variables = controller_old_portfolio_analysis(current_user)
    return render_template("old_portfolio_construction.html", **template_variables,
                           back_url=url_for('portfolio_analysis'), old=True)


@app.route('/implied_distribution_illustration/old/delete/<id>', methods=['GET', 'POST'])
@login_required
def delete_shimko_theretical(id):
    return delete_shimko_theoretical_simulation(current_user, id)


@app.route('/implied_distribution_market_application/old/delete/<id>', methods=['GET', 'POST'])
@login_required
def delete_shimko_market(id):
    return delete_shimko_market_simulation(current_user, id)


@app.route('/plain_vanilla_levy_process/old/delete/<id>', methods=['GET', 'POST'])
@login_required
def delete_levy_process(id):
    return delete_levy_process_simulation(current_user, id)


@app.route('/plain_vanilla_heston_method/old/delete/<id>', methods=['GET', 'POST'])
@login_required
def delete_heston_method(id):
    return delete_heston_method_simulation(current_user, id)


@app.route('/asian_options/old/delete/<id>', methods=['GET', 'POST'])
@login_required
def delete_asian_option(id):
    return delete_asian_option_simulation(current_user, id)


@app.route('/term_structure/old/delete/<id>', methods=['GET', 'POST'])
@login_required
def delete_term_structure(id):
    return delete_term_structure_simulation(current_user, id)


@app.route('/spread_option/old/delete/<id>', methods=['GET', 'POST'])
@login_required
def delete_spread_option(id):
    return delete_spread_option_simulation(current_user, id)


@app.route('/return_data_statistics/old/delete/<id>', methods=['GET', 'POST'])
@login_required
def delete_statistical_analysis(id):
    return delete_statistical_analysis_simulation(current_user, id)


@app.route('/portfolio_construction/old/delete/<id>', methods=['GET', 'POST'])
@login_required
def delete_portfolio_analysis(id):
    return delete_portfolio_analysis_simulation(current_user, id)


@app.route('/download_shimko_theoretical_data/<id>')
@login_required
def download_shimko_theoretical_data(id):
    response = controller_shimko_theoretical_data(current_user, id)

    return response


@app.route('/download_shimko_market_data/<id>')
@login_required
def download_shimko_market_data(id):
    response = controller_shimko_market_data(current_user, id)

    return response


@app.route('/download_levy_data/<id>')
@login_required
def download_levy_data(id):
    response = controller_levy_process_data(current_user, id)

    return response


@app.route('/download_heston_data/<id>')
@login_required
def download_heston_data(id):
    response = controller_heston_method_data(current_user, id)

    return response


@app.route('/download_asian_data/<id>')
@login_required
def download_asian_data(id):
    response = controller_asian_option_data(current_user, id)

    return response


@app.route('/download_term_data/<id>')
@login_required
def download_term_data(id):
    response = controller_term_structure_data(current_user, id)

    return response


@app.route('/download_term_daily_data/<id>')
@login_required
def download_term_daily_data(id):
    response = controller_term_structure_daily_data(current_user, id)

    return response


@app.route('/download_statistical_prices_data/<id>')
@login_required
def download_statistical_prices_data(id):
    response = controller_statistical_analysis_prices_data(current_user, id)

    return response


@app.route('/download_statistical_returns_data/<id>')
@login_required
def download_statistical_returns_data(id):
    response = controller_statistical_analysis_returns_data(current_user, id)

    return response


@app.route('/download_portfolio_data/<id>')
@login_required
def download_portfolio_data(id):
    response = controller_portfolio_analysis_data(current_user, id)

    return response


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

        return redirect(url_for('index', just_registered=1))
    return render_template("reg.html", form=form, register=True)


@app.route('/login', methods=['GET', 'POST'])
def login():
    from forms import LoginForm
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = form.get_user()
        login_user(user, remember=True)
        return redirect(url_for('index'))
    return render_template("login.html", form=form, login=True)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/about', methods=['GET', 'POST'])
def about():
    return render_template("about.html", about=True)


@app.route('/terms_service', methods=['GET', 'POST'])
def terms_service():
    return render_template("terms_service.html", about=True)


@app.route('/privacy', methods=['GET', 'POST'])
def privacy():
    return render_template("privacy.html", about=True)


if not os.path.isfile(os.path.join(os.path.dirname(__file__), 'sqlite.db')):
    db.create_all()
if 'liveweb' not in gethostname():  # this is not run on pythonanywhere
    app.run(debug=True)
