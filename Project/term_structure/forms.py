import wtforms as wtf


class ComputeForm(wtf.Form):
    model_choice = wtf.SelectField('Model', choices=[('0', 'Vasicek'), ('1', 'CIR'),
                                                     ('2', 'Nelson Siegel'), ('3', 'Svensson')], default='0')

    name_parameters = {
        '0': ['k', 't', 's', 'r'],
        '1': ['k', 't', 's', 'r'],
        '2': ['beta0', 'beta1', 'beta2', 'tau'],
        '3': ['beta0', 'beta1', 'beta2', 'tau1', 'tau2']}

    # Vasicek distribution
    kappa_vasicek = wtf.FloatField(label='name_parameters[''][0]', default=1,
                                   validators=[wtf.validators.InputRequired()])
    theta_vasicek = wtf.FloatField(label='Theta', default=1,
                                   validators=[wtf.validators.InputRequired()])
    sigma_vasicek = wtf.FloatField(label='Sigma', default=1,
                                   validators=[wtf.validators.InputRequired()])
    rho_vasicek = wtf.FloatField(label='Rho', default=1,
                                 validators=[wtf.validators.InputRequired()])

    # Cir distribution
    kappa_cir = wtf.FloatField(label='Kappa', default=1,
                               validators=[wtf.validators.InputRequired()])
    theta_cir = wtf.FloatField(label='Theta', default=1,
                               validators=[wtf.validators.InputRequired()])
    sigma_cir = wtf.FloatField(label='Sigma', default=1,
                               validators=[wtf.validators.InputRequired()])
    rho_cir = wtf.FloatField(label='Rho', default=1,
                             validators=[wtf.validators.InputRequired()])

    # Nelson Siegel
    beta0_nelson = wtf.FloatField(label='Beta0', default=1,
                                  validators=[wtf.validators.InputRequired()])
    beta1_nelson = wtf.FloatField(label='Beta1', default=1,
                                  validators=[wtf.validators.InputRequired()])
    beta2_nelson = wtf.FloatField(label='Beta2', default=1,
                                  validators=[wtf.validators.InputRequired()])
    tau_nelson = wtf.FloatField(label='Tau', default=1,
                                validators=[wtf.validators.InputRequired()])

    # Svensson distribution
    beta0_svensson = wtf.FloatField(label='beta', default=1,
                                    validators=[wtf.validators.InputRequired()])
    beta1_svensson = wtf.FloatField(label='Beta1', default=1,
                                    validators=[wtf.validators.InputRequired()])
    beta2_svensson = wtf.FloatField(label='Beta2', default=1,
                                    validators=[wtf.validators.InputRequired()])
    beta3_svensson = wtf.FloatField(label='Beta3', default=1,
                                    validators=[wtf.validators.InputRequired()])
    tau1_svensson = wtf.FloatField(label='Tau1', default=1,
                                   validators=[wtf.validators.InputRequired()])
    tau2_svensson = wtf.FloatField(label='Tau2', default=1,
                                   validators=[wtf.validators.InputRequired()])

    # Contract parameters
    file_name = wtf.FileField(label='Import File')

    discount_factor = wtf.RadioField(label='Discount Factor', choices=[('0', 'Discount Factor'), ('1', 'Spot Race')],
                                     default='0')
    least_fmin = wtf.RadioField(label='Optimization Method', choices=[('0', 'Least Squares'), ('1', 'Fmin')],
                                default='0')

    button_compute = wtf.SubmitField(label='Compute')
    button_export_table = wtf.SubmitField(label='Export Table')
    button_view_details = wtf.SubmitField(label='View Details') 
