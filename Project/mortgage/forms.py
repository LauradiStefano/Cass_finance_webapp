import wtforms as wtf
from wtforms import validators
from common_validators import greater_than_zero


class ComputeForm(wtf.Form):
    capital_amount = wtf.FloatField(label='Capital Amount', default=1000,
                                    validators=[wtf.validators.InputRequired(), greater_than_zero])

    loan_term = wtf.FloatField(label='Loan Term (Year)', default=2,
                               validators=[wtf.validators.InputRequired(),
                                           validators.NumberRange(min=1, message='The value must be greater than 1')])

    frequency = wtf.SelectField('Frequency', choices=[('0', 'Mensile'), ('1', 'Trimestrale'), ('2', 'Quadrimestrale'),
                                                      ('3', 'Semestrale'), ('4', 'Annua')], default='0')
    interest_rate = wtf.FloatField(label='Interest Rate \((\%) \)', default=2,
                                   validators=[wtf.validators.InputRequired()])

    button_compute = wtf.SubmitField(label='Compute')
    button_view_details = wtf.SubmitField(label='View Details')
