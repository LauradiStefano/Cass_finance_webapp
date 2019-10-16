import wtforms as wtf
from wtforms import validators, StringField
from wtforms.validators import InputRequired


class ComputeForm(wtf.Form):
    model_choice = wtf.SelectField('Model', choices=[('0', 'Vasicek'), ('1', 'CIR'),
                                                     ('2', 'Nelson Siegel'), ('3', 'Svensson')], default='0')

    name_parameters = {
        '0': ['$$ \kappa $$', r'$$ \theta $$', '$$ \sigma $$', r'$$ v_{0} $$'],
        '1': ['$$ \kappa $$', r'$$ \theta $$', '$$ \sigma $$', r'$$ v_{0} $$'],
        '2': [r'$$ \beta_{0} $$', r'$$ \beta_{1} $$', r'$$ \beta_{2} $$', r'$$ \tau $$'],
        '3': [r'$$ \beta_{0} $$', r'$$ \beta_{1} $$', r'$$ \beta_{2} $$', r'$$ \beta_{3} $$', r'$$ \tau_{1} $$',
              r'$$ \tau_{2} $$']}

    file_name = StringField(label='Save output as', validators=[InputRequired(), validators.Length(max=25)])

    # Vasicek distribution
    kappa_vasicek = wtf.FloatField(label=name_parameters['0'][0], default=0.1,
                                   validators=[InputRequired()])
    theta_vasicek = wtf.FloatField(label=name_parameters['0'][1], default=0.05,
                                   validators=[InputRequired()])
    sigma_vasicek = wtf.FloatField(label=name_parameters['0'][2], default=0.03,
                                   validators=[InputRequired()])
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
    beta0_svensson = wtf.FloatField(label=name_parameters['3'][0], default=1,
                                    validators=[InputRequired()])
    beta1_svensson = wtf.FloatField(label=name_parameters['3'][1], default=1,
                                    validators=[InputRequired()])
    beta2_svensson = wtf.FloatField(label=name_parameters['3'][2], default=1,
                                    validators=[InputRequired()])
    beta3_svensson = wtf.FloatField(label=name_parameters['3'][3], default=1,
                                    validators=[InputRequired()])
    tau1_svensson = wtf.FloatField(label=name_parameters['3'][4], default=1,
                                   validators=[InputRequired()])
    tau2_svensson = wtf.FloatField(label=name_parameters['3'][5], default=1,
                                   validators=[InputRequired()])

    # Contract parameters
    file_data = wtf.FileField(label='Import File')

    discount_factor = wtf.RadioField(label='Discount Factor-Spot Rate', choices=[('0', 'Spot Rate'),
                                                                                 ('1', 'Discount Factor')], default='0')
    least_fmin = wtf.RadioField(label='Optimization Method', choices=[('0', 'Non Linear Least Squares'), ('1', 'Fmin')],
                                default='0')

    button_compute = wtf.SubmitField(label='Compute')
    button_export_table = wtf.SubmitField(label='Export Table')
    button_view_details = wtf.SubmitField(label='View Details')
