import wtforms as wtf
from flask_wtf.file import FileRequired
from wtforms import validators, StringField
from wtforms.validators import InputRequired


class ComputeForm(wtf.Form):
    file_name = StringField(label='DataSet Name', validators=[InputRequired(), validators.Length(max=25)])

    file_data = wtf.FileField(label='Import File')

    model_choices = wtf.RadioField(label='Model:',
                                   choices=[('0', 'Linear Interpolation'),
                                            ('1', 'Constant Forward')], default='0')

    button_compute = wtf.SubmitField(label='Compute')
    button_export_table = wtf.SubmitField(label='Export Table')
    button_view_details = wtf.SubmitField(label='View Details')
