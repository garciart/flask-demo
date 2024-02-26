"""Class Manager

Usage:
- python3 -m flask --app cm run
- python3 -m flask --app cm run --debug # Allow hot reload
"""
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import app, db
from app.models import User, Course, Role


@app.shell_context_processor
def make_shell_context():
    # type: () -> dict
    """Start a Python interpreter in the context of the application
    for debugging.

    Usage: flask-shell

    :return: A dictionary of symbols for the Flask shell
    :rtype: dict
    """
    return {'sa': sa, 'so': so, 'db': db, 'User': User, 'Course': Course,
            'Role': Role}
