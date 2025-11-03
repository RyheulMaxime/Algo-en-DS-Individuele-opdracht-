import os

from flask import Flask
from .config import Config
from sqlalchemy import inspect

from .db import db


def create_app():
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)


    # load the instance config, if it exists, when not testing
    # app.config.from_pyfile('config.py', silent=True)

    app.config.from_object(Config)
    db.init_app(app)

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

    return app