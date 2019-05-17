import wtforms as wtf
import wtforms.fields.html5 as html5

import db_models


# from wtforms.widgets import ListWidget, CheckboxInput
# from wtforms import SelectMultipleField
#

# class MultiCheckboxField(SelectMultipleField):
#     widget = ListWidget(prefix_label=False)
#     option_widget = CheckboxInput()


class ComputeForm(wtf.Form):
    model_choice = wtf.SelectField('Model', choices=[('0', 'GBM'), ('1', 'VG'), ('2', 'Heston')], default='0')

    sigma_gaussian = wtf.FloatField(label='Sigma', default=0.17801)

    sigma_vg = wtf.FloatField(label='Sigma', default=0.18002)
    theta = wtf.FloatField(label='Theta', default=-0.13)
    kappa = wtf.FloatField(label='Kappa', default=0.73670)

    volatility_t0 = wtf.FloatField(label='V0', default=0.0102)
    alpha = wtf.FloatField(label='Alpha', default=6.21)
    beta = wtf.FloatField(label='Beta', default=0.019)
    eta = wtf.FloatField(label='Eta', default=0.61)
    rho = wtf.FloatField(label='Rho', default=-0.7)

    price = wtf.FloatField(label='Spot Price', default=100, validators=[wtf.validators.InputRequired()])
    risk_free = wtf.FloatField(label='Risk Free (%)', default=3.67, validators=[wtf.validators.InputRequired()])
    # dividend_yield = wtf.FloatField(label='Dividend Yield (%)', default=0,
    #                                 validators=[wtf.validators.InputRequired()])
    time = wtf.FloatField(label='Time to Maturity', default=1, validators=[wtf.validators.InputRequired()])
    step = wtf.FloatField(label='Monitoring Frequency', default=12, validators=[wtf.validators.InputRequired()])
    strike = wtf.FloatField(label='Strike', default=100, validators=[wtf.validators.InputRequired()])

    button_compute = wtf.SubmitField(label='Compute')
    # button_export_table = wtf.SubmitField(label='Export Table')
    # button_table = wtf.SubmitField(label='View Details')


class RegistrationForm(wtf.Form):
    username = wtf.StringField(
        label='Username', validators=[wtf.validators.DataRequired()])
    password = wtf.PasswordField(
        label='Password', validators=[
            wtf.validators.DataRequired(),
            wtf.validators.EqualTo(
                'confirm', message='Passwords must match')])
    confirm = wtf.PasswordField(
        label='Confirm Password',
        validators=[wtf.validators.DataRequired()])
    email = html5.EmailField(label='Email')
    button_registration = wtf.SubmitField(label='Sign Up')

    def validate(self):
        if not wtf.Form.validate(self):
            return False

        if db_models.db.session.query(db_models.User).filter_by(username=self.username.data).count() > 0:
            self.username.errors.append('User already exists')
            return False

        return True


class Loginform(wtf.Form):
    username = wtf.StringField(
        label='Username', validators=[wtf.validators.DataRequired()])
    password = wtf.PasswordField(
        label='Password', validators=[wtf.validators.DataRequired()])
    button_login = wtf.SubmitField(label='Log In')

    def validate(self):
        if not wtf.Form.validate(self):
            return False

        user = self.get_user()

        if user is None:
            self.username.errors.append('Unknown username')
            return False

        if not user.check_password(self.password.data):
            self.password.errors.append('Invalid password')
            return False

        return True

    def get_user(self):
        return db_models.db.session.query(db_models.User).filter_by(
            username=self.username.data).first()
