import wtforms as wtf
from wtforms import validators, StringField, IntegerField
from wtforms.validators import InputRequired


class ComputeForm(wtf.Form):
    method_choice = wtf.RadioField('Choose the Method', choices=[('0', 'Import File Excel'), ('1', 'Tickers')],
                                   validators=[InputRequired()])

    file_data = wtf.FileField(label='Import File')
    file_name = StringField(label='DataSet Name', default='Test',
                            validators=[InputRequired(), validators.Length(max=25)])
    ticker = StringField(label='Tickers', default='AAA', validators=[InputRequired()])

    start_day = IntegerField(label='Day', default=1, validators=[InputRequired()])
    start_month = IntegerField(label='Month', default=1, validators=[InputRequired()])
    start_year = IntegerField(label='Year', default=2000, validators=[InputRequired()])

    end_day = IntegerField(label='Day', default=1, validators=[InputRequired()])
    end_month = IntegerField(label='Month', default=1, validators=[InputRequired()])
    end_year = IntegerField(label='Year', default=2000, validators=[InputRequired()])

    button_compute = wtf.SubmitField(label='Compute')
    button_export_table = wtf.SubmitField(label='Export Table')
