from __future__ import annotations

from typing import Callable
from uuid import uuid4

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from hotel.manager import HotelManager
from hotel.models import __base__


@pytest.fixture
def engine():
  engine = create_engine('sqlite:///:memory:', future=True)
  __base__.metadata.create_all(engine)
  try:
    yield engine
  finally:
    __base__.metadata.drop_all(engine)
    engine.dispose()


@pytest.fixture
def session_factory(engine) -> Callable[[], Session]:
  factory = sessionmaker(bind=engine, expire_on_commit=False)

  def _factory() -> Session:
    return factory()

  return _factory


@pytest.fixture
def manager(session_factory) -> HotelManager:
  return HotelManager(session_factory)


@pytest.fixture
def user_factory(manager):
  def _create(name: str = 'User', email: str | None = None):
    email = email or f'{uuid4()}@example.com'
    return manager.add_user(name, email)

  return _create


@pytest.fixture
def guest_factory(manager, user_factory):
  def _create(name: str = 'Guest', *, attach_user: bool = True):
    user = user_factory() if attach_user else None
    user_id = user.id if user else None
    return manager.add_guest(name, user_id)

  return _create


@pytest.fixture
def room_factory(manager):
  def _create(
    number: int = 100,
    room_type: str = 'standard',
    rate: float = 120.0,
    *,
    capacity: int = 2,
    active: bool = True,
  ):
    return manager.add_room(number, room_type, rate, capacity=capacity, active=active)

  return _create
