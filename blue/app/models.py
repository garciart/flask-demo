from app import (db)

class Course(db.Model):
    """Course database model
    """
    __tablename__ = 'courses'

    course_id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(64), index=True, unique=True)
    course_code = db.Column(db.String(64))
    course_group = db.Column(db.String(64), nullable=True)
    course_desc = db.Column(db.String(256), nullable=True)

    def __repr__(self):
        return (f'{{"course_id": "{self.course_id}",'
                f'"course_name": "{self.course_name}",'
                f'"course_code": "{self.course_code}",'
                f'"course_group": "{self.course_group}",'
                f'"course_desc": "{self.course_desc}"}}')
