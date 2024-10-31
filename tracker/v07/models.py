"""Classes for the Tracker database models.
"""

from v07 import db


class Course(db.Model):
    """Course database model"""

    __tablename__ = 'courses'

    course_id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(64), unique=True, nullable=False)
    course_code = db.Column(db.String(64), unique=True, nullable=False)
    course_group = db.Column(db.String(64), nullable=False)
    course_desc = db.Column(db.String(256), nullable=True)

    def __repr__(self):
        return (
            f'{{"course_id": "{self.course_id}",'
            f'"course_name": "{self.course_name}",'
            f'"course_code": "{self.course_code}",'
            f'"course_group": "{self.course_group}",'
            f'"course_desc": "{self.course_desc}"}}'
        )
