import wtforms as wtf
from wtforms import validators


class ComputeForm(wtf.Form):
    price_1 = wtf.FloatField(label='Spot Price', default=100,
                             validators=[wtf.validators.InputRequired(), validators.NumberRange(0, 1E+20)])
    price_2 = wtf.FloatField(label='Spot Price', default=96,
                             validators=[wtf.validators.InputRequired(), validators.NumberRange(0, 1E+20)])

    dividend_yield_1 = wtf.FloatField(label='Dividend Yield', default=0.05,
                                      validators=[wtf.validators.InputRequired()])
    dividend_yield_2 = wtf.FloatField(label='Dividend Yield', default=0.05,
                                      validators=[wtf.validators.InputRequired()])

    volatility_1 = wtf.FloatField(label='$$ \sigma $$', default=0.2,
                                  validators=[wtf.validators.InputRequired()])

    volatility_2 = wtf.FloatField(label='$$ \sigma $$', default=0.1,
                                  validators=[wtf.validators.InputRequired()])

    strike = wtf.FloatField(label='Strike', default=4,
                            validators=[wtf.validators.InputRequired(), validators.NumberRange(0, 1E+20)])
    risk_free = wtf.FloatField(label='Interest Rate', default=10, validators=[wtf.validators.InputRequired()])

    time = wtf.FloatField(label='Time to Matutity', default=0.5,
                          validators=[wtf.validators.InputRequired(), validators.NumberRange(0, 1E+20)])

    rho = wtf.FloatField(label=r'$$ \rho $$', default=0.1,
                         validators=[wtf.validators.InputRequired()])

    dump = wtf.FloatField(label='Dump Parameter', default=0.75,
                          validators=[wtf.validators.InputRequired()])

    button_compute = wtf.SubmitField(label='Compute')
