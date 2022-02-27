"""
Unit tests for models in refs.
"""
from refs.models import Referral, User


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
    assert new_user.__repr__() == "<User 'annedoe'>"


def test_new_referral(new_user):
    """
    Create new referral.
    """
    referral = Referral(email="x123@example.com", referer=new_user)
    assert referral.email == "x123@example.com"
    assert referral.__repr__() == "<Referral 'x123@example.com/annedoe@example.com'>"
