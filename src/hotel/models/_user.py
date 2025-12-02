from datetime import datetime

from faker import Faker

from sqlalchemy import DateTime, String, UUID
from sqlalchemy.orm import MappedColumn, Mapped, Relationship

from hotel.models.orm.declarative import __base__
from hotel.models.orm.column import FakeColumn


class User(__base__):
  __tablename__ = 'users'
  __faker__ = Faker()

  id: MappedColumn[str] = FakeColumn('id', String(36), pattern='uuid4', primary_key=True)
  name: MappedColumn[str] = FakeColumn('name', String(256), pattern='name', nullable=False)
  email: MappedColumn[str] = FakeColumn('email', String(256), pattern=['email', 'company_email'], nullable=False, unique=True)
  created: MappedColumn[datetime] = MappedColumn('created', DateTime(), default=datetime.utcnow)
  updated: MappedColumn[datetime] = MappedColumn('updated', DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)

  guests: Mapped[list['Guest']] = Relationship(back_populates='users')

  def __iter__(self):
    for column in self.__table__.columns:
      yield column.name, getattr(self, column.name, None)


__all__ = ['User']
