import wtforms as wtf
import wtforms.fields.html5 as html5
from wtforms import validators

import db_models


def check_vg_distribution(form, field):
    """Form validation: failure if T > 30 periods."""
    kappa = form.kappa.data
    theta = field.data
    if kappa < theta:
        raise validators.ValidationError('Kappa must be greater than Beta')


class ComputeForm(wtf.Form):
    type_choice = wtf.SelectField('Distribution',
                                  choices=[('0', 'Normal'), ('1', 'VG'), ('2', 'NIG'), ('3', 'CGMY')], default='0')

    mu = wtf.FloatField(label='Mu', default=0,
                        validators=[wtf.validators.InputRequired()])
    sigma_normal = wtf.FloatField(label='Sigma', default=0.12,
                                  validators=[wtf.validators.InputRequired(), validators.NumberRange(0, 1E+20)])
    sigma_vg = wtf.FloatField(label='Sigma', default=0.12,
                              validators=[wtf.validators.InputRequired(), validators.NumberRange(0, 1E+20)])
    kappa = wtf.FloatField(label='kappa', default=0.2,
                           validators=[wtf.validators.InputRequired()])
    theta = wtf.FloatField(label='Theta', default=-0.14,
                           validators=[wtf.validators.InputRequired(), check_vg_distribution])
    c = wtf.FloatField(label='C', default=1,
                       validators=[wtf.validators.InputRequired(), validators.NumberRange(0, 1E+20)])
    g = wtf.FloatField(label='G', default=5,
                       validators=[wtf.validators.InputRequired(), validators.NumberRange(0, 1E+20)])
    m = wtf.FloatField(label='M', default=5,
                       validators=[wtf.validators.InputRequired(), validators.NumberRange(0, 1E+20)])
    y = wtf.FloatField(label='Y', default=0.5,
                       validators=[wtf.validators.InputRequired(), validators.NumberRange(0.0001, 1.9999)])

    price = wtf.FloatField(label='Spot Price', default=100,
                           validators=[wtf.validators.InputRequired(), validators.NumberRange(0, 1E+20)])
    strike_min = wtf.FloatField(label='Strike Min', default=70,
                                validators=[wtf.validators.InputRequired(), validators.NumberRange(0, 1E+20)])
    strike_max = wtf.FloatField(label='Strike Max', default=130,
                                validators=[wtf.validators.InputRequired(), validators.NumberRange(0, 1E+20)])
    risk_free = wtf.FloatField(label='Risk Free', default=2, validators=[wtf.validators.InputRequired()])
    dividend_yield = wtf.FloatField(label='Dividend Yield', default=0, validators=[wtf.validators.InputRequired()])
    time = wtf.FloatField(label='Time to expiration', default=1,
                          validators=[wtf.validators.InputRequired(), validators.NumberRange(0, 1E+20)])
    call_put = wtf.RadioField('Call-Put', choices=[('0', 'Put'), ('1', 'Call')], default='1')

    button_compute = wtf.SubmitField(label='Compute')
    button_export_table = wtf.SubmitField(label='Export Table')
    button_view_details = wtf.SubmitField(label='View Details')


class RegistrationForm(wtf.Form):
    username = wtf.StringField(
        label='Username', validators=[wtf.validators.DataRequired(), validators.Length(min=4, max=25)])
    password = wtf.PasswordField(
        label='Password', validators=[
            wtf.validators.DataRequired(),
            wtf.validators.EqualTo('confirm', message='Passwords must match')])
    confirm = wtf.PasswordField(label='Confirm Password', validators=[wtf.validators.DataRequired()])
    email = html5.EmailField(label='Email', validators=[wtf.validators.DataRequired(),
                                                        validators.Email('Please enter your email address')])
    button_registration = wtf.SubmitField(label='Sign Up')

    def validate(self):
        if not wtf.Form.validate(self):
            return False

        if db_models.db.session.query(db_models.User).filter_by(username=self.username.data).count() > 0:
            self.username.errors.append('User already exists')
            return False

        return True


class LoginForm(wtf.Form):
    username = wtf.StringField(label='Username')
    password = wtf.PasswordField(label='Password')
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
