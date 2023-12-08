import os

from dotenv import dotenv_values

from proxycroak import const


def _create_database_uri(vendor, user, passwd, host, port, current_config):
    if vendor == "sqlite":
        if host == "memory":
            return "sqlite://"

        return f"sqlite:///{current_config.INSTANCE_FOLDER_PATH}/instance/{host}"


def _check_required_values(env):
    required_fields = ["SECRET_KEY", "DB_VENDOR", "DB_HOST", "SENTRY_DSN", "LOG_DIRECTORY"]
    for field in required_fields:
        if field not in env or env.get(field) in [None, ""]:
            raise Exception(f"[init:config] Missing required value '{field}' in environment!")


class BaseConfig:
    PROJECT_NAME = "proxycroak"

    PROJECT_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

    DEBUG = False
    TESTING = False

    SECRET_KEY = "<secret_key_here>"
    INSTANCE_FOLDER_PATH = "/tmp"

    DB_VENDOR = None
    DB_HOST = None
    DB_USER = None
    DB_PASS = None
    DB_PORT = None
    DB_URI = 2

    SENTRY_DSN = None

    LOG_DIRECTORY = None

    @staticmethod
    def from_env(env):
        _check_required_values(env)

        newconfig = BaseConfig()

        newconfig.PROJECT_NAME = env.get("PROJECT_NAME", BaseConfig.PROJECT_NAME)

        newconfig.DEBUG = env.get("DEBUG", BaseConfig.DEBUG == "true")

        newconfig.TESTING = env.get("TESTING", BaseConfig.TESTING == "true")

        newconfig.INSTANCE_FOLDER_PATH = env.get("INSTANCE_FOLDER_PATH", BaseConfig.INSTANCE_FOLDER_PATH)
        if env["DB_VENDOR"].lower() not in const.DATABASE_VENDORS:
            raise Exception(
                f"[init:config] invalid database vendor: '{env['DB_VENDOR'].lower()}'. Valid db vendors: {' '.join(const.DATABASE_VENDORS)}")

        newconfig.DB_VENDOR = env["DB_VENDOR"].lower()
        newconfig.DB_HOST = env["DB_HOST"]

        newconfig.DB_USER = env.get("DB_USER")
        newconfig.DB_PASS = env.get("DB_PASS")
        newconfig.DB_PORT = env.get("DB_PORT")

        newconfig.DB_URI = _create_database_uri(newconfig.DB_VENDOR, newconfig.DB_USER, newconfig.DB_PASS,
                                                newconfig.DB_HOST, newconfig.DB_PORT, newconfig)

        newconfig.SENTRY_DSN = env.get("SENTRY_DSN")

        newconfig.LOG_DIRECTORY = env.get("LOG_DIRECTORY")

        return newconfig


def generate_config(mode=None):
    # if mode is none, try to guess:
    # If debug enabled: mode = dev
    # if testing enabled: mode = test
    # if neither enabled: mode = prod
    if mode is None:
        if os.getenv("DEBUG") == "true":
            mode = "dev"
        elif os.getenv("TESTING") == "true":
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

    config_object = BaseConfig.from_env(env)

    return config_object


CONFIG = generate_config()
