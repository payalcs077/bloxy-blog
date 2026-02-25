# Bloxy Project

A blogging website built with:
- Flask
- Flask-Login
- CSRF protection (Flask-WTF + CSRFProtect)
- SQLite (Flask-SQLAlchemy)
- OAuth authentication (Google via Authlib)
- Bootstrap 5

## Features

- User registration and login with email/password
- Google OAuth login
- Secure sessions and CSRF protection on all forms
- Role-based access: `user`, `author`, `admin`
- Users can like and comment on posts
- Authors can create/edit/delete their own posts and can also like/comment
- Admins can change user roles, delete users, and delete any post
- Responsive Bootstrap UI

## Project Structure

```text
.
├── app/
│   ├── auth/
│   ├── blog/
│   ├── static/
│   ├── templates/
│   ├── extensions.py
│   ├── forms.py
│   └── models.py
├── instance/
├── config.py
├── run.py
└── requirements.txt
```

## Local Setup

1. Create and activate a virtual environment.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Copy environment file:
   ```bash
   cp .env.example .env
   ```
4. Initialize database:
   ```bash
   flask --app run.py init-db
   ```
   If you already had an older DB schema, reset it:
   ```bash
   flask --app run.py reset-db
   ```
5. Run server:
   ```bash
   flask --app run.py run
   ```
6. Open [http://127.0.0.1:5000](http://127.0.0.1:5000)

## Google OAuth Setup

1. Create OAuth credentials in Google Cloud Console.
2. Configure consent screen and create a Web application OAuth client.
3. Set redirect URI to:
   ```text
   http://127.0.0.1:5000/auth/authorize/google
   ```
4. Put your credentials in `.env`:
   ```env
   GOOGLE_CLIENT_ID=...
   GOOGLE_CLIENT_SECRET=...
   ```
5. Restart the app.

If OAuth variables are not configured, local email/password auth still works.

## Roles

- `user`: can like and comment on blog posts
- `author`: can create, edit, and delete their own posts, and can like/comment
- `admin`: can manage users (change roles, delete users) and delete any post

## Safer Admin Workflow

- Public registration allows only `user` and `author`.
- `admin` is assigned intentionally by an existing admin in `/admin/users`.
- For first-time bootstrap, promote a trusted existing account with CLI:
  ```bash
  flask --app run.py promote-admin --email your-email@example.com
  ```

## Notes

- SQLite file is stored in `instance/blog.db` by default.
- Change `SECRET_KEY` in production.
- This starter is a base you can extend with tags, categories, and pagination.
