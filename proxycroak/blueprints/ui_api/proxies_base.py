from sqlalchemy import or_

from proxycroak.models import Card, Set
from proxycroak.const import SET_IDS


def proxies_base(parsed_decklist, options):
    errors = []
    output = []

    for card in parsed_decklist:
        card_obj = None

        if "error" in card:
            # TODO: Be more specific with the error, maybe get the specific error from the parser?
            errors.append({"card": card["line"], "message": "Invalid line"})
            continue

        if card["set_id"] in SET_IDS:
            set_obj = Set.query.filter_by(id=SET_IDS[card["set_id"]]).first()
        else:
            set_obj = Set.query.filter(
                or_(Set.ptcgoCode == card["set_id"], Set.alternatePtcgoCode == card["set_id"])).first()
            # set_obj = Set.query.filter_by(ptcgoCode=card["set_id"]).first()

        if not set_obj:
            # If we couldn't find it, it's possible that the user never provided a set
            # so try to find a similar card (same number and name)
            # Try to find similar card
            card_obj = Card.query.filter_by(name=card["card_name"], number=card["card_num"]).first()
            if not card_obj:
                # TODO: Hard-code error messages somewhere else
                errors.append({
                    "card": f"{card['amnt']}x {card['card_name']} ({card['card_num']})",
                    "message": "No results found (card misspelled or unavailable)"
                })
                continue
            else:
                errors.append({
                    "card": f"{card['amnt']}x {card['card_name']} ({card['card_num']})",
                    "message": "No exact match found, showing closest one"
                })

        if not card_obj:
            card_obj = Card.query.filter_by(set_id=set_obj.id, name=card["card_name"], number=card["card_num"]).first()

            if not card_obj:
                # Try to find similar card
                card_obj = Card.query.filter_by(name=card["card_name"], number=card["card_num"]).first()
                if not card_obj:
                    # Try fuzzy matching the card name
                    card_obj = Card.query.filter(
                        Card.name.like(card["card_name"]) | Card.name.like(f"%{card['card_num']}%")).first()

                    if not card_obj:
                        # TODO: Hard-code error messages somewhere else
                        errors.append({
                            "card": f"{card['amnt']}x {card['card_name']} ({card['card_num']})",
                            "message": "No results found (card misspelled or unavailable)"
                        })
                        continue
                    else:
                        errors.append({
                            "card": f"{card['amnt']}x {card['card_name']} ({card['card_num']})",
                            "message": "No exact match found, showing closest one"
                        })

            if card_obj:
                output.append([card, card_obj])

    return output, errors
