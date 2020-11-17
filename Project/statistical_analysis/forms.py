import wtforms as wtf
from flask_wtf.file import FileRequired
from wtforms import validators, StringField, IntegerField, FieldList
from wtforms.validators import InputRequired
from wtforms.fields.html5 import DateField


class ComputeForm(wtf.Form):
    method_choice = wtf.RadioField('Choose the Method', choices=[('0', 'Excel File'), ('1', 'Yahoo Tickers')],
                                   validators=[InputRequired()])

    file_data = wtf.FileField(label='Import File')
    file_name = StringField(label='DataSet Name', default='Test',
                            validators=[InputRequired(), validators.Length(max=25)])

    tickers_list = FieldList(StringField(label='Ticker', default='AAPL'), min_entries=1)

    entry_date = DateField('From')

    end_date = DateField('To')

    button_compute = wtf.SubmitField(label='Compute')
    button_export_table = wtf.SubmitField(label='Export Table')
    button_add_field = wtf.SubmitField(label='Add Ticker')
    button_delete_field = wtf.SubmitField(label='Delete Ticker')
