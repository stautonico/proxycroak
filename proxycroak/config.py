import os


class BaseConfig:
    PROJECT_NAME = "proxycroak"

    PROJECT_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

    DEBUG = False
    TESTING = False

    SECRET_KEY = "<secret_key_here>"
    INSTANCE_FOLDER_PATH = os.path.join("/tmp", "instance")

    @staticmethod
    def from_env(env):
        newconfig = BaseConfig()

        newconfig.PROJECT_NAME = env.get("PROJECT_NAME", BaseConfig.PROJECT_NAME)

        newconfig.DEBUG = env.get("DEBUG", BaseConfig.DEBUG)

        newconfig.TESTING = env.get("TESTING", BaseConfig.TESTING)

        if "SECRET_KEY" not in env:
            raise Exception("Missing required value 'SECRET_KEY' in environment!")

        newconfig.INSTANCE_FOLDER_PATH = env.get("INSTANCE_FOLDER_PATH", BaseConfig.INSTANCE_FOLDER_PATH)

        return newconfig
