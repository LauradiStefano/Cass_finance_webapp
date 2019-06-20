import os

from flask import render_template, request, redirect, url_for
from flask_login import LoginManager, current_user, \
    login_user, logout_user, login_required

from app import app
from asian_option.controller import controller_asian_option
from db_models import db, User
from heston_method.controller import controller_heston_method
from levy_process.controller import controller_levy_process
from shimko_market.controller import controller_shimko_market
from shimko_theoretical.controller import controller_shimko_theoretical

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(user_id)


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template("index.html", user=current_user)


@app.route('/shimko_theoretical', methods=['GET', 'POST'])
def shimko_theoretical():
    # ** = {'a':1, 'b':2} --> (a=1, b=2)
    template_variables = controller_shimko_theoretical(current_user, request)
    return render_template("shimko_theoretical.html", **template_variables)


@app.route('/shimko_market', methods=['GET', 'POST'])
def shimko_market():
    # ** = {'a':1, 'b':2} --> (a=1, b=2)
    template_variables = controller_shimko_market(current_user, request)
    return render_template("shimko_market.html", **template_variables)


@app.route('/levy_process', methods=['GET', 'POST'])
def levy_process():
    # ** = {'a':1, 'b':2} --> (a=1, b=2)
    template_variables = controller_levy_process(current_user, request)
    return render_template("levy_process.html", **template_variables)


@app.route('/heston_method', methods=['GET', 'POST'])
def heston_method():
    # ** = {'a':1, 'b':2} --> (a=1, b=2)
    template_variables = controller_heston_method(current_user, request)
    return render_template("heston_method.html", **template_variables)


@app.route('/asian_option', methods=['GET', 'POST'])
def asian_option():
    # ** = {'a':1, 'b':2} --> (a=1, b=2)
    template_variables = controller_asian_option(current_user, request)
    return render_template("asian_option.html", **template_variables)


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
        # TODO: Msg registration
        # flash('Thanks for registering')
        return redirect(url_for('index'))
    return render_template("reg.html", form=form, register=True)


@app.route('/login', methods=['GET', 'POST'])
def login():
    from forms import LoginForm
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = form.get_user()
        login_user(user)
        return redirect(url_for('index'))
    return render_template("login.html", form=form, login=True)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


if __name__ == '__main__':
    if not os.path.isfile(os.path.join(os.path.dirname(__file__), 'sqlite.db')):
        db.create_all()
    app.run(debug=True)
