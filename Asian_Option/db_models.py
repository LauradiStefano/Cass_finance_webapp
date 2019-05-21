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

    model_choice = db.Column(db.String())

    sigma_gaussian = db.Column(db.Float())

    sigma_vg = db.Column(db.Float())
    theta = db.Column(db.Float())
    kappa = db.Column(db.Float())

    volatility_t0 = db.Column(db.Float())
    alpha_heston = db.Column(db.Float())
    beta_heston = db.Column(db.Float())
    eta_heston = db.Column(db.Float())
    rho_heston = db.Column(db.Float())

    alpha_nig = db.Column(db.Float())
    beta_nig = db.Column(db.Float())
    delta_nig = db.Column(db.Float())

    c = db.Column(db.Float())
    g = db.Column(db.Float())
    m = db.Column(db.Float())
    y = db.Column(db.Float())

    alpha_meixner = db.Column(db.Float())
    beta_meixner = db.Column(db.Float())
    delta_meixner = db.Column(db.Float())

    sigma_mjd = db.Column(db.Float())
    lam_mjd = db.Column(db.Float())
    mu_x_mjd = db.Column(db.Float())
    sigma_x_mjd = db.Column(db.Float())

    sigma_dejd = db.Column(db.Float())
    lam_dejd = db.Column(db.Float())
    rho_dejd = db.Column(db.Float())
    eta1_dejd = db.Column(db.Float())
    eta2_dejd = db.Column(db.Float())

    grid = db.Column(db.Float())
    upper_range = db.Column(db.Float())
    lower_range = db.Column(db.Float())
    dump = db.Column(db.Float())
    tolerance = db.Column(db.Float())

    price = db.Column(db.Float())
    risk_free = db.Column(db.Float())
    time = db.Column(db.Float())
    step = db.Column(db.Float())
    strike = db.Column(db.Float())

    lam = db.Column(db.String())
    lower_bound = db.Column(db.String())
    optimal_strike = db.Column(db.Float())
    optimal_lower_bound = db.Column(db.Float())
    lower_bound_strike = db.Column(db.Float())

    button_compute = db.Column(db.Integer())

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User',
                           backref=db.backref('Compute', lazy='dynamic'))
