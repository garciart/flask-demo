"""Class for the Member database model using SQLAlchemy ORM Declarative Mapping.
"""

from typing import List, Optional

from sqlalchemy import String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from tracker_99.models import db
from tracker_99.models.xtra.assoc import Association

CASCADE_ARG = 'all, delete-orphan'


class Course(db.Model):
    """Course database model"""

    __tablename__ = 'courses'

    course_id: Mapped[int] = mapped_column(primary_key=True)
    course_name: Mapped[str] = mapped_column(String(64), nullable=False)
    course_code: Mapped[str] = mapped_column(String(64), nullable=False)
    course_group: Mapped[Optional[str]] = mapped_column(String(64))
    course_desc: Mapped[Optional[str]] = mapped_column(String(256))

    # Here are the unique constraints
    __table_args__ = (
        UniqueConstraint('course_name'),
        UniqueConstraint('course_code'),
        UniqueConstraint('course_name', 'course_code', name='uq_course_name_code'),
    )

    associations: Mapped[List['Association']] = relationship('Association',
                                                             back_populates='course',
                                                             cascade=CASCADE_ARG
                                                             )

    def to_dict(self):
        return {
            'course_id': self.course_id,
            'course_name': self.course_name,
            'course_code': self.course_code,
            'course_desc': self.course_desc,
        }
