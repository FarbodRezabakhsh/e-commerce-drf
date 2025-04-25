
from .base import *

DEBUG = True
ALLOWED_HOSTS = ["*"]
DATABASES["default"]["NAME"] = BASE_DIR / "db.sqlite3"
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
