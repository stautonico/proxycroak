import os

from sentry_sdk import capture_exception
from dotenv import dotenv_values

from proxycroak import const


def _create_database_uri(vendor, user, passwd, host, port, current_config):
    if vendor == "sqlite":
        if host == "memory":
            return "sqlite://"

        return f"sqlite:///{current_config.INSTANCE_FOLDER_PATH}/instance/{host}?check_same_thread=False"

    elif vendor == "mysql":
        return f"mysql+mysqlconnector://{user}:{passwd}@{host}:{port}/proxycroak"

    else:
        print(f"[init:config:FATAL] Invalid database vendor: '{vendor}'")


def _check_required_values(env):
    required_fields = ["SECRET_KEY", "DB_VENDOR", "DB_HOST", "SENTRY_DSN", "LOG_DIRECTORY", "DISCORD_URL",
                       "ENVIRONMENT"]
    for field in required_fields:
        if field not in env or env.get(field) in [None, ""]:
            print(f"[init:config:FATAL] Missing required value '{field}' in environment!")
            exit(1)

    # The "VERSION" file should exist (should be auto generated by docker or whatever
    if not os.path.exists("VERSION") and not env.get("ENVIRONMENT") == "tools":
        # This field should be set automatically, and if it's not something's broken
        capture_exception(Exception(
            "[init:config:FATAL] The 'VERSION' file is missing! This file should be auto-generated! Something is broken!"))
        print(
            f"[init:config:FATAL] The 'VERSION' file is missing! This file should be auto-generated! Something is broken!")
        exit(1)

    if not env.get("ENVIRONMENT") == "tools":
        try:
            with open("VERSION", "r") as f:
                content = f.read()

                # We expect 2 lines
                version, build_num = content.split("\n")

                if content.count(".") != 2:
                    raise Exception()
        except Exception as e:
            # This field should be set automatically, and if it's not something's broken
            print(
                f"[init:config:FATAL] The 'VERSION' file is invalid! This file should be auto-generated! Something is broken!")
            exit(1)


class BaseConfig:
    PROJECT_NAME = "proxycroak"

    PROJECT_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

    DEBUG = False
    TESTING = False

    ENVIRONMENT = None

    SECRET_KEY = "<secret_key_here>"
    INSTANCE_FOLDER_PATH = "/tmp"

    DB_VENDOR = None
    DB_HOST = None
    DB_USER = None
    DB_PASS = None
    DB_PORT = None
    DB_URI = None

    SENTRY_DSN = None

    LOG_DIRECTORY = None

    DISCORD_URL = None

    BUILD_VERSION = None
    BUILD_HASH = None

    @staticmethod
    def from_env(env):
        _check_required_values(env)

        newconfig = BaseConfig()

        newconfig.PROJECT_NAME = env.get("PROJECT_NAME", BaseConfig.PROJECT_NAME)

        newconfig.DEBUG = env.get("DEBUG", BaseConfig.DEBUG == "true")

        # Validate the environment
        environment = env.get("ENVIRONMENT").lower()

        if environment not in const.ENVIRONMENTS:
            raise Exception(
                f"[init:config] invalid environment: '{env['ENVIRONMENT'].lower()}'. Valid environments: {', '.join(const.ENVIRONMENTS)}")

        newconfig.TESTING = env.get("TESTING", BaseConfig.TESTING == "true")

        newconfig.INSTANCE_FOLDER_PATH = env.get("INSTANCE_FOLDER_PATH", BaseConfig.INSTANCE_FOLDER_PATH)
        if env["DB_VENDOR"].lower() not in const.DATABASE_VENDORS:
            raise Exception(
                f"[init:config] invalid database vendor: '{env['DB_VENDOR'].lower()}'. Valid db vendors: {', '.join(const.DATABASE_VENDORS)}")

        newconfig.DB_VENDOR = env["DB_VENDOR"].lower()
        newconfig.DB_HOST = env["DB_HOST"]

        newconfig.DB_USER = env.get("DB_USER")
        newconfig.DB_PASS = env.get("DB_PASS")
        newconfig.DB_PORT = env.get("DB_PORT")

        newconfig.DB_URI = _create_database_uri(newconfig.DB_VENDOR, newconfig.DB_USER, newconfig.DB_PASS,
                                                newconfig.DB_HOST, newconfig.DB_PORT, newconfig)

        newconfig.SENTRY_DSN = env.get("SENTRY_DSN")

        newconfig.LOG_DIRECTORY = env.get("LOG_DIRECTORY")

        newconfig.DISCORD_URL = env.get("DISCORD_URL")

        if not env.get("ENVIRONMENT") == "tools":
            with open("VERSION", "r") as f:
                # We expect 2 lines
                newconfig.BUILD_VERSION, newconfig.BUILD_HASH = f.read().split("\n")

        return newconfig


def generate_config(mode=None):
    # if mode is none, try to guess:
    # If debug enabled: mode = dev
    # if testing enabled: mode = test
    # if neither enabled: mode = prod
    if mode is None:
        if os.getenv("DEBUG"):
            mode = "dev"
        elif os.getenv("TESTING"):
            mode = "test"
        else:
            mode = "prod"

    if mode not in ["dev", "prod", "test"]:
        raise Exception(f"Invalid run mode '{mode}'! Valid modes are 'dev', 'prod', and 'test'!")

    if mode == "dev":
        env = dotenv_values(".env")
    else:
        # Load .env.prod or .env.test
        env = dotenv_values(f".env.{mode}")

    config_object = BaseConfig.from_env({**env, **os.environ})

    return config_object


CONFIG = generate_config()
