from flask import request
from sqlalchemy import exc

from refs import db
from refs.models import Referral, User

# fmt: off
from refs.users import users_blueprint
# fmt: on
from refs.utils import serialize


@users_blueprint.route("/", methods=["GET"])
def index():
    return "<p>Welcome to ref.ly</p>"


@users_blueprint.route("/v1/users", methods=["GET"])
def get_users():
    user_id = request.args.get("id", "")
    query = User.query.all()
    if user_id:
        query = User.query.filter_by(id=user_id)
    serialized_users = [serialize(user) for user in query]

    status = 1 if len(serialized_users) > 0 else 0
    code = 200 if len(serialized_users) > 0 else 404
    errors = (
        []
        if len(serialized_users) > 0
        else ["User with id {} was not found.".format(user_id)]
    )

    return {
        "message": "Query results: " + str(len(serialized_users)) + " records",
        "data": serialized_users,
        "errors": errors,
        "status": status,
        "code": str(code),
    }


@users_blueprint.route("/v1/create/user", methods=["POST"])
def create_user():
    errors = []
    data = {}
    status = 0
    message = ""
    code = 400  # Default is bad request

    # Check if data is set or provided in request.
    if request.data:
        response = request.get_json()
        try:
            email, username = (
                response["email"],
                response["username"],
            )
            referral_code = response.get("referral_code", None)

            try:
                user = User(username=username, email=email, balance=0)
                # Check if reference code exists.
                if referral_code is not None:
                    referral = Referral.query.filter_by(
                        referral_code=str(referral_code), email=email, joined=False
                    )
                    db.session.add(user)
                    if referral.count() == 1:
                        referral_record = referral.first()
                        referer_user = User.query.filter_by(
                            id=referral_record.referer_id
                        ).first()
                        # Assign a $10 to invitee user account.
                        user.balance = 10
                        referral_record.joined = True
                        db.session.add(referral_record)
                        # Award referer user a $10.
                        if int(referral.count()) % 5 == 0:
                            referer_user.balance = referer_user.balance + 10
                else:
                    db.session.add(user)
                db.session.commit()
                data = {
                    "username": str(user.username),
                    "current_balance": str(user.balance),
                    "email": str(user.email),
                }
                code = 201
                status = 1
                message = "User successfully created."
            except exc.IntegrityError as e:
                errors.append(str(e.orig))
                db.session.rollback()
                message = "Registration failed."
        except KeyError as e:
            message = "Error: Required key not provided"
            errors.append("A required key " + str(e) + " was not provided.")

    return {
        "message": message,
        "data": data,
        "errors": errors,
        "status": status,
        "code": str(code),
    }
