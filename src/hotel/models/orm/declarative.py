import random

from faker import Faker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.sql.sqltypes import Integer

from .column import FakeColumn

class __base__(DeclarativeBase):
  __faker__ = Faker()

  @classmethod
  def fake(cls) -> '__base__':
    values = {}

    # noinspection PyTypeChecker
    for column in cls.__table__.columns:
      if not isinstance(column, FakeColumn):
        continue

      if isinstance(column.type, Integer) and column.autoincrement:
        values[column.name] = column.info.get('increment', 1)
        column.info['increment'] = values[column.name] + 1
      else:
        faker: Faker = cls.__faker__

        if not faker:
          continue

        pattern = column.info['pattern']

        if not pattern:
          raise ValueError('Faker Pattern Not Found')

        if isinstance(pattern, list):
          method = random.choice(pattern)
        else:
          method = pattern

        values[column.name] = getattr(faker, method)()

    return cls(**values)


__all__ = ['__base__']
