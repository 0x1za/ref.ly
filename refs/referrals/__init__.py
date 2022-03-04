"""
The referrals Blueprint handles the referrals management for this application.
"""
from flask import Blueprint

referrals_blueprint = Blueprint("referrals", __name__, template_folder="templates")

# flake8: noqa: F401
# fmt: off
from refs.referrals import routes
# fmt: on
