"""main forms manager.
"""
from flask_wtf import FlaskForm
from wtforms import widgets, SelectMultipleField, SubmitField


class MultiCheckboxField(SelectMultipleField):
    """Create the MultiCheckboxField widget
    """
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class SimpleForm(FlaskForm):
    """Parameters for a simple form template.
    """
    planets = MultiCheckboxField('Label')
    # example = RadioField('Label')
    submit = SubmitField('Submit')
