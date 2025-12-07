import os

from flask import Flask
from .config import Config
from sqlalchemy import inspect
# from logging.config import dictConfig
from flask_socketio import SocketIO

from .db import db
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user


# Voor logging in python debugger "Server Side":
# dictConfig({
#     'version': 1,
#     'formatters': {'default': {
#         'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
#     }},
#     'handlers': {'wsgi': {
#         'class': 'logging.StreamHandler',
#         'stream': 'ext://flask.logging.wsgi_errors_stream',
#         'formatter': 'default'
#     }},
#     'root': {
#         'level': 'INFO',
#         'handlers': ['wsgi']
#     }
# })

socketio = SocketIO()
login_manager = LoginManager()

def create_app():
    # create and configure the app
    app = Flask(__name__, instance_relative_config=False)

    # load the instance config, if it exists, when not testing
    # app.config.from_pyfile('config.py', silent=True)

    app.config.from_object(Config)
    db.init_app(app)

    # login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "login"

    # Chack If DB needs to be created
    # with app.app_context():
    #     db.create_all()  # Create sql tables for our data models
    
    # chack if tables exist
    # inspector = inspect(db.engine)
    # print("Tables in DB:", inspector.get_table_names(schema="public"))

    # ensure the instance folder exists
    # try:
    #     os.makedirs(app.instance_path)
    # except OSError:
    #     pass

    from .routes import main
    app.register_blueprint(main)

    socketio.init_app(app, logger=True, engineio_logger=True, cors_allowed_origins="*")
    
    
    return app

# app = create_app()

