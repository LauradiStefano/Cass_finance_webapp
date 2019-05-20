import wtforms as wtf
import wtforms.fields.html5 as html5

import db_models


class ComputeForm(wtf.Form):
    model_choice = wtf.SelectField('Model',
                                   choices=[('0', 'GBM'), ('1', 'VG'), ('2', 'Heston'), ('3', 'NIG'), ('4', 'CGMY')],
                                   default='0')

    sigma_gaussian = wtf.FloatField(label='Sigma', default=0.17801)

    sigma_vg = wtf.FloatField(label='Sigma', default=0.180022)
    theta = wtf.FloatField(label='Theta', default=-0.136105)
    kappa = wtf.FloatField(label='Kappa', default=0.736703)

    volatility_t0 = wtf.FloatField(label='V0', default=0.0102)
    alpha_heston = wtf.FloatField(label='Alpha', default=6.21)
    beta_heston = wtf.FloatField(label='Beta', default=0.019)
    eta = wtf.FloatField(label='Eta', default=0.61)
    rho = wtf.FloatField(label='Rho', default=-0.79)

    alpha_nig = wtf.FloatField(label='Alpha', default=6.1882)
    beta_nig = wtf.FloatField(label='Beta', default=-3.8941)
    delta_nig = wtf.FloatField(label='Delta', default=0.1622)

    c = wtf.FloatField(label='C', default=0.0244)
    g = wtf.FloatField(label='G', default=0.0765)
    m = wtf.FloatField(label='M', default=7.5515)
    y = wtf.FloatField(label='Y', default=1.2945)

    grid = wtf.FloatField(label='Grid Point (2^)', default=15)
    upper_range = wtf.FloatField(label='Upper Range', default=2)
    lower_range = wtf.FloatField(label='Lower Range', default=-2)
    dump = wtf.FloatField(label='Dump Parameter', default=1.5)
    tolerance = wtf.FloatField(label='Tolerance', default=50)

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
