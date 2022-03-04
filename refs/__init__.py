from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app(config_filename=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile(config_filename)
    initialize_extensions(app)
    register_blueprints(app)
    Migrate(app, db)
    return app


def initialize_extensions(app):
    db.init_app(app)


def register_blueprints(app):
    from refs.referrals import referrals_blueprint
    from refs.users import users_blueprint

    app.register_blueprint(referrals_blueprint)
    app.register_blueprint(users_blueprint)
