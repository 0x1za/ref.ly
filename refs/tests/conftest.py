import pytest

from refs import User, app, db


@pytest.fixture(scope="module")
def new_user():
    user = User(email="annedoe@example.com", username="annedoe")
    return user


@pytest.fixture(scope="module")
def test_client():
    # Create a test client using the Flask application configured for testing
    with app.test_client() as testing_client:
        # Establish an application context
        with app.app_context():
            yield testing_client  # this is where the testing happens!


@pytest.fixture(scope="module")
def init_database(test_client):
    # Create the database and the database table
    db.create_all()

    # Insert user data
    user1 = User(email="johndoe@example.com", username="johndoe")
    user2 = User(email="annedoe@example.com", username="annedoe")
    db.session.add(user1)
    db.session.add(user2)

    # Commit the changes for the users
    db.session.commit()

    yield  # this is where the testing happens!

    db.drop_all()
