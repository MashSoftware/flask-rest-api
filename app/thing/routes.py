import json
from datetime import datetime

from app import db
from app.models import Thing
from app.thing import bp
from flask import Response, url_for
from flask_negotiate import consumes, produces


@bp.route("", methods=["GET"])
@produces("application/json")
def get_things():
    """Get a list of Things."""
    things = Thing.query.all()

    if things:
        results = []
        for thing in things:
            results.append(thing.as_dict())

        return Response(
            json.dumps(results, sort_keys=True, separators=(",", ":")),
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
    thing = Thing()

    db.session.add(thing)
    db.session.commit()

    response = Response(repr(thing), mimetype="application/json", status=201)
    response.headers["Location"] = url_for("thing.get_thing", thing_id=thing.id)

    return response


@bp.route("/<uuid:thing_id>", methods=["GET"])
@produces("application/json")
def get_thing(thing_id):
    """Get a Thing for a given ID."""
    thing = Thing.query.get_or_404(str(thing_id))

    return Response(repr(thing), mimetype="application/json", status=200)


@bp.route("/<uuid:thing_id>", methods=["PUT"])
@consumes("application/json")
@produces("application/json")
def update_thing(thing_id):
    """Update a Thing for a given ID."""
    thing = Thing.query.get_or_404(str(thing_id))

    thing.updated_at = datetime.utcnow()

    db.session.add(thing)
    db.session.commit()

    return Response(repr(thing), mimetype="application/json", status=200)


@bp.route("/<uuid:thing_id>", methods=["DELETE"])
@produces("application/json")
def delete_thing(thing_id):
    """Delete a Thing for a given ID."""
    thing = Thing.query.get_or_404(str(thing_id))

    db.session.delete(thing)
    db.session.commit()

    return Response(mimetype="application/json", status=204)
