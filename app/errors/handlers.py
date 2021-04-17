import json

from app.errors import bp
from flask import Response
from werkzeug.exceptions import HTTPException, InternalServerError


@bp.app_errorhandler(HTTPException)
def http_error(error):
    return Response(
        response=json.dumps(
            {"code": error.code, "name": error.name, "description": error.description},
            separators=(",", ":"),
        ),
        mimetype="application/json",
        status=error.code,
    )


@bp.app_errorhandler(Exception)
def unhandled_exception(error):
    raise InternalServerError
