import math

import wtforms as wtf
from wtforms import validators


def check_vg_distribution(form, field):
    """Form validation: failure if T > 30 periods."""
    kappa = form.kappa_vg.data
    theta = field.data
    if kappa < theta:
        raise validators.ValidationError('Kappa must be greater than Beta')


def check_nig_distribution(form, field):
    """Form validation: failure if T > 30 periods."""
    a_nig = form.a_nig.data
    b_nig = field.data

    if abs(b_nig) < 0 or abs(b_nig) > a_nig:
        raise validators.ValidationError('Beta must be between 0 and alpha')


class ComputeForm(wtf.Form):
    model_choice = wtf.SelectField('Model',
                                   choices=[('0', 'Normal'), ('1', 'VG'), ('2', 'Heston'), ('3', 'NIG'), ('4', 'CGMY'),
                                            ('5', 'Meixner'), ('6', 'MJD'), ('7', 'DEJD'), ('8', 'CEV'), ('9', 'O-U')],
                                   default='0')

    # GBM distribution
    sigma_gaussian = wtf.FloatField(label='$$ \sigma $$', default=0.17801,
                                    validators=[wtf.validators.InputRequired(), validators.NumberRange(0, 1E+20)])

    # VG distribution
    sigma_vg = wtf.FloatField(label='$$ \sigma $$', default=0.180022,
                              validators=[wtf.validators.InputRequired(), validators.NumberRange(0, 1E+20)])
    theta_vg = wtf.FloatField(label=r'$$ \theta $$', default=-0.136105,
                              validators=[wtf.validators.InputRequired(), check_vg_distribution])
    kappa_vg = wtf.FloatField(label='$$ v $$', default=0.736703, validators=[wtf.validators.InputRequired()])

    # Heston distribution
    volatility_t0 = wtf.FloatField(label='$$ \ v_{0} $$', default=0.0102,
                                   validators=[wtf.validators.InputRequired(), validators.NumberRange(0, 1E+20)])
    alpha_heston = wtf.FloatField(label=r'$$ \alpha $$', default=6.21,
                                  validators=[wtf.validators.InputRequired(), validators.NumberRange(0, 1E+20)])
    beta_heston = wtf.FloatField(label=r'$$ \beta $$', default=0.019,
                                 validators=[wtf.validators.InputRequired(), validators.NumberRange(0, 1E+20)])
    gamma_heston = wtf.FloatField(label='$$ \gamma $$', default=0.61,
                                  validators=[wtf.validators.InputRequired(), validators.NumberRange(0, 1E+20)])
    rho_heston = wtf.FloatField(label=r'$$ \rho $$', default=-0.79,
                                validators=[wtf.validators.InputRequired(), validators.NumberRange(-1, 1)])

    # NIG distribution
    a_nig = wtf.FloatField(label='$$ a $$', default=6.1882, validators=[wtf.validators.InputRequired()])
    b_nig = wtf.FloatField(label='$$ b $$', default=-3.8941,
                           validators=[wtf.validators.InputRequired(), check_nig_distribution])
    delta_nig = wtf.FloatField(label='$$ \delta $$', default=0.1622,
                               validators=[wtf.validators.InputRequired(), validators.NumberRange(0, 1E+20)])

    # CGMY distribution
    c = wtf.FloatField(label='$$ C $$', default=0.0244,
                       validators=[wtf.validators.InputRequired(), validators.NumberRange(0, 1E+20)])
    g = wtf.FloatField(label='$$ G $$', default=0.0765,
                       validators=[wtf.validators.InputRequired(), validators.NumberRange(0, 1E+20)])
    m = wtf.FloatField(label='$$ M $$', default=7.5515,
                       validators=[wtf.validators.InputRequired(), validators.NumberRange(0, 1E+20)])
    y = wtf.FloatField(label='$$ Y $$', default=1.2945,
                       validators=[wtf.validators.InputRequired(), validators.NumberRange(0.0001, 1.9999)])

    # Meixner distribution
    a_meixner = wtf.FloatField(label='$$ a $$', default=0.3977,
                               validators=[wtf.validators.InputRequired(), validators.NumberRange(0, 1E+20)])
    b_meixner = wtf.FloatField(label='$$ b $$', default=-1.494,
                               validators=[wtf.validators.InputRequired(), validators.NumberRange(-math.pi, math.pi)])
    delta_meixner = wtf.FloatField(label='$$ \delta $$', default=0.3462,
                                   validators=[wtf.validators.InputRequired(), validators.NumberRange(0, 1E+20)])

    # MJD distribution
    sigma_mjd = wtf.FloatField(label='$$ \sigma $$', default=0.126349,
                               validators=[wtf.validators.InputRequired(), validators.NumberRange(0, 1E+20)])
    lam_mjd = wtf.FloatField(label='$$ l $$', default=0.174814, validators=[wtf.validators.InputRequired()])
    mu_x_mjd = wtf.FloatField(label='$$ \mu_{x} $$', default=-0.390078, validators=[wtf.validators.InputRequired()])
    sigma_x_mjd = wtf.FloatField(label='$$ \sigma_{x} $$', default=0.338796,
                                 validators=[wtf.validators.InputRequired(), validators.NumberRange(0, 1E+20)])

    # DEJD distribution
    sigma_dejd = wtf.FloatField(label='$$ \sigma $$', default=0.120381,
                                validators=[wtf.validators.InputRequired(), validators.NumberRange(0, 1E+20)])
    lam_dejd = wtf.FloatField(label='$$ l $$', default=0.330966, validators=[wtf.validators.InputRequired()])
    rho_dejd = wtf.FloatField(label=r'$$ \rho $$', default=0.20761, validators=[wtf.validators.InputRequired()])
    eta1_dejd = wtf.FloatField(label='$$ \eta_{1} $$', default=9.65997, validators=[wtf.validators.InputRequired()])
    eta2_dejd = wtf.FloatField(label='$$ \eta_{2} $$', default=3.13868, validators=[wtf.validators.InputRequired()])

    # CEV distribution
    beta_cev = wtf.FloatField(label=r'$$ \beta $$', default=-0.25,
                              validators=[wtf.validators.InputRequired(), validators.NumberRange(-1, 1E+20)])

    # Exponential Gaussian distribution

    epsilon_exp = wtf.FloatField(label=r'$$ \varepsilon $$', default=4.282364642,
                                 validators=[wtf.validators.InputRequired(), validators.NumberRange(-1, 1E+20)])
    k1_exp = wtf.FloatField(label='$$ \kappa_{1} $$', default=5.4462283548,
                            validators=[wtf.validators.InputRequired(), validators.NumberRange(-1, 1E+20)])
    sigma_exp = wtf.FloatField(label='$$ \sigma $$ ', default=0.361786273,
                               validators=[wtf.validators.InputRequired(), validators.NumberRange(-1, 1E+20)])

    price_exp = wtf.FloatField(label='Spot Price', default=3.89849373300000,
                               validators=[wtf.validators.InputRequired(), validators.NumberRange(0, 1E+20)])
    strike_exp = wtf.FloatField(label='Price', default=49.3280918417284,
                                validators=[wtf.validators.InputRequired(), validators.NumberRange(0, 1E+20)])
    risk_free_exp = wtf.FloatField(label='Interest Rate \((\%) \)', default=0.01,
                                   validators=[wtf.validators.InputRequired(), validators.NumberRange(0, 1E+20)])
    time_exp = wtf.FloatField(label='Time to Maturity (Years)', default=0.083333,
                              validators=[wtf.validators.InputRequired(), validators.NumberRange(0, 1E+20)])
    step_exp = wtf.FloatField(label='Number of Monitoring Dates', default=22,
                              validators=[wtf.validators.InputRequired(), validators.NumberRange(0, 1E+20)])
    upper_range_exp = wtf.FloatField(label='Grid Upper Bound', default=6, validators=[wtf.validators.InputRequired()])
    lower_range_exp = wtf.FloatField(label='Grid Lower Bound', default=3, validators=[wtf.validators.InputRequired()])

    # Implementation Parameter
    grid = wtf.FloatField(label='Grid Points (2^)', default=12,
                          validators=[wtf.validators.InputRequired(), validators.NumberRange(2, 20)])
    upper_range = wtf.FloatField(label='Grid Upper Bound', default=2, validators=[wtf.validators.InputRequired()])
    lower_range = wtf.FloatField(label='Grid Lower Bound', default=-2, validators=[wtf.validators.InputRequired()])
    dump = wtf.FloatField(label='Damping Coefficient', default=1.5, validators=[wtf.validators.InputRequired()])
    tolerance = wtf.FloatField(label='Tolerance', default=0.00001, validators=[wtf.validators.InputRequired()])

    # Contract Parameters
    price = wtf.FloatField(label='Spot Price', default=100,
                           validators=[wtf.validators.InputRequired(), validators.NumberRange(0, 1E+20)])
    risk_free = wtf.FloatField(label='Interest Rate \((\%) \)', default=3.67, validators=[wtf.validators.InputRequired()])
    # dividend_yield = wtf.FloatField(label='Dividend Yield \((\%) \)', default=0,
    #                                 validators=[wtf.validators.InputRequired()])
    time = wtf.FloatField(label='Time to Maturity (Years)', default=1,
                          validators=[wtf.validators.InputRequired(), validators.NumberRange(0, 1E+20)])
    step = wtf.FloatField(label='Number of Monitoring Dates', default=12,
                          validators=[wtf.validators.InputRequired(), validators.NumberRange(0, 1E+20)])
    strike = wtf.FloatField(label='Price', default=100,
                            validators=[wtf.validators.InputRequired(), validators.NumberRange(0, 1E+20)])

    button_compute = wtf.SubmitField(label='Compute')
    # button_export_table = wtf.SubmitField(label='Export Table')
    # button_table = wtf.SubmitField(label='View Details')
