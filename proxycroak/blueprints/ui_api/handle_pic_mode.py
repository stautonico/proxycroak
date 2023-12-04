import os

from proxycroak.models import Card, Set


def handle_pic_mode(parsed_decklist, options):
    output = [[]]

    img_name = "small.webp" if options["lowres"] else "large.webp"

    # TODO: I wonder if this can be optimized
    for card in parsed_decklist:
        set_obj = Set.query.filter_by(ptcgoCode=card["set_id"]).first()


        if not set_obj:
            print(f"Can't find set {card['set_id']}")
            # TODO: Find a way to return errors (maybe a dict)
            continue

        card_obj = Card.query.filter_by(set_id=set_obj.id, name=card["card_name"]).first()

        if not card_obj:
            print(f"Can't find card with set {set_obj.id} and {card['card_name']}")
            # TODO: Find a way to return errors (maybe a dict)
            continue

        for x in range(card["amnt"]):
            if len(output[-1]) != 3:
                output[-1].append({"type": "pic", "data": os.path.join(card_obj.image, img_name)})
            else:
                output.append([{"type": "pic", "data": os.path.join(card_obj.image, img_name)}])

    return output
