import csv
import json
from datetime import datetime
from io import StringIO

from app import db
from app.models import Thing, User
from app.thing import bp
from flask import Response, request, url_for
from flask_httpauth import HTTPTokenAuth
from flask_negotiate import consumes, produces
from jsonschema import FormatChecker, ValidationError, validate
from werkzeug.exceptions import BadRequest

auth = HTTPTokenAuth(scheme="Bearer")

# JSON schema for thing requests
with open("openapi.json") as json_file:
    openapi = json.load(json_file)
thing_schema = openapi["components"]["schemas"]["ThingRequest"]


@auth.verify_token
def authenticate(token):
    return User.verify_token(token)


@bp.route("", methods=["GET"])
@produces("application/json", "text/csv")
@auth.login_required
def list_things():
    """Get a list of Things."""
    sort_by = request.args.get("sort", type=str)
    name_query = request.args.get("name", type=str)
    colour_filter = request.args.get("colour", type=str)

    query = Thing.query

    if name_query:
        query = query.filter(Thing.name.ilike(f"%{name_query}%"))
    if colour_filter:
        query = query.filter(Thing.colour == colour_filter)
    if sort_by and sort_by != "name":
        query = query.order_by(getattr(Thing, sort_by).asc(), Thing.name.asc())
    else:
        query = query.order_by(Thing.name.asc())

    things = query.all()

    if things:
        if "application/json" in request.headers.getlist("accept"):
            results = [thing.list_item() for thing in things]

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
                w.writerow(("ID", "NAME", "COLOUR", "CREATED_AT", "UPDATED_AT"))
                yield data.getvalue()
                data.seek(0)
                data.truncate(0)

                # write each item
                for thing in things:
                    w.writerow(
                        (
                            thing.id,
                            thing.name,
                            thing.colour,
                            thing.created_at.isoformat(),
                            thing.updated_at.isoformat() if thing.updated_at else None,
                        )
                    )
                    yield data.getvalue()
                    data.seek(0)
                    data.truncate(0)

            response = Response(generate(), mimetype="text/csv", status=200)
            response.headers.set("Content-Disposition", "attachment", filename="things.csv")
            return response
    else:
        return Response(mimetype="application/json", status=204)


@bp.route("", methods=["POST"])
@consumes("application/json")
@produces("application/json")
@auth.login_required
def create_thing():
    """Create a new Thing."""

    # Validate request against schema
    try:
        validate(request.json, thing_schema, format_checker=FormatChecker())
    except ValidationError as e:
        raise BadRequest(e.message)

    thing = Thing(
        name=request.json["name"],
        colour=request.json["colour"],
        user_id=auth.current_user().id,
    )

    db.session.add(thing)
    db.session.commit()

    response = Response(repr(thing), mimetype="application/json", status=201)
    response.headers["Location"] = url_for("thing.get_thing", thing_id=thing.id)

    return response


@bp.route("/<uuid:thing_id>", methods=["GET"])
@produces("application/json")
@auth.login_required
def get_thing(thing_id):
    """Get a Thing with a specific ID."""
    thing = Thing.query.get_or_404(str(thing_id))

    return Response(repr(thing), mimetype="application/json", status=200)


@bp.route("/<uuid:thing_id>", methods=["PUT"])
@consumes("application/json")
@produces("application/json")
@auth.login_required
def update_thing(thing_id):
    """Update a Thing with a specific ID."""

    # Validate request against schema
    try:
        validate(request.json, thing_schema, format_checker=FormatChecker())
    except ValidationError as e:
        raise BadRequest(e.message)

    thing = Thing.query.get_or_404(str(thing_id))

    thing.name = request.json["name"].title().strip()
    thing.colour = request.json["colour"].strip()
    thing.updated_at = datetime.utcnow()

    db.session.add(thing)
    db.session.commit()

    return Response(repr(thing), mimetype="application/json", status=200)


@bp.route("/<uuid:thing_id>", methods=["DELETE"])
@produces("application/json")
@auth.login_required
def delete_thing(thing_id):
    """Delete a Thing with a specific ID."""
    thing = Thing.query.get_or_404(str(thing_id))

    db.session.delete(thing)
    db.session.commit()

    return Response(mimetype="application/json", status=204)
