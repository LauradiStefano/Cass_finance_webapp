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
    type_choice = wtf.SelectField('Model',
                                  choices=[('0', 'Normal'), ('1', 'VG'), ('2', 'NIG'), ('3', 'CGMY')], default='0')

    mu = wtf.FloatField(label='$$ \mu $$', default=0,
                        validators=[wtf.validators.InputRequired()])

    # Normal distribution
    sigma_normal = wtf.FloatField(label='$$ \sigma $$', default=0.12,
                                  validators=[wtf.validators.InputRequired(), greater_than_zero])

    # VG distribution
    sigma_vg = wtf.FloatField(label='$$ \sigma $$', default=0.12,
                              validators=[wtf.validators.InputRequired(), greater_than_zero])
    kappa_vg = wtf.FloatField(label='$$ \kappa $$', default=0.2,
                              validators=[wtf.validators.InputRequired(), kappa_vg_check])
    theta_vg = wtf.FloatField(label=r'$$ \theta $$', default=-0.14,
                              validators=[wtf.validators.InputRequired(), theta_vg_check])

    # NIG distribution
    sigma_nig = wtf.FloatField(label='$$ \sigma $$', default=0.16,
                               validators=[wtf.validators.InputRequired(), greater_than_zero])
    kappa_nig = wtf.FloatField(label='$$ \kappa $$', default=0.2,
                               validators=[wtf.validators.InputRequired(), kappa_nig_check])
    theta_nig = wtf.FloatField(label=r'$$ \theta $$', default=-0.12,
                               validators=[wtf.validators.InputRequired(),
                                           validators.NumberRange(min=-1, max=1,
                                                                  message='The value must be between -1 and 1')])

    # CGMY distribution
    c = wtf.FloatField(label='$$ C $$', default=1,
                       validators=[wtf.validators.InputRequired(), greater_than_zero])
    g = wtf.FloatField(label='$$ G $$', default=5,
                       validators=[wtf.validators.InputRequired(), greater_than_zero])
    m = wtf.FloatField(label='$$ M $$', default=5,
                       validators=[wtf.validators.InputRequired(), greater_than_zero])
    y = wtf.FloatField(label='$$ Y $$', default=0.5,
                       validators=[wtf.validators.InputRequired(), y_cgmy_check])

    # Contract parameters
    price = wtf.FloatField(label='Spot Price', default=100,
                           validators=[wtf.validators.InputRequired(), greater_than_zero])
    strike_min = wtf.FloatField(label='Minimum Strike', default=70,
                                validators=[wtf.validators.InputRequired(), greater_than_zero])
    strike_max = wtf.FloatField(label='Maximum Strike', default=130,
                                validators=[wtf.validators.InputRequired(), greater_than_zero])
    risk_free = wtf.FloatField(label='Interest Rate \((\%) \)', default=2,
                               validators=[wtf.validators.InputRequired()])
    dividend_yield = wtf.FloatField(label='Dividend Yield \((\%) \)', default=0,
                                    validators=[wtf.validators.InputRequired()])
    time = wtf.FloatField(label='Time to Maturity (Years)', default=0.5,
                          validators=[wtf.validators.InputRequired(), greater_than_zero])
    call_put = wtf.RadioField('Option Type', choices=[('1', 'Call'), ('0', 'Put')], default='1')

    button_compute = wtf.SubmitField(label='Compute')
    button_export_table = wtf.SubmitField(label='Export Table')
    button_view_details = wtf.SubmitField(label='View Details')

    def validate(self):
        if not super(ComputeForm, self).validate():
            return False
        valid = True
        if self.strike_min.data >= self.strike_max.data:
            self.strike_min.errors.append('The value must be smaller than maximum')
            valid = False

        if self.strike_max.data <= self.strike_min.data:
            self.strike_max.errors.append('The value must be greater than minimum')
            valid = False
        return valid
