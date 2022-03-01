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


def test_new_referral(new_user, init_database):
    """
    Create new referral.
    """
    referral = Referral(
        email="x123@example.com", referer_id=User.query.filter_by(id=1).first().id
    )
    assert referral.email == "x123@example.com"
    assert referral.referer_id == 1
    assert referral.__repr__() == "<Referral 'x123@example.com'>"
