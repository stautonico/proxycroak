import base64

from flask import Blueprint, render_template, send_from_directory, abort, request
from sqlalchemy import asc

from proxycroak.const import lookup_set_code_by_id
from proxycroak.util.decklist import parse_decklist
from proxycroak.blueprints.ui_api.handle_pic_mode import handle_pic_mode
from proxycroak.models import SharedDecklist, Set, UnreleasedSet
from proxycroak.util.handle_proxies_page import handle_proxies_page
from proxycroak.util.errors import make_invalid_dl_error
from proxycroak.logging import logger

from sentry_sdk import capture_exception

blueprint = Blueprint("ui", __name__, url_prefix="/")


@blueprint.route("/")
def index():
    meta = {"title": "",
            "description": "Proxycroak is a simple tool to print Pokémon proxy cards for playtesting, straight from a decklist.",
            "tags": ["home"]}
    return render_template("pages/index.html", meta=meta)


@blueprint.route("/features")
def features():
    meta = {"title": "Features",
            "description": "Find out how to print Pokémon proxy cards for playtesting.",
            "tags": ["features"]}

    return render_template("pages/features.html", meta=meta)


@blueprint.route("/changelog")
def changelog():
    meta = {
        "title": "Changelog",
        "description": "Latest project changes and news.",
        "tags": ["changelog"]
    }

    return render_template("pages/changelog.html", meta=meta)


@blueprint.route("/help")
def help():
    meta = {
        "title": "Help",
        "description": "FAQ and known bugs. Read before starting to print Pokémon proxy cards!",
        "tags": ["help"]
    }

    return render_template("pages/help.html", meta=meta)


@blueprint.route("/share/<sid>")
def share(sid):
    META = {
        "title": "Proxies",
        "description": "A simple tool for deck testing: choose the format (pics or text), and print up to 3 decks made of combined Pokémon proxy cards.",
        "tags": ["proxies"]
    }

    # See if a shared decklist with the given sid exists
    dl = SharedDecklist.query.get(sid)

    if not dl:
        logger.warn(f"User tried to access invalid share: id {sid}", "share")
        abort(404)

    # TODO: Save options?
    options = {
        "lowres": False,
        "watermark": False,
        "legacy": False,
        "illustration": False,
        "nomin": False,
        "jp": False,
        "exclude_secrets": False
    }

    output, errors = handle_pic_mode(parse_decklist(dl.decklist), options)

    return render_template("pages/proxies.html", meta=META, rows=output, errors=errors, share_id=dl.id)


@blueprint.route("/set_codes")
def set_codes():
    META = {
        "title": "Set Codes",
        "description": "A table showing all of the PTCGO/PTCGL set codes to use in your deckists",
        "tags": ["setcodes"]
    }

    sets = Set.query.order_by(asc(Set.releaseDate)).all()
    unreleased_sets_dirty = UnreleasedSet.query.order_by(asc(UnreleasedSet.updatedAt)).all()
    unreleased_sets_clean = []

    for s in unreleased_sets_dirty:
        s.name = s.name + " (Unreleased)"
        unreleased_sets_clean.append(s)



    # set (lol) the set codes for SVI+
    # What this crazy conditional does:
    # If we don't have a set id (SVI+), use the one from the const file
    # OR
    # If we do have one, but we're dealing with BRS, ASR, anything with a TG/GG
    # AND
    # if the word "trainer/galarian gallery" is in the name (to only do the TG/GG not the normal set)
    # OR
    # The set name is "Shiny Vault"
    # then we grab from the const file
    # TODO: Optimize?
    for s in sets:
        if not s.ptcgoCode \
                or (s.ptcgoCode in ["BRS", "ASR", "LOR", "SIT", "CRZ"] \
                    and (
                            "trainer gallery" in s.name.lower() \
                            or "galarian gallery" in s.name.lower())) \
                or s.name == "Shiny Vault":
            s.ptcgoCode = lookup_set_code_by_id(s.id) or s.id.upper()

    return render_template("pages/set_codes.html", meta=META, sets=[*sets, *unreleased_sets_clean])


@blueprint.route("/issues/cards")
def card_issues():
    META = {
        "title": "Card Issues",
        "description": "A table of all of the cards that are missing or contain some kind of issue",
        "tags": ["issues", "cards"]
    }

    return render_template("pages/card_issues.html", meta=META)


@blueprint.route("/import")
def import_route():
    META = {
        "title": "Proxies",
        "description": "A simple tool for deck testing: choose the format (pics or text), and print up to 3 decks made of combined Pokémon proxy cards.",
        "tags": ["proxies"]
    }

    options = {
        "lowres": False,
        "watermark": False,
        "legacy": False,
        "illustration": False,
        "nomin": False,
        "jp": False,
        "exclude_secrets": False
    }

    # TODO: This is unsafe due to users being able to get the real IP of the backend
    #       as well as allowing the user to make an http request to any server of their choosing
    # if "url" in request.args:
    #     try:
    #         r = requests.get(request.args["url"])
    #         if "text/plain" in r.headers.get("Content-Type", ""):
    #             print(r.text)
    #         else:
    #             # TODO: Return an error
    #             pass
    #     except Exception as e:
    #         # TODO: Log here
    #         capture_exception(e)
    #         # TODO: Return error page
    if "base64list" in request.args:
        # print(request.args["list"])
        try:
            l = base64.b64decode(request.args["base64list"])
            try:
                decoded_list = l.decode("utf-8")
            except Exception as e:
                # capture_exception(e)
                try:
                    decoded_list = l.decode("latin-1")
                except Exception as e2:
                    logger.error(f"The provided decklist was neither utf-8 or latin-1. Unable to import. {e2}",
                                 "import")
                    capture_exception(e2)
                    return make_invalid_dl_error(request.args["base64list"])

            return handle_proxies_page({"decks[0]": decoded_list, "mode": "pic"}, META)
        except Exception as e:
            logger.error(f"Something is wrong with the provided decklist. Base64 decoding failed: {e}", "import")
            capture_exception(e)
            return make_invalid_dl_error(request.args["base64list"])

    abort(400)


@blueprint.route("/static/<path:path>")
def static_asset(path):
    return send_from_directory("static", path)


# Meta stuff
@blueprint.route("/robots.txt")
def robotstxt():
    return send_from_directory("static/meta", "robots.txt")


@blueprint.route("/.well-known/<path:path>")
def well_known(path):
    return send_from_directory("static/meta/.well-known", path)
