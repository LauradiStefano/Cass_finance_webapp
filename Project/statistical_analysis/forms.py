import wtforms as wtf
from wtforms import validators, StringField, IntegerField
from wtforms.validators import InputRequired


class ComputeForm(wtf.Form):
    method_choice = wtf.RadioField('Choose the Method', choices=[('0', 'Import File Excel'), ('1', 'Tickers')],
                                   validators=[InputRequired()])

    file_data = wtf.FileField(label='Import File')
    file_name = StringField(label='DataSet Name', validators=[InputRequired(), validators.Length(max=25)])
    ticker = StringField(label='Tickers', validators=[InputRequired(), validators.Length(max=25)])

    start_day = IntegerField(label='Day', validators=[InputRequired(), validators.Length(max=25)])
    start_month = IntegerField(label='Month', validators=[InputRequired(), validators.Length(max=25)])
    start_year = IntegerField(label='Year', validators=[InputRequired(), validators.Length(max=25)])

    end_day = IntegerField(label='Day', validators=[InputRequired(), validators.Length(max=25)])
    end_month = IntegerField(label='Month', validators=[InputRequired(), validators.Length(max=25)])
    end_year = IntegerField(label='Year', validators=[InputRequired(), validators.Length(max=25)])

    button_compute = wtf.SubmitField(label='Compute')
    button_export_table = wtf.SubmitField(label='Export Table')
