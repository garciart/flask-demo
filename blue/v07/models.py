"""Classes for the Blue database models.
"""

from v07 import db

__all__ = ['Course', 'CourseGroup']


class CourseGroup(db.Model):
    """Course group database model"""

    __tablename__ = 'course_groups'

    course_group_id = db.Column(db.Integer, primary_key=True)
    course_group_code = db.Column(db.String(8), index=True, unique=True)
    course_group_name = db.Column(db.String(64), unique=True)

    courses = db.relationship('Course', back_populates='course_group_assoc', lazy='dynamic')

    course_group_desc = db.Column(db.String(256), nullable=True)

    def __repr__(self):
        return (
            f'{{"course_group_id": "{self.course_group_id}",'
            f'"course_group_code": "{self.course_group_code}",'
            f'"course_group_name": "{self.course_group_name}",'
            f'"course_group_desc": "{self.course_group_desc}"}}'
        )


class Course(db.Model):
    """Course database model"""

    __tablename__ = 'courses'

    course_id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(64), index=True, unique=True)
    course_code = db.Column(db.String(16))

    course_group_id = db.Column(db.Integer, db.ForeignKey('course_groups.course_group_id'))
    course_group_assoc = db.relationship('CourseGroup', back_populates='courses')

    course_desc = db.Column(db.String(256), nullable=True)

    def __repr__(self):
        return (
            f'{{"course_id": "{self.course_id}",'
            f'"course_name": "{self.course_name}",'
            f'"course_code": "{self.course_code}",'
            f'"course_group_id": "{self.course_group_id}",'
            f'"course_desc": "{self.course_desc}"}}'
        )
