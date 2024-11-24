"""Creates the Tracker database.
"""
from tracker_13.models import db
from tracker_13.models.member import Member


def create_db():
    """Function to initialize the database (create tables and insert data)"""
    # Create tables if they don't exist
    db.create_all()

    # Add default members if needed (only if members don't exist yet)
    _members = [
        Member(member_name='Admin', member_email='admin@tracker.com'),
        Member(member_name='Leto.Atreides', member_email='leto.atreides@atreides.com'),
        Member(member_name='Paul.Atreides', member_email='paul.atreides@atreides.com'),
        Member(member_name='Jessica.Nerus', member_email='jessica.nerus@atreides.com'),
        Member(member_name='Thufir.Hawat', member_email='thufir.hawat@atreides.com'),
        Member(member_name='Gurney.Halleck', member_email='gurney.halleck@atreides.com'),
        Member(member_name='Duncan.Idaho', member_email='duncan.idaho@atreides.com'),
        Member(member_name='Vladimir.Harkonnen', member_email='vladmir.harkonnen@harkonnen.com'),
        Member(member_name='Glossu.Rabban', member_email='glossu.rabban@harkonnen.com'),
        Member(member_name='Feyd-Rautha.Rabban', member_email='feyd-rautha.rabban@harkonnen.com'),
        Member(member_name='Piter.DeVries', member_email='piter.devries@harkonnen.com'),
        Member(member_name='Shaddam.Corrino', member_email='shaddam.corrino@corrino.com'),
        Member(member_name='Irulan.Corrino', member_email='irulan.corrino@corrino.com'),
        Member(member_name='Liet.Kynes', member_email='liet.kynes@fremen.com'),
        Member(member_name='Chani.Kynes', member_email='chani.kynes@fremen.com'),
        Member(member_name='Stilgar.Tabr', member_email='stilgar.tabr@fremen.com'),
    ]

    # Set admin password
    _members[0].set_password('Change.Me.321')

    # Set passwords for members
    _demo_password = 'Change.Me.123'

    for m in _members[1:]:
        m.set_password(_demo_password)

    # Add members and commit
    db.session.add_all(_members)
    db.session.commit()
