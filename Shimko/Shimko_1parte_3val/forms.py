import wtforms as wtf
import wtforms.fields.html5 as html5
from wtforms import SelectMultipleField, validators
from wtforms.widgets import ListWidget, CheckboxInput

import db_models


class MultiCheckboxField(SelectMultipleField):
    widget = ListWidget(prefix_label=False)
    option_widget = CheckboxInput()


class ComputeForm(wtf.Form):
    strike_min = wtf.FloatField(label='Min Strike', default=325,
                                validators=[wtf.validators.InputRequired(), validators.NumberRange(0, 1E+20)])

    strike_atm = wtf.FloatField(label='Atm Strike', default=390,
                                validators=[wtf.validators.InputRequired(), validators.NumberRange(0, 1E+20)])
    strike_max = wtf.FloatField(label='Max Strike', default=425,
                                validators=[wtf.validators.InputRequired(), validators.NumberRange(0, 1E+20)])

    volatility_min = wtf.FloatField(label='Min Volatility ', default=11.3,
                                    validators=[wtf.validators.InputRequired(), validators.NumberRange(0, 1E+20)])
    volatility_atm = wtf.FloatField(label='Atm Volatility', default=6.5,
                                    validators=[wtf.validators.InputRequired(), validators.NumberRange(0, 1E+20)])
    volatility_max = wtf.FloatField(label='Max Volatility', default=4.5,
                                    validators=[wtf.validators.InputRequired(), validators.NumberRange(0, 1E+20)])
    price = wtf.FloatField(label='Spot Price', default=387,
                           validators=[wtf.validators.InputRequired(), validators.NumberRange(0, 1E+20)])
    risk_free = wtf.FloatField(label='Risk Free', default=5.04, validators=[wtf.validators.InputRequired()])
    div_yield = wtf.FloatField(label='Dividend Yield', default=0, validators=[wtf.validators.InputRequired()])
    time = wtf.FloatField(label='Time to expiration', default=0.1666,
                          validators=[wtf.validators.InputRequired(), validators.NumberRange(0, 1E+20)])
    plot_choice = MultiCheckboxField('Plot', choices=[('0', 'Pdf Prices'), ('1', 'Cdf Prices'),
                                                      ('2', 'Cdf Returns')])
    button_compute = wtf.SubmitField(label='Compute')
    button_view_details = wtf.SubmitField(label='View Details')
    button_export_table = wtf.SubmitField(label='Export Table')


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


class LoginForm(wtf.Form):
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
