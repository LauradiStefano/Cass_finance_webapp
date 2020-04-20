import wtforms as wtf
from wtforms import validators, StringField
from wtforms.validators import InputRequired

from common_validators import greater_than_zero


class ComputeForm(wtf.Form):
    model_choice = wtf.SelectField('Model',
                                   choices=[('1', 'Cox-Ingersoll-Ross'), ('2', 'Nelson-Siegel'), ('3', 'Svensson'),
                                            ('0', 'Vasicek')], default='1')

    name_parameters = {
        '0': ['$$ \kappa $$', r'$$ \theta $$', '$$ \sigma $$', r'$$ v_{0} $$'],
        '1': ['$$ \kappa $$', r'$$ \theta $$', '$$ \sigma $$', r'$$ v_{0} $$'],
        '2': [r'$$ \beta_{0} $$', r'$$ \beta_{1} $$', r'$$ \beta_{2} $$', r'$$ \tau $$'],
        '3': [r'$$ \beta_{0} $$', r'$$ \beta_{1} $$', r'$$ \beta_{2} $$', r'$$ \beta_{3} $$', r'$$ \tau_{1} $$',
              r'$$ \tau_{2} $$']}

    file_name = StringField(label='DataSet Name', validators=[InputRequired(), validators.Length(max=25)])

    # Vasicek distribution
    kappa_vasicek = wtf.FloatField(label=name_parameters['0'][0], default=0.1,
                                   validators=[InputRequired(), greater_than_zero])
    theta_vasicek = wtf.FloatField(label=name_parameters['0'][1], default=0.05,
                                   validators=[InputRequired()])
    sigma_vasicek = wtf.FloatField(label=name_parameters['0'][2], default=0.03,
                                   validators=[InputRequired(), greater_than_zero])
    rho_vasicek = wtf.FloatField(label=name_parameters['0'][3], default=0.04,
                                 validators=[InputRequired()])

    # Cir distribution
    kappa_cir = wtf.FloatField(label=name_parameters['1'][0], default=0.1,
                               validators=[InputRequired()])
    theta_cir = wtf.FloatField(label=name_parameters['1'][1], default=0.05,
                               validators=[InputRequired()])
    sigma_cir = wtf.FloatField(label=name_parameters['1'][2], default=0.03,
                               validators=[InputRequired()])
    rho_cir = wtf.FloatField(label=name_parameters['1'][3], default=0.04,
                             validators=[InputRequired()])

    # Nelson Siegel
    beta0_nelson = wtf.FloatField(label=name_parameters['2'][0], default=0.02,
                                  validators=[InputRequired()])
    beta1_nelson = wtf.FloatField(label=name_parameters['2'][1], default=0.01,
                                  validators=[InputRequired()])
    beta2_nelson = wtf.FloatField(label=name_parameters['2'][2], default=0.5,
                                  validators=[InputRequired()])
    tau_nelson = wtf.FloatField(label=name_parameters['2'][3], default=2.3,
                                validators=[InputRequired()])

    # Svensson distribution
    beta0_svensson = wtf.FloatField(label=name_parameters['3'][0], default=0.472,
                                    validators=[InputRequired()])
    beta1_svensson = wtf.FloatField(label=name_parameters['3'][1], default=-1.086,
                                    validators=[InputRequired()])
    beta2_svensson = wtf.FloatField(label=name_parameters['3'][2], default=12.189,
                                    validators=[InputRequired()])
    beta3_svensson = wtf.FloatField(label=name_parameters['3'][3], default=-14.293,
                                    validators=[InputRequired()])
    tau1_svensson = wtf.FloatField(label=name_parameters['3'][4], default=2.132,
                                   validators=[InputRequired()])
    tau2_svensson = wtf.FloatField(label=name_parameters['3'][5], default=2.307,
                                   validators=[InputRequired()])

    # Contract parameters
    file_data = wtf.FileField(label='Import File')

    discount_factor = wtf.RadioField(label='Calibrate to:',
                                     choices=[('0', 'Spot Rate Term Structure'),
                                              ('1', 'Discount Factor Term Structure')], default='0')
    least_fmin = wtf.RadioField(label='Optimization Method:',
                                choices=[('0', ' Levenberg-Marquardt '),
                                         ('1', 'Downhill Simplex Algorithm')], default='0')

    button_compute = wtf.SubmitField(label='Compute')
    button_export_table = wtf.SubmitField(label='Export Table')
    button_view_details = wtf.SubmitField(label='View Details')
