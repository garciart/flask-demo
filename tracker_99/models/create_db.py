"""Creates the Tracker database.
"""

from tracker_99.models import db
from tracker_99.models.models import Course, Member, Role, Association


def create_db():
    """Function to initialize the database (create tables and insert data)"""
    # Create tables if they don't exist
    db.create_all()

    # pylint: disable=line-too-long
    _courses = [
        Course(
            course_name='Introductory Programming',
            course_code='CMSC 115',
            course_group='CMSC',
            course_desc='A study of structured and object-oriented programming using the Java language.',
        ),
        Course(
            course_name='Intermediate Programming',
            course_code='CMSC 215',
            course_group='CMSC',
            course_desc='Further study of the Java programming language.',
        ),
        Course(
            course_name='Relational Database Concepts and Applications',
            course_code='CMSC 320',
            course_group='CMSC',
            course_desc='A study of the functions, underlying concepts, and applications of enterprise relational database management systems (RDBMS) in a business environment.',
        ),
        Course(
            course_name='Capstone in Computer Science',
            course_code='CMSC 495',
            course_group='CMSC',
            course_desc='An overview of computer technologies, with an emphasis on integration of concepts, practical application, and critical thinking.',
        ),
        Course(
            course_name='Building Secure Python Applications',
            course_code='SDEV 300',
            course_group='SDEV',
            course_desc='A hands-on study of best practices and strategies for building secure Python desktop and web applications.',
        ),
        Course(
            course_name='Detecting Software Vulnerabilities',
            course_code='SDEV 325',
            course_group='SDEV',
            course_desc='An in-depth, practical application of techniques and tools for detecting and documenting software vulnerabilities and risks.',
        ),
        Course(
            course_name='Database Security',
            course_code='SDEV 350',
            course_group='SDEV',
            course_desc='A study of processes and techniques for securing databases.',
        ),
        Course(
            course_name='Fundamentals of Computer Troubleshooting',
            course_code='CMIT 202',
            course_group='CMIT',
            course_desc='A thorough review of computer hardware and software, with emphasis on the application of current and appropriate computing safety and environmental practices.',
        ),
        Course(
            course_name='Fundamentals of Networking',
            course_code='CMIT 265',
            course_group='CMIT',
            course_desc='An introduction to networking technologies for local area networks, wide area networks, and wireless networks.',
        ),
        Course(
            course_name='Introduction to Linux',
            course_code='CMIT 291',
            course_group='CMIT',
            course_desc='A study of the Linux operating system.',
        ),
        Course(
            course_name='Mathematics for Data Science',
            course_code='DATA 230',
            course_group='DATA',
            course_desc='A practical introduction to the mathematical principles applied within the context of data science.',
        ),
        Course(
            course_name='Foundations of Data Science',
            course_code='DATA 300',
            course_group='DATA',
            course_desc='An examination of the role of data science within business and society.',
        ),
        Course(
            course_name='Introduction to Data Analytics',
            course_code='DATA 320',
            course_group='DATA',
            course_desc='A practical introduction to the methodology, practices, and requirements of data science to ensure that data is relevant and properly manipulated to solve problems and address a variety of real-world projects and business scenarios.',
        ),
        Course(
            course_name='Cybersecurity for Leaders and Managers',
            course_code='CSIA 300',
            course_group='CSIA',
            course_desc="A foundational study of cybersecurity principles, practices, and strategies in the establishment, management, and governance of an enterprise's cybersecurity program.",
        ),
        Course(
            course_name='Cybersecurity Processes and Technologies',
            course_code='CSIA 310',
            course_group='CSIA',
            course_desc='A study of the processes and technologies used to implement and manage enterprise IT security operations.',
        ),
        Course(
            course_name='Cybersecurity in Business and Industry',
            course_code='CSIA 350',
            course_group='CSIA',
            course_desc='A study of the application and integration of cybersecurity principles, frameworks, standards, and best practices to the management, governance, and policy development processes for businesses.',
        ),
    ]
    # pylint: enable=line-too-long

    # Add courses and commit
    db.session.add_all(_courses)
    db.session.commit()

    _members = [
        Member(member_name='Admin', member_email='admin@tracker.com', is_admin=True),
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

    _roles = [
        Role(role_name='Unassigned', role_privilege='0'),
        Role(role_name='Student', role_privilege='1'),
        Role(role_name='Teacher', role_privilege='10'),
        Role(role_name='Chair', role_privilege='20'),
    ]

    # Add roles and commit
    db.session.add_all(_roles)
    db.session.commit()

    # Do not use the 'Unassigned' role or role_id 1
    # Students in the 'Unassigned' role will be deleted
    # from the Associations table to save space
    db.session.query(Role).filter(Role.role_id == 1).delete()
    db.session.commit()

    # Add member, course, and role associations
    _associations = [
        Association(member_id='2', course_id='1', role_id='4'),
        Association(member_id='3', course_id='1', role_id='3'),
        Association(member_id='4', course_id='1', role_id='2'),
        Association(member_id='5', course_id='1', role_id='2'),
        Association(member_id='6', course_id='2', role_id='4'),
        Association(member_id='7', course_id='2', role_id='3'),
        Association(member_id='8', course_id='2', role_id='2'),
        Association(member_id='9', course_id='2', role_id='2'),
        Association(member_id='10', course_id='3', role_id='4'),
        Association(member_id='11', course_id='3', role_id='3'),
        Association(member_id='12', course_id='3', role_id='2'),
        Association(member_id='13', course_id='3', role_id='2'),
        Association(member_id='14', course_id='4', role_id='4'),
        Association(member_id='15', course_id='4', role_id='3'),
        Association(member_id='16', course_id='4', role_id='2'),
        Association(member_id='2', course_id='4', role_id='2'),
        Association(member_id='3', course_id='5', role_id='4'),
        Association(member_id='4', course_id='5', role_id='3'),
        Association(member_id='5', course_id='5', role_id='2'),
        Association(member_id='6', course_id='5', role_id='2'),
        Association(member_id='7', course_id='6', role_id='4'),
        Association(member_id='8', course_id='6', role_id='3'),
        Association(member_id='9', course_id='6', role_id='2'),
        Association(member_id='10', course_id='6', role_id='2'),
        Association(member_id='11', course_id='7', role_id='4'),
        Association(member_id='12', course_id='7', role_id='3'),
        Association(member_id='13', course_id='7', role_id='2'),
        Association(member_id='14', course_id='7', role_id='2'),
        Association(member_id='15', course_id='8', role_id='4'),
        Association(member_id='16', course_id='8', role_id='3'),
        Association(member_id='2', course_id='8', role_id='2'),
        Association(member_id='3', course_id='8', role_id='2'),
        Association(member_id='4', course_id='9', role_id='4'),
        Association(member_id='5', course_id='9', role_id='3'),
        Association(member_id='6', course_id='9', role_id='2'),
        Association(member_id='7', course_id='9', role_id='2'),
        Association(member_id='8', course_id='10', role_id='4'),
        Association(member_id='9', course_id='10', role_id='3'),
        Association(member_id='10', course_id='10', role_id='2'),
        Association(member_id='11', course_id='10', role_id='2'),
        Association(member_id='12', course_id='11', role_id='4'),
        Association(member_id='13', course_id='11', role_id='3'),
        Association(member_id='14', course_id='11', role_id='2'),
        Association(member_id='15', course_id='11', role_id='2'),
        Association(member_id='16', course_id='12', role_id='4'),
        Association(member_id='2', course_id='12', role_id='3'),
        Association(member_id='3', course_id='12', role_id='2'),
        Association(member_id='4', course_id='12', role_id='2'),
        Association(member_id='5', course_id='13', role_id='4'),
        Association(member_id='6', course_id='13', role_id='3'),
        Association(member_id='7', course_id='13', role_id='2'),
        Association(member_id='8', course_id='13', role_id='2'),
        Association(member_id='9', course_id='14', role_id='4'),
        Association(member_id='10', course_id='14', role_id='3'),
        Association(member_id='11', course_id='14', role_id='2'),
        Association(member_id='12', course_id='14', role_id='2'),
        Association(member_id='13', course_id='15', role_id='4'),
        Association(member_id='14', course_id='15', role_id='3'),
        Association(member_id='15', course_id='15', role_id='2'),
        Association(member_id='16', course_id='15', role_id='2'),
        Association(member_id='2', course_id='16', role_id='4'),
        Association(member_id='3', course_id='16', role_id='3'),
        Association(member_id='4', course_id='16', role_id='2'),
        Association(member_id='5', course_id='16', role_id='2'),
    ]

    # Add associations and commit
    db.session.add_all(_associations)
    db.session.commit()
