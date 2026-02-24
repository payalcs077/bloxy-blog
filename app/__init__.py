import os

from flask import Flask

from config import Config

from .extensions import csrf, db, login_manager, oauth


def create_app(config_class=Config):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_class)

    os.makedirs(app.instance_path, exist_ok=True)

    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    oauth.init_app(app)

    login_manager.login_view = "auth.login"
    login_manager.login_message_category = "warning"

    if app.config.get("GITHUB_CLIENT_ID") and app.config.get("GITHUB_CLIENT_SECRET"):
        oauth.register(
            name="github",
            client_id=app.config["GITHUB_CLIENT_ID"],
            client_secret=app.config["GITHUB_CLIENT_SECRET"],
            access_token_url="https://github.com/login/oauth/access_token",
            authorize_url="https://github.com/login/oauth/authorize",
            api_base_url="https://api.github.com/",
            client_kwargs={"scope": "read:user user:email"},
        )

    from .auth.routes import bp as auth_bp
    from .blog.routes import bp as blog_bp
    from .admin.routes import bp as admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(blog_bp)
    app.register_blueprint(admin_bp)

    @app.cli.command("init-db")
    def init_db_command():
        db.create_all()
        print("Database initialized.")

    @app.cli.command("reset-db")
    def reset_db_command():
        db.drop_all()
        db.create_all()
        print("Database reset.")

    @app.context_processor
    def inject_now():
        from datetime import UTC, datetime

        return {"now": datetime.now(UTC)}

    return app
