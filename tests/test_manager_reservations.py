from __future__ import annotations

from datetime import date, timedelta
from uuid import uuid4

import pytest
from sqlalchemy.exc import NoResultFound

from hotel.exceptions import InvalidDateRangeError, RoomUnavailableError
from hotel.models import Reservation


def _dates(days: int = 2):
  start = date.today()
  return start, start + timedelta(days=days)


def test_create_reservation_success(manager, guest_factory, room_factory, session_factory):
  guest = guest_factory()
  room = room_factory(number=200)
  checkin, checkout = _dates()

  reservation = manager.create_reservation(guest.id, room.id, checkin, checkout)

  session = session_factory()
  try:
    stored = session.query(Reservation).filter_by(id=reservation.id).one()
    assert stored.total == room.price(1 * (checkout - checkin).days)
  finally:
    session.close()


def test_create_reservation_invalid_dates(manager, guest_factory, room_factory):
  guest = guest_factory()
  room = room_factory(number=201)
  start = date.today()
  with pytest.raises(InvalidDateRangeError):
    manager.create_reservation(guest.id, room.id, start, start)


def test_create_reservation_missing_guest(manager, room_factory):
  room = room_factory(number=202)
  checkin, checkout = _dates()
  with pytest.raises(NoResultFound):
    manager.create_reservation(str(uuid4()), room.id, checkin, checkout)


def test_create_reservation_missing_room(manager, guest_factory):
  guest = guest_factory()
  checkin, checkout = _dates()
  with pytest.raises(NoResultFound):
    manager.create_reservation(guest.id, str(uuid4()), checkin, checkout)


def test_create_reservation_room_unavailable(manager, guest_factory, room_factory):
  guest = guest_factory()
  room = room_factory(number=203)
  checkin, checkout = _dates()
  manager.create_reservation(guest.id, room.id, checkin, checkout)

  with pytest.raises(RoomUnavailableError):
    manager.create_reservation(guest.id, room.id, checkin + timedelta(days=1), checkout + timedelta(days=1))


def test_list_reservations(manager, guest_factory, room_factory):
  guest = guest_factory()
  room = room_factory(number=204)
  checkin, checkout = _dates()
  manager.create_reservation(guest.id, room.id, checkin, checkout)

  reservations = manager.list_reservations()

  assert len(reservations) == 1
  assert {'id', 'guest', 'room', 'checkin', 'checkout', 'total'} <= reservations[0].keys()


def test_cancel_reservation(manager, guest_factory, room_factory, session_factory):
  guest = guest_factory()
  room = room_factory(number=205)
  checkin, checkout = _dates()
  reservation = manager.create_reservation(guest.id, room.id, checkin, checkout)

  deleted = manager.cancel_reservation(reservation.id)
  assert deleted is True

  session = session_factory()
  try:
    assert session.query(Reservation).filter_by(id=reservation.id).one_or_none() is None
  finally:
    session.close()


def test_cancel_reservation_missing(manager):
  assert manager.cancel_reservation(str(uuid4())) is False
