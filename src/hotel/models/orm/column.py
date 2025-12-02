from typing import TypeVar

from sqlalchemy.schema import Column
from sqlalchemy.types import TypeEngine
from sqlalchemy.sql.base import SchemaEventTarget
from sqlalchemy.sql.sqltypes import Integer

T = TypeVar('T')


class FakeColumn(Column):
  def __init__(
    self,
    __name_pos: str | TypeEngine[T] | SchemaEventTarget | None = None,
    __type_pos: TypeEngine[T] | SchemaEventTarget | None = None,
    *args: SchemaEventTarget,
    pattern: str | list[str] | None = None,
    **kwargs
  ):
    info = kwargs.get('info', {})

    if isinstance(__name_pos, Integer) or isinstance(__type_pos, Integer):
      primary_key = kwargs.get('primary_key', False)
      autoincrement = kwargs.get('auto_increment', False)

      if primary_key and pattern:
        raise ValueError('Faker Is Not Supported For Integer Primary Key Columns')

      if autoincrement:
        info.setdefault('increment', 1)
    else:
      if not pattern:
        raise ValueError('Faker & Pattern Required')

      info.setdefault('pattern', pattern)

    kwargs.setdefault('info', info)

    super().__init__(__name_pos, __type_pos, *args, **kwargs)


__all__ = ['FakeColumn']
