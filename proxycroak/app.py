import logging
import os
from datetime import datetime as dt

print(os.environ)
print(os.getcwd())
print(os.listdir())

from flask.logging import default_handler
from flask import Flask, render_template, request
from flask_migrate import Migrate
import sentry_sdk

from proxycroak.config import CONFIG
from proxycroak.database import db
from proxycroak.scheduler import scheduler
from proxycroak.models import SharedDecklist
from proxycroak.util.cards_db import update_sets
from proxycroak.logging import logger


def create_app(mode=None):
    logger.info("Building config...", "init")
    if not os.path.exists(os.path.join(CONFIG.INSTANCE_FOLDER_PATH, "instance")):
        os.mkdir(os.path.join(CONFIG.INSTANCE_FOLDER_PATH, "instance"))

    logger.info("Successfully built config. Starting to init app...", "init")
    app = Flask(CONFIG.PROJECT_NAME, instance_path=CONFIG.INSTANCE_FOLDER_PATH, instance_relative_config=True)

    configure_blueprints(app)
    configure_filter(app)
    configure_error_handlers(app)
    configure_middleware(app)
    configure_logging(app)
    configure_additional(app)
    configure_teardown(app)

    logger.info("App successfully configured", "init")

    return app


def configure_blueprints(app):
    logger.info("Configuring blueprints...", "init")
    from proxycroak.blueprints import ui, ui_api

    app.register_blueprint(ui.blueprint)
    app.register_blueprint(ui_api.blueprint)


def configure_filter(app):
    logger.info("Configuring filters...", "init")
    # from proxycroak.filters import current_url
    #
    # app.jinja_env.filters["current_url"] = current_url


def configure_error_handlers(app):
    logger.info("Configuring error handlers...", "init")

    @app.errorhandler(500)
    def internal_server_error(e):
        meta = {
            "title": "500",
            "description": "Internal server error!",
            "tags": ["500"]
        }

        return render_template("errors/500.html", meta=meta), 500

    @app.errorhandler(404)
    def not_found(e):
        meta = {
            "title": "404",
            "description": "Page not found!",
            "tags": ["404"]
        }

        return render_template("errors/404.html", meta=meta), 404

    @app.errorhandler(400)
    def bad_request(e):
        meta = {
            "title": "400",
            "description": "Bad Request",
            "tags": ["400"]
        }

        return render_template("errors/400.html", meta=meta), 400


def configure_middleware(app):
    logger.info("Configuring middleware...", "init")

    from proxycroak.models import Set, Card, SharedDecklist

    # Configure the database
    app.config["SQLALCHEMY_DATABASE_URI"] = CONFIG.DB_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config["SQLALCHEMY_CHECK_SAME_THREAD"] = False
    db.init_app(app)

    with app.app_context():
        db.create_all()

    # Configure flask-migrate for migration support
    migrate = Migrate(app, db)

    # idk if this is considered middleware, but we'll put it here anyway
    sentry_sdk.init(
        dsn=CONFIG.SENTRY_DSN,
        traces_sample_rate=1.0,
        profiles_sample_rate=1.0,
        enable_tracing=True,
        # debug=CONFIG.DEBUG,
        environment="development" if CONFIG.DEBUG else "testing" if CONFIG.TESTING else "production"
    )

    scheduler.init_app(app)

    # Check if maintenance mode is enabled
    @app.before_request
    def check_maintenance_mode():
        if os.path.exists("MAINTENANCE_MODE"):
            if not request.path.startswith("/static"):
                META = {
                    "title": "Maintenance",
                    "description": "Proxycroak is currently under maintenance and should be back up and running soon!",
                    "tags": ["maintenance"]
                }
                return render_template("pages/maintenance.html", meta=META)


def configure_logging(app):
    logger.info("Configuring logging...", "init")

    handler = logging.FileHandler(os.path.join(CONFIG.LOG_DIRECTORY, "requests.log"))
    handler.setLevel(logging.DEBUG if CONFIG.DEBUG else logging.INFO)
    formatter = logging.Formatter('[%(levelname)s] - %(message)s')
    handler.setFormatter(formatter)

    app.logger.removeHandler(default_handler)
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.DEBUG if CONFIG.DEBUG else logging.INFO)

    @app.after_request
    def after_request(response):
        # If we're requesting a static asset, don't log it
        if "static" not in request.path:
            app.logger.info(
                "(%s) - %s | %s | %s | %s | len: %s | %s",
                dt.utcnow().strftime("%b/%d/%Y:%H:%M:%S.%f")[:-3],
                request.remote_addr,
                request.method,
                request.path,
                response.status,
                response.content_length,
                request.user_agent,
            )

        return response


def configure_additional(app):
    logger.info("Configuring additional...", "init")

    app.config["SCHEDULER_API_ENABLED"] = True
    """Misc things to do when the app starts"""

    def delete_expired_shares():
        with app.app_context():
            # Get a list of all jobs that are expired
            shares = SharedDecklist.query.filter(SharedDecklist.expires <= dt.now()).all()
            if len(shares) > 0:
                logger.info(f"Deleting {len(shares)} expires shares...", "cron:delete_expired_shares")
            for share in shares:
                db.session.delete(share)

            db.session.commit()

    # Add a job to check and delete expired shares (runs once per day)
    scheduler.add_job(func=delete_expired_shares, trigger="interval", hours=24, id="delete-expired-shares")

    def update_cards_database():
        with app.app_context():
            update_sets()

    # Add a job to check if any sets have updates. If they do, pull the changes (runs once per day)
    scheduler.add_job(func=update_cards_database, trigger="interval", hours=24, id="update-sets")
    # scheduler.add_job(func=update_cards_database, trigger="interval", seconds=5, id="update-sets")

    scheduler.start()

    # Configure global variables that are available in any template
    @app.context_processor
    def inject_global_vars():
        return dict(DISCORD_URL=CONFIG.DISCORD_URL, BUILD_VERSION=CONFIG.BUILD_VERSION)


def configure_teardown(app):
    """Things to do when the app shuts down"""

    logger.info("Configuring teardown...", "init")


    # @app.teardown_appcontext
    # def stop_scheduler(exception=None):
    #     scheduler.shutdown()
