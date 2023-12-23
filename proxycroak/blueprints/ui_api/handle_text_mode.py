from proxycroak.models import Card, Set
from proxycroak.const import SET_IDS, lookup_set_code_by_id, minify_card_text
from proxycroak.util.serialize import load_card
from proxycroak.util.card_to_html import type_to_html

from proxycroak.blueprints.ui_api.proxies_base import proxies_base



def handle_text_mode(parsed_decklist, options):
    final_output = [[]]

    output, errors = proxies_base(parsed_decklist, options)

    cleaned_output = []
    for card, card_obj in output:
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
                    atk["text"] = minify_card_text(atk["text"] or "")

                atks.append(atk)

            loaded_card["attacks"] = atks

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

        if loaded_card["rules"]:
            rules = []
            for rule in loaded_card["rules"]:
                rules.append(minify_card_text(rule) if not options["nomin"] else rule)

            loaded_card["rules"] = rules

        # If we have an SVI+ set code, set it from our dict
        if loaded_card["set"].ptcgoCode is None:
            loaded_card["set"].ptcgoCode = lookup_set_code_by_id(loaded_card["set_id"])

        cleaned_output.append([card, loaded_card])

    for card, card_obj in cleaned_output:
        for x in range(card["amnt"]):
            if len(final_output[-1]) != 3:
                final_output[-1].append({"type": "text", "data": card_obj})
            else:
                final_output.append([{"type": "text", "data": card_obj}])

    return final_output, errors
