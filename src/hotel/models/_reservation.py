from datetime import date, datetime

from sqlalchemy import Date, DateTime, Float, ForeignKey, UUID
from sqlalchemy.orm import Mapped, MappedColumn, Relationship

from hotel.models.orm.declarative import __base__
from hotel.models._guest import Guest
from hotel.models._room import Room


class Reservation(__base__):
  __tablename__ = 'reservations'

  id: MappedColumn[UUID] = MappedColumn('id', UUID, primary_key=True)
  guest: MappedColumn[str] = MappedColumn(ForeignKey('guests.id'), nullable=False)
  room: MappedColumn[str] = MappedColumn(ForeignKey('rooms.id'), nullable=False)
  checkin: MappedColumn[date] = MappedColumn(Date, nullable=False)
  checkout: MappedColumn[date] = MappedColumn(Date, nullable=False)
  total: MappedColumn[float] = MappedColumn(Float, nullable=False)
  created: MappedColumn[datetime] = MappedColumn(DateTime, default=datetime.utcnow)

  guests: Mapped[Guest] = Relationship(back_populates='reservations')
  rooms: Mapped[Room] = Relationship(back_populates='reservations')

  def __iter__(self):
    for column in self.__table__.columns:
      yield column.name, getattr(self, column.name, None)

  def nights(self) -> int:
    return (self.checkout - self.checkin).days


__all__ = ['Reservation']

