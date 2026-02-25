import os
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent
INSTANCE_DIR = BASE_DIR / "instance"
load_dotenv(BASE_DIR / ".env")

def _database_uri() -> str:
    raw = os.getenv("DATABASE_URL")
    if not raw:
        db_path = INSTANCE_DIR / "blog.db"
        db_path.parent.mkdir(parents=True, exist_ok=True)
        return f"sqlite:///{db_path.as_posix()}"

    # Normalize relative SQLite paths against project root so startup directory does not matter.
    if raw.startswith("sqlite:///") and not raw.startswith("sqlite:////"):
        relative_path = raw.removeprefix("sqlite:///")
        db_path = Path(relative_path)
        if not db_path.is_absolute():
            db_path = (BASE_DIR / db_path).resolve()
        db_path.parent.mkdir(parents=True, exist_ok=True)
        return f"sqlite:///{db_path.as_posix()}"

    return raw


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-change-this-secret")
    SQLALCHEMY_DATABASE_URI = _database_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
