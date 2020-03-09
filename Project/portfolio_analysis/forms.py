import wtforms as wtf
from wtforms import validators, StringField
from wtforms.validators import InputRequired


class ComputeForm(wtf.Form):
    file_name = StringField(label='DataSet Name', validators=[InputRequired(), validators.Length(max=25)])

    file_data = wtf.FileField(label='Import File')

    n_portfolio = wtf.IntegerField(label='Number of Simulated Portfolios', default=100,
                                   validators=[wtf.validators.InputRequired()])

    button_compute = wtf.SubmitField(label='Compute')
