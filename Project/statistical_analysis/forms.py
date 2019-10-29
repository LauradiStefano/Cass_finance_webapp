import wtforms as wtf
from wtforms import validators, StringField
from wtforms.validators import InputRequired


class ComputeForm(wtf.Form):
    file_data = wtf.FileField(label='Import File')
    file_name = StringField(label='DataSet Name', validators=[InputRequired(), validators.Length(max=25)])

    button_compute = wtf.SubmitField(label='Compute')
    button_export_table = wtf.SubmitField(label='Export Table')

