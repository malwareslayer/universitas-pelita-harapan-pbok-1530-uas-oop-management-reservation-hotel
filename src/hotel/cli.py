import argparse

from collections.abc import Sequence

from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError, IntegrityError
from sqlalchemy.engine.create import create_engine

from hotel.models import __base__, User
from hotel.web import create


argument = argparse.ArgumentParser(prog='ml', description='Machine Learning SQL Injection Collector')
command = argument.add_subparsers(dest='command')


def main(argv: Sequence[str] | None = None) -> int:
  database = command.add_parser('db', help='Database')
  db = database.add_subparsers(dest='db')

  c = db.add_parser('create', help='Initialize Database Hotel')
  c.add_argument(
    'url',
    type=str,
    nargs='?',
    default='sqlite:///db/main.db',
    help='Path To Create The Database For Storing Ingestion Payload Malicious & Benign',
  )
  c.add_argument(
    '--fake-count-user',
    type=int,
    default=50,
    help='How Much Fake Users To Create In The Database',
  )

  application = command.add_parser('app', help='Database')
  application.add_argument(
    'url',
    type=str,
    nargs='?',
    default='sqlite:///db/main.db',
    help='Path To Create The Database For Storing Ingestion Payload Malicious & Benign',
  )

  parse = argument.parse_args(argv)

  match parse.command:
    case 'db':
      match parse.db:
        case 'create':
          engine = create_engine(parse.url)

          try:
            __base__.metadata.create_all(engine)
          except (argparse.ArgumentError, OperationalError) as e:
            raise ConnectionError(str(e)) from e

          factory = sessionmaker(bind=engine)
          session = factory()

          for _ in range(parse.fake_count_user):
            user = User.fake()

            session.add(user)

            try:
              session.commit()
            except IntegrityError:
              session.rollback()
        case _:
          raise AttributeError('Unknown Command')
    case 'app':
      create(parse.url)
    case _:
      raise AttributeError('Unknown Command')

  return 0


__all__ = ['main']
