import wtforms as wtf
from flask_wtf.file import FileRequired
from wtforms import validators, StringField
from wtforms.validators import InputRequired


class ComputeForm(wtf.Form):
    file_name = StringField(label='DataSet Name', validators=[InputRequired(), validators.Length(max=25)])

    file_data = wtf.FileField(label='Import File', validators=[FileRequired()])

    button_compute = wtf.SubmitField(label='Compute')
