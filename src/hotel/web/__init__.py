from flask import Flask, g, jsonify, current_app
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine.create import create_engine

from .route.guest import guest
from .route.reservation import reservation
from .route.user import user
from .route.room import room

app = Flask(__name__)

app.config.setdefault('ENGINE', None)
app.config.setdefault('FACTORY', None)


app.register_blueprint(user)
app.register_blueprint(room)
app.register_blueprint(guest)
app.register_blueprint(reservation)

@app.before_request
def inject():
  engine = current_app.config.get('ENGINE')
  factory = current_app.config.get('FACTORY')

  if engine:
    g.engine = engine

  if factory:
    g.factory = factory


def create(url: str):
  engine = create_engine(url)
  factory = sessionmaker(bind=engine)

  app.config['ENGINE'] = engine
  app.config['FACTORY'] = factory

  app.run(host='127.0.0.1', port=8080, debug=True)


__all__ = ['app', 'create']
