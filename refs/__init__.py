import secrets

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    balance = db.Column(db.Integer, default=0, nullable=False)

    def __repr__(self):
        return "<User %r>" % self.username


class Referral(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False)
    referer_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    referer = db.relationship("User", backref=db.backref("users", lazy=True))
    referral_code = db.Column(
        db.String(60), unique=True, nullable=False, default=secrets.token_urlsafe(8)
    )
    joined = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return "<Referral %r>" % self.referral_code
