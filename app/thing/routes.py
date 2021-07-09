import json
from datetime import datetime

from app import db
from app.models import Thing
from app.thing import bp
from flask import Response, request, url_for
from flask_negotiate import consumes, produces
from jsonschema import FormatChecker, ValidationError, validate
from werkzeug.exceptions import BadRequest

# JSON schema for thing requests
with open("openapi.json") as json_file:
    openapi = json.load(json_file)
thing_schema = openapi["components"]["schemas"]["ThingRequest"]


@bp.route("", methods=["GET"])
@produces("application/json")
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
    if sort_by != "name":
        query = query.order_by(getattr(Thing, sort_by).asc(), Thing.name.asc())
    else:
        query = query.order_by(Thing.name.asc())
    
    things = query.all()

    if things:
        results = [thing.list_item() for thing in things]

        return Response(
            json.dumps(results, separators=(",", ":")),
            mimetype="application/json",
            status=200,
        )
    else:
        return Response(mimetype="application/json", status=204)


@bp.route("", methods=["POST"])
@consumes("application/json")
@produces("application/json")
def create_thing():
    """Create a new Thing."""

    # Validate request against schema
    try:
        validate(request.json, thing_schema, format_checker=FormatChecker())
    except ValidationError as e:
        raise BadRequest(e.message)

    thing = Thing(name=request.json["name"], colour=request.json["colour"])

    db.session.add(thing)
    db.session.commit()

    response = Response(repr(thing), mimetype="application/json", status=201)
    response.headers["Location"] = url_for("thing.get_thing", thing_id=thing.id)

    return response


@bp.route("/<uuid:thing_id>", methods=["GET"])
@produces("application/json")
def get_thing(thing_id):
    """Get a Thing with a specific ID."""
    thing = Thing.query.get_or_404(str(thing_id))

    return Response(repr(thing), mimetype="application/json", status=200)


@bp.route("/<uuid:thing_id>", methods=["PUT"])
@consumes("application/json")
@produces("application/json")
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
def delete_thing(thing_id):
    """Delete a Thing with a specific ID."""
    thing = Thing.query.get_or_404(str(thing_id))

    db.session.delete(thing)
    db.session.commit()

    return Response(mimetype="application/json", status=204)
