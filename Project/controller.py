import os
from _socket import gethostname

from flask import render_template, request, redirect, url_for
from flask_login import LoginManager, current_user, \
    login_user, logout_user, login_required

from app import app
from asian_option.controller import controller_asian_option, controller_old_asian_option, delete_asian_option_simulation
from db_models import db, User
from heston_method.controller import controller_heston_method, controller_old_heston_method, \
    delete_heston_method_simulation
from levy_process.controller import controller_levy_process, controller_old_levy_process, delete_levy_process_simulation
from portfolio_analysis.controller import controller_portfolio_analysis, controller_old_portfolio_analysis, \
    delete_portfolio_analysis_simulation
from shimko_market.controller import controller_shimko_market, controller_old_shimko_market, \
    delete_shimko_market_simulation
from shimko_theoretical.controller import controller_old_shimko_theoretical, controller_shimko_theoretical, \
    delete_shimko_theoretical_simulation
from spread_option.controller import controller_spread_option, controller_old_spread_option, \
    delete_spread_option_simulation
from statistical_analysis.controller import controller_statistical_analysis, controller_old_statistical_analysis, \
    delete_statistical_analysis_simulation
from term_structure.controller import controller_term_structure, controller_old_term_structure, \
    delete_term_structure_simulation

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(user_id)


@app.route('/', methods=['GET', 'POST'])
def index():
    just_registered = request.args.get('just_registered')
    return render_template("index.html", user=current_user, index=True, just_registered=just_registered)


@app.route('/shimko_theoretical', methods=['GET', 'POST'])
def shimko_theoretical():
    # ** = {'a':1, 'b':2} --> (a=1, b=2)
    template_variables = controller_shimko_theoretical(current_user, request)
    return render_template("shimko_theoretical.html", **template_variables, table_export=True)


@app.route('/shimko_market', methods=['GET', 'POST'])
def shimko_market():
    # ** = {'a':1, 'b':2} --> (a=1, b=2)
    template_variables = controller_shimko_market(current_user, request)
    return render_template("shimko_market.html", **template_variables, table_export=True)


@app.route('/levy_process', methods=['GET', 'POST'])
def levy_process():
    # ** = {'a':1, 'b':2} --> (a=1, b=2)
    template_variables = controller_levy_process(current_user, request)
    return render_template("levy_process.html", **template_variables, table_export=True)


@app.route('/heston_method', methods=['GET', 'POST'])
def heston_method():
    # ** = {'a':1, 'b':2} --> (a=1, b=2)
    template_variables = controller_heston_method(current_user, request)
    return render_template("heston_method.html", **template_variables, table_export=True)


@app.route('/asian_option', methods=['GET', 'POST'])
def asian_option():
    # ** = {'a':1, 'b':2} --> (a=1, b=2)
    template_variables = controller_asian_option(current_user, request)
    return render_template("asian_option.html", **template_variables)


@app.route('/term_structure', methods=['GET', 'POST'])
def term_structure():
    template_variables = controller_term_structure(current_user, request)
    return render_template("term_structure.html", **template_variables)


@app.route('/spread_option', methods=['GET', 'POST'])
def spread_option():
    template_variables = controller_spread_option(current_user, request)
    return render_template("spread_option.html", **template_variables)


@app.route('/statistical_analysis', methods=['GET', 'POST'])
def statistical_analysis():
    template_variables = controller_statistical_analysis(current_user, request)
    return render_template("statistical_analysis.html", **template_variables, table_export=True)


@app.route('/plot_statistical_analysis', methods=['GET', 'POST'])
def plot_statistical_analysis():
    template_variables = controller_statistical_analysis(current_user, request)
    return render_template("plot_statistical_analysis.html", **template_variables)


@app.route('/portfolio_analysis', methods=['GET', 'POST'])
def portfolio_analysis():
    template_variables = controller_portfolio_analysis(current_user, request)
    return render_template("portfolio_analysis.html", **template_variables)


@app.route('/shimko_theoretical/old')
@login_required
def old_shimko_theoretical():
    template_variables = controller_old_shimko_theoretical(current_user)
    return render_template("old_shimko_theoretical.html", **template_variables, back_url=url_for('shimko_theoretical'),
                           old=True)


@app.route('/shimko_market/old')
@login_required
def old_shimko_market():
    template_variables = controller_old_shimko_market(current_user)
    return render_template("old_shimko_market.html", **template_variables, back_url=url_for('shimko_market'), old=True)


@app.route('/levy_process/old')
@login_required
def old_levy_process():
    template_variables = controller_old_levy_process(current_user)
    return render_template("old_levy_process.html", **template_variables, back_url=url_for('levy_process'), old=True)


@app.route('/heston_method/old')
@login_required
def old_heston_method():
    template_variables = controller_old_heston_method(current_user)
    return render_template("old_heston_method.html", **template_variables, back_url=url_for('heston_method'), old=True)


@app.route('/asian_option/old')
@login_required
def old_asian_option():
    template_variables = controller_old_asian_option(current_user)
    return render_template("old_asian_option.html", **template_variables, back_url=url_for('asian_option'), old=True)


@app.route('/term_structure/old')
def old_term_structure():
    template_variables = controller_old_term_structure(current_user)
    return render_template("old_term_structure.html", **template_variables, back_url=url_for('term_structure'),
                           old=True)


@app.route('/spread_option/old')
def old_spread_option():
    template_variables = controller_old_spread_option(current_user)
    return render_template("old_spread_option.html", **template_variables, back_url=url_for('spread_option'),
                           old=True)


@app.route('/statistical_analysis/old')
def old_statistical_analysis():
    template_variables = controller_old_statistical_analysis(current_user)
    return render_template("old_statistical_analysis.html", **template_variables,
                           back_url=url_for('statistical_analysis'), old=True)


@app.route('/portfolio_analysis/old')
def old_portfolio_analysis():
    template_variables = controller_old_portfolio_analysis(current_user)
    return render_template("old_portfolio_analysis.html", **template_variables,
                           back_url=url_for('portfolio_analysis'), old=True)


@app.route('/shimko_theoretical/old/delete/<id>', methods=['GET', 'POST'])
@login_required
def delete_shimko_theretical(id):
    return delete_shimko_theoretical_simulation(current_user, id)


@app.route('/shimko_market/old/delete/<id>', methods=['GET', 'POST'])
@login_required
def delete_shimko_market(id):
    return delete_shimko_market_simulation(current_user, id)


@app.route('/levy_process/old/delete/<id>', methods=['GET', 'POST'])
@login_required
def delete_levy_process(id):
    return delete_levy_process_simulation(current_user, id)


@app.route('/heston_method/old/delete/<id>', methods=['GET', 'POST'])
@login_required
def delete_heston_method(id):
    return delete_heston_method_simulation(current_user, id)


@app.route('/asian_option/old/delete/<id>', methods=['GET', 'POST'])
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


@app.route('/statistical_analysis/old/delete/<id>', methods=['GET', 'POST'])
@login_required
def delete_statistical_analysis(id):
    return delete_statistical_analysis_simulation(current_user, id)


@app.route('/portfolio_analysis/old/delete/<id>', methods=['GET', 'POST'])
@login_required
def delete_portfolio_analysis(id):
    return delete_portfolio_analysis_simulation(current_user, id)


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


if not os.path.isfile(os.path.join(os.path.dirname(__file__), 'sqlite.db')):
    db.create_all()
if 'liveweb' not in gethostname():  # this is not run on pythonanywhere
    app.run(debug=True)
