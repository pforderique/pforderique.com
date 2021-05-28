from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import MY_SECRET_KEY
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = 'dbmain.db'

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = MY_SECRET_KEY
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}'.format(DB_NAME)
    db.init_app(app)

    from .views import views
    from .testviews import testviews
    from .dbapi import dbapi
    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(testviews, url_prefix="/test")
    app.register_blueprint(dbapi, url_prefix="/dbapi")

    create_database(app)

    return app

def create_database(app:Flask):
    # create only it it doesnt exist yet
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print("Database created!")