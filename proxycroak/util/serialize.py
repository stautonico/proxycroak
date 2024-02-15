from json import loads

from sqlalchemy import inspect


def recursive_json_loads(obj):
    if isinstance(obj, str):
        try:
            return recursive_json_loads(loads(obj))
        except ValueError:
            # If the string cannot be parsed as JSON, return it as is
            return obj
    elif isinstance(obj, list):
        return [recursive_json_loads(item) for item in obj]
    elif isinstance(obj, dict):
        return {key: recursive_json_loads(value) for key, value in obj.items()}
    else:
        return obj


def serialize_card(card, unreleased_card=False):
    if unreleased_card:
        output = {
            "id": card.id,
            "image": card.image,
            "name": card.name,
            "number": card.number,
            "set_id": card.set_id
        }
    else:
        output = {
            "id": card.id,
            "abilities": card.abilities,
            "artist": card.artist,
            "ancientTrait": card.ancientTrait,
            "attacks": card.attacks,
            "convertedRetreatCost": card.convertedRetreatCost,
            "evolvesFrom": card.evolvesFrom,
            "flavorText": card.flavorText,
            "hp": card.hp,
            "image": card.image,
            "regulationMark": card.regulationMark,
            "legalities": card.legalities,
            "name": card.name,
            "nationalPokedexNumbers": card.nationalPokedexNumbers,
            "number": card.number,
            "rarity": card.rarity,
            "resistances": card.resistances,
            "retreatCost": card.retreatCost,
            "rules": card.rules,
            "subtypes": card.subtypes,
            "supertype": card.supertype,
            "types": card.types,
            "weaknesses": card.weaknesses,
            "set_id": card.set_id
        }

    return output


def seralize_set(set, unreleased=False):
    if unreleased:
        output = {
            "id": set.id,
            "name": set.name,
            "ptcgoCode": set.ptcgoCode,
            "alternatePtcgoCode": set.alternatePtcgoCode,
            "updatedAt": set.updatedAt
        }
    else:
        output = {
            "id": set.id,
            "legalities": set.legalities,
            "name": set.name,
            "printedTotal": set.printedTotal,
            "ptcgoCode": set.ptcgoCode,
            "releaseDate": set.releaseDate,
            "series": set.series,
            "total": set.total,
            "updatedAt": set.updatedAt,
        }

    return output


# TODO: I don't like the name of this, but we'll leave it as this until I come up with something better
def load_card(card):
    output = {}

    # TODO: Can this be optimized?
    mapper = inspect(card)

    for col in mapper.attrs:
        key = col.key
        value = getattr(card, key)

        if key in ["abilities", "ancientTrait", "attacks", "legalities", "nationalPokedexNumbers", "resistances",
                   "retreatCost", "rules", "subtypes", "types", "weaknesses"]:
            if value is not None:
                output[key] = recursive_json_loads(value)
            else:
                output[key] = None
        else:
            output[key] = value

    return output
