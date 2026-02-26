# Bloxy

This is my Flask blogging website project for college.

## What it has

- Login/register with email-password
- Google OAuth login
- Roles: `user`, `author`, `admin`
- Authors can create posts
- Users/authors can like and comment
- Admin can manage users and posts

## Tech used

- Flask
- Flask-Login
- Flask-WTF (CSRF)
- Flask-SQLAlchemy (SQLite)
- Authlib (Google OAuth)
- Bootstrap

## Run locally

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
flask --app run.py init-db
python run.py
```

Open: `http://127.0.0.1:5000`

## Required env vars

```env
SECRET_KEY=change-this
DATABASE_URL=sqlite:///instance/blog.db
GOOGLE_CLIENT_ID=your-client-id
GOOGLE_CLIENT_SECRET=your-client-secret
AUTO_CREATE_DB=true
TRUST_PROXY_HEADERS=true
```

## Railway deploy

1. Push code to GitHub.
2. In Railway, deploy from this GitHub repo.
3. Add env vars in Railway.
4. Generate public domain.

Health check:

`https://your-domain.up.railway.app/healthz`

## Google OAuth redirect URIs

- Local: `http://127.0.0.1:5000/auth/authorize/google`
- Railway: `https://your-domain.up.railway.app/auth/authorize/google`

## First admin setup

```bash
flask --app run.py promote-admin --email your-email@example.com
```
