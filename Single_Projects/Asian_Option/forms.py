import math

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


def check_nig_distribution(form, field):
    """Form validation: failure if T > 30 periods."""
    a_nig = form.a_nig.data
    b_nig = field.data

    if abs(b_nig) < 0 or abs(b_nig) > a_nig:
        raise validators.ValidationError('Beta must be between 0 and alpha')


class ComputeForm(wtf.Form):
    model_choice = wtf.SelectField('Distribution',
                                   choices=[('0', 'GBM'), ('1', 'VG'), ('2', 'Heston'), ('3', 'NIG'), ('4', 'CGMY'),
                                            ('5', 'Meixner'), ('6', 'MJD'), ('7', 'DEJD'), ('8', 'CEV')], default='0')

    # GBM distribution
    sigma_gaussian = wtf.FloatField(label='Sigma', default=0.17801,
                                    validators=[wtf.validators.InputRequired(), validators.NumberRange(0, 1E+20)])

    # VG distribution
    sigma_vg = wtf.FloatField(label='Sigma', default=0.180022,
                              validators=[wtf.validators.InputRequired(), validators.NumberRange(0, 1E+20)])
    theta = wtf.FloatField(label='Theta', default=-0.136105,
                           validators=[wtf.validators.InputRequired(), check_vg_distribution])
    kappa = wtf.FloatField(label='Kappa', default=0.736703, validators=[wtf.validators.InputRequired()])

    # Heston distribution
    volatility_t0 = wtf.FloatField(label='V0', default=0.0102,
                                   validators=[wtf.validators.InputRequired(), validators.NumberRange(0, 1E+20)])
    alpha_heston = wtf.FloatField(label='Alpha', default=6.21,
                                  validators=[wtf.validators.InputRequired(), validators.NumberRange(0, 1E+20)])
    beta_heston = wtf.FloatField(label='Beta', default=0.019,
                                 validators=[wtf.validators.InputRequired(), validators.NumberRange(0, 1E+20)])
    gamma_heston = wtf.FloatField(label='Eta', default=0.61,
                                  validators=[wtf.validators.InputRequired(), validators.NumberRange(0, 1E+20)])
    rho_heston = wtf.FloatField(label='Rho', default=-0.79,
                                validators=[wtf.validators.InputRequired(), validators.NumberRange(-1, 1)])

    # NIG distribution
    a_nig = wtf.FloatField(label='A', default=6.1882, validators=[wtf.validators.InputRequired()])
    b_nig = wtf.FloatField(label='B', default=-3.8941,
                           validators=[wtf.validators.InputRequired(), check_nig_distribution])
    delta_nig = wtf.FloatField(label='Delta', default=0.1622,
                               validators=[wtf.validators.InputRequired(), validators.NumberRange(0, 1E+20)])

    # CGMY distribution
    c = wtf.FloatField(label='C', default=0.0244,
                       validators=[wtf.validators.InputRequired(), validators.NumberRange(0, 1E+20)])
    g = wtf.FloatField(label='G', default=0.0765,
                       validators=[wtf.validators.InputRequired(), validators.NumberRange(0, 1E+20)])
    m = wtf.FloatField(label='M', default=7.5515,
                       validators=[wtf.validators.InputRequired(), validators.NumberRange(0, 1E+20)])
    y = wtf.FloatField(label='Y', default=1.2945,
                       validators=[wtf.validators.InputRequired(), validators.NumberRange(0.0001, 1.9999)])

    # Meixner distribution
    a_meixner = wtf.FloatField(label='A', default=0.3977,
                               validators=[wtf.validators.InputRequired(), validators.NumberRange(0, 1E+20)])
    b_meixner = wtf.FloatField(label='B', default=-1.494,
                               validators=[wtf.validators.InputRequired(), validators.NumberRange(-math.pi, math.pi)])
    delta_meixner = wtf.FloatField(label='Delta', default=0.3462,
                                   validators=[wtf.validators.InputRequired(), validators.NumberRange(0, 1E+20)])

    # MJD distribution
    sigma_mjd = wtf.FloatField(label='Sigma', default=0.126349,
                               validators=[wtf.validators.InputRequired(), validators.NumberRange(0, 1E+20)])
    lam_mjd = wtf.FloatField(label='Lambda', default=0.174814, validators=[wtf.validators.InputRequired()])
    mu_x_mjd = wtf.FloatField(label='Mu', default=-0.390078, validators=[wtf.validators.InputRequired()])
    sigma_x_mjd = wtf.FloatField(label='Sigma', default=0.338796,
                                 validators=[wtf.validators.InputRequired(), validators.NumberRange(0, 1E+20)])

    # DEJD distribution
    sigma_dejd = wtf.FloatField(label='Sigma', default=0.120381,
                                validators=[wtf.validators.InputRequired(), validators.NumberRange(0, 1E+20)])
    lam_dejd = wtf.FloatField(label='Lambda', default=0.330966, validators=[wtf.validators.InputRequired()])
    rho_dejd = wtf.FloatField(label='Rho', default=0.20761, validators=[wtf.validators.InputRequired()])
    eta1_dejd = wtf.FloatField(label='Eta 1', default=9.65997, validators=[wtf.validators.InputRequired()])
    eta2_dejd = wtf.FloatField(label='Eta 2', default=3.13868, validators=[wtf.validators.InputRequired()])

    # CEV distribution
    beta_cev = wtf.FloatField(label='Beta', default=-0.25,
                              validators=[wtf.validators.InputRequired(), validators.NumberRange(-1, 1E+20)])

    grid = wtf.FloatField(label='Grid Point (2^)', default=15,
                          validators=[wtf.validators.InputRequired(), validators.NumberRange(2, 20)])
    upper_range = wtf.FloatField(label='Upper Range', default=2, validators=[wtf.validators.InputRequired()])
    lower_range = wtf.FloatField(label='Lower Range', default=-2, validators=[wtf.validators.InputRequired()])
    dump = wtf.FloatField(label='Dump Parameter', default=1.5, validators=[wtf.validators.InputRequired()])
    tolerance = wtf.FloatField(label='Tolerance', default=0.00001, validators=[wtf.validators.InputRequired()])

    price = wtf.FloatField(label='Spot Price', default=100,
                           validators=[wtf.validators.InputRequired(), validators.NumberRange(0, 1E+20)])
    risk_free = wtf.FloatField(label='Risk Free', default=3.67, validators=[wtf.validators.InputRequired()])
    # dividend_yield = wtf.FloatField(label='Dividend Yield (%)', default=0,
    #                                 validators=[wtf.validators.InputRequired()])
    time = wtf.FloatField(label='Time to Maturity', default=1,
                          validators=[wtf.validators.InputRequired(), validators.NumberRange(0, 1E+20)])
    step = wtf.FloatField(label='Monitoring Frequency', default=12,
                          validators=[wtf.validators.InputRequired(), validators.NumberRange(0, 1E+20)])
    strike = wtf.FloatField(label='Strike', default=100,
                            validators=[wtf.validators.InputRequired(), validators.NumberRange(0, 1E+20)])

    button_compute = wtf.SubmitField(label='Compute')
    # button_export_table = wtf.SubmitField(label='Export Table')
    # button_table = wtf.SubmitField(label='View Details')


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
