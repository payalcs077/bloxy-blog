from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import current_user

from ..extensions import db
from ..models import ROLE_ADMIN, ROLE_AUTHOR, ROLE_USER, Post, User


bp = Blueprint("admin", __name__, url_prefix="/admin")


@bp.before_request
def enforce_admin():
    if not current_user.is_authenticated:
        return redirect(url_for("auth.login", next=request.path))

    if not current_user.is_admin:
        abort(403)


@bp.route("/users")
def users():
    users_list = User.query.order_by(User.created_at.desc()).all()
    return render_template("admin/users.html", users=users_list)


@bp.route("/users/<int:user_id>/role", methods=["POST"])
def update_user_role(user_id: int):
    user = User.query.get_or_404(user_id)
    new_role = (request.form.get("role") or "").strip().lower()

    if new_role not in (ROLE_USER, ROLE_AUTHOR, ROLE_ADMIN):
        flash("Invalid role selected.", "danger")
        return redirect(url_for("admin.users"))

    if user.id == current_user.id and new_role != ROLE_ADMIN:
        flash("You cannot remove your own admin role.", "warning")
        return redirect(url_for("admin.users"))

    user.role = new_role
    db.session.commit()
    flash(f"Updated role for {user.username} to {new_role}.", "success")
    return redirect(url_for("admin.users"))


@bp.route("/users/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id: int):
    user = User.query.get_or_404(user_id)
    if user.id == current_user.id:
        flash("You cannot delete your own admin account.", "warning")
        return redirect(url_for("admin.users"))

    db.session.delete(user)
    db.session.commit()
    flash(f"Deleted user {user.username}.", "info")
    return redirect(url_for("admin.users"))


@bp.route("/posts")
def posts():
    posts_list = Post.query.order_by(Post.created_at.desc()).all()
    return render_template("admin/posts.html", posts=posts_list)


@bp.route("/posts/<int:post_id>/delete", methods=["POST"])
def delete_post(post_id: int):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash(f"Deleted post '{post.title}'.", "info")
    return redirect(url_for("admin.posts"))
