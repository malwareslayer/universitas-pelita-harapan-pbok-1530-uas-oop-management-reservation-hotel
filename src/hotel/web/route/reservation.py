from uuid import uuid4
from flask import Blueprint, request, g
from flask.views import MethodView

from sqlalchemy.exc import IntegrityError

from hotel.models import Reservation

reservation = Blueprint('reservation', __name__)


class _Reservation(MethodView):

  def get(self, uuid: str | None = None):
    factory = g.get('factory', None)

    if not factory:
      return {'message': 'No Factory'}, 400

    session = factory()

    if uuid:
      _reservation = session.query(Reservation).filter(Reservation.id == uuid).one_or_none()

      if not _reservation:
        return {'message': 'Reservation not found'}, 404

      return _reservation, 200
    else:
      return {
        'data': [dict(_room) for _room in session.query(Reservation).all()]
      }

  def post(self):
    factory = g.get('factory', None)

    if not factory:
      return {'message': 'No Factory'}, 400

    session = factory()

    _reservation = Reservation(id=uuid4(), **request.get_json())

    session.add(_reservation)

    try:
      session.commit()
    except IntegrityError:
      session.rollback()

      return {'message': 'Reservation already exists'}, 409

    return dict(_reservation), 201

  def patch(self, uuid: str):
    factory = g.get('factory', None)

    if not factory:
      return {'message': 'No Factory'}, 400

    session = factory()

    _reservation = session.query(Reservation).filter(Reservation.id == uuid).update(**request.get_json())

    session.commit()

    return {'message': 'Successfully Update Reservation'}, 200

  def delete(self, uuid: str):
    factory = g.get('factory', None)

    if not factory:
      return {'message': 'No Factory'}, 400

    session = factory()

    _reservation = session.query(Reservation).filter(Reservation.id == uuid).first()

    if not _reservation:
      return {'message': 'Reservation Not Found'}, 404

    session.delete(_reservation)
    session.commit()

    return {'message': 'Successfully Delete Reservation'}, 204


view_func = _Reservation.as_view('reservation')

reservation.add_url_rule('/reservations', view_func=view_func, methods=['GET', 'POST'])
reservation.add_url_rule('/reservations/<uuid:str>', view_func=view_func, methods=['GET', 'PATCH', 'DELETE'])


__all__ = ['reservation']
