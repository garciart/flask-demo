"""Class for the Role database model using SQLAlchemy ORM Declarative Mapping.
"""

from typing import List

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from tracker_99.models import db
from tracker_99.models.xtra.assoc import Association

CASCADE_ARG = 'all, delete-orphan'


class Role(db.Model):
    """Role database model
    """
    __tablename__ = 'roles'

    role_id: Mapped[int] = mapped_column(primary_key=True)
    role_name: Mapped[str] = mapped_column(String(64), unique=True)
    role_privilege: Mapped[int] = mapped_column(unique=True)

    associations: Mapped[List['Association']] = relationship('Association', back_populates='role',
                                                             cascade=CASCADE_ARG)

    def to_dict(self):
        return {
            'role_id': self.role_id,
            'role_name': self.role_name,
            'role_privilege': self.role_privilege
        }
