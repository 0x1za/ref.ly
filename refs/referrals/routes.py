from typing import Tuple

from flask import request

from refs import db
from refs.models import Referral, User
from refs.referrals import referrals_blueprint
from refs.utils import validate_email


@referrals_blueprint.route("/v1/create/referral", methods=["POST"])
def create_referral():
    errors = []
    data = {}
    status = 0
    message = ""
    code = 400  # Default is bad request

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
                            reference = Referral(
                                email=invitee_email, referer_id=refer.id
                            )
                            db.session.add(reference)
                            db.session.commit()

                            message = "Referral successfully created"
                            data = {
                                "id": reference.id,
                                "referral_code": reference.referral_code,
                                "referer": referer_email,
                                "invitee": invitee_email,
                            }
                            code = 201
                            status = 1
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
                            + " is not a valid email."
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

    return {
        "message": message,
        "data": data,
        "errors": errors,
        "status": status,
        "code": str(code),
    }
