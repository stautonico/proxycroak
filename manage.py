import argparse
import os, sys
import dotenv

from proxycroak.app import create_app
from proxycroak.util import cards_db

dotenv.load_dotenv(".env")

BASE_DIR = os.path.join(os.path.dirname(__file__))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

VALID_COMMANDS = ["updatesets"]


def main():
    parser = argparse.ArgumentParser(description="Manage the proxycroak app")

    parser.add_argument("command", type=str, help="The command to run")

    args = parser.parse_args()

    app = create_app()

    if args.command.lower() not in VALID_COMMANDS:
        print(f"'{args.command}' unrecognized command. Valid commands: {', '.join(VALID_COMMANDS)}")

    elif args.command.lower() == "updatesets":
        with app.app_context():
            cards_db.update_sets()


if __name__ == '__main__':
    main()
