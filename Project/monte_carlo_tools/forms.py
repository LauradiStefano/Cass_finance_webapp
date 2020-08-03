import wtforms as wtf

from common_validators import greater_than_zero


class ComputeForm(wtf.Form):
    model_choice = wtf.SelectField('Model',
                                   choices=[('0', 'Arithmetic Brownian Motion'), ('1', 'Cox-Ingersoll-Ross'),
                                            ('2', 'DEJD'), ('3', 'Exponentially Weighted Moving Average'),
                                            ('4', 'GARCH'), ('5', 'Geometric Brownian Motion'), ('6', 'Heston'),
                                            ('7', 'MJD'), ('8', 'Mean Reverting Gaussian'), ('9', 'Variance-Gamma')],
                                   default='0')

    # Arithmetic Brownian Motion distribution
    mu_abm = wtf.FloatField(label=r'$$ \mu $$', default=0,
                            validators=[wtf.validators.InputRequired()])
    sigma_abm = wtf.FloatField(label=r'$$ \sigma $$', default=0.2,
                               validators=[wtf.validators.InputRequired(), greater_than_zero])

    # Cox-Ingersoll-Ross distribution
    mu_cir = wtf.FloatField(label=r'$$ \mu $$', default=0.05,
                            validators=[wtf.validators.InputRequired()])
    sigma_cir = wtf.FloatField(label=r'$$ \sigma $$', default=0.1,
                               validators=[wtf.validators.InputRequired(), greater_than_zero])
    alpha_cir = wtf.FloatField(label=r'$$ \alpha $$', default=1,
                               validators=[wtf.validators.InputRequired()])

    # DEJD distribution
    mu_dejd = wtf.FloatField(label=r'$$ \mu $$', default=0.01,
                             validators=[wtf.validators.InputRequired()])
    sigma_dejd = wtf.FloatField(label=r'$$ \sigma $$', default=0.2,
                                validators=[wtf.validators.InputRequired()])
    lam_dejd = wtf.FloatField(label='$$ l $$', default=0.1, validators=[wtf.validators.InputRequired()])
    rho_dejd = wtf.FloatField(label=r'$$ \rho $$', default=0.2, validators=[wtf.validators.InputRequired()])
    eta1_dejd = wtf.FloatField(label=r'$$ \eta_{1} $$', default=12, validators=[wtf.validators.InputRequired()])
    eta2_dejd = wtf.FloatField(label=r'$$ \eta_{2} $$', default=23, validators=[wtf.validators.InputRequired()])

    # EWMA distribution
    mu_ewma = wtf.FloatField(label=r'$$ \mu $$', default=0,
                             validators=[wtf.validators.InputRequired()])
    volatility_t0_ewma = wtf.FloatField(label=r'$$ v_0 $$', default=0.2, validators=[wtf.validators.InputRequired()])
    omega_ewma = wtf.FloatField(label=r'$$ \omega $$', default=0, validators=[wtf.validators.InputRequired()])
    alpha_ewma = wtf.FloatField(label=r'$$ \alpha $$', default=0.1, validators=[wtf.validators.InputRequired()]
                                )
    beta_ewma = wtf.FloatField(label=r'$$ \beta $$', default=0.9, validators=[wtf.validators.InputRequired()]
                               )
    asymm_ewma = wtf.FloatField(label=r'$$ \gamma $$', default=0, validators=[wtf.validators.InputRequired()]
                                )

    # GARCH distribution
    mu_garch = wtf.FloatField(label=r'$$ \mu $$', default=0, validators=[wtf.validators.InputRequired()])
    volatility_t0_garch = wtf.FloatField(label=r'$$ v_0 $$', default=0.2 ** 2 / 250,
                                         validators=[wtf.validators.InputRequired()])
    omega_garch = wtf.FloatField(label=r'$$ \omega $$', default=5.7800 * 10 ** (-6),
                                 validators=[wtf.validators.InputRequired()])
    alpha_garch = wtf.FloatField(label=r'$$ \alpha $$', default=0.1, validators=[wtf.validators.InputRequired()])
    beta_garch = wtf.FloatField(label=r'$$ \beta $$', default=0.86, validators=[wtf.validators.InputRequired()])
    asymm_garch = wtf.FloatField(label=r'$$ \gamma $$', default=0, validators=[wtf.validators.InputRequired()])

    # Geometric Brownian Motion distribution
    mu_gbm = wtf.FloatField(label=r'$$ \mu $$', default=0.01,
                            validators=[wtf.validators.InputRequired()])
    sigma_gbm = wtf.FloatField(label=r'$$ \sigma $$', default=0.2,
                               validators=[wtf.validators.InputRequired(), greater_than_zero])

    # Heston
    mu_heston = wtf.FloatField(label=r'$$ \mu $$', default=0,
                               validators=[wtf.validators.InputRequired()])
    volatility_t0_heston = wtf.FloatField(label=r'$$ v_0 $$', default=0.2 ** 2,
                                          validators=[wtf.validators.InputRequired(), greater_than_zero])
    alpha_heston = wtf.FloatField(label=r'$$ \alpha $$', default=0.1,
                                  validators=[wtf.validators.InputRequired()])
    beta_heston = wtf.FloatField(label=r'$$ \beta $$', default=0.25 ** 2,
                                 validators=[wtf.validators.InputRequired()])
    eta_heston = wtf.FloatField(label=r'$$ \eta $$', default=0.2,
                                validators=[wtf.validators.InputRequired()])
    rho_heston = wtf.FloatField(label=r'$$ \rho $$', default=-0.8,
                                validators=[wtf.validators.InputRequired()])

    # MJD distribution
    mu_mjd = wtf.FloatField(label=r'$$ \mu $$', default=0.01,
                            validators=[wtf.validators.InputRequired()])
    sigma_mjd = wtf.FloatField(label=r'$$ \sigma $$', default=0.1,
                               validators=[wtf.validators.InputRequired()])
    lam_mjd = wtf.FloatField(label='$$ l $$', default=0.5, validators=[wtf.validators.InputRequired()])
    mu_x_mjd = wtf.FloatField(label=r'$$ \mu_{x} $$', default=-0.1, validators=[wtf.validators.InputRequired()])
    sigma_x_mjd = wtf.FloatField(label=r'$$ \sigma_{x} $$', default=0.2,
                                 validators=[wtf.validators.InputRequired()])

    # Mean Reverting Gaussian distribution
    mu_mrg = wtf.FloatField(label=r'$$ \mu $$', default=0.05,
                            validators=[wtf.validators.InputRequired()])
    sigma_mrg = wtf.FloatField(label=r'$$ \sigma $$', default=0.1,
                               validators=[wtf.validators.InputRequired(), greater_than_zero])
    alpha_mrg = wtf.FloatField(label=r'$$ \alpha $$', default=1,
                               validators=[wtf.validators.InputRequired()])

    # Variance Gamma distribution
    sigma_vg = wtf.FloatField(label=r'$$ \sigma $$', default=0.2,
                              validators=[wtf.validators.InputRequired()])
    theta_vg = wtf.FloatField(label=r'$$ \theta $$', default=-0.01,
                              validators=[wtf.validators.InputRequired()])
    kappa_vg = wtf.FloatField(label='$$ v $$', default=0.3, validators=[wtf.validators.InputRequired()])

    # Contract parameters
    price_abm = wtf.FloatField(label='Starting Value', default=0,
                               validators=[wtf.validators.InputRequired()])

    price_cir = wtf.FloatField(label='Starting Value', default=0.1,
                               validators=[wtf.validators.InputRequired()])

    price_dejd = wtf.FloatField(label='Starting Value', default=0,
                                validators=[wtf.validators.InputRequired()])

    price_ewma = wtf.FloatField(label='Starting Value', default=0,
                                validators=[wtf.validators.InputRequired()])

    price_garch = wtf.FloatField(label='Starting Value', default=0,
                                 validators=[wtf.validators.InputRequired()])

    price_gbm = wtf.FloatField(label='Starting Value', default=1,
                               validators=[wtf.validators.InputRequired()])

    price_heston = wtf.FloatField(label='Starting Value', default=0,
                                  validators=[wtf.validators.InputRequired()])

    price_mjd = wtf.FloatField(label='Starting Value', default=0,
                               validators=[wtf.validators.InputRequired()])

    price_mrg = wtf.FloatField(label='Starting Value', default=0.1,
                               validators=[wtf.validators.InputRequired()])

    price_vg = wtf.FloatField(label='Starting Value', default=0,
                              validators=[wtf.validators.InputRequired()])

    time = wtf.FloatField(label='Time to Maturity (Years)', default=5,
                          validators=[wtf.validators.InputRequired(), greater_than_zero])
    number_step = wtf.IntegerField(label='Number of Steps', default=50,
                                   validators=[wtf.validators.InputRequired(), greater_than_zero])
    number_paths = wtf.IntegerField(label='Number of Paths', default=1000,
                                    validators=[wtf.validators.InputRequired(), greater_than_zero])

    button_compute = wtf.SubmitField(label='Compute')
    button_export_table = wtf.SubmitField(label='Export Table')
    button_view_details = wtf.SubmitField(label='View Details')
