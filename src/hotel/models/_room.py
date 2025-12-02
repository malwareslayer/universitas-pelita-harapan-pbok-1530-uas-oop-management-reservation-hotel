from enum import Enum
from datetime import datetime

from sqlalchemy import Boolean, DateTime, Float, Integer, UUID, Enum as SQLEnum
from sqlalchemy.orm import Mapped, MappedColumn, Relationship

from hotel.models.orm.declarative import __base__


class RoomType(Enum):
  STANDARD = 'STANDARD'
  DELUXE = 'DELUXE'
  SUITE = 'SUITE'


class Room(__base__):
  __tablename__ = 'rooms'
  __pricing__: float = 1.0

  id: MappedColumn[UUID] = MappedColumn('id', UUID(), primary_key=True)
  number: Mapped[str] = MappedColumn('number', Integer(), unique=True, nullable=False)
  _type: Mapped[str] = MappedColumn('type', SQLEnum(RoomType), nullable=False)
  rate: Mapped[float] = MappedColumn('rate', Float(), nullable=False)
  capacity: Mapped[int] = MappedColumn('capacity', Integer(), nullable=False, default=2)
  active: Mapped[bool] = MappedColumn('active', Boolean(), default=True)
  created: MappedColumn[datetime] = MappedColumn('created', DateTime(), default=datetime.utcnow)
  updated: MappedColumn[datetime] = MappedColumn('updated', DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)

  reservations: Mapped[list['Reservation']] = Relationship(back_populates='rooms')

  __mapper_args__ = {
    'polymorphic_on': _type,
    'polymorphic_identity': 'room',
  }

  def __iter__(self):
    for column in self.__table__.columns:
      k = column.name
      v = getattr(self, column.name, getattr(self, f'_{column.name}', None))

      if isinstance(v, RoomType):
        v = v.value

      yield k, v

  def price(self, nights: int) -> float:
    if nights <= 0:
      raise ValueError('Number of nights must be positive')

    return round(self.rate * self.__pricing__ * nights, 2)


class StandardRoom(Room):
  __mapper_args__ = {'polymorphic_identity': RoomType.STANDARD}
  __pricing__ = 1.0


class DeluxeRoom(Room):
  __mapper_args__ = {'polymorphic_identity': RoomType.DELUXE}
  __pricing__ = 1.35


class SuiteRoom(Room):
  __mapper_args__ = {'polymorphic_identity': RoomType.SUITE}
  __pricing__ = 1.75


__all__ = [
  'RoomType',
  'Room',
  'StandardRoom',
  'DeluxeRoom',
  'SuiteRoom',
]

