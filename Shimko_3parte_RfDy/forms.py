import db_models
import wtforms.fields.html5 as html5
import wtforms as wtf
from wtforms.validators import InputRequired, DataRequired, Length, EqualTo
from flask_wtf.file import FileRequired
from wtforms import SelectMultipleField
from wtforms.widgets import ListWidget, CheckboxInput


class MultiCheckboxField(SelectMultipleField):
    widget = ListWidget(prefix_label=False)
    option_widget = CheckboxInput()


class ComputeForm(wtf.Form):

    file_name = wtf.FileField(label='Import File')
    price = wtf.FloatField(label='Price', validators=[InputRequired()])
    risk_free = wtf.FloatField(label='Risk Free (%)', validators=[InputRequired()])
    div_yield = wtf.FloatField(label='Dividend Yield (%)', validators=[InputRequired()])
    call_put_flag = wtf.RadioField('Call/Put', choices=[('1', 'Call'), ('0', 'Put'), ('2', 'Both')],
                                   validators=[InputRequired()])
    plot_choice = MultiCheckboxField('Plot', choices=[('0', 'plotPrice'), ('1', 'plotCdfPrice'),
                                                      ('2', 'plotCdfReturns')], validators=[])
    button_compute = wtf.SubmitField(label='Compute')


class RegistrationForm(wtf.Form):
    username = wtf.StringField(label='Username', validators=[DataRequired(), Length(min=4, max=25)])
    password = wtf.PasswordField(label='Password',
                                 validators=[DataRequired(), EqualTo('confirm', message='Passwords must match')])
    confirm = wtf.PasswordField(label='Confirm Password', validators=[DataRequired()])
    email = html5.EmailField(label='Email', validators=[Length(min=6, max=35)])
    button_registration = wtf.SubmitField(label='Compute')

    def validate(self):
        if not wtf.Form.validate(self):
            return False

        if db_models.db.session.query(db_models.User).filter_by(username=self.username.data).count() > 0:
            self.username.errors.append('User already exists')
            return False

        return True


class Loginform(wtf.Form):
    username = wtf.StringField(
        label='Username', validators=[DataRequired()])
    password = wtf.PasswordField(label='Password', validators=[DataRequired()])
    button_login = wtf.SubmitField(label='Compute')

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
