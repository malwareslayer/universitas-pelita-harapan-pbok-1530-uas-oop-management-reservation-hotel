from uuid import uuid4
from flask import Blueprint, request, g
from flask.views import MethodView

from sqlalchemy.exc import IntegrityError

from hotel.models import Room

room = Blueprint('room', __name__)


class _Room(MethodView):

  def get(self, uuid: str | None = None):
    factory = g.get('factory', None)

    if not factory:
      return {'message': 'No Factory'}, 400

    session = factory()

    if uuid:
      _room = session.query(Room).filter(Room.id == uuid).one_or_none()

      if not _room:
        return {'message': 'Room not found'}, 404

      return _room, 200
    else:
      return {
        'data': [dict(_room) for _room in session.query(Room).all()]
      }

  def post(self):
    factory = g.get('factory', None)

    if not factory:
      return {'message': 'No Factory'}, 400

    session = factory()

    _room = Room(id=uuid4(), **request.get_json())

    session.add(_room)

    try:
      session.commit()
    except IntegrityError:
      session.rollback()

      return {'message': 'Room already exists'}, 409

    return dict(_room), 201

  def patch(self, uuid: str):
    factory = g.get('factory', None)

    if not factory:
      return {'message': 'No Factory'}, 400

    session = factory()

    _room = session.query(Room).filter(Room.id == uuid).update(**request.get_json())

    session.commit()

    return {'message': 'Successfully Update Room'}, 200

  def delete(self, uuid: str):
    factory = g.get('factory', None)

    if not factory:
      return {'message': 'No Factory'}, 400

    session = factory()

    _room = session.query(Room).filter(Room.id == uuid).first()

    if not _room:
      return {'message': 'Room not found'}, 404

    session.delete(_room)
    session.commit()

    return {'message': 'Successfully Delete Room'}, 204


view_func = _Room.as_view('room')

room.add_url_rule('/rooms', view_func=view_func, methods=['GET', 'POST'])
room.add_url_rule('/rooms/<uuid:str>', view_func=view_func, methods=['GET', 'PATCH', 'DELETE'])


__all__ = ['room']
