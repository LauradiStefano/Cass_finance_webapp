import wtforms as wtf
from wtforms import SelectMultipleField, validators
from wtforms.widgets import ListWidget, CheckboxInput


class MultiCheckboxField(SelectMultipleField):
    widget = ListWidget(prefix_label=False)
    option_widget = CheckboxInput()


class ComputeForm(wtf.Form):
    strike_min = wtf.FloatField(label='Min Strike', default=325,
                                validators=[wtf.validators.InputRequired(), validators.NumberRange(0, 1E+20)])

    strike_atm = wtf.FloatField(label='Atm Strike', default=390,
                                validators=[wtf.validators.InputRequired(), validators.NumberRange(0, 1E+20)])
    strike_max = wtf.FloatField(label='Max Strike', default=425,
                                validators=[wtf.validators.InputRequired(), validators.NumberRange(0, 1E+20)])

    volatility_min = wtf.FloatField(label='Min Volatility ', default=11.3,
                                    validators=[wtf.validators.InputRequired(), validators.NumberRange(0, 1E+20)])
    volatility_atm = wtf.FloatField(label='Atm Volatility', default=6.5,
                                    validators=[wtf.validators.InputRequired(), validators.NumberRange(0, 1E+20)])
    volatility_max = wtf.FloatField(label='Max Volatility', default=4.5,
                                    validators=[wtf.validators.InputRequired(), validators.NumberRange(0, 1E+20)])
    price = wtf.FloatField(label='Spot Price', default=387,
                           validators=[wtf.validators.InputRequired(), validators.NumberRange(0, 1E+20)])
    risk_free = wtf.FloatField(label='Interest Rate', default=5.04, validators=[wtf.validators.InputRequired()])
    div_yield = wtf.FloatField(label='Dividend Yield', default=0, validators=[wtf.validators.InputRequired()])
    time = wtf.FloatField(label='Time to expiration', default=0.1666,
                          validators=[wtf.validators.InputRequired(), validators.NumberRange(0, 1E+20)])
    plot_choice = MultiCheckboxField('Plot', choices=[('0', 'Pdf Prices'), ('1', 'Cdf Prices'),
                                                      ('2', 'Cdf Returns')])
    button_compute = wtf.SubmitField(label='Compute')
    button_view_details = wtf.SubmitField(label='View Details')
    button_export_table = wtf.SubmitField(label='Export Table')
