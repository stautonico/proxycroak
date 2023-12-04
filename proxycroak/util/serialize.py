from json import loads


def serialize_card(card):
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
        "image": "TODO: Generate image folder path when downloading image",
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
