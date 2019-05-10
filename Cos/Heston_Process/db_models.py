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

    time = db.Column(db.Float())
    heston_pdf = db.Column(db.String())
    returns = db.Column(db.String())
    price = db.Column(db.Float())
    call_put = db.Column(db.Integer())
    risk_free = db.Column(db.Float())
    dividend_yield = db.Column(db.Float())
    strike_min = db.Column(db.Float())
    strike_max = db.Column(db.Float())
    strike = db.Column(db.String())
    implied_volatility = db.Column(db.String())

    mu = db.Column(db.Float())
    volatility_t0 = db.Column(db.Float())
    volatility_hat = db.Column(db.Float())
    lam = db.Column(db.Float())
    chi = db.Column(db.Float())
    rho = db.Column(db.Float())

    button_compute = db.Column(db.Integer())

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User',
                           backref=db.backref('Compute', lazy='dynamic'))
