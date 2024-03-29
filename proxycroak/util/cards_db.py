import os
from time import sleep
from json import dumps
from datetime import datetime
from hashlib import sha256

import pokemontcgsdk as tcgapi
import requests
from sentry_sdk import capture_exception

from proxycroak.models import Set, Card
from proxycroak.database import db
from proxycroak.util.serialize import serialize_card
from proxycroak.util.image import convert_to_webp
from proxycroak.logging import logger


def generate_set_payload(ptcglset):
    legalities = {
        "unlimited": ptcglset.legalities.unlimited,
        "expanded": ptcglset.legalities.expanded,
        "standard": ptcglset.legalities.standard
    }

    payload = {
        "id": ptcglset.id,
        "legalities": dumps(legalities),
        "name": ptcglset.name,
        "printedTotal": ptcglset.printedTotal,
        "ptcgoCode": ptcglset.ptcgoCode,
        "releaseDate": datetime.strptime(ptcglset.releaseDate, "%Y/%m/%d"),
        "series": ptcglset.series,
        "total": ptcglset.total,
        "updatedAt": datetime.strptime(ptcglset.updatedAt, "%Y/%m/%d %H:%M:%S")
    }

    return payload


def generate_card_payload(ptcglcard):
    payload = {
        "id": ptcglcard.id,
        "artist": ptcglcard.artist,
        "convertedRetreatCost": ptcglcard.convertedRetreatCost,
        "evolvesFrom": ptcglcard.evolvesFrom,
        "flavorText": ptcglcard.flavorText,
        "hp": ptcglcard.hp,
        "image": "/set/by/later/code",
        "regulationMark": ptcglcard.regulationMark,
        "name": ptcglcard.name,
        "nationalPokedexNumbers": dumps(ptcglcard.nationalPokedexNumbers) if ptcglcard.nationalPokedexNumbers else None,
        "number": ptcglcard.number,
        "rarity": ptcglcard.rarity,
        "retreatCost": dumps(ptcglcard.retreatCost),
        "rules": dumps(ptcglcard.rules) if ptcglcard.rules else None,
        "subtypes": dumps(ptcglcard.subtypes) if ptcglcard.subtypes else None,
        "supertype": ptcglcard.supertype,
        "types": dumps(ptcglcard.types) if ptcglcard.types else None,
        "resistances": None,
        "weaknesses": None,
        "set_id": ptcglcard.set.id
    }

    if ptcglcard.abilities:
        # Convert the abilities to json
        abilities = []

        for abil in ptcglcard.abilities:
            abilities.append({
                "name": abil.name,
                "text": abil.text,
                "type": abil.type
            })
        payload["abilities"] = dumps(abilities)
    else:
        payload["abilities"] = None

    # Convert the legalities to json
    payload["legalities"] = dumps({
        "unlimited": ptcglcard.legalities.unlimited,
        "expanded": ptcglcard.legalities.expanded,
        "standard": ptcglcard.legalities.standard
    })

    if ptcglcard.ancientTrait:
        # Convert the ancient trait to json
        payload["ancientTrait"] = dumps({
            "name": ptcglcard.ancientTrait.name,
            "text": ptcglcard.ancientTrait.text
        })
    else:
        payload["ancientTrait"] = None

    if ptcglcard.attacks:
        # Convert the attacks to json
        attacks = []

        for atk in ptcglcard.attacks:
            attacks.append({
                "name": atk.name,
                "cost": dumps(atk.cost),
                "convertedEnergyCost": atk.convertedEnergyCost,
                "damage": atk.damage,
                "text": atk.text
            })

        payload["attacks"] = dumps(attacks)
    else:
        payload["attacks"] = None

    if ptcglcard.resistances:
        # Convert resistances to json
        resistances = []

        for res in ptcglcard.resistances:
            resistances.append({
                "type": res.type,
                "value": res.value
            })

        payload["resistances"] = dumps(resistances)
    else:
        payload["resistances"] = None

    if ptcglcard.weaknesses:
        # Convert weaknesses to json
        weaknesses = []

        for res in ptcglcard.weaknesses:
            weaknesses.append({
                "type": res.type,
                "value": res.value
            })

        payload["weaknesses"] = dumps(weaknesses)
    else:
        payload["weaknesses"] = None

    return payload


def update_sets():
    # Go through each set and check if we have it in the database
    sets = tcgapi.Set.all()
    # sets = [tcgapi.Set.find("swsh12"), tcgapi.Set.find("sv1"), tcgapi.Set.find("sv2"), tcgapi.Set.find("sv3"),
    #         tcgapi.Set.find("sv3pt5"), tcgapi.Set.find("sv4")]
    added_new = False

    for s in sets:
        print(f"Working on {s.name}...")
        in_db_set = Set.query.get(s.id)

        # If we do not have the set, insert it into the database
        if not in_db_set:
            payload = generate_set_payload(s)

            new_set = Set(**payload)
            db.session.add(new_set)

            add_new_cards_for_set(s.id)
            added_new = True
        else:
            # If we do have the set, check if the new updated date is > the updated date in the database
            if in_db_set.updatedAt < datetime.strptime(s.updatedAt, "%Y/%m/%d %H:%M:%S"):
                # If it is, update the set and all related cards
                payload = generate_set_payload(s)
                for k, v in payload.items():
                    setattr(in_db_set, k, v)

                update_cards_for_set(s.id)
            else:
                logger.info("Not updating any sets, none have updates", "cron:update_sets")

        if added_new:
            logger.info(f"Done with {s.name}. Sleeping for 10 seconds...", "cron:update_sets")
            sleep(10)

        db.session.commit()


def make_new_card(card_obj):
    image_folder_path = os.path.join("proxycroak", "static", "img", "cards", card_obj.set.id, card_obj.id)
    os.makedirs(image_folder_path, exist_ok=True)

    r = requests.get(card_obj.images.small)

    if r.status_code == 200:
        convert_to_webp(r.content, os.path.join(image_folder_path, "small.webp"))
        # make_cropped_image(r.content, os.path.join(image_folder_path, "small_cropped.webp"), (22, 50, 224, 176))
    else:
        logger.warn(f"Can't retrieve small image for {card_obj.name}. Status code: {r.status_code}",
                    "cron:make_new_card")

    r = requests.get(card_obj.images.large)

    if r.status_code == 200:
        convert_to_webp(r.content, os.path.join(image_folder_path, "large.webp"))
        # make_cropped_image(r.content, os.path.join(image_folder_path, "large_cropped.webp"), (60, 146, 674, 526))
    else:
        logger.warn(f"Can't retrieve large image for {card_obj.name}. Status code: {r.status_code}",
                    "cron:make_new_card")

    newcard = Card(**generate_card_payload(card_obj))

    # The first part should be removed (proxycroak)
    newcard.image = os.path.join("/", *(image_folder_path.split(os.sep)[1:]))

    db.session.add(newcard)


def add_new_cards_for_set(set_id):
    cards_in_set = tcgapi.Card.where(q=f"set.id:{set_id}")

    if not os.path.exists("proxycroak/static"):
        capture_exception(Exception("FATAL: STATIC DIRECTORY DOESN'T EXIST! (add_new_cards_for_set)"))
        logger.fatal(f"proxycroak/static DOES NOT EXIST OR IS INACCESSIBLE", "cron:add_new_cards_for_set")
        # TODO: Send mobile notification
        exit(1)

    for c in cards_in_set:
        make_new_card(c)


def update_cards_for_set(set_id):
    cards_in_set = tcgapi.Card.where(q=f"set.id:{set_id}")

    if not os.path.exists("proxycroak/static"):
        capture_exception(Exception("FATAL: STATIC DIRECTORY DOESN'T EXIST! (update_cards_for_set)"))
        logger.fatal(f"proxycroak/static DOES NOT EXIST OR IS INACCESSIBLE", "cron:update_cards_for_set")
        # TODO: Send mobile notification
        exit(1)

    for c in cards_in_set:
        # Check if we have the card in the database
        in_db_card = Card.query.get(c.id)

        if in_db_card:

            # Calculate the hash of the card from the API
            from_api_hash = sha256(dumps(generate_card_payload(c), sort_keys=True).encode()).hexdigest()

            # Calculate the hash of the card from the database
            from_db_hash = sha256(dumps(serialize_card(in_db_card), sort_keys=True).encode()).hexdigest()

            # If the hashes are different, update the card
            if from_api_hash != from_db_hash:
                payload = generate_card_payload(c)
                for k, v in payload.items():
                    setattr(in_db_card, k, v)

            # TODO: Update images
        else:
            make_new_card(c)
