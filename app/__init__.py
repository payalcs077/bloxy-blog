import os

import click
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

    if app.config.get("GOOGLE_CLIENT_ID") and app.config.get("GOOGLE_CLIENT_SECRET"):
        oauth.register(
            name="google",
            client_id=app.config["GOOGLE_CLIENT_ID"],
            client_secret=app.config["GOOGLE_CLIENT_SECRET"],
            server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
            client_kwargs={"scope": "openid email profile"},
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

    @app.cli.command("promote-admin")
    @click.option("--email", required=True, help="Email for an existing account")
    def promote_admin_command(email: str):
        from .models import ROLE_ADMIN, User

        user = User.query.filter_by(email=email.lower()).first()
        if user is None:
            raise click.ClickException(f"User not found for email: {email}")

        user.role = ROLE_ADMIN
        db.session.commit()
        click.echo(f"User '{user.username}' promoted to admin.")

    @app.context_processor
    def inject_now():
        from datetime import UTC, datetime

        return {"now": datetime.now(UTC)}

    return app
