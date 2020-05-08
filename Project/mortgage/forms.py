import wtforms as wtf
from wtforms import validators
from common_validators import greater_than_zero


class ComputeForm(wtf.Form):
    capital_amount = wtf.FloatField(label='Capital Amount', default=1000,
                                    validators=[wtf.validators.InputRequired(), greater_than_zero])

    loan_term = wtf.FloatField(label='Loan Term (Year)', default=2,
                               validators=[wtf.validators.InputRequired(),
                                           validators.NumberRange(min=1, message='The value must be greater than 1')])

    frequency = wtf.SelectField('Frequency', choices=[('12', 'Mensile'), ('4', 'Trimestrale'), ('3', 'Quadrimestrale'),
                                                      ('2', 'Semestrale'), ('1', 'Annua')], default='12')
    interest_rate = wtf.FloatField(label='Interest Rate \((\%) \)', default=2,
                                   validators=[wtf.validators.InputRequired()])

    button_compute = wtf.SubmitField(label='Compute')
    button_view_details = wtf.SubmitField(label='View Details')
    button_export_table = wtf.SubmitField(label='Export Table')
