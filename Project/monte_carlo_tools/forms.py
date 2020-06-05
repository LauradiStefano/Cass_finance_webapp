import wtforms as wtf
from wtforms import validators

from common_validators import greater_than_zero


def kappa_vg_check(form, field):
    kappa_vg = field.data
    if kappa_vg <= 0 or kappa_vg >= 2.5:
        raise validators.ValidationError('The value must be between 0 and 2.5')


def theta_vg_check(form, field):
    theta_vg = field.data
    if theta_vg <= -1 or theta_vg >= 1:
        raise validators.ValidationError('The value must be between -1 and 1')


def kappa_nig_check(form, field):
    kappa_nig = field.data
    if kappa_nig <= 0 or kappa_nig >= 6:
        raise validators.ValidationError('The value must be between 0 and 6')


def y_cgmy_check(form, field):
    y_cgmy = field.data
    if y_cgmy >= 2:
        raise validators.ValidationError('The value must be smaller than 2')


class ComputeForm(wtf.Form):
    model_choice = wtf.SelectField('Model',
                                   choices=[('0', 'Arithmetic Brownian Motion'), ('1', 'Geometric Brownian Motion'),
                                            ('2', 'Cox-Ingersoll-Ross'), ('3', 'Mean Reverting Gaussian'),
                                            ('4', 'Heston')], default='0')

    # Arithmetic Brownian Motion distribution
    mu_abm = wtf.FloatField(label='$$ \mu $$', default=0,
                            validators=[wtf.validators.InputRequired()])
    sigma_abm = wtf.FloatField(label='$$ \sigma $$', default=0.2,
                               validators=[wtf.validators.InputRequired(), greater_than_zero])

    # Geometric Brownian Motion distribution
    mu_gbm = wtf.FloatField(label='$$ \mu $$', default=0.01,
                            validators=[wtf.validators.InputRequired()])
    sigma_gbm = wtf.FloatField(label='$$ \sigma $$', default=0.2,
                               validators=[wtf.validators.InputRequired(), greater_than_zero])

    # Cox-Ingersoll-Ross distribution
    mu_cir = wtf.FloatField(label='$$ \mu $$', default=0.05,
                            validators=[wtf.validators.InputRequired()])
    sigma_cir = wtf.FloatField(label='$$ \sigma $$', default=0.1,
                               validators=[wtf.validators.InputRequired(), greater_than_zero])
    alpha_cir = wtf.FloatField(label=r'$$ \alpha $$', default=1,
                               validators=[wtf.validators.InputRequired()])

    # Mean Reverting Gaussian distribution
    mu_mrg = wtf.FloatField(label='$$ \mu $$', default=0.05,
                            validators=[wtf.validators.InputRequired()])
    sigma_mrg = wtf.FloatField(label='$$ \sigma $$', default=0.1,
                               validators=[wtf.validators.InputRequired(), greater_than_zero])
    alpha_mrg = wtf.FloatField(label=r'$$ \alpha $$', default=1,
                               validators=[wtf.validators.InputRequired()])

    # Heston
    mu_heston = wtf.FloatField(label='$$ \mu $$', default=0,
                               validators=[wtf.validators.InputRequired()])
    volatility_t0_heston = wtf.FloatField(label=r'$$ v_0 $$', default=0.2**2,
                                          validators=[wtf.validators.InputRequired(), greater_than_zero])
    alpha_heston = wtf.FloatField(label=r'$$ \alpha $$', default=0.1,
                                  validators=[wtf.validators.InputRequired()])
    beta_heston = wtf.FloatField(label=r'$$ \beta $$', default=0.25**2,
                                 validators=[wtf.validators.InputRequired()])
    eta_heston = wtf.FloatField(label=r'$$ \eta $$', default=0.2,
                                validators=[wtf.validators.InputRequired()])
    rho_heston = wtf.FloatField(label=r'$$ \rho $$', default=-0.8,
                                validators=[wtf.validators.InputRequired()])

    # Contract parameters
    price = wtf.FloatField(label='Spot Price', default=100,
                           validators=[wtf.validators.InputRequired(), greater_than_zero])
    time = wtf.FloatField(label='Time to Maturity (Years)', default=5,
                          validators=[wtf.validators.InputRequired(), greater_than_zero])
    number_step = wtf.IntegerField(label='Number of Step', default=50,
                                   validators=[wtf.validators.InputRequired(), greater_than_zero])
    number_paths = wtf.IntegerField(label='Number of Paths', default=1000,
                                    validators=[wtf.validators.InputRequired(), greater_than_zero])

    button_compute = wtf.SubmitField(label='Compute')
    button_export_table = wtf.SubmitField(label='Export Table')
    button_view_details = wtf.SubmitField(label='View Details')
