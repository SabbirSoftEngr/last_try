import os
from pathlib import Path
from dotenv import load_dotenv, find_dotenv
import dj_database_url

# -------------------------------------------------
# Paths & Environment
# -------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# Load .env (for local dev). Render will use Environment tab instead.
env_path = find_dotenv()
if env_path:
    load_dotenv(env_path)

# -------------------------------------------------
# Core Settings
# -------------------------------------------------
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-me")
DEBUG = os.getenv("DEBUG", "False") == "True"
ALLOWED_HOSTS = [
    h.strip() for h in os.getenv(
        "ALLOWED_HOSTS",
        "last-try-gjck.onrender.com,127.0.0.1,localhost"
    ).split(",")
]

# -------------------------------------------------
# Installed apps
# -------------------------------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "core",  # your app
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # for static files
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "bloodbank.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "bloodbank.wsgi.application"

# -------------------------------------------------
# Database (Render Postgres)
# -------------------------------------------------
DATABASES = {
    "default": dj_database_url.config(
        default="postgresql://bloodbank_rxk0_user:wiYV7gtBrGsEb65rtfZGv6EARR7Bj6vh"
                "@dpg-d2rcd2idbo4c73d4uqng-a.oregon-postgres.render.com:5432/bloodbank_rxk0",
        conn_max_age=600,
        ssl_require=True,
    )
}

# -------------------------------------------------
# Password validation
# -------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# -------------------------------------------------
# Internationalization
# -------------------------------------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Dhaka"
USE_I18N = True
USE_TZ = True

# -------------------------------------------------
# Static files
# -------------------------------------------------
STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# -------------------------------------------------
# Auth redirects
# -------------------------------------------------
LOGIN_REDIRECT_URL = "home"
LOGOUT_REDIRECT_URL = "home"

# -------------------------------------------------
# Email (via Gmail SMTP)
# -------------------------------------------------
EMAIL_BACKEND = os.getenv("EMAIL_BACKEND", "django.core.mail.backends.smtp.EmailBackend")
EMAIL_HOST = os.getenv("EMAIL_HOST", "smtp.gmail.com")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", "587"))
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS", "True") == "True"
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", "ronkemaye2@gmail.com")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", "your-gmail-app-password")
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL", "Blood Bank <ronkemaye2@gmail.com>")
