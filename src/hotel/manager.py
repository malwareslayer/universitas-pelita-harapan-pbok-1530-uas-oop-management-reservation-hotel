from __future__ import annotations
from datetime import date
from typing import Callable
from uuid import UUID, uuid4

from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound

from hotel.exceptions import InvalidDateRangeError, RoomUnavailableError
from hotel.models import Guest, Reservation, Room, User, room as make_room

SessionFactory = Callable[[], Session]


class HotelManager:
  def __init__(self, session_factory: SessionFactory):
    if not callable(session_factory):
      raise ValueError('session_factory must be callable')
    self._factory = session_factory

  def add_user(self, name: str, email: str) -> User:
    session = self._factory()
    try:
      user = User(id=str(uuid4()), name=name, email=email)
      session.add(user)
      session.commit()
      session.refresh(user)
      return user
    except Exception:
      session.rollback()
      raise
    finally:
      session.close()

  def list_users(self) -> list[dict]:
    session = self._factory()
    try:
      return [dict(user) for user in session.query(User).order_by(User.created.desc())]
    finally:
      session.close()

  def add_guest(self, name: str, user_id: str | None = None) -> Guest:
    session = self._factory()
    try:
      guest = Guest(id=uuid4(), name=name, user=user_id)
      session.add(guest)
      session.commit()
      session.refresh(guest)
      return guest
    except Exception:
      session.rollback()
      raise
    finally:
      session.close()

  def list_guests(self) -> list[dict]:
    session = self._factory()
    try:
      return [dict(guest) for guest in session.query(Guest).order_by(Guest.created.desc())]
    finally:
      session.close()

  def add_room(self, number: int, room_type: str, rate: float, *, capacity: int = 2, active: bool = True) -> Room:
    session = self._factory()
    try:
      room = make_room(room_type, id=uuid4(), number=number, rate=rate, capacity=capacity, active=active)
      session.add(room)
      session.commit()
      session.refresh(room)
      return room
    except Exception:
      session.rollback()
      raise
    finally:
      session.close()

  def list_rooms(self) -> list[dict]:
    session = self._factory()
    try:
      return [dict(room) for room in session.query(Room).order_by(Room.number.asc())]
    finally:
      session.close()

  def _validate_reservation(self, checkin: date, checkout: date):
    if checkout <= checkin:
      raise InvalidDateRangeError('checkout must be later than checkin')

  def _ensure_room_available(self, session: Session, room_id: UUID, checkin: date, checkout: date):
    conflict = session.query(Reservation).filter(
      Reservation.room == room_id,
      Reservation.checkin < checkout,
      Reservation.checkout > checkin,
    ).first()
    if conflict:
      raise RoomUnavailableError('room already booked for selected dates')

  def create_reservation(self, guest_id: UUID | str, room_id: UUID | str, checkin: date, checkout: date) -> Reservation:
    self._validate_reservation(checkin, checkout)
    session = self._factory()
    try:
      guest_key = self._to_uuid(guest_id)
      room_key = self._to_uuid(room_id)
      guest = session.get(Guest, guest_key)
      room = session.get(Room, room_key)
      if not guest:
        raise NoResultFound('guest not found')
      if not room:
        raise NoResultFound('room not found')

      self._ensure_room_available(session, room_key, checkin, checkout)

      nights = (checkout - checkin).days
      total = room.price(nights)
      reservation = Reservation(
        id=uuid4(),
        guest=guest.id,
        room=room.id,
        checkin=checkin,
        checkout=checkout,
        total=total,
      )
      session.add(reservation)
      session.commit()
      session.refresh(reservation)
      return reservation
    except Exception:
      session.rollback()
      raise
    finally:
      session.close()

  def list_reservations(self) -> list[dict]:
    session = self._factory()
    try:
      return [dict(reservation) for reservation in session.query(Reservation).order_by(Reservation.created.desc())]
    finally:
      session.close()

  def cancel_reservation(self, reservation_id: UUID | str) -> bool:
    session = self._factory()
    try:
      reservation_key = self._to_uuid(reservation_id)
      reservation = session.get(Reservation, reservation_key)
      if not reservation:
        return False
      session.delete(reservation)
      session.commit()
      return True
    except Exception:
      session.rollback()
      raise
    finally:
      session.close()

  @staticmethod
  def _to_uuid(value: UUID | str) -> UUID:
    if isinstance(value, UUID):
      return value
    return UUID(str(value))


__all__ = ['HotelManager']
