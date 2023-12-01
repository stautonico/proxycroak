from flask import Flask, render_template
from dotenv import dotenv_values

from proxycroak.config import BaseConfig


def generate_config(mode="dev"):
    if mode not in ["dev", "prod", "test"]:
        raise Exception(f"Invalid run mode '{mode}'! Valid modes are 'dev', 'prod', and 'test'!")

    if mode == "dev":
        env = dotenv_values(".env")
    else:
        # Load .env.prod or .env.test
        env = dotenv_values(f".env.{mode}")

    config_object = BaseConfig.from_env(env)

    return config_object


def create_app(mode="dev"):
    config = generate_config(mode)

    app = Flask(config.PROJECT_NAME, instance_path=config.INSTANCE_FOLDER_PATH, instance_relative_config=True)

    configure_blueprints(app)
    configure_filter(app)
    configure_error_handlers(app)

    return app


def configure_blueprints(app):
    from proxycroak.blueprints import ui

    app.register_blueprint(ui.blueprint)


def configure_filter(app):
    from proxycroak.filters import current_url

    app.jinja_env.filters["current_url"] = current_url


def configure_error_handlers(app):
    @app.errorhandler(404)
    def not_found(e):
        meta = {
            "title": "404",
            "description": "Page not found!",
            "tags": ["404"]
        }

        return render_template("errors/404.html", meta=meta), 404
