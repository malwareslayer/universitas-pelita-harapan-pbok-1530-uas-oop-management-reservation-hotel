from __future__ import annotations

from hotel.models import Guest


def test_add_guest_with_user_link(manager, user_factory, session_factory):
  user = user_factory(name='User1', email='user1@example.com')
  guest = manager.add_guest('Guest1', user.id)

  session = session_factory()
  try:
    stored = session.query(Guest).filter_by(id=guest.id).one()
    assert stored.user == user.id
  finally:
    session.close()


def test_add_guest_without_user(manager, session_factory):
  guest = manager.add_guest('Solo Guest')

  session = session_factory()
  try:
    stored = session.query(Guest).filter_by(id=guest.id).one()
    assert stored.user is None
  finally:
    session.close()


def test_list_guests(manager):
  manager.add_guest('Guest A')
  manager.add_guest('Guest B')

  guests = manager.list_guests()

  assert len(guests) == 2
  assert {'id', 'name', 'created', 'updated'} <= guests[0].keys()

