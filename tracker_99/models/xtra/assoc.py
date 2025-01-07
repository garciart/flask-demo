"""Association Class for the Member, Role, and Course database model
using SQLAlchemy ORM Declarative Mapping.
"""

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from tracker_99.models import db
from tracker_99.models.models import Course, Member, Role, Association


class Association(db.Model):
    """Association database model
    Note: This is a three-way relationship
    """
    __tablename__ = 'associations'

    course_id: Mapped[int] = mapped_column(ForeignKey(Course.course_id), primary_key=True,
                                           nullable=False)
    role_id: Mapped[int] = mapped_column(ForeignKey(Role.role_id), primary_key=True, nullable=False)
    member_id: Mapped[int] = mapped_column(ForeignKey(Member.member_id), primary_key=True,
                                           nullable=False)

    course: Mapped['Course'] = relationship(back_populates='associations')
    role: Mapped['Role'] = relationship(back_populates='associations')
    member: Mapped['Member'] = relationship(back_populates='associations')

    def has_access_to_course(self, course: 'Course', role_name: str) -> bool:
        """Check if the member has access to the course with a specific role."""
        for association in self.associations:
            if association.course == course and association.role.role_name == role_name:
                return True
        return False

    def to_dict(self):
        return {
            'course_id': self.course_id,
            'role_id': self.role_id,
            'member_id': self.member_id
        }
