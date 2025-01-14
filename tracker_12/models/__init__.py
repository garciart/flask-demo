"""Base class for the Tracker database models using SQLAlchemy ORM Declarative Mapping.
"""

from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

# Create an instance of the SQLAlchemy class
db = SQLAlchemy()

migrate = Migrate()
