import wtforms as wtf
from wtforms import validators

from common_validators import greater_than_zero


class ComputeForm(wtf.Form):
    price_1 = wtf.FloatField(label=r'Spot Price \((S_1) \)', default=100,
                             validators=[wtf.validators.InputRequired(), greater_than_zero])
    price_2 = wtf.FloatField(label=r'Spot Price \((S_2)\)', default=96,
                             validators=[wtf.validators.InputRequired(), greater_than_zero])

    dividend_yield_1 = wtf.FloatField(label='Dividend Yield \((\%) \)', default=5,
                                      validators=[wtf.validators.InputRequired()])
    dividend_yield_2 = wtf.FloatField(label='Dividend Yield \((\%) \)', default=5,
                                      validators=[wtf.validators.InputRequired()])

    volatility_1 = wtf.FloatField(label=r'Volatility 1st Asset \((\sigma_1) \)', default=0.2,
                                  validators=[wtf.validators.InputRequired(), greater_than_zero])
    volatility_2 = wtf.FloatField(label='Volatility 2nd Asset \((\sigma_2) \)', default=0.1,
                                  validators=[wtf.validators.InputRequired(), greater_than_zero])

    strike = wtf.FloatField(label='Strike', default=4,
                            validators=[wtf.validators.InputRequired(), greater_than_zero])
    risk_free = wtf.FloatField(label='Interest Rate \((\%) \)', default=10, validators=[wtf.validators.InputRequired()])

    time = wtf.FloatField(label='Time to Maturity (Years)', default=1,
                          validators=[wtf.validators.InputRequired(), greater_than_zero])

    rho = wtf.FloatField(label=r' Correlation \((\rho) \)', default=0.5,
                         validators=[wtf.validators.InputRequired(),
                                     validators.NumberRange(min=-1, max=1,
                                                            message='The value must be between than -1 and 1')])

    dump = wtf.FloatField(label='Damping Coefficient', default=0.75,
                          validators=[wtf.validators.InputRequired()])

    button_compute = wtf.SubmitField(label='Compute')
