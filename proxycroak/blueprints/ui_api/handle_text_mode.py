import os

from proxycroak.models import Card, Set
from proxycroak.const import SET_IDS, lookup_set_code_by_id, minify_card_text
from proxycroak.util.serialize import load_card
from proxycroak.util.card_to_html import type_to_html


def handle_text_mode(parsed_decklist, options):
    errors = []
    output = [[]]

    # TODO: Mimify text if option is enable
    # TODO: Include cropped image if option is enabled

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

        loaded_card = load_card(card_obj)

        # TODO: Optimize
        if loaded_card["types"]:
            types = []
            for t in loaded_card["types"]:
                types.append(type_to_html(t))

            loaded_card["types"] = types

        if loaded_card["abilities"]:
            abils = []
            for a in loaded_card["abilities"]:
                if not options["nomin"]:
                    a["text"] = minify_card_text(a["text"])
                abils.append(a)

            loaded_card["abilities"] = abils

        if loaded_card["attacks"]:
            atks = []
            for atk in loaded_card["attacks"]:
                atkout = []
                for cost in atk["cost"]:
                    atkout.append(type_to_html(cost))
                atk["cost"] = atkout

                if not options["nomin"]:
                    atk["text"] = minify_card_text(atk["text"])

                atks.append(atk)

            loaded_card["attacks"] = atks

        print(loaded_card["attacks"])

        if loaded_card["weaknesses"]:
            weaks = []
            for w in loaded_card["weaknesses"]:
                w["type"] = type_to_html(w["type"])
                weaks.append(w)

            loaded_card["weaknesses"] = weaks

        if loaded_card["resistances"]:
            res = []
            for r in loaded_card["resistances"]:
                r["type"] = type_to_html(r["type"])
                res.append(r)

            loaded_card["resistances"] = res

        if loaded_card["retreatCost"]:
            rcs = []
            for rc in loaded_card["retreatCost"]:
                rc = type_to_html(rc)
                rcs.append(rc)

            loaded_card["retreatCost"] = rcs

        # If we have a SVI+ set code, set it from our dict
        if loaded_card["set"].ptcgoCode is None:
            loaded_card["set"].ptcgoCode = lookup_set_code_by_id(loaded_card["set_id"])

        for x in range(card["amnt"]):
            if len(output[-1]) != 3:
                output[-1].append({"type": "text", "data": loaded_card})
            else:
                output.append([{"type": "text", "data": loaded_card}])

    return output, errors
