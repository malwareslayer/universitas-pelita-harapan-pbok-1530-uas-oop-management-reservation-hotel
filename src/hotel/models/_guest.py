from typing import List
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, UUID
from sqlalchemy.orm import Mapped, MappedColumn, Relationship

from hotel.models.orm.declarative import __base__
from hotel.models._user import User


class Guest(__base__):
  __tablename__ = 'guests'

  id: MappedColumn[UUID] = MappedColumn('id', UUID, primary_key=True)
  user: MappedColumn[User] = MappedColumn(ForeignKey('users.id'), nullable=True)
  name: MappedColumn[str] = MappedColumn('name', String(100), nullable=False)
  created: MappedColumn[datetime] = MappedColumn('created', DateTime, default=datetime.utcnow)
  updated: MappedColumn[datetime] = MappedColumn('updated', DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

  users: Mapped['User'] = Relationship(back_populates='guests')
  reservations: Mapped[List['Reservation']] = Relationship(back_populates='guests')

  def __iter__(self):
    for column in self.__table__.columns:
      yield column.name, getattr(self, column.name, None)


__all__ = ['Guest']
