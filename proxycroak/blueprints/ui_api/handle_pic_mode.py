import os

from proxycroak.blueprints.ui_api.proxies_base import proxies_base


def handle_pic_mode(parsed_decklist, options):
    final_output = [[]]
    output, errors = proxies_base(parsed_decklist, options)

    img_name = "small.webp" if options["lowres"] else "large.webp"

    for card, card_obj in output:
        for x in range(card["amnt"]):
            if len(final_output[-1]) != 3:
                final_output[-1].append({"type": "pic", "data": os.path.join(card_obj.image, img_name)})
            else:
                final_output.append([{"type": "pic", "data": os.path.join(card_obj.image, img_name)}])

    return final_output, errors
