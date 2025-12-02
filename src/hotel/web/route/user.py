from uuid import uuid4
from flask import Blueprint, request, g
from flask.views import MethodView
from sqlalchemy.exc import IntegrityError

from hotel.models import User

user = Blueprint('user', __name__)


class _User(MethodView):

  def get(self, uuid: str | None = None):
    factory = g.get('factory', None)

    if not factory:
      return {'message': 'No Factory'}, 400

    session = factory()

    if uuid:
      _user = session.query(User).filter(User.id == uuid).one_or_none()

      if not _user:
        return {'message': 'User not found'}, 404

      return _user, 200
    else:
      return {
        'data': [dict(_user) for _user in session.query(User).all()]
      }

  def post(self):
    factory = g.get('factory', None)

    if not factory:
      return {'message': 'No Factory'}, 400

    session = factory()

    _user = User(id=str(uuid4()), **request.get_json())

    session.add(_user)

    try:
      session.commit()
    except IntegrityError:
      session.rollback()

      return {'message': 'User Already Exists'}, 409

    return _user, 201

  def patch(self, uuid: str):
    factory = g.get('factory', None)

    if not factory:
      return {'message': 'No Factory'}, 400

    session = factory()

    _user = session.query(User).filter(User.id == uuid).update(**request.get_json())

    session.commit()

    return {'message': 'Successfully Update User'}, 200

  def delete(self, uuid: str):
    factory = g.get('factory', None)

    if not factory:
      return {'message': 'No Factory'}, 400

    session = factory()

    _user = session.query(User).filter(User.id == uuid).first()

    if not _user:
      return {'message': 'User not found'}, 404

    session.delete(_user)
    session.commit()

    return {'message': 'Successfully Delete User'}, 204


view_func = _User.as_view('user')

user.add_url_rule('/users', view_func=view_func, methods=['GET', 'POST'])

user.add_url_rule('/users/<uuid:str>', view_func=view_func, methods=['GET', 'PATCH', 'DELETE'])

user.add_url_rule('/user', view_func=view_func)
