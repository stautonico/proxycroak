import argparse
import sys
import os
from datetime import datetime

import requests
from bs4 import BeautifulSoup
import dotenv

dotenv.load_dotenv("../.env")

sys.path.insert(0, "..")

from proxycroak.database import db
from proxycroak.models import UnreleasedSet, UnreleasedCard
from proxycroak.app import create_app
from proxycroak.util.image import convert_to_webp

app = create_app()

parser = argparse.ArgumentParser(
    prog=sys.argv[0],
    description="Download proxies of unreleased sets from justinbasil.com"
)

parser.add_argument("set_id", help="The internal set id from justinbasil (e.g. sv4, sv5...)")
parser.add_argument("set_name", help="The name of the set")
parser.add_argument("set_code", help="The 3 (usually) letter set code (e.g. SVI, PAL, OBF...)")
parser.add_argument("img_dir",
                    help="The directory where the set folder will be created and all the images will be stored")

args = parser.parse_args()

r = requests.get(f"https://www.justinbasil.com/proxies/{args.set_id}")

if r.status_code != 200:
    print(f"[error] Failed to retrieve https://www.justinbasil.com/proxies/{args.set_id} (status: {r.status_code})")
    exit(1)

soup = BeautifulSoup(r.text, "html.parser")

my_divs = soup.find_all("div", {"class": "sqs-block gallery-block sqs-block-gallery"})

images = my_divs[0].find_all("img")

set_folder = os.path.join(args.img_dir, args.set_id)

if not os.path.exists(set_folder):
    try:
        os.mkdir(set_folder)
    except Exception as e:
        print("[error] Failed to make set directory!")
        exit(1)

with app.app_context():
    setexists = UnreleasedSet.query.get(args.set_id)

    if not setexists:
        newset = UnreleasedSet(
            id=args.set_id,
            name=args.set_name.title(),
            ptcgoCode=args.set_code,
            updatedAt=datetime.now()
        )

        db.session.add(newset)

    for i, img in enumerate(images):
        src = img.get("src")
        if src is not None:
            card_name = img["alt"].replace(".png", "")

            card_id = f"{args.set_id}-{i + 1}"

            newcard = UnreleasedCard(
                id=card_id,
                image=f"/static/img/unreleased/cards/{args.set_id}/{card_id}",
                name=card_name,
                number=f"{i + 1}",
                set_id=args.set_id
            )

            db.session.add(newcard)

            card_path = os.path.join(set_folder, card_id)
            if not os.path.exists(card_path) or not os.path.exists(os.path.join(card_path, "large.png")):
                r = requests.get(src)
                if r.status_code == 200:
                    try:
                        os.mkdir(card_path)
                    except Exception as e:
                        print(f"[error] failed to make directory for card {card_id}")
                        exit(1)

                    convert_to_webp(r.content, os.path.join(set_folder, card_id, "large.webp"))
                else:
                    print(f"[warn] Failed to retrieve image for '{card_id}' ({card_name})")
                    continue

            print(f"Inserting '{card_id}' into database...")


    db.session.commit()
