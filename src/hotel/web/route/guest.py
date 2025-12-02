from uuid import uuid4
from flask import Blueprint, request, g
from flask.views import MethodView
from sqlalchemy.exc import IntegrityError

from hotel.models import Guest, User


guest = Blueprint('guest', __name__)


class _Guest(MethodView):

  def get(self, uuid: str | None = None):
    factory = g.get('factory', None)

    if not factory:
      return {'message': 'No Factory'}, 400

    session = factory()

    if uuid:
      _guest = session.query(Guest).filter(Guest.id == uuid).one_or_none()

      if not _guest:
        return {'message': 'Guest not found'}, 404

      return _guest, 200
    else:
      return {
        'data': [dict(_guest) for _guest in session.query(Guest).all()]
      }

  def post(self):
    factory = g.get('factory', None)

    if not factory:
      return {'message': 'No Factory'}, 400

    session = factory()

    _guest = Guest(
      id=str(uuid4()),
      **request.get_json()
    )

    _user = session.query(Guest).filter(Guest.id == _guest.user).one_or_none()

    if not _user:
      return {'message': 'User not found'}, 404

    session.add(_guest)

    try:
      session.commit()
    except IntegrityError:
      session.rollback()

      return {'message': 'Guest Already Exists'}, 409

    return _guest, 201

  def patch(self, uuid: str):
    factory = g.get('factory', None)

    if not factory:
      return {'message': 'No Factory'}, 400

    session = factory()

    _guest = session.query(Guest).filter(Guest.id == uuid).update(**request.get_json())

    session.commit()

    return {'message': 'Successfully Update Guest'}, 200

  def delete(self, uuid: str):
    factory = g.get('factory', None)

    if not factory:
      return {'message': 'No Factory'}, 400

    session = factory()

    _guest = session.query(Guest).filter(Guest.id == uuid).first()

    if not _guest:
      return {'message': 'Guest Not Found'}, 404

    session.delete(_guest)
    session.commit()

    return {'message': 'Successfully Delete Guest'}, 204


view_func = _Guest.as_view('guest')

guest.add_url_rule('/guests', view_func=view_func, methods=['GET', 'POST'])
guest.add_url_rule('/guests/<uuid:str>', view_func=view_func, methods=['GET', 'PATCH', 'DELETE'])


__all__ = ['guest']
