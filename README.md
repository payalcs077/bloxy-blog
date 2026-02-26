# Bloxy Project

Bloxy is a Flask blogging platform with role-based access, Google OAuth login, SQLite storage, and a cosmic purple/pink theme.

## Stack

- Flask
- Flask-Login
- Flask-WTF (CSRF)
- Flask-SQLAlchemy (SQLite)
- Authlib (Google OAuth)
- Bootstrap 5
- Gunicorn (deployment server)

## Features

- Email/password registration + login
- Google OAuth login
- Roles:
  - `user`: like + comment
  - `author`: write/edit own posts + like/comment
  - `admin`: manage roles/users + delete any post
- Admin dashboards (`/admin/users`, `/admin/posts`)
- CSRF protection
- Health endpoint: `/healthz`

## Local Run

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
flask --app run.py init-db
python run.py
```

Open: `http://127.0.0.1:5000`

## Environment Variables

```env
SECRET_KEY=replace-with-a-strong-secret
DATABASE_URL=sqlite:///instance/blog.db
GOOGLE_CLIENT_ID=...
GOOGLE_CLIENT_SECRET=...
AUTO_CREATE_DB=true
TRUST_PROXY_HEADERS=true
```

## Deploy (Recommended: Railway)

This project includes a Railway config file:

- `railway.toml`

### Steps

1. Push this repo to GitHub.
2. In Railway, click **New Project** -> **Deploy from GitHub repo**.
3. Select this repository (`payalcs077/bloxy-blog`).
4. Railway will read `railway.toml` and use the configured Gunicorn start command.
5. In service variables, add:
   - `SECRET_KEY`
   - `GOOGLE_CLIENT_ID`
   - `GOOGLE_CLIENT_SECRET`
   - `AUTO_CREATE_DB=true`
   - `TRUST_PROXY_HEADERS=true`
6. Go to **Settings -> Networking** and click **Generate Domain**.

App URL will look like:

`https://<service-name>.up.railway.app`

### Google OAuth callback for deployed app

In Google Cloud Console OAuth client, add:

`https://<service-name>.up.railway.app/auth/authorize/google`

Keep local callback too:

`http://127.0.0.1:5000/auth/authorize/google`

## Deploy (Alternative: Render)

If needed, this repo also has:

- `render.yaml`
- `Procfile`

Use the same env vars and callback pattern with your Render domain.

## Admin Workflow (Safer)

Public signup only creates `user` or `author`.

First admin bootstrap:

```bash
flask --app run.py promote-admin --email your-email@example.com
```

After that, admin can promote/restrict users from `/admin/users`.

## Notes

- SQLite is fine for college demos.
- On free hosting, SQLite storage may reset on redeploy/restart.
- For persistent data, switch to managed Postgres.
