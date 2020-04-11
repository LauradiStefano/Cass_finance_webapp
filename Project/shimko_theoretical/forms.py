import wtforms as wtf
from wtforms import SelectMultipleField
from wtforms.widgets import ListWidget, CheckboxInput

from common_validators import greater_than_zero


class MultiCheckboxField(SelectMultipleField):
    widget = ListWidget(prefix_label=False)
    option_widget = CheckboxInput()


class ComputeForm(wtf.Form):
    strike_min = wtf.FloatField(label='Minimum', default=325,
                                validators=[wtf.validators.InputRequired(), greater_than_zero])

    strike_atm = wtf.FloatField(label='At-The-Money', default=390,
                                validators=[wtf.validators.InputRequired(), greater_than_zero])
    strike_max = wtf.FloatField(label='Maximum', default=425,
                                validators=[wtf.validators.InputRequired(), greater_than_zero])

    volatility_min = wtf.FloatField(label='Minimum', default=4.5,
                                    validators=[wtf.validators.InputRequired(), greater_than_zero])
    volatility_atm = wtf.FloatField(label='At-The-Money', default=6.5,
                                    validators=[wtf.validators.InputRequired(), greater_than_zero])
    volatility_max = wtf.FloatField(label='Maximum', default=11.3,
                                    validators=[wtf.validators.InputRequired(), greater_than_zero])
    price = wtf.FloatField(label='Current Spot Price', default=387,
                           validators=[wtf.validators.InputRequired(), greater_than_zero])
    risk_free = wtf.FloatField(label='Interest Rate \((\%) \)', default=5.04,
                               validators=[wtf.validators.InputRequired()])
    div_yield = wtf.FloatField(label='Dividend Yield \((\%) \)', default=0,
                               validators=[wtf.validators.InputRequired()])
    time = wtf.FloatField(label='Time to Maturity (Years)', default=0.1666,
                          validators=[wtf.validators.InputRequired(), greater_than_zero])
    plot_choice = MultiCheckboxField('Plot', choices=[('0', 'Pdf of Spot Prices'), ('1', 'Cdf of Spot Prices'),
                                                      ('2', 'Cdf of Log-Returns')])
    button_compute = wtf.SubmitField(label='Compute')
    button_view_details = wtf.SubmitField(label='View Details')
    button_export_table = wtf.SubmitField(label='Export Table')

    def validate(self):
        if not super(ComputeForm, self).validate():
            return False

        valid = True
        if self.strike_min.data >= self.strike_atm.data or self.strike_min.data >= self.strike_max.data:
            self.strike_min.errors.append('The value must be smaller than at the money and maximum')
            valid = False

        if self.strike_atm.data <= self.strike_min.data or self.strike_atm.data >= self.strike_max.data:
            self.strike_atm.errors.append('The value must be between minimum and maximum')
            valid = False

        if self.strike_max.data <= self.strike_min.data or self.strike_max.data <= self.strike_atm.data:
            self.strike_max.errors.append('The value must be greater than minimum and at the money')
            valid = False

##        if self.volatility_min.data >= self.volatility_atm.data or self.volatility_min.data >= self.volatility_max.data:
##            self.volatility_min.errors.append('The value must be smaller than at the money and maximum')
##            valid = False
##
##        if self.volatility_atm.data <= self.volatility_min.data or self.volatility_atm.data >= self.volatility_max.data:
##            self.volatility_atm.errors.append('The value must be between minimum and maximum')
##            valid = False
##
##        if self.volatility_max.data <= self.volatility_min.data or self.volatility_max.data <= self.volatility_atm.data:
##            self.volatility_max.errors.append('The value must be greater than minimum and at the money')
##            valid = False

        return valid
