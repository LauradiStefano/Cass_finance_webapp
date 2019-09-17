import wtforms as wtf


class ComputeForm(wtf.Form):
    type_choice = wtf.SelectField('Model',
                                  choices=[('0', 'Vasicek'), ('1', 'CIR'), ('2', 'Nelson Siegel'), ('3', 'Svensson')],
                                  default='0')

    # Vasicek distribution
    kappa_vasicek = wtf.FloatField(label='Kappa', default=1,
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

    # Svensson
    beta0_svensson = wtf.FloatField(label='Beta0', default=1,
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
    import_file = wtf.FloatField(label='Import',
                                 validators=[wtf.validators.InputRequired()])
    discount_factor = wtf.RadioField(label='Discount Factor', choices=[('0', 'Discount'), ('1', 'Factor Spot Race')],
                                     default='0')
    least_fmin = wtf.RadioField(label='Optimization Method', choices=[('0', 'Least Squares'), ('1', 'Fmin')],
                                default='0')

    button_compute = wtf.SubmitField(label='Compute')
    button_export_table = wtf.SubmitField(label='Export Table')
    # button_view_details = wtf.SubmitField(label='View Details')
