import hmac
import re

from flask import Blueprint, current_app, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from ..extensions import db, oauth
from ..forms import LoginForm, RegistrationForm
from ..models import ROLE_ADMIN, ROLE_USER, ROLE_VALUES, User


bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("blog.index"))

    form = RegistrationForm()
    if form.validate_on_submit():
        selected_role = form.role.data
        if selected_role not in ROLE_VALUES:
            flash("Invalid role selected.", "danger")
            return render_template("auth/register.html", form=form)

        if selected_role == ROLE_ADMIN:
            expected_admin_token = (current_app.config.get("ADMIN_REGISTRATION_TOKEN", "") or "").strip()
            provided_admin_token = (form.admin_token.data or "").strip()
            if not expected_admin_token:
                flash("Admin registration is disabled on this server.", "danger")
                return render_template("auth/register.html", form=form)
            if not hmac.compare_digest(provided_admin_token, expected_admin_token):
                flash("Invalid admin registration token.", "danger")
                return render_template("auth/register.html", form=form)

        existing = User.query.filter(
            (User.email == form.email.data.lower()) | (User.username == form.username.data)
        ).first()
        if existing:
            flash("Email or username is already in use.", "danger")
            return render_template("auth/register.html", form=form)

        user = User(
            username=form.username.data,
            email=form.email.data.lower(),
            role=selected_role,
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        login_user(user)
        flash("Account created. Welcome!", "success")
        return redirect(url_for("blog.index"))

    return render_template("auth/register.html", form=form)


@bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("blog.index"))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if not user or not user.check_password(form.password.data):
            flash("Invalid email or password.", "danger")
            return render_template("auth/login.html", form=form)

        login_user(user, remember=form.remember.data)
        next_url = request.args.get("next")
        if next_url and next_url.startswith("/") and not next_url.startswith("//"):
            return redirect(next_url)

        flash("Signed in successfully.", "success")
        return redirect(url_for("blog.index"))

    return render_template("auth/login.html", form=form)


@bp.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("blog.index"))


@bp.route("/login/github")
def login_github():
    github = oauth.create_client("github")
    if github is None:
        flash("GitHub OAuth is not configured on this server.", "warning")
        return redirect(url_for("auth.login"))

    redirect_uri = url_for("auth.github_authorize", _external=True)
    return github.authorize_redirect(redirect_uri)


@bp.route("/authorize/github")
def github_authorize():
    github = oauth.create_client("github")
    if github is None:
        flash("GitHub OAuth is not configured on this server.", "warning")
        return redirect(url_for("auth.login"))

    try:
        github.authorize_access_token()
    except Exception:
        flash("GitHub authorization failed. Please try again.", "danger")
        return redirect(url_for("auth.login"))

    profile_response = github.get("user")
    profile = profile_response.json() if profile_response.ok else {}

    github_id = profile.get("id")
    if github_id is None:
        flash("GitHub login failed. Missing account identifier.", "danger")
        return redirect(url_for("auth.login"))

    email = profile.get("email")
    if not email:
        emails_response = github.get("user/emails")
        if emails_response.ok:
            emails = emails_response.json()
            primary_verified = next(
                (entry["email"] for entry in emails if entry.get("primary") and entry.get("verified")),
                None,
            )
            any_verified = next((entry["email"] for entry in emails if entry.get("verified")), None)
            email = primary_verified or any_verified

    email = (email or f"github_{github_id}@users.noreply.github.com").lower()
    oauth_sub = str(github_id)

    user = User.query.filter_by(oauth_provider="github", oauth_sub=oauth_sub).first()

    if user is None:
        existing_email_user = User.query.filter_by(email=email).first()
        if existing_email_user and not (
            existing_email_user.oauth_provider is None and existing_email_user.oauth_sub is None
        ):
            flash("This email is already linked to another account.", "danger")
            return redirect(url_for("auth.login"))

        if existing_email_user:
            existing_email_user.oauth_provider = "github"
            existing_email_user.oauth_sub = oauth_sub
            user = existing_email_user
        else:
            base_username = profile.get("login") or f"github_{github_id}"
            user = User(
                username=_unique_username(base_username),
                email=email,
                oauth_provider="github",
                oauth_sub=oauth_sub,
                role=ROLE_USER,
            )
            db.session.add(user)

        db.session.commit()

    login_user(user)
    flash("Signed in with GitHub.", "success")
    return redirect(url_for("blog.index"))


def _unique_username(base_username: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9_.-]", "", base_username).lower() or "user"
    candidate = cleaned[:30]

    suffix = 1
    while User.query.filter_by(username=candidate).first():
        suffix_text = str(suffix)
        candidate = f"{cleaned[: 30 - len(suffix_text)]}{suffix_text}"
        suffix += 1

    return candidate
