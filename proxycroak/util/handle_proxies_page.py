import datetime
import random
import string

from flask import render_template

from proxycroak.util.decklist import parse_decklist
from proxycroak.blueprints.ui_api.handle_pic_mode import handle_pic_mode
from proxycroak.blueprints.ui_api.handle_text_mode import handle_text_mode
from proxycroak.logging import logger
from proxycroak.models import SharedDecklist
from proxycroak.database import db
from proxycroak.util.errors import make_invalid_dl_error


def handle_proxies_page(data, meta, opts=None):
    options = opts or {
        "lowres": False,
        "watermark": False,
        "legacy": False,
        "illustration": False,
        "nomin": False,
        "jp": False,
        "exclude_secrets": False
    }

    # TODO: Don't hardcode decks[0]
    dl = data["decks[0]"].replace("\r", "")

    # Remove empty lines
    lines = dl.split("\n")

    while "" in lines:
        lines.remove("")

    # TODO: The REALLY big ones will be handled by nginx I think
    if len(lines) > 100:
        logger.error(f"User provided decklist with length {len(lines)}", "decklist")
        return render_template("errors/error.html",
                               errors=[f"Decklist too long! (Max lines: 100, you provided {len(lines):,})"],
                               meta={"title": "Error", "description": "Something went wrong along the way"})

    # TODO: Don't hardcode decks[0]
    # TODO: Include errors
    parsed_list = parse_decklist(data["decks[0]"])
    if parsed_list is [] or parsed_list is None:
        return make_invalid_dl_error(data['decks[0]'])

    if data["mode"] == "pic":
        output, errors = handle_pic_mode(parsed_list, options)
    else:
        output, errors = handle_text_mode(parsed_list, options)

    # Make sure this ID isn't used
    counter = 0
    while True:
        random_id = ''.join(random.choices(string.ascii_uppercase +
                                           string.digits, k=8))

        shared_dl = SharedDecklist.query.get(random_id)

        if not shared_dl:
            break
        else:
            counter += 1

        # THIS SHOULD NEVER HAPPEN, but it doesn't hurt to be safe
        # In theory, this can go on FOREVER if we're unlucky enough,
        # so after 100 tries, just fail
        if counter == 100:
            return render_template("errors/error.html",
                                   errors=[
                                       f"The chance of this error occuring is astronomically small. You should go play the lottery."],
                                   meta={"title": "Error", "description": "Something went wrong along the way"})

            # Save the decklist
    sharedDecklist = SharedDecklist(
        id=random_id,
        # TODO: Don't hard code this
        decklist=data["decks[0]"],
        expires=datetime.datetime.now() + datetime.timedelta(days=6 * 30)
    )

    db.session.add(sharedDecklist)
    db.session.commit()

    return render_template("pages/proxies.html", meta=meta, rows=output, errors=errors, share_id=random_id,
                           options=options)
