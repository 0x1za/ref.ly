from flask import Flask
from flask_sqlalchemy import SQLAlchemy


def create_app(config_filename):
    app = Flask(__name__)
    app.config.from_pyfile(config_filename)

    db = SQLAlchemy(app)

    return db
