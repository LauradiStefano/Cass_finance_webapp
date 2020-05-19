import wtforms as wtf
from wtforms import validators, StringField
from wtforms.validators import InputRequired


class ComputeForm(wtf.Form):
    file_name = StringField(label='DataSet Name', validators=[InputRequired(), validators.Length(max=25)])

    file_data = wtf.FileField(label='Import File')

    n_portfolio = wtf.IntegerField(label='Number of Simulated Portfolios', default=100,
                                   validators=[wtf.validators.InputRequired(),
                                               validators.NumberRange
                                               (min=0, max=10000,
                                                message='The value must be between than 0 and 10000')])

    short_selling = wtf.RadioField('Short Selling:', choices=[('1', 'Yes'), ('0', 'No')],
                                   validators=[InputRequired()], default='1')

    button_compute = wtf.SubmitField(label='Compute')
