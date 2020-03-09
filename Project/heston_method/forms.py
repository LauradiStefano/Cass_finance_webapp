import wtforms as wtf
from wtforms import validators


class ComputeForm(wtf.Form):
    mu = wtf.FloatField(label='$$ \mu $$', default=-0.1473, validators=[wtf.validators.InputRequired()])
    volatility_t0 = wtf.FloatField(label=r'$$ v_0 $$', default=0.0175,
                                   validators=[wtf.validators.InputRequired(), validators.NumberRange(0, 1E+20)])
    volatility_hat = wtf.FloatField(label='$$ \hat{v} $$', default=0.0398,
                                    validators=[wtf.validators.InputRequired(), validators.NumberRange(0, 1E+20)])
    lam = wtf.FloatField(label='$$ \lambda $$', default=1.5768,
                         validators=[wtf.validators.InputRequired(), validators.NumberRange(0, 1E+20)])
    chi = wtf.FloatField(label='$$ \chi $$', default=0.5751,
                         validators=[wtf.validators.InputRequired(), validators.NumberRange(0, 1E+20)])
    rho = wtf.FloatField(label=r'$$ \rho $$', default=-0.5711,
                         validators=[wtf.validators.InputRequired(), validators.NumberRange(-1, 1)])

    price = wtf.FloatField(label='Spot Price', default=100,
                           validators=[wtf.validators.InputRequired(), validators.NumberRange(0, 1E+20)])
    strike_min = wtf.FloatField(label='Strike Min', default=70,
                                validators=[wtf.validators.InputRequired(), validators.NumberRange(0, 1E+20)])
    strike_max = wtf.FloatField(label='Strike Max', default=130,
                                validators=[wtf.validators.InputRequired(), validators.NumberRange(0, 1E+20)])
    risk_free = wtf.FloatField(label='Interest Rate \((\%) \)', default=0, validators=[wtf.validators.InputRequired()])
    dividend_yield = wtf.FloatField(label='Dividend Yield \((\%) \)', default=0, validators=[wtf.validators.InputRequired()])
    time = wtf.FloatField(label='Time to Maturity (Years)', default=1,
                          validators=[wtf.validators.InputRequired(), validators.NumberRange(0, 1E+20)])
    call_put = wtf.RadioField('Option Type', choices=[('1', 'Call'), ('0', 'Put')], default='1')

    button_compute = wtf.SubmitField(label='Compute')
    button_export_table = wtf.SubmitField(label='Export Table')
    button_view_details = wtf.SubmitField(label='View Details')
