from __future__ import annotations

import pytest

from hotel.models import Room


def test_add_room(manager, session_factory):
  created = manager.add_room(101, 'standard', 100.0)

  session = session_factory()
  try:
    stored = session.query(Room).filter_by(id=created.id).one()
    assert stored.number == 101
    assert stored.rate == 100.0
  finally:
    session.close()


def test_list_rooms_sorted(manager):
  manager.add_room(102, 'standard', 90.0)
  manager.add_room(101, 'standard', 80.0)

  rooms = manager.list_rooms()

  assert [room['number'] for room in rooms] == [101, 102]


def test_add_room_invalid_type(manager):
  with pytest.raises(ValueError):
    manager.add_room(999, 'unknown', 50.0)

