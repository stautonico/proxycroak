from flask import Blueprint, jsonify, request

from sqlalchemy import text

from proxycroak.database import db
from proxycroak.util.handle_proxies_api import handle_proxies_api

blueprint = Blueprint("public_api", __name__, url_prefix="/api/v1")


@blueprint.route("/ping")
def ping():
    return "pong"


@blueprint.route("/health")
def health():
    """
    In this route, we confirm all of our external services and such. For now, its only the database
    TODO: Maybe put a "under maintenance" status here?
    """
    status = "ok"
    try:
        result = db.session.execute(text("SELECT 1"))
        if result.fetchone()[0] != 1:
            status = "critically degraded"
    except Exception:
        status = "critically degraded"

    return jsonify({"status": status})


@blueprint.route("/proxy", methods=["POST"])
def proxy():
    # Step 1: Validate the options the user passed
    print(request.json)

    return handle_proxies_api(request.json, request.json)
