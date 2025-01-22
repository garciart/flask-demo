"""Administration forms manager
"""

from flask_wtf import FlaskForm
from wtforms import SubmitField


class SimpleForm(FlaskForm):
    """Basic form to capture data on submit."""

    submit = SubmitField()
