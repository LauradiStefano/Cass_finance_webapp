import wtforms as wtf
import wtforms.fields.html5 as html5
from wtforms import validators

import db_models


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
