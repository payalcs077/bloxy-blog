from flask import Blueprint, abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from ..extensions import db
from ..forms import CommentForm, PostForm
from ..models import Comment, Like, Post


bp = Blueprint("blog", __name__)


@bp.route("/")
def index():
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return render_template("blog/index.html", posts=posts)


@bp.route("/post/<int:post_id>")
def post_detail(post_id: int):
    post = Post.query.get_or_404(post_id)
    comment_form = CommentForm()
    liked_by_current_user = False
    if current_user.is_authenticated:
        liked_by_current_user = (
            Like.query.filter_by(user_id=current_user.id, post_id=post.id).first() is not None
        )

    return render_template(
        "blog/post_detail.html",
        post=post,
        comment_form=comment_form,
        liked_by_current_user=liked_by_current_user,
    )


@bp.route("/post/new", methods=["GET", "POST"])
@login_required
def post_create():
    if not current_user.can_write_posts:
        flash("Only authors can create posts.", "warning")
        return redirect(url_for("blog.index"))

    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, body=form.body.data, author_id=current_user.id)
        db.session.add(post)
        db.session.commit()
        flash("Post published.", "success")
        return redirect(url_for("blog.post_detail", post_id=post.id))

    return render_template("blog/post_form.html", form=form, page_title="Create Post")


@bp.route("/post/<int:post_id>/edit", methods=["GET", "POST"])
@login_required
def post_edit(post_id: int):
    post = Post.query.get_or_404(post_id)
    if not current_user.can_write_posts:
        flash("Only authors can edit posts.", "warning")
        return redirect(url_for("blog.post_detail", post_id=post.id))

    if post.author_id != current_user.id and not current_user.is_admin:
        abort(403)

    form = PostForm(obj=post)
    if form.validate_on_submit():
        post.title = form.title.data
        post.body = form.body.data
        db.session.commit()
        flash("Post updated.", "success")
        return redirect(url_for("blog.post_detail", post_id=post.id))

    return render_template("blog/post_form.html", form=form, page_title="Edit Post")


@bp.route("/post/<int:post_id>/delete", methods=["POST"])
@login_required
def post_delete(post_id: int):
    post = Post.query.get_or_404(post_id)
    if post.author_id != current_user.id and not current_user.is_admin:
        abort(403)

    db.session.delete(post)
    db.session.commit()
    flash("Post deleted.", "info")
    return redirect(url_for("blog.index"))


@bp.route("/post/<int:post_id>/comment", methods=["POST"])
@login_required
def post_comment(post_id: int):
    post = Post.query.get_or_404(post_id)
    if not current_user.can_comment_like:
        flash("Only users can like and comment on posts.", "warning")
        return redirect(url_for("blog.post_detail", post_id=post.id))

    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(body=form.body.data, author_id=current_user.id, post_id=post.id)
        db.session.add(comment)
        db.session.commit()
        flash("Comment added.", "success")
    else:
        flash("Comment could not be added. Please check the input.", "danger")

    return redirect(url_for("blog.post_detail", post_id=post.id))


@bp.route("/post/<int:post_id>/like", methods=["POST"])
@login_required
def post_like(post_id: int):
    post = Post.query.get_or_404(post_id)
    if not current_user.can_comment_like:
        flash("Only users can like and comment on posts.", "warning")
        return redirect(url_for("blog.post_detail", post_id=post.id))

    like = Like.query.filter_by(user_id=current_user.id, post_id=post.id).first()
    if like:
        db.session.delete(like)
        flash("Like removed.", "info")
    else:
        db.session.add(Like(user_id=current_user.id, post_id=post.id))
        flash("Post liked.", "success")

    db.session.commit()
    return redirect(url_for("blog.post_detail", post_id=post.id))
