"""
The referrals Blueprint handles the referrals management for this application.
"""
from flask import Blueprint

# flake8: noqa: F401
from refs.referrals import routes

referrals_blueprint = Blueprint("referrals", __name__, template_folder="templates")
