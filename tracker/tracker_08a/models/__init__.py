"""Base class for the Tracker database models using SQLAlchemy ORM Declarative Mapping.
"""

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import declarative_base

# Create an instance of the SQLAlchemy class here to avoid circular imports
db = SQLAlchemy()

# Define the declarative base class for SQLAlchemy models
Base = declarative_base()
