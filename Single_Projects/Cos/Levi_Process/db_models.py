from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from app import app

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    pw_hash = db.Column(db.String(80))
    email = db.Column(db.String(120), nullable=True)

    def __repr__(self):
        return '<User %r>' % self.username

    def check_password(self, pw):
        return check_password_hash(self.pw_hash, pw)

    def set_password(self, pw):
        self.pw_hash = generate_password_hash(pw)

    def is_authenticated(self):
        # Return True if the user is authenticated
        return True

    def is_active(self):
        # True, as all users are active."""
        return True

    def is_anonymous(self):
        # False, as anonymous users aren't supported.
        return False

    def get_id(self):
        return self.id


class Compute(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    parameters = db.Column(db.String())
    time = db.Column(db.Float())
    pdf_underlying_asset = db.Column(db.String())
    underlying_prices = db.Column(db.String())
    price = db.Column(db.Float())
    call_put = db.Column(db.String())
    risk_free = db.Column(db.Float())
    dividend_yield = db.Column(db.Float())
    option_prices = db.Column(db.String())
    strike_min = db.Column(db.Float())
    strike_max = db.Column(db.Float())
    strike = db.Column(db.String())
    implied_volatility = db.Column(db.String())
    norm_pdf = db.Column(db.String())
    type_choice = db.Column(db.String())
    number_of_strike = db.Column(db.String())

    mu = db.Column(db.Float())
    sigma_normal = db.Column(db.Float())
    sigma_vg = db.Column(db.Float())
    kappa = db.Column(db.Float())
    theta = db.Column(db.Float())
    c = db.Column(db.Float())
    g = db.Column(db.Float())
    m = db.Column(db.Float())
    y = db.Column(db.Float())

    mean = db.Column(db.Float())
    variance = db.Column(db.Float())
    skewness = db.Column(db.Float())
    kurtosis = db.Column(db.Float())

    button_compute = db.Column(db.Integer())
    button_export_table = db.Column(db.Integer())
    button_view_details = db.Column(db.Integer())

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User',
                           backref=db.backref('Compute', lazy='dynamic'))
