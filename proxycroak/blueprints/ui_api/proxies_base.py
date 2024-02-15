from sqlalchemy import or_

from proxycroak.models import Card, Set, UnreleasedCard, UnreleasedSet
from proxycroak.const import SET_IDS


def find_set(card, hide_unreleased=False):
    if card["set_id"] in SET_IDS:
        set_obj = Set.query.filter_by(id=SET_IDS[card["set_id"]]).first()
    else:
        set_obj = Set.query.filter(
            or_(Set.ptcgoCode == card["set_id"], Set.alternatePtcgoCode == card["set_id"])).first()

    if not set_obj and not hide_unreleased:
        set_obj = UnreleasedSet.query.filter(
            or_(UnreleasedSet.ptcgoCode == card["set_id"], UnreleasedSet.alternatePtcgoCode == card["set_id"])).first()

    return set_obj


def fuzzy_find_card_or_error(card, hide_unreleased=False):
    error = None

    card_obj = Card.query.filter_by(name=card["card_name"], number=card["card_num"]).first()
    # If we can't find any card, we can check for unreleased cards
    if not card_obj:
        if not hide_unreleased:
            card_obj = UnreleasedCard.query.filter_by(name=card["card_name"], number=card["card_num"]).first()

        if not card_obj:
            # TODO: Hard-code error messages somewhere else
            error = {
                "card": f"{card['amnt']}x {card['card_name']} (#{card['card_num']})",
                "message": "No results found (card misspelled or unavailable)"
            }
    else:
        error = {
            "card": f"{card['amnt']}x {card['card_name']} (#{card['card_num']})",
            "message": "No exact match found, showing closest one"
        }

    return card_obj, error


def find_card_with_set_or_error(card, set_obj, hide_unreleased=False):
    error = None

    card_obj = Card.query.filter_by(set_id=set_obj.id, name=card["card_name"], number=card["card_num"]).first()

    # Check for unreleased cards before we try to fuzzy match
    if not card_obj:
        if not hide_unreleased:
            card_obj = UnreleasedCard.query.filter_by(set_id=set_obj.id, name=card["card_name"],
                                                      number=card["card_num"]).first()

        # If we STILL can't find the card object, try to find a similar card
        if not card_obj:
            card_obj, error = fuzzy_find_card_or_error(card, hide_unreleased)

    return card_obj, error


def proxies_base(parsed_decklist, options):
    errors = []
    output = []

    # TODO: This entire code is confusing to follow, improve this
    for card in parsed_decklist:
        if "error" in card:
            # TODO: Be more specific with the error, maybe get the specific error from the parser?
            errors.append({"card": card["line"], "message": "Invalid line"})
            continue

        set_obj = find_set(card, hide_unreleased=options["hideUnreleased"])

        if not set_obj:
            # If we couldn't find it, it's possible that the user never provided a set
            # so try to find a similar card (same number and name)
            # Try to find similar card
            card_obj, local_error = fuzzy_find_card_or_error(card, hide_unreleased=options["hideUnreleased"])

            if local_error:
                errors.append(local_error)
                continue

            # At this point, we have our card object, so just add it to our output
            # and continue to the next iteration
            output.append([card, card_obj])
            continue

        # If we reached this point, we have a set
        card_obj, local_error = find_card_with_set_or_error(card, set_obj, hide_unreleased=options["hideUnreleased"])

        if card_obj:
            output.append([card, card_obj])
        else:
            errors.append(local_error)

    return output, errors
