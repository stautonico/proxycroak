from flask import Blueprint, render_template, send_from_directory

from proxycroak.util.cards_db import update_sets

blueprint = Blueprint("ui", __name__, url_prefix="/")


@blueprint.route("/")
def index():
    meta = {"title": "",
            "description": "A simple tool for deck testing: choose the format (pics or text), and print up to 3 decks made of combined Pokémon proxy cards.",
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


@blueprint.route("/debug")
def debug():
    update_sets()
    return "<h1>Done!</h1>"



@blueprint.route("/static/<path:path>")
def static_asset(path):
    return send_from_directory("static", path)
