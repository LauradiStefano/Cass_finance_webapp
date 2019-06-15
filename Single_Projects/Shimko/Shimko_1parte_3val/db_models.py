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

    strike_min = db.Column(db.Float())
    strike_atm = db.Column(db.Float())
    strike_max = db.Column(db.Float())
    volatility_min = db.Column(db.Float())
    volatility_atm = db.Column(db.Float())
    volatility_max = db.Column(db.Float())
    price = db.Column(db.Float())
    risk_free = db.Column(db.Float())
    div_yield = db.Column(db.Float())
    time = db.Column(db.Float())
    button_compute = db.Column(db.Integer())
    button_view_details = db.Column(db.Integer())
    button_export_table = db.Column(db.Integer())

    a0 = db.Column(db.Float())
    a1 = db.Column(db.Float())
    a2 = db.Column(db.Float())
    strike = db.Column(db.String())
    implied_volatility = db.Column(db.String())
    volatility = db.Column(db.String())
    st = db.Column(db.String())
    pdf = db.Column(db.String())
    pdf_returns = db.Column(db.String())
    area_prices = db.Column(db.Float())
    expected_price = db.Column(db.Float())
    sigma2_price = db.Column(db.Float())
    skewness_prices = db.Column(db.Float())
    kurtosis_prices = db.Column(db.Float())
    skewness_prices_log_n = db.Column(db.Float())
    kurtosis_prices_log_n = db.Column(db.Float())
    area_returns = db.Column(db.Float())
    m1_returns = db.Column(db.Float())
    m2_returns = db.Column(db.Float())
    skewness_log_returns = db.Column(db.Float())
    kurtosis_log_returns = db.Column(db.Float())
    pdf_bench_log_prices = db.Column(db.String())
    pdf_bench_norm_returns = db.Column(db.String())
    ret_t = db.Column(db.String())
    skewness_normal = db.Column(db.Float())
    kurtosis_normal = db.Column(db.Float())
    cdf_prices = db.Column(db.String())
    cdf_returns = db.Column(db.String())
    cdf_bench_norm_returns = db.Column(db.String())
    cdf_bench_log_prices = db.Column(db.String())
    statistic_prices = db.Column(db.Float())
    statistic_returns = db.Column(db.Float())
    pvalue_prices = db.Column(db.Float())
    pvalue_returns = db.Column(db.Float())

    plot_choice = db.Column(db.String())

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User',
                           backref=db.backref('Compute', lazy='dynamic'))
