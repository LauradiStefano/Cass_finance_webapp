import wtforms as wtf
from wtforms import validators, StringField, IntegerField, FieldList
from wtforms.validators import InputRequired


class ComputeForm(wtf.Form):
    method_choice = wtf.RadioField('Choose the Method', choices=[('0', 'Import File Excel'), ('1', 'Tickers')],
                                   validators=[InputRequired()])

    file_data = wtf.FileField(label='Import File')
    file_name = StringField(label='DataSet Name', default='Test',
                            validators=[InputRequired(), validators.Length(max=25)])
    tickers = StringField(label='Tickers', default='AAPL',
                          validators=[InputRequired()])
    # ticker_list = FieldList(StringField(tickers), min_entries=1)

    start_day = IntegerField(label='Day', default=15, validators=[InputRequired()])
    start_month = IntegerField(label='Month', default=11, validators=[InputRequired()])
    start_year = IntegerField(label='Year', default=2015, validators=[InputRequired()])

    end_day = IntegerField(label='Day', default=15, validators=[InputRequired()])
    end_month = IntegerField(label='Month', default=11, validators=[InputRequired()])
    end_year = IntegerField(label='Year', default=2018, validators=[InputRequired()])

    button_compute = wtf.SubmitField(label='Compute')
    button_export_table = wtf.SubmitField(label='Export Table')
    button_add_row = wtf.SubmitField(label='Add Row')
