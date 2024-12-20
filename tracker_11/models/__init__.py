"""Base class for the Tracker database models using SQLAlchemy ORM Declarative Mapping.
"""

from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

# Create an instance of the SQLAlchemy class to configure and interact with the database
db = SQLAlchemy()

# Create an instance of the Migrate class that will be used to manage database migrations
migrate = Migrate()
