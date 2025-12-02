from __future__ import annotations

from hotel.models import User


def test_add_user_persists(manager, session_factory):
  created = manager.add_user('Alice', 'alice@example.com')

  session = session_factory()
  try:
    stored = session.query(User).filter_by(id=created.id).one()
    assert stored.email == 'alice@example.com'
  finally:
    session.close()


def test_list_users_returns_dicts(manager):
  manager.add_user('Alice', 'alice@example.com')
  manager.add_user('Bob', 'bob@example.com')

  users = manager.list_users()

  assert len(users) == 2
  assert {'id', 'name', 'email', 'created', 'updated'} <= users[0].keys()
  assert sorted(user['email'] for user in users) == ['alice@example.com', 'bob@example.com']

