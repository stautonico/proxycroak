# This is a very rough test, but it's only meant for basic testing

import pytest
import sys
import os
from secrets import token_urlsafe
import dotenv
from bs4 import BeautifulSoup
from parameterized import parameterized

import mysql.connector

dotenv.load_dotenv(".env")
dotenv.load_dotenv("../.env")

sys.path.extend(["..", "../proxycroak"])

from proxycroak import create_app
from proxycroak.const import SET_IDS
from proxycroak.config import CONFIG

mydb = mysql.connector.connect(
    host=CONFIG.DB_HOST,
    port=CONFIG.DB_PORT,
    user=CONFIG.DB_USER,
    password=CONFIG.DB_PASS,
    database="proxycroak"
)

c = mydb.cursor()


def find_setid_reverse(set_id):
    for ptcgocode, id in SET_IDS.items():
        if id == set_id:
            return ptcgocode

    return None


def card_to_json(card):
    return {
        "id": card[0],
        "abilities": card[1],
        "artist": card[2],
        "ancientTrait": card[3],
        "attacks": card[4],
        "convertedRetreatCost": card[5],
        "evolvesFrom": card[6],
        "flavorText": card[7],
        "hp": card[8],
        "image": card[9],
        "regulationMark": card[10],
        "legalities": card[11],
        "name": card[12],
        "nationalPokedexNumbers": card[13],
        "number": card[14],
        "rarity": card[15],
        "resistances": card[16],
        "retreatCost": card[17],
        "rules": card[18],
        "subtypes": card[19],
        "supertype": card[20],
        "types": card[21],
        "weaknesses": card[22],
        "set_id": card[23]
    }


def set_to_json(set):
    return {
        "id": set[0],
        "legalities": set[1],
        "name": set[2],
        "printedTotal": set[3],
        "ptcgoCode": set[4],
        "releaseDate": set[5],
        "series": set[6],
        "total": set[7],
        "updatedAt": set[8],
        "alternatePtcgoCode": set[9]
    }


def make_line(card, set):
    if set["ptcgoCode"] is None:
        set["ptcgoCode"] = find_setid_reverse(set["id"])

    output = f"1 {card['name']} {set['ptcgoCode']} {card['number']}"
    return output


def generate_lines():
    c.execute("SELECT * FROM card;")
    cards = c.fetchall()
    c.execute("SELECT * FROM `set`;")
    dirty_sets = c.fetchall()

    lines = []

    sets = {}

    for s in dirty_sets:
        s = set_to_json(s)
        sets[s["id"]] = s

    for rawcard in cards:
        card = card_to_json(rawcard)
        line = make_line(card, sets[card["set_id"]])
        lines.append(line)

    return lines


lines = generate_lines()

app = create_app("test")
ctx = app.app_context()
ctx.push()
client = app.test_client()


@parameterized.expand([
    [x] for x in lines
])
def test_cards(line):
    response = client.post("/ui/api/proxies", data={
        "options[lowres]": False,
        "options[watermark]": False,
        "options[legacy]": False,
        "options[illustration]": False,
        "options[nomin]": False,
        "options[jp]": False,
        "options[exclude_secrets]": False,
        "options[hideUnreleased]": False,
        "submit": "Generate",
        "mode": "pic",
        "activeDeck": "1",
        "decks[0]": line
    })
    assert response.status_code == 200

    soup = BeautifulSoup(response.get_data(as_text=True), "html.parser")
    card = soup.select(".proxyDeck__card")[0]

    img = card.find("img")

    img_response = client.get(img.get("src"))

    assert img_response.status_code == 200
