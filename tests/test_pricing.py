from datetime import date, timedelta

import pytest

from hotel._manager.room import DeluxeRoom, Room, StandardRoom, SuiteRoom


def _build_room(cls, base_rate=100.0):
    room = cls(number="101", base_rate=base_rate, capacity=2)
    return room


def test_standard_room_price():
    room = _build_room(StandardRoom)
    assert room.price(3) == pytest.approx(300.0)


def test_deluxe_room_price():
    room = _build_room(DeluxeRoom)
    assert room.price(2) == pytest.approx(270.0)


def test_suite_room_price():
    room = _build_room(SuiteRoom)
    assert room.price(1) == pytest.approx(175.0)


def test_price_invalid_nights():
    room = _build_room(StandardRoom)
    with pytest.raises(ValueError):
        room.price(0)

