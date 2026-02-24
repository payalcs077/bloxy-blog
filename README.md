# Bloxy Project

A blogging website built with:
- Flask
- Flask-Login
- CSRF protection (Flask-WTF + CSRFProtect)
- SQLite (Flask-SQLAlchemy)
- OAuth authentication (GitHub via Authlib)
- Docker + Docker Compose
- Bootstrap 5

## Features

- User registration and login with email/password
- GitHub OAuth login
- Secure sessions and CSRF protection on all forms
- Role-based access: `user`, `author`, `admin`
- Users can like and comment on posts
- Authors can create/edit/delete their own posts
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
├── requirements.txt
├── Dockerfile
└── docker-compose.yml
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

## Docker Setup

1. Copy env file:
   ```bash
   cp .env.example .env
   ```
2. Start container:
   ```bash
   docker compose up --build
   ```
3. Open [http://127.0.0.1:5000](http://127.0.0.1:5000)

## GitHub OAuth Setup

1. Create a GitHub OAuth App.
2. Set callback URL to:
   ```text
   http://127.0.0.1:5000/auth/authorize/github
   ```
   For Docker, `http://localhost:5000/auth/authorize/github` also works.
3. Put your credentials in `.env`:
   ```env
   GITHUB_CLIENT_ID=...
   GITHUB_CLIENT_SECRET=...
   ```
4. Restart the app.

If OAuth variables are not configured, local email/password auth still works.

## Roles

- `user`: can like and comment on blog posts
- `author`: can create, edit, and delete their own posts
- `admin`: can manage users (change roles, delete users) and delete any post

If you want to allow admin signups from the register form, set this in `.env`:

```env
ADMIN_REGISTRATION_TOKEN=your-secret-token
```

Admin registration requires this token.

## Notes

- SQLite file is stored in `instance/blog.db` by default.
- Change `SECRET_KEY` in production.
- This starter is a base you can extend with tags, categories, and pagination.
