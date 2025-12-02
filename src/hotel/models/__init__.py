from ._user import User
from ._room import RoomType, Room, StandardRoom, DeluxeRoom, SuiteRoom
from ._guest import Guest
from ._reservation import Reservation

from .orm.declarative import __base__
from .orm.column import FakeColumn


def room(_type: str, **kwargs):
  if _type.lower() == 'standard':
    cls = StandardRoom
  elif _type.lower() == 'deluxe':
    cls = DeluxeRoom
  elif _type.lower() == 'suite':
    cls = SuiteRoom
  else:
    raise ValueError(f'Room Type {_type!r} is not supported')

  return cls(**kwargs)


__all__ = [
  'User',
  'RoomType',
  'Room',
  'StandardRoom',
  'DeluxeRoom',
  'SuiteRoom',
  'Guest',
  'Reservation',
  'FakeColumn',
  '__base__',
  'room',
]
