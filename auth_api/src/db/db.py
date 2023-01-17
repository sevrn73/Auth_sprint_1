from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from core.config import db_settings


db = SQLAlchemy()
SQLALCHEMY_DATABASE_URI = f'postgresql://{db_settings.user}:{db_settings.host}@{":".join((db_settings.host, str(db_settings.port)))}/{db_settings.dbname}'

def init_db(app: Flask):
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    db.init_app(app) 