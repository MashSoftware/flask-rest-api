from app.thing import bp
from flask_negotiate import consumes, produces
from werkzeug.exceptions import NotImplemented


@bp.route("", methods=["GET"])
@produces("application/json")
def get_things():
    """Get a list of Things."""
    raise NotImplemented  # noqa: F901


@bp.route("", methods=["POST"])
@consumes("application/json")
@produces("application/json")
def create_thing():
    """Create a new Thing."""
    raise NotImplemented  # noqa: F901


@bp.route("/<uuid:thing_id>", methods=["GET"])
@produces("application/json")
def get_thing(thing_id):
    """Get a Thing for a given ID."""
    raise NotImplemented  # noqa: F901


@bp.route("/<uuid:thing_id>", methods=["PUT"])
@consumes("application/json")
@produces("application/json")
def update_thing(thing_id):
    """Update a Thing for a given ID."""
    raise NotImplemented  # noqa: F901


@bp.route("/<uuid:thing_id>", methods=["DELETE"])
@produces("application/json")
def delete_thing(thing_id):
    """Delete a Thing for a given ID."""
    raise NotImplemented  # noqa: F901
