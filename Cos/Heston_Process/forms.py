import wtforms as wtf
import db_models
import wtforms.fields.html5 as html5
from wtforms.widgets import ListWidget, CheckboxInput
from wtforms import SelectMultipleField


class MultiCheckboxField(SelectMultipleField):
    widget = ListWidget(prefix_label=False)
    option_widget = CheckboxInput()


class ComputeForm(wtf.Form):

    mu = wtf.FloatField(label='Mu', default=4.4579)
    volatility_t0 = wtf.FloatField(label='Vol t0', default=0.0175)
    volatility_hat = wtf.FloatField(label='Vol hat', default=0.0398)
    lam = wtf.FloatField(label='Lamda', default=1.5768)
    chi = wtf.FloatField(label='Chi', default=0.5751)
    rho = wtf.FloatField(label='Rho', default=-0.5711)

    price = wtf.FloatField(label='Price', default=100, validators=[wtf.validators.InputRequired()])
    strike_min = wtf.FloatField(label='Strike Min', default=70, validators=[wtf.validators.InputRequired()])
    strike_max = wtf.FloatField(label='Strike Max', default=130, validators=[wtf.validators.InputRequired()])
    risk_free = wtf.FloatField(label='Risk Free (%)', default=0, validators=[wtf.validators.InputRequired()])
    dividend_yield = wtf.FloatField(label='Dividend Yield (%)', default=0,
                                    validators=[wtf.validators.InputRequired()])
    time = wtf.FloatField(label='Time expiration', default=1, validators=[wtf.validators.InputRequired()])
    call_put = wtf.RadioField('Call/Put', choices=[('1', 'Call'), ('0', 'Put')], default='1')

    button_compute = wtf.SubmitField(label='Compute')
    button_export_table = wtf.SubmitField(label='Export Table')
    button_view_details = wtf.SubmitField(label='View Details')


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
