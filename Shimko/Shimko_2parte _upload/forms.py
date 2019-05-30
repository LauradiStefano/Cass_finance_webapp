import wtforms as wtf
import wtforms.fields.html5 as html5
from wtforms import SelectMultipleField
from wtforms.validators import InputRequired, DataRequired, Length, EqualTo
from wtforms.widgets import ListWidget, CheckboxInput

import db_models


class MultiCheckboxField(SelectMultipleField):
    widget = ListWidget(prefix_label=False)
    option_widget = CheckboxInput()


class ComputeForm(wtf.Form):
    file_name = wtf.FileField(label='Import File')
    price = wtf.FloatField(label='Spot Price', validators=[InputRequired()])
    risk_free = wtf.FloatField(label='Risk Free', default=5.04, validators=[InputRequired()])
    div_yield = wtf.FloatField(label='Dividend Yield', default=3.14, validators=[InputRequired()])

    risk_dividend = wtf.SelectField('Risk Free & Dividend Yield', choices=[('0', 'True'), ('1', 'False')], default='1')
    call_put_flag = wtf.RadioField('Call-Put', choices=[('0', 'Put'), ('1', 'Call'), ('2', 'Both')],
                                   validators=[InputRequired()], default='2')
    plot_choice = MultiCheckboxField('Plot', choices=[('0', 'Pdf Prices'), ('1', 'Cdf Prices'),
                                                      ('2', 'Cdf Returns')])
    button_compute = wtf.SubmitField(label='Compute')
    button_view_details = wtf.SubmitField(label='View Details')
    button_export_table = wtf.SubmitField(label='Export Table')


class RegistrationForm(wtf.Form):
    username = wtf.StringField(label='Username', validators=[DataRequired(), Length(min=4, max=25)])
    password = wtf.PasswordField(label='Password',
                                 validators=[DataRequired(), EqualTo('confirm', message='Passwords must match')])
    confirm = wtf.PasswordField(label='Confirm Password', validators=[DataRequired()])
    email = html5.EmailField(label='Email', validators=[Length(min=6, max=35)])
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
        label='Username', validators=[DataRequired()])
    password = wtf.PasswordField(label='Password', validators=[DataRequired()])
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
