# Bloxy Project

Bloxy is a Flask blogging platform with role-based access, Google OAuth login, SQLite storage, and a custom cosmic-themed UI.

## Tech Stack

- Flask
- Flask-Login
- Flask-WTF (CSRF)
- Flask-SQLAlchemy (SQLite)
- Authlib (Google OAuth)
- Bootstrap 5

## Current Features

- Email/password registration and login
- Google OAuth login
- Role-based access:
  - `user`: like/comment on posts
  - `author`: create/edit/delete own posts + like/comment
  - `admin`: manage users/roles + delete any post
- Post CRUD for authors/admins
- Likes and comments on posts
- Admin dashboard for user and post moderation
- CSRF protection on forms
- Cosmic purple/pink theme UI

## Project Structure

```text
.
├── app/
│   ├── admin/
│   │   └── routes.py
│   ├── auth/
│   │   └── routes.py
│   ├── blog/
│   │   └── routes.py
│   ├── static/
│   │   ├── images/
│   │   └── style.css
│   ├── templates/
│   │   ├── admin/
│   │   ├── auth/
│   │   ├── blog/
│   │   └── base.html
│   ├── extensions.py
│   ├── forms.py
│   └── models.py
├── config.py
├── requirements.txt
├── run.py
└── instance/
```

## Local Setup

1. Create and activate virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create env file:

```bash
cp .env.example .env
```

4. Initialize database:

```bash
flask --app run.py init-db
```

5. Run app:

```bash
python run.py
```

6. Open:

- [http://127.0.0.1:5000](http://127.0.0.1:5000)

## Environment Variables

Set in `.env`:

```env
SECRET_KEY=replace-with-a-strong-secret
DATABASE_URL=sqlite:///instance/blog.db
GOOGLE_CLIENT_ID=...
GOOGLE_CLIENT_SECRET=...
```

## Google OAuth Setup

1. Create OAuth credentials in Google Cloud Console.
2. Create OAuth Client ID for Web application.
3. Add this redirect URI:

```text
http://127.0.0.1:5000/auth/authorize/google
```

4. Put credentials in `.env` (`GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`).
5. Restart app.

## Admin Workflow (Safer)

Public registration does not create admins directly.

- Users can sign up as `user` or `author`
- Existing admin can promote users in `/admin/users`
- First admin bootstrap via CLI:

```bash
flask --app run.py promote-admin --email your-email@example.com
```

## Useful Commands

```bash
flask --app run.py init-db
flask --app run.py reset-db
flask --app run.py promote-admin --email your-email@example.com
```

## Notes

- SQLite file default location: `instance/blog.db`
- App runs on port `5000` from `run.py`
- This project currently has no Docker setup
