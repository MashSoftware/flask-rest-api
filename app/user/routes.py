import csv
import json
from datetime import datetime
from io import StringIO

from app import db
from app.models import User
from app.user import bp
from flask import Response, request, url_for
from flask_negotiate import consumes, produces
from jsonschema import FormatChecker, ValidationError, validate
from werkzeug.exceptions import BadRequest

# JSON schema for user requests
with open("openapi.json") as json_file:
    openapi = json.load(json_file)
user_schema = openapi["components"]["schemas"]["UserRequest"]


@bp.route("", methods=["GET"])
@produces("application/json", "text/csv")
def list_users():
    """Get a list of Users."""
    sort_by = request.args.get("sort", type=str)
    email_query = request.args.get("email_address", type=str)

    query = User.query

    if email_query:
        query = query.filter(User.email_address.ilike(f"%{email_query}%"))
    if sort_by and sort_by != "email_address":
        query = query.order_by(getattr(User, sort_by).asc(), User.email_address.asc())
    else:
        query = query.order_by(User.email_address.asc())

    users = query.all()

    if users:
        if "application/json" in request.headers.getlist("accept"):
            results = [user.list_item() for user in users]

            return Response(
                json.dumps(results, separators=(",", ":")),
                mimetype="application/json",
                status=200,
            )
        elif "text/csv" in request.headers.getlist("accept"):

            def generate():
                data = StringIO()
                w = csv.writer(data)

                # write header
                w.writerow(("ID", "EMAIL_ADDRESS", "CREATED_AT", "UPDATED_AT"))
                yield data.getvalue()
                data.seek(0)
                data.truncate(0)

                # write each item
                for user in users:
                    w.writerow(
                        (
                            user.id,
                            user.email_address,
                            user.created_at.isoformat(),
                            user.updated_at.isoformat() if user.updated_at else None,
                        )
                    )
                    yield data.getvalue()
                    data.seek(0)
                    data.truncate(0)

            response = Response(generate(), mimetype="text/csv", status=200)
            response.headers.set("Content-Disposition", "attachment", filename="users.csv")
            return response
    else:
        return Response(mimetype="application/json", status=204)


@bp.route("", methods=["POST"])
@consumes("application/json")
@produces("application/json")
def create_user():
    """Create a new User."""

    # Validate request against schema
    try:
        validate(request.json, user_schema, format_checker=FormatChecker())
    except ValidationError as e:
        raise BadRequest(e.message)

    if User.query.filter_by(email_address=request.json["email_address"]).first() is not None:
        raise BadRequest()

    user = User(email_address=request.json["email_address"], password=request.json["password"])

    db.session.add(user)
    db.session.commit()

    response = Response(repr(user), mimetype="application/json", status=201)
    response.headers["Location"] = url_for("user.get_user", user_id=user.id)

    return response


@bp.route("/<uuid:user_id>", methods=["GET"])
@produces("application/json")
def get_user(user_id):
    """Get a User with a specific ID."""
    user = User.query.get_or_404(str(user_id))

    return Response(repr(user), mimetype="application/json", status=200)


@bp.route("/<uuid:user_id>", methods=["PUT"])
@consumes("application/json")
@produces("application/json")
def update_user(user_id):
    """Update a User with a specific ID."""

    # Validate request against schema
    try:
        validate(request.json, user_schema, format_checker=FormatChecker())
    except ValidationError as e:
        raise BadRequest(e.message)

    user = User.query.get_or_404(str(user_id))

    user.email_address = request.json["email_address"].lower().strip()
    user.updated_at = datetime.utcnow()

    db.session.add(user)
    db.session.commit()

    return Response(repr(user), mimetype="application/json", status=200)


@bp.route("/<uuid:user_id>", methods=["DELETE"])
@produces("application/json")
def delete_user(user_id):
    """Delete a User with a specific ID."""
    user = User.query.get_or_404(str(user_id))

    db.session.delete(user)
    db.session.commit()

    return Response(mimetype="application/json", status=204)
