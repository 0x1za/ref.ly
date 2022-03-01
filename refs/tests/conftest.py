import pytest

# fmt: off
from refs.app import app
from refs.models import Referral, User, db

# fmt: on


@pytest.fixture(scope="module")
def new_user():
    user = User(email="annedoe@example.com", username="annedoe")
    return user


@pytest.fixture(scope="module")
def test_client():
    client = app.test_client()
    return client


@pytest.fixture(scope="module")
def init_database():
    # Create the database and the database table
    db.create_all()

    # Insert user data
    user = User(email="johndoe@example.com", username="johndoe")
    user2 = User(email="janedoe@example.com", username="janedoe")

    db.session.add(user)
    db.session.add(user2)
    # Commit the changes for the users
    db.session.commit()

    referral = Referral(
        email="invited_user@example.com", referer_id=user.id, referral_code="0WXOGQI"
    )
    db.session.add(referral)
    db.session.commit()

    yield  # this is where the testing happens!

    db.drop_all()
