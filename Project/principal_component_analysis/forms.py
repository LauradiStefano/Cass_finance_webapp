import wtforms as wtf
from wtforms import validators, StringField, IntegerField, FieldList
from wtforms.validators import InputRequired


class ComputeForm(wtf.Form):
    method_choice = wtf.RadioField('Choose the Method', choices=[('0', 'Excel File'), ('1', 'Yahoo Tickers')],
                                   default='0', validators=[InputRequired()])

    file_data = wtf.FileField(label='Import File')
    file_name = StringField(label='DataSet Name', default='Test',
                            validators=[InputRequired(), validators.Length(max=25)])

    asset_flag = wtf.RadioField('Quantity to Analyze:',
                                choices=[('3', 'Levels'), ('2', 'Changes'), ('0', 'Log-Returns'),
                                         ('1', 'Percentage Returns')], validators=[InputRequired()], default='0')

    matrix_flag = wtf.RadioField('Covariance-Correlation:',
                                 choices=[('0', 'Covariance Matrix'), ('1', 'Correlation Matrix')],
                                 validators=[InputRequired()], default='0')

    explained_variance = wtf.FloatField(label='Desidered explained variance', default=0.9,
                                        validators=[wtf.validators.InputRequired(),
                                                    validators.NumberRange(min=0, max=1,
                                                                           message='The value must be between 0 and 1')])

    tickers_list = FieldList(StringField(label='Ticker'), min_entries=2)

    start_day = IntegerField(label='Day', default=15, validators=[InputRequired()])
    start_month = IntegerField(label='Month', default=11, validators=[InputRequired()])
    start_year = IntegerField(label='Year', default=2015, validators=[InputRequired()])

    end_day = IntegerField(label='Day', default=15, validators=[InputRequired()])
    end_month = IntegerField(label='Month', default=11, validators=[InputRequired()])
    end_year = IntegerField(label='Year', default=2018, validators=[InputRequired()])

    button_compute = wtf.SubmitField(label='Compute')
    button_export_table = wtf.SubmitField(label='Export Table')
    button_add_field = wtf.SubmitField(label='Add Ticker')
    button_delete_field = wtf.SubmitField(label='Delete Ticker')
