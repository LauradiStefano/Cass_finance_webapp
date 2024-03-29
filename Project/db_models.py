from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

from app import app

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(10))
    first_name = db.Column(db.String(80))
    second_name = db.Column(db.String(80))
    organization = db.Column(db.String(80))
    job_title = db.Column(db.String(80))
    pw_hash = db.Column(db.String(80))
    email = db.Column(db.String(120), nullable=False, unique=True)

    def __repr__(self):
        return '<User %r>' % self.email

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
    file_name = db.Column(db.String())

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

    # CGMY distribution
    c = db.Column(db.Float())
    g = db.Column(db.Float())
    m = db.Column(db.Float())
    y = db.Column(db.Float())

    # NIG distribution
    sigma_nig = db.Column(db.Float())
    kappa_nig = db.Column(db.Float())
    theta_nig = db.Column(db.Float())

    # Gaussian distribution
    sigma_normal = db.Column(db.Float())

    # VG distribution
    sigma_vg = db.Column(db.Float())
    kappa_vg = db.Column(db.Float())
    theta_vg = db.Column(db.Float())

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

    # CEV distribution
    beta_cev = db.Column(db.Float())

    # CGMY distribution
    c = db.Column(db.Float())
    g = db.Column(db.Float())
    m = db.Column(db.Float())
    y = db.Column(db.Float())

    # DEJD distribution
    sigma_dejd = db.Column(db.Float())
    lam_dejd = db.Column(db.Float())
    rho_dejd = db.Column(db.Float())
    eta1_dejd = db.Column(db.Float())
    eta2_dejd = db.Column(db.Float())

    # Heston distribution
    volatility_t0 = db.Column(db.Float())
    alpha_heston = db.Column(db.Float())
    beta_heston = db.Column(db.Float())
    gamma_heston = db.Column(db.Float())
    rho_heston = db.Column(db.Float())

    # Meixner distribution
    a_meixner = db.Column(db.Float())
    b_meixner = db.Column(db.Float())
    delta_meixner = db.Column(db.Float())

    # MJD distribution
    sigma_mjd = db.Column(db.Float())
    lam_mjd = db.Column(db.Float())
    mu_x_mjd = db.Column(db.Float())
    sigma_x_mjd = db.Column(db.Float())

    # NIG distribution
    a_nig = db.Column(db.Float())
    b_nig = db.Column(db.Float())
    delta_nig = db.Column(db.Float())

    # GBM (Normal) distribution
    sigma_gaussian = db.Column(db.Float())

    # Exponential Gaussian (O-U) distribution
    epsilon_exp = db.Column(db.Float())
    k1_exp = db.Column(db.Float())
    sigma_exp = db.Column(db.Float())
    price_exp = db.Column(db.Float())
    strike_exp = db.Column(db.Float())
    risk_free_exp = db.Column(db.Float())
    time_exp = db.Column(db.Float())
    step_exp = db.Column(db.Float())
    upper_range_exp = db.Column(db.Float())
    lower_range_exp = db.Column(db.Float())

    # VG distribution
    sigma_vg = db.Column(db.Float())
    theta_vg = db.Column(db.Float())
    kappa_vg = db.Column(db.Float())

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


class term_structure(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    model_choice = db.Column(db.String())
    file_name = db.Column(db.String())

    # Cir distribution
    kappa_cir = db.Column(db.Float())
    theta_cir = db.Column(db.Float())
    sigma_cir = db.Column(db.Float())
    rho_cir = db.Column(db.Float())

    # Nelson Siegel distribution
    beta0_nelson = db.Column(db.Float())
    beta1_nelson = db.Column(db.Float())
    beta2_nelson = db.Column(db.Float())
    tau_nelson = db.Column(db.Float())

    # Svensson distribution
    beta0_svensson = db.Column(db.Float())
    beta1_svensson = db.Column(db.Float())
    beta2_svensson = db.Column(db.Float())
    beta3_svensson = db.Column(db.Float())
    tau1_svensson = db.Column(db.Float())
    tau2_svensson = db.Column(db.Float())

    # Vasicek distribution
    kappa_vasicek = db.Column(db.Float())
    theta_vasicek = db.Column(db.Float())
    sigma_vasicek = db.Column(db.Float())
    rho_vasicek = db.Column(db.Float())

    discount_factor = db.Column(db.String())
    least_fmin = db.Column(db.String())

    parameters = db.Column(db.String())
    time = db.Column(db.String())
    market_discount_factor = db.Column(db.String())
    model_discount_factor = db.Column(db.String())
    market_spot_rate = db.Column(db.String())
    model_spot_rate = db.Column(db.String())
    discount_factor_model_error = db.Column(db.String())
    spot_rate_model_error = db.Column(db.String())
    name_param = db.Column(db.String())
    number_of_time = db.Column(db.String())
    rmse_discount_factor = db.Column(db.Float())
    rmse_spot_rate = db.Column(db.Float())

    annual_basis_date = db.Column(db.String())
    daily_discount_factor = db.Column(db.String())
    daily_model_spot_rate = db.Column(db.String())
    dates = db.Column(db.String())

    button_compute = db.Column(db.Integer())
    button_export_table = db.Column(db.Integer())
    button_view_details = db.Column(db.Integer())

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('compute_term_structure', lazy='dynamic'))


class spread_option(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    price_1 = db.Column(db.Float())
    price_2 = db.Column(db.Float())
    dividend_yield_1 = db.Column(db.Float())
    dividend_yield_2 = db.Column(db.Float())
    volatility_1 = db.Column(db.Float())
    volatility_2 = db.Column(db.Float())

    strike = db.Column(db.Float())
    risk_free = db.Column(db.Float())
    time = db.Column(db.Float())
    rho = db.Column(db.Float())
    dump = db.Column(db.Float())
    spread_option_price = db.Column(db.Float())

    button_compute = db.Column(db.Integer())

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('compute_spread_option', lazy='dynamic'))


class statisitcal_analysis(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    method_choice = db.Column(db.String())
    file_name = db.Column(db.String())

    entry_date = db.Column(db.Date())
    end_date = db.Column(db.Date())

    mean = db.Column(db.String())
    variance = db.Column(db.String())
    volatility = db.Column(db.String())
    skewness = db.Column(db.String())
    kurtosis = db.Column(db.String())
    min_return = db.Column(db.String())
    max_return = db.Column(db.String())
    jb_test = db.Column(db.String())
    pvalue = db.Column(db.String())
    number_of_tickers = db.Column(db.Integer())
    tickers = db.Column(db.String())
    n_observation = db.Column(db.String())
    log_returns = db.Column(db.String())
    dates = db.Column(db.String())
    prices = db.Column(db.String())

    button_compute = db.Column(db.Integer())
    button_export_table = db.Column(db.Integer())
    button_add_field = db.Column(db.Integer())
    button_delete_field = db.Column(db.Integer())

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('compute_statistical_analysis', lazy='dynamic'))


class portfolio_analysis(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    file_name = db.Column(db.String())
    n_portfolio = db.Column(db.Integer())
    short_selling = db.Column(db.String())

    returns = db.Column(db.String())
    standard_deviations = db.Column(db.String())
    means = db.Column(db.String())
    efficient_means = db.Column(db.String())
    efficient_std = db.Column(db.String())
    efficient_weights = db.Column(db.String())
    tickers = db.Column(db.String())

    button_compute = db.Column(db.Integer())

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('compute_portfolio_analysis', lazy='dynamic'))


class mortgage(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    capital_amount = db.Column(db.Float())
    loan_term = db.Column(db.Float())
    frequency = db.Column(db.String())
    interest_rate = db.Column(db.Float())

    dates = db.Column(db.String())
    residual_debt = db.Column(db.String())
    capital_share = db.Column(db.String())
    interest_share = db.Column(db.String())
    debt_share = db.Column(db.String())
    rate_value = db.Column(db.Float())
    number_of_rates = db.Column(db.String())

    button_compute = db.Column(db.Integer())
    button_view_details = db.Column(db.Integer())
    button_export_table = db.Column(db.Integer())

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('compute_mortgage', lazy='dynamic'))


class principal_component_analysis(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    method_choice = db.Column(db.String())
    file_name = db.Column(db.String())
    asset_flag = db.Column(db.String())
    matrix_flag = db.Column(db.String())
    explained_variance = db.Column(db.Float())

    entry_date = db.Column(db.Date())
    end_date = db.Column(db.Date())

    evalues = db.Column(db.String())
    autovect = db.Column(db.String())
    pc_terms = db.Column(db.String())

    button_compute = db.Column(db.Integer())
    button_export_table = db.Column(db.Integer())
    button_add_field = db.Column(db.Integer())
    button_delete_field = db.Column(db.Integer())

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('compute_principal_component_analysis', lazy='dynamic'))


class temperature(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    file_name = db.Column(db.String())

    log_temp = db.Column(db.Integer())
    trend_temp_par = db.Column(db.Integer())
    lambda_zero = db.Column(db.Float())
    lambda_one = db.Column(db.Float())
    lambda_two = db.Column(db.Float())
    lambda_three = db.Column(db.Float())

    button_compute = db.Column(db.Integer())
    button_export_table = db.Column(db.Integer())
    button_add_field = db.Column(db.Integer())
    button_delete_field = db.Column(db.Integer())

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('compute_temperature', lazy='dynamic'))


class linear_interpolation_constant_forward(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    file_name = db.Column(db.String())
    model_choices = db.Column(db.String())
    time_plot = db.Column(db.String())
    daily_time_plot = db.Column(db.String())
    market_discount_factor = db.Column(db.String())
    model_discount_factor = db.Column(db.String())
    market_spot_rate = db.Column(db.String())
    model_spot_rate = db.Column(db.String())
    date_db = db.Column(db.String())

    button_compute = db.Column(db.Integer())
    button_export_table = db.Column(db.Integer())
    button_add_field = db.Column(db.Integer())
    button_delete_field = db.Column(db.Integer())

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('compute_linear_interpolation_constant_forward', lazy='dynamic'))


class monte_carlo_tools(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    model_choice = db.Column(db.String())

    mu_abm = db.Column(db.Float())
    sigma_abm = db.Column(db.Float())

    mu_cir = db.Column(db.Float())
    sigma_cir = db.Column(db.Float())
    alpha_cir = db.Column(db.Float())

    mu_dejd = db.Column(db.Float())
    sigma_dejd = db.Column(db.Float())
    lam_dejd = db.Column(db.Float())
    rho_dejd = db.Column(db.Float())
    eta1_dejd = db.Column(db.Float())
    eta2_dejd = db.Column(db.Float())

    mu_ewma = db.Column(db.Float())
    volatility_t0_ewma = db.Column(db.Float())
    alpha_ewma = db.Column(db.Float())
    beta_ewma = db.Column(db.Float())

    mu_garch = db.Column(db.Float())
    volatility_t0_garch = db.Column(db.Float())
    omega_garch = db.Column(db.Float())
    alpha_garch = db.Column(db.Float())
    beta_garch = db.Column(db.Float())
    asymm_garch = db.Column(db.Float())

    mu_gbm = db.Column(db.Float())
    sigma_gbm = db.Column(db.Float())

    mu_heston = db.Column(db.Float())
    volatility_t0_heston = db.Column(db.Float())
    alpha_heston = db.Column(db.Float())
    beta_heston = db.Column(db.Float())
    eta_heston = db.Column(db.Float())
    rho_heston = db.Column(db.Float())

    mu_mjd = db.Column(db.Float())
    sigma_mjd = db.Column(db.Float())
    lam_mjd = db.Column(db.Float())
    mu_x_mjd = db.Column(db.Float())
    sigma_x_mjd = db.Column(db.Float())

    mu_mrg = db.Column(db.Float())
    sigma_mrg = db.Column(db.Float())
    alpha_mrg = db.Column(db.Float())

    sigma_vg = db.Column(db.Float())
    thetha_vg = db.Column(db.Float())
    kappa_vg = db.Column(db.Float())

    price_abm = db.Column(db.Float())
    price_cir = db.Column(db.Float())
    price_dejd = db.Column(db.Float())
    price_ewma = db.Column(db.Float())
    price_garch = db.Column(db.Float())
    price_gbm = db.Column(db.Float())
    price_heston = db.Column(db.Float())
    price_mjd = db.Column(db.Float())
    price_mrg = db.Column(db.Float())
    price_vg = db.Column(db.Float())

    time = db.Column(db.Float())
    number_step = db.Column(db.Integer())
    number_paths = db.Column(db.Integer())

    simulated_paths = db.Column(db.String())
    timestep = db.Column(db.String())
    quantiles = db.Column(db.String())
    moments = db.Column(db.String())

    button_compute = db.Column(db.Integer())
    button_export_table = db.Column(db.Integer())
    button_view_details = db.Column(db.Integer())

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('compute_monte_carlo_tools', lazy='dynamic'))
