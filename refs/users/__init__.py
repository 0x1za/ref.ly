"""
The users Blueprint handles the user management for this application.
"""
from flask import Blueprint

# flake8: noqa: F401
from refs.users import routes

users_blueprint = Blueprint("users", __name__, template_folder="templates")
