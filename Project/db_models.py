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


class shimko_theoretical_model(db.Model):
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

    user = db.relationship('User', backref=db.backref('compute_shimko_theoretical', lazy='dynamic'))


class shimko_market_model(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    strike_min = db.Column(db.Float())
    strike_max = db.Column(db.Float())
    price = db.Column(db.Float())
    time = db.Column(db.Float())
    call_put_flag = db.Column(db.String())
    plot_choice = db.Column(db.String())
    button_compute = db.Column(db.Integer())
    button_view_details = db.Column(db.Integer())
    button_export_table = db.Column(db.Integer())

    file_name = db.Column(db.String())

    strike_data = db.Column(db.String())
    a0 = db.Column(db.Float())
    a1 = db.Column(db.Float())
    a2 = db.Column(db.Float())
    strike_plot = db.Column(db.String())
    implied_volatility = db.Column(db.String())
    risk_free = db.Column(db.Float())
    div_yield = db.Column(db.Float())

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
    volatility_time = db.Column(db.String())
    r2 = db.Column(db.Float())
    returns_t = db.Column(db.String())
    skewness_normal = db.Column(db.Float())
    kurtosis_normal = db.Column(db.Float())
    cdf_prices = db.Column(db.String())
    cdf_returns = db.Column(db.String())
    cdf_bench_log_prices = db.Column(db.String())
    cdf_bench_norm_returns = db.Column(db.String())
    statistic_prices = db.Column(db.Float())
    statistic_returns = db.Column(db.Float())
    pvalue_prices = db.Column(db.Float())
    pvalue_returns = db.Column(db.Float())
    risk_dividend = db.Column(db.String())

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    user = db.relationship('User', backref=db.backref('compute_shimko_market', lazy='dynamic'))

    # relationship between Model-User and User-Model


class levy_process(db.Model):
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

    # Gaussian distribution
    sigma_normal = db.Column(db.Float())

    # VG distribution
    sigma_vg = db.Column(db.Float())
    kappa_vg = db.Column(db.Float())
    theta_vg = db.Column(db.Float())

    # NIG distribution
    sigma_nig = db.Column(db.Float())
    kappa_nig = db.Column(db.Float())
    theta_nig = db.Column(db.Float())

    # CGMY distribution
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
    user = db.relationship('User', backref=db.backref('compute_levy_process', lazy='dynamic'))


class heston_method(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    time = db.Column(db.Float())
    heston_pdf = db.Column(db.String())
    returns = db.Column(db.String())
    price = db.Column(db.Float())
    call_put = db.Column(db.String())
    risk_free = db.Column(db.Float())
    dividend_yield = db.Column(db.Float())
    strike_min = db.Column(db.Float())
    strike_max = db.Column(db.Float())
    strike = db.Column(db.String())
    implied_volatility = db.Column(db.String())
    option_prices = db.Column(db.String())
    number_of_strike = db.Column(db.String())
    norm_pdf = db.Column(db.String())
    mean = db.Column(db.Float())
    variance = db.Column(db.Float())
    skewness = db.Column(db.Float())
    kurtosis = db.Column(db.Float())

    mu = db.Column(db.Float())
    volatility_t0 = db.Column(db.Float())
    volatility_hat = db.Column(db.Float())
    lam = db.Column(db.Float())
    chi = db.Column(db.Float())
    rho = db.Column(db.Float())

    button_compute = db.Column(db.Integer())
    button_export_table = db.Column(db.Integer())
    button_view_details = db.Column(db.Integer())

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('compute_heston_method', lazy='dynamic'))


class asian_option(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    model_choice = db.Column(db.String())

    # GBM distribution
    sigma_gaussian = db.Column(db.Float())

    # VG distribution
    sigma_vg = db.Column(db.Float())
    theta = db.Column(db.Float())
    kappa = db.Column(db.Float())

    # Heston distribution
    volatility_t0 = db.Column(db.Float())
    alpha_heston = db.Column(db.Float())
    beta_heston = db.Column(db.Float())
    gamma_heston = db.Column(db.Float())
    rho_heston = db.Column(db.Float())

    # NIG distribution
    a_nig = db.Column(db.Float())
    b_nig = db.Column(db.Float())
    delta_nig = db.Column(db.Float())

    # CGMY distribution
    c = db.Column(db.Float())
    g = db.Column(db.Float())
    m = db.Column(db.Float())
    y = db.Column(db.Float())

    # Meixner distribution
    a_meixner = db.Column(db.Float())
    b_meixner = db.Column(db.Float())
    delta_meixner = db.Column(db.Float())

    # MJD distribution
    sigma_mjd = db.Column(db.Float())
    lam_mjd = db.Column(db.Float())
    mu_x_mjd = db.Column(db.Float())
    sigma_x_mjd = db.Column(db.Float())

    # DEJD distribution
    sigma_dejd = db.Column(db.Float())
    lam_dejd = db.Column(db.Float())
    rho_dejd = db.Column(db.Float())
    eta1_dejd = db.Column(db.Float())
    eta2_dejd = db.Column(db.Float())

    # CEV distribution
    beta_cev = db.Column(db.Float())

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
    user = db.relationship('User', backref=db.backref('compute_asian_option', lazy='dynamic'))
