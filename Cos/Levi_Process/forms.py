import db_models
import wtforms as wtf
import wtforms.fields.html5 as html5


class ComputeForm(wtf.Form):
    type_choice = wtf.SelectField('Distribution',
                                  choices=[('1', 'Normal'), ('2', 'VG'), ('3', 'NIG'), ('4', 'CGMY')], default='1')

    mu = wtf.FloatField(label='Mu', default=0)
    sigma = wtf.FloatField(label='Sigma', default=0.12)
    kappa = wtf.FloatField(label='kappa', default=0.2)
    theta = wtf.FloatField(label='Theta', default=-0.14)
    c = wtf.FloatField(label='C', default=1)
    g = wtf.FloatField(label='G', default=5)
    m = wtf.FloatField(label='M', default=5)
    y = wtf.FloatField(label='Y', default=0.5)

    price = wtf.FloatField(label='Price', default=100, validators=[wtf.validators.InputRequired()])
    strike_min = wtf.FloatField(label='Strike Min', default=70, validators=[wtf.validators.InputRequired()])
    strike_max = wtf.FloatField(label='Strike Max', default=130, validators=[wtf.validators.InputRequired()])
    risk_free = wtf.FloatField(label='Risk Free (%)', default=2, validators=[wtf.validators.InputRequired()])
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
