import re
from typing import Tuple

from flask import request
from sqlalchemy import exc

from refs import app, db
from refs.models import Referral, User


# Utils
def validate_email(email):
    regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
    if re.fullmatch(regex, email):
        return True
    else:
        return False


@app.route("/", methods=["GET"])
def index():
    return "<p>Hello World</p>"


@app.route("/v1/create/user", methods=["POST"])
def create_user():
    errors = []
    data = {}
    status = 0
    message = ""

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
                user = User(username=username, email=email)
                # Check if reference code exists.
                db.session.add(user)
                if referral_code is not None:
                    referral = Referral.query.filter_by(
                        referral_code=str(referral_code), email=email
                    )
                    if referral.count() == 1:
                        # Assign a $10 to invitee user account.
                        referral = referral.first()
                        user.balance = 10
                        referral.joined = 1
                        referer_user = User.query.filter_by(
                            id=referral.referer_id
                        ).first()
                        referer_count = Referral.query.filter_by(
                            referer_id=referral.referer_id, joined=1
                        ).count()
                        # Award referer user a $10.
                        if int(referer_count) % 5 == 0:
                            referer_user.balance = referer_user.balance + 10
                db.session.commit()
                data = {
                    "username": str(user.username),
                    "current_balance": str(user.balance),
                    "email": str(user.email),
                }
                status = 1
                message = "User successfully created."
            except exc.IntegrityError as e:
                errors.append(str(e.orig))
                message = "Registration failed."
        except KeyError as e:
            message = "Error: Required key not provided"
            errors.append("A required key " + str(e) + " was not provided.")

    return {"message": message, "data": data, "errors": errors, "status": status}


@app.route("/v1/create/referral", methods=["POST"])
def create_referral():
    errors = []
    data = {}
    status = 0
    message = ""

    # Check if data is set or provided in request.
    if request.data:
        response = request.get_json()
        try:
            invitee_email, referer_email = (
                response["invitee_email"],
                response["referer_email"],
            )
            valid_emails: Tuple[bool, bool] = (
                validate_email(invitee_email),
                validate_email(referer_email),
            )
            if invitee_email != referer_email:
                if all(valid_emails):
                    # Get referer id.
                    refer = User.query.filter_by(email=referer_email).first()
                    invitee = User.query.filter_by(email=invitee_email).count()

                    if refer is not None and invitee != 1:
                        refer_exists = Referral.query.filter_by(
                            referer_id=refer.id, email=invitee_email
                        ).count()
                        if refer_exists == 0:
                            # Create a new referral record.
                            reference = Referral(email=invitee_email, referer=refer)
                            message = "Referral successfully created"
                            data = {
                                "id": reference.id,
                                "referral_code": reference.referral_code,
                                "referer": reference.referer.email,
                                "invitee": reference.email,
                            }
                            status = 1
                            db.session.add(reference)
                            db.session.commit()
                        else:
                            errors.append(
                                "You have already invited user with email `"
                                + str(invitee_email)
                                + "`"
                            )
                            message = "DuplicateRecord"
                    else:
                        # Log error if the user is not found or invitee
                        # user already exists.
                        if refer is None:
                            errors.append(
                                "User with email "
                                + str(referer_email)
                                + " does not exist."
                            )
                        elif invitee == 1:
                            errors.append(
                                "User with email "
                                + str(referer_email)
                                + " already exists."
                            )
                else:
                    if not valid_emails[0]:
                        errors.append(
                            "invitee_email: "
                            + str(invitee_email)
                            + "` is not a valid email."
                        )
                    elif not valid_emails[1]:
                        errors.append(
                            "referer_email: "
                            + str(referer_email)
                            + " is not a valid email."
                        )
                    message = "ValidationError"
            else:
                errors += ["You cannot send a referral to yourself."]
        except KeyError as e:
            errors.append("A required key " + str(e) + " was not provided.")

    return {"message": message, "data": data, "errors": errors, "status": status}


if __name__ == "__main__":
    app.run(debug=True)
