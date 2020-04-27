from string import ascii_uppercase, ascii_lowercase, digits

import wtforms as wtf
import wtforms.fields.html5 as html5
from flask_wtf import RecaptchaField
from wtforms import validators

import db_models


def contains(required_chars, s):
    return any(c in required_chars for c in s)


def contains_upper(s):
    return contains(ascii_uppercase, s)


def contains_lower(s):
    return contains(ascii_lowercase, s)


def contains_digit(s):
    return contains(digits, s)


def contains_special(s):
    return contains(r"""!@$%^&*()_-+={}[]|\,.></?~`"':;""", s)


def length(s):
    return len(s) >= 5


def check_password(form, field):
    password = form.password.data

    if not length(password):
        raise validators.ValidationError('Password must be at least 5 characters long')

    if not contains_upper(password):
        raise validators.ValidationError('Password must contain at least one upper case character')

    if not contains_lower(password):
        raise validators.ValidationError('Password must contain at least one lower case character')

    if not contains_digit(password):
        raise validators.ValidationError('Password must contain at least one number')

    if not contains_special(password):
        raise validators.ValidationError('Password must contain at least one special characters')


class RegistrationForm(wtf.Form):
    title = wtf.SelectField('Title', choices=[('0', 'Mr'), ('1', 'Mrs'), ('3', 'Ms')], default='0')

    first_name = wtf.StringField(label='Given Name',
                                 validators=[wtf.validators.DataRequired(), validators.Length(min=4, max=25)])
    second_name = wtf.StringField(
        label='Family Name', validators=[wtf.validators.DataRequired(), validators.Length(min=4, max=25)])
    organization = wtf.StringField(
        label='Organization', validators=[wtf.validators.DataRequired(), validators.Length(min=3, max=40)])
    job_title = wtf.StringField(
        label='Job Title', validators=[wtf.validators.DataRequired(), validators.Length(min=4, max=40)])
    password = wtf.PasswordField(label='Create Password',
                                 validators=[wtf.validators.DataRequired(),
                                             wtf.validators.EqualTo('confirm', message='Passwords must match'),
                                             check_password])
    confirm = wtf.PasswordField(label='Verify Password', validators=[wtf.validators.DataRequired()])

    email = html5.EmailField(label='Email',
                             validators=[wtf.validators.DataRequired(),
                                         validators.Length(min=6, message='Please enter a valid email address'),
                                         validators.Email('Please enter a valid email address')])
    recaptcha = RecaptchaField()
    button_registration = wtf.SubmitField(label='Sign Up')

    def validate(self):
        if not wtf.Form.validate(self):
            return False

        if db_models.db.session.query(db_models.User).filter_by(email=self.email.data).count() > 0:
            self.email.errors.append('User already exists')
            return False

        return True


class LoginForm(wtf.Form):
    email = html5.EmailField(label='Email')
    password = wtf.PasswordField(label='Password')
    button_login = wtf.SubmitField(label='Log In')

    def validate(self):
        if not wtf.Form.validate(self):
            return False

        user = self.get_user()

        if user is None:
            self.email.errors.append('Unknown user')
            return False

        if not user.check_password(self.password.data):
            self.password.errors.append('Invalid password')
            return False

        return True

    def get_user(self):
        return db_models.db.session.query(db_models.User).filter_by(
            email=self.email.data).first()
