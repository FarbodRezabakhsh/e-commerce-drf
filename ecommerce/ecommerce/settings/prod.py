
from .base import *
import environ

env = environ.Env()
environ.Env.read_env(BASE_DIR / ".env")   # load variables from .env file

DATABASES["default"] = {
    "ENGINE": "django.db.backends.postgresql",
    "NAME": env("POSTGRES_DB"),
    "USER": env("POSTGRES_USER"),
    "PASSWORD": env("POSTGRES_PASSWORD"),
    "HOST": env("POSTGRES_HOST"),
    "PORT": env("POSTGRES_PORT", default="5432"),
}

SECRET_KEY = env("DJANGO_SECRET_KEY")
