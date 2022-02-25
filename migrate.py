from app import Referral, User, db

db.session.query(User).delete()
db.session.query(Referral).delete()
db.session.commit()
db.create_all()

admin = User(username="admin", email="admin@example.com")
db.session.add(admin)
db.session.commit()
referral = Referral(email="mwizasimbeye@gmail.com", referer=admin)
db.session.add(referral)

db.session.commit()
