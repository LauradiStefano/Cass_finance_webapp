import wtforms as wtf
from flask_wtf.file import FileRequired
from wtforms import SelectMultipleField, validators, StringField
from wtforms.validators import InputRequired
from wtforms.widgets import ListWidget, CheckboxInput

from common_validators import greater_than_zero


class MultiCheckboxField(SelectMultipleField):
    widget = ListWidget(prefix_label=False)
    option_widget = CheckboxInput()


class ComputeForm(wtf.Form):
    file_data = wtf.FileField(label='Import File')
    file_name = StringField(label='DataSet Name', validators=[InputRequired(), validators.Length(max=25)])
    price = wtf.FloatField(label='Current Spot Price', validators=[InputRequired(), greater_than_zero])
    risk_free = wtf.FloatField(label='Interest Rate \((\%) \)', default=5.04, validators=[InputRequired()])
    div_yield = wtf.FloatField(label='Dividend Yield \((\%) \)', default=3.14, validators=[InputRequired()])

    risk_dividend = wtf.RadioField('Interest Rate & Dividend Yield', choices=[('0', 'True'), ('1', 'False')],
                                   default='1')
    call_put_flag = wtf.RadioField('Call-Put', choices=[('1', 'Call'), ('0', 'Put'), ('2', 'Both')],
                                   validators=[InputRequired()], default='2')
    plot_choice = MultiCheckboxField('Plot', choices=[('0', 'Pdf of Spot Prices'), ('1', 'Cdf of Spot Prices'),
                                                      ('2', 'Cdf of Log-Returns')])
    button_compute = wtf.SubmitField(label='Compute')
    button_view_details = wtf.SubmitField(label='View Details')
    button_export_table = wtf.SubmitField(label='Export Table')
