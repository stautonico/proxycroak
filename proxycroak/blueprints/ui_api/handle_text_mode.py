import os

from proxycroak.models import Card, Set
from proxycroak.const import SET_IDS
from proxycroak.util.serialize import serialize_card


def handle_text_mode(parsed_decklist, options):
    errors = []
    output = [[]]

    img_name = "small.webp" if options["lowres"] else "large.webp"

    # TODO: Can this be optimized without 100,000 if statements
    for card in parsed_decklist:
        card_obj = None

        if card["set_id"] in SET_IDS:
            set_obj = Set.query.filter_by(id=SET_IDS[card["set_id"]]).first()
        else:
            set_obj = Set.query.filter_by(ptcgoCode=card["set_id"]).first()

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
                    card_obj = Card.query.filter(Card.name.like(card["card_name"]) | Card.name.like(f"%{card['card_num']}%")).first()

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

        for x in range(card["amnt"]):
            if len(output[-1]) != 3:
                output[-1].append({"type": "text", "data": serialize_card(card_obj)})
            else:
                output.append([{"type": "text", "data": serialize_card(card_obj)}])

    return output, errors