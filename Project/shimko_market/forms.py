import wtforms as wtf
from wtforms import SelectMultipleField, validators
from wtforms.validators import InputRequired
from wtforms.widgets import ListWidget, CheckboxInput


class MultiCheckboxField(SelectMultipleField):
    widget = ListWidget(prefix_label=False)
    option_widget = CheckboxInput()


class ComputeForm(wtf.Form):
    file_name = wtf.FileField(label='Import File')
    price = wtf.FloatField(label='Spot Price', validators=[InputRequired(), validators.NumberRange(0, 1E+20)])
    risk_free = wtf.FloatField(label='Interest Rate', default=5.04, validators=[InputRequired()])
    div_yield = wtf.FloatField(label='Dividend Yield', default=3.14, validators=[InputRequired()])

    risk_dividend = wtf.RadioField('Interest Rate & Dividend Yield', choices=[('0', 'True'), ('1', 'False')],
                                   default='1')
    call_put_flag = wtf.RadioField('Call-Put', choices=[ ('1', 'Call'), ('0', 'Put'), ('2', 'Both')],
                                   validators=[InputRequired()], default='2')
    plot_choice = MultiCheckboxField('Plot', choices=[('0', 'Pdf Prices'), ('1', 'Cdf Prices'),
                                                      ('2', 'Cdf Returns')])
    button_compute = wtf.SubmitField(label='Compute')
    button_view_details = wtf.SubmitField(label='View Details')
    button_export_table = wtf.SubmitField(label='Export Table')
