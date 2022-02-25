"""
Unit tests for models in refs.
"""
from refs import User


def test_new_user():
    """
    Create a new user.
    """
    user = User(email="johndoe@example.com", username="johndoe")
    assert user.email == "johndoe@example.com"
    assert user.username == "johndoe"


def test_new_user_with_fixture(new_user):
    """
    Creating user from fixture.
    """
    assert new_user.email == "annedoe@example.com"
    assert new_user.username == "annedoe"
