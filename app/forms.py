from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, SelectField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional, Regexp

from .models import ROLE_ADMIN, ROLE_AUTHOR, ROLE_USER


class RegistrationForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[
            DataRequired(),
            Length(min=3, max=30),
            Regexp(r"^[A-Za-z0-9_.-]+$", message="Use letters, numbers, dots, underscores, and dashes."),
        ],
    )
    email = StringField("Email", validators=[DataRequired(), Email(), Length(max=255)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8, max=128)])
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[DataRequired(), EqualTo("password", message="Passwords must match.")],
    )
    role = SelectField(
        "Role",
        validators=[DataRequired()],
        choices=[
            (ROLE_USER, "User (like/comment only)"),
            (ROLE_AUTHOR, "Author (write posts)"),
            (ROLE_ADMIN, "Admin (full control)"),
        ],
        default=ROLE_USER,
    )
    admin_token = PasswordField("Admin Registration Token", validators=[Optional(), Length(max=255)])
    submit = SubmitField("Create Account")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email(), Length(max=255)])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember me")
    submit = SubmitField("Sign In")


class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(min=3, max=140)])
    body = TextAreaField("Content", validators=[DataRequired(), Length(min=10)])
    submit = SubmitField("Save")


class CommentForm(FlaskForm):
    body = TextAreaField("Comment", validators=[DataRequired(), Length(min=2, max=1000)])
    submit = SubmitField("Add Comment")
