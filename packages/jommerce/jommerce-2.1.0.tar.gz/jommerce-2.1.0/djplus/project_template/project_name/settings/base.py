from os import environ as SECRETS # noqa
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent


# General
# ----------------------------------------------------------------------------------------------------------------------
SECRET_KEY = SECRETS.get("DJANGO_SECRET_KEY")
DEBUG = True
ALLOWED_HOSTS = SECRETS.get("DJANGO_ALLOWED_HOSTS", "").split()
ROOT_URLCONF = '{{project_name}}.urls'
WSGI_APPLICATION = '{{project_name}}.wsgi.application'


# Apps
# ----------------------------------------------------------------------------------------------------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]


# Middleware
# ----------------------------------------------------------------------------------------------------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# Templates
# ----------------------------------------------------------------------------------------------------------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


# Databases
# ----------------------------------------------------------------------------------------------------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'


# Authentication
# ----------------------------------------------------------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

PASSWORD_HASHERS = [{% if argon2 %}
    "django.contrib.auth.hashers.Argon2PasswordHasher",
{% elif bcrypt %}
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
{% else %}
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
{% endif %}]

# Internationalization
# ----------------------------------------------------------------------------------------------------------------------
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static and Media files
# ----------------------------------------------------------------------------------------------------------------------
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [
    BASE_DIR / "static",
]
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"
