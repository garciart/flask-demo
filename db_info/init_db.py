"""Data for app.db database.

IMPORTANT - Ensure you have performed an initial migration of models.py first

Usage: python3 -m db_info.init_db
"""
import app
from app.models import (User, Course, Role, Association)

# Disable line length errors
# Flake8: noqa: E501
# pylint:disable=C0301:line-too-long


def main():
    """Drop and recreate the database
    """
    app_instance = app.create_app()

    with app_instance.app_context():
        app.db.drop_all()
        app.db.create_all()

        c1 = Course(course_name='Introductory Programming',
                    course_code='CMSC 115', course_group='CMSC',
                    course_desc='A study of structured and object-oriented programming using the Java language. ')
        c2 = Course(course_name='Intermediate Programming',
                    course_code='CMSC 215', course_group='CMSC',
                    course_desc='Further study of the Java programming language.')
        c3 = Course(course_name='Relational Database Concepts and Applications',
                    course_code='CMSC 320', course_group='CMSC',
                    course_desc='A study of the functions, underlying concepts, and applications of enterprise relational database management systems (RDBMS) in a business environment.')
        c4 = Course(course_name='Capstone in Computer Science',
                    course_code='CMSC 495', course_group='CMSC',
                    course_desc='An overview of computer technologies, with an emphasis on integration of concepts, practical application, and critical thinking.')
        c5 = Course(course_name='Building Secure Python Applications',
                    course_code='SDEV 300', course_group='SDEV',
                    course_desc='A hands-on study of best practices and strategies for building secure Python desktop and web applications.')
        c6 = Course(course_name='Detecting Software Vulnerabilities',
                    course_code='SDEV 325', course_group='SDEV',
                    course_desc='An in-depth, practical application of techniques and tools for detecting and documenting software vulnerabilities and risks.')
        c7 = Course(course_name='Database Security',
                    course_code='SDEV 350', course_group='SDEV',
                    course_desc='A study of processes and techniques for securing databases.')
        c8 = Course(course_name='Fundamentals of Computer Troubleshooting',
                    course_code='CMIT 202', course_group='CMIT',
                    course_desc='A thorough review of computer hardware and software, with emphasis on the application of current and appropriate computing safety and environmental practices.')
        c9 = Course(course_name='Fundamentals of Networking',
                    course_code='CMIT 265', course_group='CMIT',
                    course_desc='An introduction to networking technologies for local area networks, wide area networks, and wireless networks.')
        c10 = Course(course_name='Introduction to Linux',
                    course_code='CMIT 291', course_group='CMIT',
                    course_desc='A study of the Linux operating system.')
        c11 = Course(course_name='Mathematics for Data Science',
                    course_code='DATA 230', course_group='DATA',
                    course_desc='A practical introduction to the mathematical principles applied within the context of data science.')
        c12 = Course(course_name='Foundations of Data Science',
                    course_code='DATA 300', course_group='DATA',
                    course_desc='An examination of the role of data science within business and society.')
        c13 = Course(course_name='Introduction to Data Analytics',
                    course_code='DATA 320', course_group='DATA',
                    course_desc='A practical introduction to the methodology, practices, and requirements of data science to ensure that data is relevant and properly manipulated to solve problems and address a variety of real-world projects and business scenarios.')
        c14 = Course(course_name='Cybersecurity for Leaders and Managers',
                    course_code='CSIA 300', course_group='CSIA',
                    course_desc="A foundational study of cybersecurity principles, practices, and strategies in the establishment, management, and governance of an enterprise's cybersecurity program.")
        c15 = Course(course_name='Cybersecurity Processes and Technologies',
                    course_code='CSIA 310', course_group='CSIA',
                    course_desc='A study of the processes and technologies used to implement and manage enterprise IT security operations.')
        c16 = Course(course_name='Cybersecurity in Business and Industry',
                    course_code='CSIA 350', course_group='CSIA',
                    course_desc='A study of the application and integration of cybersecurity principles, frameworks, standards, and best practices to the management, governance, and policy development processes for businesses.')

        app.db.session.add_all([c1, c2, c3, c4, c5, c6, c7, c8, c9, c10,
                                c11, c12, c13, c14, c15, c16])

        r1 = Role(role_name='Chair', role_privilege='15')
        r2 = Role(role_name='Teacher', role_privilege='14')
        r3 = Role(role_name='Student', role_privilege='1')
        # Do not use the 'Not Assigned' role
        # Unassigned students will be deleted from the Associations table
        # to save space
        # r4 = Role(role_name='Not Assigned', role_privilege='0')

        app.db.session.add_all([r1, r2, r3])

        u1 = User(username='Admin', user_email='admin@example.com', is_admin=True)
        u2 = User(username='Leto.Atreides', user_email='leto@atreides.com', is_admin=False)
        u3 = User(username='Paul.Atreides', user_email='paul@atreides.com', is_admin=False)
        u4 = User(username='Jessica.Nerus', user_email='jessica@atreides.com', is_admin=False)
        u5 = User(username='Thufir.Hawat', user_email='thufir@atreides.com', is_admin=False)
        u6 = User(username='Gurney.Halleck', user_email='gurney@atreides.com', is_admin=False)
        u7 = User(username='Duncan.Idaho', user_email='duncan@atreides.com', is_admin=False)
        u8 = User(username='Vladimir.Harkonnen', user_email='vladmir@harkonnen.com', is_admin=False)
        u9 = User(username='Glossu.Rabban ', user_email='glossu@harkonnen.com', is_admin=False)
        u10 = User(username='Feyd.Rautha.Rabban', user_email='feyd@harkonnen.com', is_admin=False)
        u11 = User(username='Piter.De.Vries', user_email='piter@harkonnen.com', is_admin=False)
        u12 = User(username='Shaddam.Corrino.IV', user_email='shaddam@corrino.com', is_admin=False)
        u13 = User(username='Irulan.Corrino', user_email='irulan@corrino.com', is_admin=False)
        u14 = User(username='Liet.Kynes', user_email='liet@fremen.com', is_admin=False)
        u15 = User(username='Chani.Kynes', user_email='chani@fremen.com', is_admin=False)
        u16 = User(username='Stilgar.Tabr', user_email='Stilgar@fremen.com', is_admin=False)

        _demo_password = 'Change.Me.123'

        u1.set_password('admin')
        u2.set_password(_demo_password)
        u3.set_password(_demo_password)
        u4.set_password(_demo_password)
        u5.set_password(_demo_password)
        u6.set_password(_demo_password)
        u7.set_password(_demo_password)
        u8.set_password(_demo_password)
        u9.set_password(_demo_password)
        u10.set_password(_demo_password)
        u11.set_password(_demo_password)
        u12.set_password(_demo_password)
        u13.set_password(_demo_password)
        u14.set_password(_demo_password)
        u15.set_password(_demo_password)
        u16.set_password(_demo_password)

        app.db.session.add_all([u1, u2, u3, u4, u5, u6, u7, u8, u9, u10,
                                u11, u12, u13, u14, u15, u16])

        a1 = Association(user_id='2', course_id='1', role_id='1')
        a2 = Association(user_id='3', course_id='1', role_id='2')
        a3 = Association(user_id='4', course_id='1', role_id='3')
        a4 = Association(user_id='5', course_id='1', role_id='3')
        a5 = Association(user_id='6', course_id='2', role_id='1')
        a6 = Association(user_id='7', course_id='2', role_id='2')
        a7 = Association(user_id='8', course_id='2', role_id='3')
        a8 = Association(user_id='9', course_id='2', role_id='3')
        a9 = Association(user_id='10', course_id='3', role_id='1')
        a10 = Association(user_id='11', course_id='3', role_id='2')
        a11 = Association(user_id='12', course_id='3', role_id='3')
        a12 = Association(user_id='13', course_id='3', role_id='3')
        a13 = Association(user_id='14', course_id='4', role_id='1')
        a14 = Association(user_id='15', course_id='4', role_id='2')
        a15 = Association(user_id='16', course_id='4', role_id='3')
        a16 = Association(user_id='2', course_id='4', role_id='3')
        a17 = Association(user_id='3', course_id='5', role_id='1')
        a18 = Association(user_id='4', course_id='5', role_id='2')
        a19 = Association(user_id='5', course_id='5', role_id='3')
        a20 = Association(user_id='6', course_id='5', role_id='3')
        a21 = Association(user_id='7', course_id='6', role_id='1')
        a22 = Association(user_id='8', course_id='6', role_id='2')
        a23 = Association(user_id='9', course_id='6', role_id='3')
        a24 = Association(user_id='10', course_id='6', role_id='3')
        a25 = Association(user_id='11', course_id='7', role_id='1')
        a26 = Association(user_id='12', course_id='7', role_id='2')
        a27 = Association(user_id='13', course_id='7', role_id='3')
        a28 = Association(user_id='14', course_id='7', role_id='3')
        a29 = Association(user_id='15', course_id='8', role_id='1')
        a30 = Association(user_id='16', course_id='8', role_id='2')
        a31 = Association(user_id='2', course_id='8', role_id='3')
        a32 = Association(user_id='3', course_id='8', role_id='3')
        a33 = Association(user_id='4', course_id='9', role_id='1')
        a34 = Association(user_id='5', course_id='9', role_id='2')
        a35 = Association(user_id='6', course_id='9', role_id='3')
        a36 = Association(user_id='7', course_id='9', role_id='3')
        a37 = Association(user_id='8', course_id='10', role_id='1')
        a38 = Association(user_id='9', course_id='10', role_id='2')
        a39 = Association(user_id='10', course_id='10', role_id='3')
        a40 = Association(user_id='11', course_id='10', role_id='3')
        a41 = Association(user_id='12', course_id='11', role_id='1')
        a42 = Association(user_id='13', course_id='11', role_id='2')
        a43 = Association(user_id='14', course_id='11', role_id='3')
        a44 = Association(user_id='15', course_id='11', role_id='3')
        a45 = Association(user_id='16', course_id='12', role_id='1')
        a46 = Association(user_id='2', course_id='12', role_id='2')
        a47 = Association(user_id='3', course_id='12', role_id='3')
        a48 = Association(user_id='4', course_id='12', role_id='3')
        a49 = Association(user_id='5', course_id='13', role_id='1')
        a50 = Association(user_id='6', course_id='13', role_id='2')
        a51 = Association(user_id='7', course_id='13', role_id='3')
        a52 = Association(user_id='8', course_id='13', role_id='3')
        a53 = Association(user_id='9', course_id='14', role_id='1')
        a54 = Association(user_id='10', course_id='14', role_id='2')
        a55 = Association(user_id='11', course_id='14', role_id='3')
        a56 = Association(user_id='12', course_id='14', role_id='3')
        a57 = Association(user_id='13', course_id='15', role_id='1')
        a58 = Association(user_id='14', course_id='15', role_id='2')
        a59 = Association(user_id='15', course_id='15', role_id='3')
        a60 = Association(user_id='16', course_id='15', role_id='3')
        a61 = Association(user_id='2', course_id='16', role_id='1')
        a62 = Association(user_id='3', course_id='16', role_id='2')
        a63 = Association(user_id='4', course_id='16', role_id='3')
        a64 = Association(user_id='5', course_id='16', role_id='3')

        app.db.session.add_all([a1, a2, a3, a4, a5, a6, a7, a8, a9,
                                a10, a11, a12, a13, a14, a15, a16, a17, a18, a19,
                                a20, a21, a22, a23, a24, a25, a26, a27, a28, a29,
                                a30, a31, a32, a33, a34, a35, a36, a37, a38, a39,
                                a40, a41, a42, a43, a44, a45, a46, a47, a48, a49,
                                a50, a51, a52, a53, a54, a55, a56, a57, a58, a59,
                                a60, a61, a62, a63, a64])

        app.db.session.commit()


if __name__ == '__main__':
    main()
