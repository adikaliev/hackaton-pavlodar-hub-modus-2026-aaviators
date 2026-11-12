"""Settings for the employee feedback system (hackathon MVP).

Everything deployment-specific comes from environment variables, which may be
put in a local `.env` file (see `.env.example`). Nothing secret is committed.
"""
import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


def _load_env_file(path: Path) -> None:
    """Minimal `.env` reader, so the project needs no extra dependency."""
    if not path.exists():
        return
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


_load_env_file(BASE_DIR / ".env")


def env_bool(name: str, default: bool) -> bool:
    return os.environ.get(name, "1" if default else "0").strip().lower() in {"1", "true", "yes", "on"}


TESTING = "test" in sys.argv[1:2]

SECRET_KEY = os.environ.get("SECRET_KEY", "dev-only-key-change-me-in-production")
DEBUG = env_bool("DEBUG", True)
ALLOWED_HOSTS = [h.strip() for h in os.environ.get("ALLOWED_HOSTS", "*").split(",") if h.strip()]
CSRF_TRUSTED_ORIGINS = [o.strip() for o in os.environ.get("CSRF_TRUSTED_ORIGINS", "").split(",") if o.strip()]

# Demo mode: role switcher instead of a login, the demo clock and the "reset data" button.
DEMO_MODE = env_bool("DEMO_MODE", True)
# Run escalation and the integration dispatcher in a background thread of the web process.
# In production run `python manage.py worker` as a separate process instead.
INLINE_WORKER = env_bool("INLINE_WORKER", True) and not TESTING
WORKER_INTERVAL_SECONDS = int(os.environ.get("WORKER_INTERVAL_SECONDS", "5"))

# Base URL used in links sent to external channels (Telegram, Bitrix24).
PUBLIC_BASE_URL = os.environ.get("PUBLIC_BASE_URL", "http://localhost:8000").rstrip("/")

# Telegram is the only real external integration. The token lives only in `.env`.
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_BOT_USERNAME = os.environ.get("TELEGRAM_BOT_USERNAME", "")

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "feedback",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "feedback.middleware.CurrentEmployeeMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "feedback.context.shell",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# Runtime data (database, uploads) lives in storage/, which is git-ignored.
STORAGE_DIR = Path(os.environ.get("STORAGE_DIR", BASE_DIR / "storage"))
STORAGE_DIR.mkdir(parents=True, exist_ok=True)

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": STORAGE_DIR / "demo.sqlite3",
        "OPTIONS": {
            "timeout": 20,
            "transaction_mode": "IMMEDIATE",
            "init_command": "PRAGMA journal_mode=WAL; PRAGMA synchronous=NORMAL;",
        },
    }
}
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Country settings (solution design, section 8): language, time zone and the
# working-day calendar are configuration, not code. The calendar itself is in
# the database (admin -> "Календарь") and is seeded from data/calendar_kz.json.
LANGUAGE_CODE = os.environ.get("APP_LANGUAGE", "ru")
TIME_ZONE = os.environ.get("APP_TIME_ZONE", "Asia/Almaty")  # UTC+5
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATIC_ROOT = STORAGE_DIR / "staticfiles"
STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
}
WHITENOISE_USE_FINDERS = True  # serve app static files without a collectstatic step

MEDIA_URL = "uploads/"
MEDIA_ROOT = STORAGE_DIR / "uploads"

# Attachment limits (solution design, section 8).
ATTACHMENT_MAX_BYTES = 10 * 1024 * 1024
ATTACHMENT_ALLOWED_EXTENSIONS = {
    "png", "jpg", "jpeg", "gif", "webp", "pdf", "txt", "csv", "doc", "docx", "xls", "xlsx",
}
DATA_UPLOAD_MAX_MEMORY_SIZE = 12 * 1024 * 1024

SEED_DIR = BASE_DIR / "data"

SESSION_COOKIE_AGE = 60 * 60 * 24 * 14
MESSAGE_STORAGE = "django.contrib.messages.storage.session.SessionStorage"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "root": {"handlers": ["console"], "level": "WARNING"},
    "loggers": {"feedback": {"handlers": ["console"], "level": "INFO", "propagate": False}},
}
