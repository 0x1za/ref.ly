"""
The users Blueprint handles the user management for this application.
"""
from flask import Blueprint

users_blueprint = Blueprint("users", __name__, template_folder="templates")

# flake8: noqa: F401
# fmt: off
from refs.users import routes
# fmt: on
