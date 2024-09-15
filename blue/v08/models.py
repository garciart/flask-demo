"""Classes for the Blue database models.
"""

from v08 import db

__all__ = ['Course', 'CourseGroup']


class CourseGroup(db.Model):
    """Course group database model"""

    __tablename__ = 'course_groups'

    course_group_id = db.Column(db.Integer, primary_key=True)
    course_group_code = db.Column(db.String(4), unique=True, nullable=False)
    course_group_name = db.Column(db.String(64), unique=True, nullable=False)
    course_group_desc = db.Column(db.String(256), nullable=True)

    # Define the relationship with Course
    course_rel = db.relationship('Course', back_populates='course_group_rel')

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
    course_name = db.Column(db.String(64), unique=True, nullable=False)
    course_code = db.Column(db.String(8), unique=True, nullable=False)
    course_desc = db.Column(db.String(256), nullable=True)

    # Foreign key to CourseGroup
    course_group_id = db.Column(db.Integer, db.ForeignKey('course_groups.course_group_id'))

    # Define the relationship with CourseGroup
    course_group_rel = db.relationship('CourseGroup', back_populates='course_rel')

    def __repr__(self):
        return (
            f'{{"course_id": "{self.course_id}",'
            f'"course_name": "{self.course_name}",'
            f'"course_code": "{self.course_code}",'
            f'"course_group_id": "{self.course_group_id}",'
            f'"course_desc": "{self.course_desc}"}}'
        )
