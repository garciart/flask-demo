"""Database Factory.

To initialize:
  flask init-db
  flask --app app init-db

To access in a function:
  from . import db
  db.init_app(app)
"""
import sqlite3
import click
from flask import current_app, g
from werkzeug import exceptions
from app.app_utils import validate_input


def get_db():
    # type: () -> sqlite3.Connection
    """Connect to the database if not already connected

    :return: The database connection
    :rtype: sqlite3.Connection
    """
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['SQLALCHEMY_DATABASE_URI'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        # Tells the connection to return rows that behave like dicts to allow
        # accessing columns by name
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    # type: (exceptions) -> None
    """Close the database.

    :param exceptions e: The reason for closing from the
    werkzeug.exceptions class

    :return: None
    """
    # Validate inputs
    if e is not None:
        validate_input('e', e, exceptions)

    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    # type: () -> None
    """Command to initialize the database from a SQL script.

    Warning - This command clears the existing data and creates new tables.

    Usage:
      - flask init-db
      - flask --app app init-db

    :return: None
    """
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
def init_db_command():
    # type: () -> None
    """Wrapper for the init_db() function.

    :return: None
    """
    init_db()
    click.echo('Database initialized.')


def init_app(app):
    """Register the close_db and init_db_command functions with
    the application instance.

    To access in a function:
      from . import db;
      db.init_app(app)

    :param Flask.app.Flask app: The application instance

    :return: None
    """
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
