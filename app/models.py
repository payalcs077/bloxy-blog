from datetime import UTC, datetime

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from .extensions import db, login_manager

ROLE_USER = "user"
ROLE_AUTHOR = "author"
ROLE_ADMIN = "admin"
ROLE_VALUES = (ROLE_USER, ROLE_AUTHOR, ROLE_ADMIN)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=True)
    oauth_provider = db.Column(db.String(50), nullable=True)
    oauth_sub = db.Column(db.String(255), nullable=True)
    role = db.Column(db.String(20), nullable=False, default=ROLE_USER)
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(UTC))

    posts = db.relationship("Post", back_populates="author", lazy=True, cascade="all, delete-orphan")
    comments = db.relationship("Comment", back_populates="author", lazy=True, cascade="all, delete-orphan")
    likes = db.relationship("Like", back_populates="user", lazy=True, cascade="all, delete-orphan")

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        if not self.password_hash:
            return False
        return check_password_hash(self.password_hash, password)

    @property
    def is_admin(self) -> bool:
        return self.role == ROLE_ADMIN

    @property
    def can_write_posts(self) -> bool:
        return self.role in (ROLE_AUTHOR, ROLE_ADMIN)

    @property
    def can_comment_like(self) -> bool:
        return self.role in (ROLE_USER, ROLE_ADMIN)


@login_manager.user_loader
def load_user(user_id: str):
    return db.session.get(User, int(user_id))


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140), nullable=False)
    body = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(UTC))
    updated_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC))

    author_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    author = db.relationship("User", back_populates="posts")
    comments = db.relationship("Comment", back_populates="post", lazy=True, cascade="all, delete-orphan")
    likes = db.relationship("Like", back_populates="post", lazy=True, cascade="all, delete-orphan")


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(UTC))

    author_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"), nullable=False)

    author = db.relationship("User", back_populates="comments")
    post = db.relationship("Post", back_populates="comments")


class Like(db.Model):
    __table_args__ = (db.UniqueConstraint("user_id", "post_id", name="uq_like_user_post"),)

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(UTC))

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"), nullable=False)

    user = db.relationship("User", back_populates="likes")
    post = db.relationship("Post", back_populates="likes")
