import random
import string

from refs import db


def random_code():
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=8))


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    balance = db.Column(db.Integer, default=0, nullable=False)
    referrals = db.relationship("Referral", backref=db.backref("user", lazy=True))

    def __repr__(self):
        return "<User %r>" % self.username


class Referral(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False)
    referer_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    referral_code = db.Column(
        db.String(60), unique=True, nullable=False, default=random_code
    )
    joined = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return "<Referral %r>" % str(self.email)
