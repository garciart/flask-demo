"""Data for app.db database

Usage: python3 -m app.init_db
"""
from app import app, db
from app.models import User, Course, Role, Association

# flake8: noqa: E502
# pylint: disable=C0301

def main():
    """Drop and recreate the database
    """

    with app.app_context():
        db.drop_all()
        db.create_all()

        u1 = User(username='Leto.Atreides', user_group='Atreides', user_email='leto@atreides.com')
        u2 = User(username='Paul.Atreides', user_group='Atreides', user_email='paul@atreides.com')
        u3 = User(username='Jessica.Nerus', user_group='Atreides', user_email='jessica@atreides.com')
        u4 = User(username='Thufir.Hawat', user_group='Atreides', user_email='thufir@atreides.com')
        u5 = User(username='Gurney.Halleck', user_group='Atreides', user_email='gurney@atreides.com')
        u6 = User(username='Duncan.Idaho', user_group='Atreides', user_email='duncan@atreides.com')
        u7 = User(username='Vladmir.Harkonnen', user_group='Harkonnen', user_email='vladmir@harkonnen.com')
        u8 = User(username='Glossu.Rabban ', user_group='Harkonnen', user_email='glossu@harkonnen.com')
        u9 = User(username='Feyd.Rautha.Rabban', user_group='Harkonnen', user_email='feyd@harkonnen.com')
        u10 = User(username='Piter.De.Vries', user_group='Harkonnen', user_email='piter@harkonnen.com')
        u11 = User(username='Shaddam.Corrino.IV', user_group='Corrino', user_email='shaddam@corrino.com')
        u12 = User(username='Irulan.Corrino', user_group='Corrino', user_email='irulan@corrino.com')
        u13 = User(username='Liet.Kynes', user_group='Fremen', user_email='liet@fremen.com')
        u14 = User(username='Chani.Kynes', user_group='Fremen', user_email='chani@fremen.com')
        u15 = User(username='Stilgar.Tabr', user_group='Fremen', user_email='Stilgar@fremen.com')

        DEMO_PASSWORD = 'Change.Me.123'
        u1.set_password(DEMO_PASSWORD)
        u2.set_password(DEMO_PASSWORD)
        u3.set_password(DEMO_PASSWORD)
        u4.set_password(DEMO_PASSWORD)
        u5.set_password(DEMO_PASSWORD)
        u6.set_password(DEMO_PASSWORD)
        u7.set_password(DEMO_PASSWORD)
        u8.set_password(DEMO_PASSWORD)
        u9.set_password(DEMO_PASSWORD)
        u10.set_password(DEMO_PASSWORD)
        u11.set_password(DEMO_PASSWORD)
        u12.set_password(DEMO_PASSWORD)
        u13.set_password(DEMO_PASSWORD)
        u14.set_password(DEMO_PASSWORD)
        u15.set_password(DEMO_PASSWORD)

        db.session.add_all([u1, u2, u3, u4, u5, u6, u7, u8, u9, u10, u11, u12, u13, u14, u15])

        c1 = Course(course_name='Building Secure Python Applications',
                    course_code='SDEV300',
                    course_desc='A hands-on study of best practices and strategies for building secure Python desktop and web applications.')
        c2 = Course(course_name='Detecting Software Vulnerabilities',
                    course_code='SDEV325',
                    course_desc='An in-depth, practical application of techniques and tools for detecting and documenting software vulnerabilities and risks.')
        c3 = Course(course_name='Database Security',
                    course_code='SDEV350',
                    course_desc='A study of processes and techniques for securing databases.')
        c4 = Course(course_name='Securing Mobile Apps',
                    course_code='SDEV355',
                    course_desc='A hands-on study of best practices for designing and building secure mobile applications.')
        c5 = Course(course_name='Secure Software Engineering',
                    course_code='SDEV360',
                    course_desc='An in-depth study of the processes, standards, and regulations associated with secure software engineering.')
        c6 = Course(course_name='Secure Programming in the Cloud',
                    course_code='SDEV400',
                    course_desc='A hands-on study of programming secure applications in the cloud.')
        c7 = Course(course_name='Mitigating Software Vulnerabilities',
                    course_code='SDEV425',
                    course_desc='An in-depth analysis and evaluation of the mitigation of software vulnerabilities.')
        c8 = Course(course_name='Risk Analysis and Threat Modeling',
                    course_code='SDEV455',
                    course_desc='An examination of the risks and threats associated with application development.')
        c9 = Course(course_name='Software Security Testing',
                    course_code='SDEV460',
                    course_desc='A hands-on study of exploits, attacks, and techniques used to penetrate application security defenses and strategies for mitigating such attacks.')

        db.session.add_all([c1, c2, c3, c4, c5, c6, c7, c8, c9])

        r1 = Role(role_name='Administrator')
        r2 = Role(role_name='Teacher')
        r3 = Role(role_name='Student')

        db.session.add_all([r1, r2, r3])

        a1 = Association(user_id='1', course_id='9', role_id='1')
        a2 = Association(user_id='2', course_id='8', role_id='2')
        a3 = Association(user_id='3', course_id='7', role_id='3')
        a4 = Association(user_id='4', course_id='6', role_id='3')
        a5 = Association(user_id='5', course_id='5', role_id='2')
        a6 = Association(user_id='6', course_id='4', role_id='1')
        a7 = Association(user_id='7', course_id='3', role_id='1')
        a8 = Association(user_id='8', course_id='2', role_id='2')
        a9 = Association(user_id='9', course_id='1', role_id='3')
        a10 = Association(user_id='10', course_id='1', role_id='3')
        a11 = Association(user_id='11', course_id='2', role_id='2')
        a12 = Association(user_id='12', course_id='3', role_id='1')
        a13 = Association(user_id='13', course_id='4', role_id='1')
        a14 = Association(user_id='14', course_id='5', role_id='2')
        a15 = Association(user_id='1', course_id='6', role_id='3')
        a16 = Association(user_id='2', course_id='7', role_id='3')
        a17 = Association(user_id='3', course_id='8', role_id='2')
        a18 = Association(user_id='4', course_id='9', role_id='1')
        a19 = Association(user_id='5', course_id='9', role_id='2')
        a20 = Association(user_id='6', course_id='8', role_id='3')
        a21 = Association(user_id='7', course_id='7', role_id='3')
        a22 = Association(user_id='8', course_id='6', role_id='2')
        a23 = Association(user_id='9', course_id='5', role_id='1')
        a24 = Association(user_id='10', course_id='4', role_id='1')
        a25 = Association(user_id='11', course_id='3', role_id='2')
        a26 = Association(user_id='12', course_id='2', role_id='3')
        a27 = Association(user_id='13', course_id='1', role_id='3')
        a28 = Association(user_id='14', course_id='1', role_id='2')
        a29 = Association(user_id='15', course_id='2', role_id='1')
        a30 = Association(user_id='15', course_id='3', role_id='2')

        db.session.add_all([a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, a11, a12, a13,
                            a14, a15, a16, a17, a18, a19, a20, a21, a22, a23, a24,
                            a25, a26, a27, a28, a29, a30])

        db.session.commit()

if __name__ == '__main__':
    main()
