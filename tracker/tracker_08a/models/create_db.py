"""Creates the Tracker database.
"""
from .. import db
from .user import User


def create_db():
    """Function to initialize the database (create tables and insert data)"""
    # Create tables if they don't exist
    db.create_all()

    # Add default users if needed (only if users don't exist yet)
    _users = [
        User(user_name='Admin', user_email='admin@example.com'),
        User(user_name='Leto.Atreides', user_email='leto@atreides.com'),
        User(user_name='Paul.Atreides', user_email='paul@atreides.com'),
        User(user_name='Jessica.Nerus', user_email='jessica@atreides.com'),
        User(user_name='Thufir.Hawat', user_email='thufir@atreides.com'),
        User(user_name='Gurney.Halleck', user_email='gurney@atreides.com'),
        User(user_name='Duncan.Idaho', user_email='duncan@atreides.com'),
        User(user_name='Vladimir.Harkonnen', user_email='vladmir@harkonnen.com'),
        User(user_name='Glossu.Rabban', user_email='glossu@harkonnen.com'),
        User(user_name='Feyd.Rautha.Rabban', user_email='feyd@harkonnen.com'),
        User(user_name='Piter.De.Vries', user_email='piter@harkonnen.com'),
        User(user_name='Shaddam.Corrino.IV', user_email='shaddam@corrino.com'),
        User(user_name='Irulan.Corrino', user_email='irulan@corrino.com'),
        User(user_name='Liet.Kynes', user_email='liet@fremen.com'),
        User(user_name='Chani.Kynes', user_email='chani@fremen.com'),
        User(user_name='Stilgar.Tabr', user_email='Stilgar@fremen.com')
    ]

    _users[0].set_password('Change.Me.321')

    _demo_password = 'Change.Me.123'

    # Set passwords for users
    for u in _users[1:]:
        u.set_password(_demo_password)

    # Add users and commit
    db.session.add_all(_users)
    db.session.commit()
