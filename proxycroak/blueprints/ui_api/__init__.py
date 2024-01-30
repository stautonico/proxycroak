from flask import Blueprint, request, redirect, url_for, abort, jsonify
from sentry_sdk import capture_exception

from proxycroak.blueprints.ui_api.handle_pic_mode import handle_pic_mode
from proxycroak.blueprints.ui_api.handle_text_mode import handle_text_mode
from proxycroak.models import Card, Set
from proxycroak.util.handle_proxies_page import handle_proxies_page
from proxycroak.util.serialize import serialize_card, recursive_json_loads, seralize_set
from proxycroak.logging import logger
from proxycroak import const

blueprint = Blueprint("ui_api", __name__, url_prefix="/ui/api")


@blueprint.route("/proxies", methods=["GET", "POST"])
def proxies():
    if request.method == "GET":
        return redirect(url_for("ui.index"))
    else:
        META = {
            "title": "Proxies",
            "description": "A simple tool for deck testing: choose the format (pics or text), and print up to 3 decks made of combined Pokémon proxy cards.",
            "tags": ["proxies"]
        }

        # Load the form data
        form_data = request.form

        data = {}
        options = {
            "lowres": False,
            "watermark": False,
            "legacy": False,
            "illustration": False,
            "nomin": False,
            "jp": False,
            "exclude_secrets": False
        }

        if "mode" in form_data:
            data["mode"] = form_data["mode"]
        else:
            # TODO: Provide a proper error page
            logger.error("User did not provide a mode", "proxies")
            abort(400)

        if "activeDeck" in form_data:
            data["activeDeck"] = form_data["activeDeck"]
        else:
            logger.error("User did not provide an active deck", "proxies")
            # TODO: Provide a proper error page
            abort(400)

        has_active_deck = False

        # if "activeDeck[0]" in form_data:
        #     data["activeDeck[0]"] = form_data["activeDeck[0]"]
        #     has_active_deck = True
        #
        # if "activeDeck[1]" in form_data:
        #     data["activeDeck[1]"] = form_data["activeDeck[1]"]
        #     has_active_deck = True
        #
        # if "activeDeck[2]" in form_data:
        #     data["activeDeck[2]"] = form_data["activeDeck[2]"]
        #     has_active_deck = True
        #
        # if not has_active_deck:
        #     logger.error("User did not provide an any decks", "proxies")
        #     # TODO: Provide a proper error page
        #     abort(400)

        if "decks[0]" in form_data:
            data["decks[0]"] = form_data["decks[0]"]

        if "decks[1]" in form_data:
            data["decks[1]"] = form_data["decks[1]"]

        if "decks[2]" in form_data:
            data["decks[2]"] = form_data["decks[2]"]

        # TODO: Find a better way to do this

        for opt in ["lowres", "watermark", "legacy", "illustration", "nomin", "jp", "exclude_secrets"]:
            if f"options[{opt}]" in form_data:
                options[opt] = form_data[f"options[{opt}]"] == "1"

        return handle_proxies_page(data, META, options)


@blueprint.route("/search", methods=["GET"])
def search():
    try:
        entries = Card.query.filter(Card.name.ilike(f"%{request.args.to_dict()['name']}%")).all()
        return jsonify([recursive_json_loads(serialize_card(e)) for e in entries])
    except Exception as e:
        logger.warn(f"Something went wrong when trying to search for cards: '{e}'", "ui_api::search")
        capture_exception(e)
        return jsonify([])


@blueprint.route("/set/<string:set_id>", methods=["GET"])
def set_get(set_id):
    try:
        s = Set.query.get(set_id)

        # If the set doesn't have a ptcgo code, grab it from the const table
        if not s.ptcgoCode:
            s.ptcgoCode = const.lookup_set_code_by_id(s.id)

        return jsonify(seralize_set(s))
    except Exception as e:
        print(e)
        return jsonify({"error": "set not found"}), 404
