import json

from flask import Response
from flask_httpauth import HTTPBasicAuth
from flask_negotiate import produces

from app.auth import bp
from app.models import User

auth = HTTPBasicAuth()


@bp.route("token", methods=["GET"])
@produces("application/json")
@auth.login_required
def get_token():
    return Response(
        json.dumps({"token": auth.current_user().generate_token()}, separators=(",", ":")),
        mimetype="application/json",
        status=200,
    )


@auth.verify_password
def authenticate(email_address, password):
    user = User.query.filter_by(email_address=email_address).first()
    if user and user.check_password(password):
        return user
