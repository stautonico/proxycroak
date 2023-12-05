from flask import Blueprint, request, render_template, redirect, url_for

from proxycroak.util.decklist import parse_decklist
from proxycroak.blueprints.ui_api.handle_pic_mode import handle_pic_mode

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
            "litemin": False,
            "jp": False,
            "exclude_secrets": False
        }

        if "mode" in form_data:
            data["mode"] = form_data["mode"]
        else:
            # TODO: Fail with error page
            pass

        if "activeDeck" in form_data:
            data["activeDeck"] = form_data["activeDeck"]
        else:
            # TODO: Fail with error page
            pass

        has_active_deck = False

        if "activeDeck[0]" in form_data:
            data["activeDeck[0]"] = form_data["activeDeck[0]"]
            has_active_deck = True

        if "activeDeck[1]" in form_data:
            data["activeDeck[1]"] = form_data["activeDeck[1]"]
            has_active_deck = True

        if "activeDeck[2]" in form_data:
            data["activeDeck[2]"] = form_data["activeDeck[2]"]
            has_active_deck = True

        if not has_active_deck:
            # TODO: Fail with error page
            pass

        if "decks[0]" in form_data:
            data["decks[0]"] = form_data["decks[0]"]

        if "decks[1]" in form_data:
            data["decks[1]"] = form_data["decks[1]"]

        if "decks[2]" in form_data:
            data["decks[2]"] = form_data["decks[2]"]

        # TODO: Find a better way to do this

        for opt in ["lowres", "watermark", "legacy", "illustration", "litemin", "jp", "exclude_secrets"]:
            if f"options[{opt}]" in form_data:
                options[opt] = form_data[f"options[{opt}]"] == "1"

        # TODO: Don't hardcode decks[0]
        # TODO: Include errors
        output, errors = handle_pic_mode(parse_decklist(data["decks[0]"]), options)

        return render_template("pages/proxies.html", meta=META, rows=output, errors=errors)
