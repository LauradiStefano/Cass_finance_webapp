from wtforms import validators


def greater_than_zero(form, field):
    value = field.data
    if value <= 0:
        raise validators.ValidationError('The value must be greater than 0')
