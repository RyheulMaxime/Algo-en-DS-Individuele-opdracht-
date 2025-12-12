import os

from flask import Flask
from .config import Config
from sqlalchemy import inspect
# from logging.config import dictConfig

from .db import db
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user


login_manager = LoginManager()

def create_app():
    # create and configure the app
    app = Flask(__name__, instance_relative_config=False)

    # load the instance config, if it exists, when not testing
    # app.config.from_pyfile('config.py', silent=True)

    app.config.from_object(Config)
    db.init_app(app)

    login_manager.init_app(app)
    login_manager.login_view = "login"

    # ensure the instance folder exists
    # try:
    #     os.makedirs(app.instance_path)
    # except OSError:
    #     pass

    from .routes import main
    app.register_blueprint(main)
    
    
    return app

# app = create_app()

