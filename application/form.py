from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, widgets, SelectMultipleField
from wtforms.validators import DataRequired, ValidationError


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


def validate_at_least_two_checked(form, field):
    checked_count = len(field.data)
    if checked_count < 2:
        raise ValidationError("Please select at least two checkboxes.")


class UserDataForm(FlaskForm):
    checkboxes = [
        ('normal_operation', 'Normal Operation'),
        ('high_load', 'High Load'),
        ('low_load', 'Low Load'),
        ('disconnect_generator_3_high', 'Disconnect Generator 3 (High Load)'),
        ('disconnect_generator_3_low', 'Disconnect Generator 3 (Low Load)'),
        ('disconnect_line_bus_5_6_high', 'Disconnect Line Between Bus 5 and 6 (High Load)'),
        ('disconnect_line_bus_5_6_low', 'Disconnect Line Between Bus 5 and 6 (Low Load)')
    ]
    example = MultiCheckboxField('Label', choices=checkboxes, validators=[validate_at_least_two_checked])
    submit = SubmitField('Generate Data')
