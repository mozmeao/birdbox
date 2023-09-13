# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

"""
Django settings for birdbox project.
"""

# Build paths inside the project like this: os.path.join(BIRDBOX_BASE_DIR, ...)
import os
import sys
from os.path import abspath
from pathlib import Path

import dj_database_url
import sentry_sdk
from everett.manager import ConfigManager
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.logging import ignore_logger
from wagtail.embeds.oembed_providers import vimeo, youtube

try:
    from dotenv import load_dotenv

    load_dotenv()  # take environment variables from .env.
except ImportError:
    # dotenv is not available - e.g. in production mode
    pass

config = ConfigManager.basic_config()

APP_NAME = "birdbox"
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BIRDBOX_BASE_DIR = os.path.dirname(PROJECT_DIR)
ROOT_DIR = Path(__file__).resolve().parents[3]


def path_from_root(*args):
    return abspath(str(ROOT_DIR.joinpath(*args)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# Application definition

INSTALLED_APPS = [
    "wagtail.contrib.forms",
    "wagtail.contrib.redirects",
    "wagtail.contrib.settings",
    "wagtail.contrib.modeladmin",
    "wagtail.embeds",
    "wagtail.sites",
    "wagtail.users",
    "wagtail.snippets",
    "wagtail.documents",
    "wagtail.images",
    "wagtail.search",
    "wagtail.admin",
    "wagtail",
    "modelcluster",
    "search",
    "taggit",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "product_details",
    "wagtailstreamforms",  # Has to come ahead of any custom apps that might extend it
    "generic_chooser",  # Needed by wagtailstreamforms - see https://github.com/labd/wagtailstreamforms/issues/216
    "common",
    "microsite",
]

MIDDLEWARE = [
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    # set_remote_addr_from_forwarded_for must come before rate_limiter
    "common.middleware.set_remote_addr_from_forwarded_for",
    "common.middleware.rate_limiter",
    "django_ratelimit.middleware.RatelimitMiddleware",
    "wagtail.contrib.redirects.middleware.RedirectMiddleware",
]

ROOT_URLCONF = "birdbox.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(PROJECT_DIR, "templates"),
            os.path.join(PROJECT_DIR, "common", "templates"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "wagtail.contrib.settings.context_processors.settings",
                "microsite.context_processors.google_tag",
            ],
        },
    },
]

# WSGI_APPLICATION doesn't need to be defined here

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    "default": config(
        "DATABASE_URL",
        default=f"sqlite:////{os.path.join(BIRDBOX_BASE_DIR, 'data', 'birdbox.sqlite3')}",
        parser=dj_database_url.parse,
    )
}
DEFAULT_AUTO_FIELD = "django.db.models.AutoField"  # No need for BigIntAutoField

# Cacheing

if REDIS_URL := config("REDIS_URL", default="", parser=str):
    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": REDIS_URL,
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
            },
        }
    }
else:
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.db.DatabaseCache",
            "LOCATION": "birdbox_cache",
        }
    }

# Storage
# If config is available, we use Google Cloud Storage, else (for local dev)
# fall back to filesytem storage

GS_BUCKET_NAME = config("GS_BUCKET_NAME", default="", parser=str)
GS_PROJECT_ID = config("GS_PROJECT_ID", default="", parser=str)

if GS_BUCKET_NAME and GS_PROJECT_ID:
    DEFAULT_FILE_STORAGE = "storages.backends.gcloud.GoogleCloudStorage"
    GS_DEFAULT_ACL = "publicRead"
    GS_FILE_OVERWRITE = True

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Email
EMAIL_HOST = config("EMAIL_HOST", default="localhost")
EMAIL_PORT = config("EMAIL_PORT", default="25", parser=int)
EMAIL_HOST_USER = config("EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD", default="")
EMAIL_USE_TLS = config("EMAIL_USE_TLS", default="false", parser=bool)
EMAIL_SUBJECT_PREFIX = config("EMAIL_SUBJECT_PREFIX", default="")

DEFAULT_FROM_EMAIL = config(
    "DEFAULT_FROM_EMAIL",
    default="mozilla.com <noreply@mozilla.com>",
)

if EMAIL_HOST_USER and EMAIL_HOST_PASSWORD:
    default_email_backend = "django.core.mail.backends.smtp.EmailBackend"
else:
    default_email_backend = "django.core.mail.backends.console.EmailBackend"


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

STATICFILES_DIRS = [
    os.path.join(PROJECT_DIR, "static"),
]

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

STATIC_ROOT = os.path.join(BIRDBOX_BASE_DIR, "static_collected")
STATIC_URL = "/static/"

MEDIA_ROOT = os.path.join(BIRDBOX_BASE_DIR, "media")
MEDIA_URL = "/media/"


def set_whitenoise_headers(headers, path, url):
    if "/fonts/" in url:
        headers["Cache-Control"] = "public, max-age=604800"  # one week


WHITENOISE_ADD_HEADERS_FUNCTION = set_whitenoise_headers
WHITENOISE_ROOT = config(
    "WHITENOISE_ROOT",
    default=path_from_root("root_files"),
)
WHITENOISE_MAX_AGE = 6 * 60 * 60  # 6 hours

# Wagtail settings

WAGTAIL_SITE_NAME = "birdbox"

# We're sticking to LTS releases of Wagtail, so we don't want to be told there's a new version if that's not LTS
WAGTAIL_ENABLE_UPDATE_CHECK = False

# Search
# https://docs.wagtail.org/en/stable/topics/search/backends.html
WAGTAILSEARCH_BACKENDS = {
    "default": {
        "BACKEND": "wagtail.search.backends.database",
    }
}

# Base URL to use when referring to full URLs within the Wagtail admin backend -
# e.g. in notification emails. Don't include '/admin' or a trailing slash
WAGTAILADMIN_BASE_URL = config(
    "WAGTAILADMIN_BASE_URL",
    default="http://birdbox.mozilla.com",
)

WAGTAILEMBEDS_FINDERS = [
    {
        "class": "wagtail.embeds.finders.oembed",
        "providers": [
            # Only these two
            youtube,
            vimeo,
        ],
    }
]

WAGTAILIMAGES_EXTENSIONS = [
    "gif",
    "jpg",
    "jpeg",
    "png",
    "webp",
    "svg",
]

# https://docs.wagtail.org/en/stable/advanced_topics/customisation/page_editing_interface.html#limiting-features-in-a-rich-text-field
RICHTEXT_FEATURES__FULL = [
    # Order here is the order used in the editor UI
    "h2",
    "h3",
    "bold",
    "italic",
    "strikethrough",
    "code",
    "blockquote",
    "link",
    "ol",
    "ul",
]

RICHTEXT_FEATURES__SIMPLE = [
    "bold",
    "italic",
    "strikethrough",
    "link",
    "ol",
    "ul",
]

RICHTEXT_FEATURES__ARTICLE = RICHTEXT_FEATURES__FULL
RICHTEXT_FEATURES__BLOGPAGE = RICHTEXT_FEATURES__FULL
RICHTEXT_FEATURES__BIO = RICHTEXT_FEATURES__SIMPLE
RICHTEXT_FEATURES__DETAIL = RICHTEXT_FEATURES__SIMPLE

# Logging

LOG_LEVEL = config("LOG_LEVEL", default="INFO")

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "root": {
        "level": LOG_LEVEL,
        "handlers": ["console"],
    },
    "formatters": {
        "verbose": {"format": "%(levelname)s %(asctime)s %(module)s %(message)s"},
    },
    "handlers": {
        "null": {
            "class": "logging.NullHandler",
        },
        "console": {
            "class": "logging.StreamHandler",
            "stream": sys.stdout,
            "formatter": "verbose",
        },
    },
    "loggers": {
        "django.db.backends": {
            "level": "ERROR",
            "handlers": ["console"],
            "propagate": False,
        },
    },
}

# DisallowedHost gets a lot of action thanks to scans/bots/scripts,
# but we need not take any action because it's already HTTP 400-ed.
# Note that we ignore at the Sentry client level
ignore_logger("django.security.DisallowedHost")

# Sentry
SENTRY_DSN = config("SENTRY_DSN", default="")

if SENTRY_DSN:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        release=config("GIT_SHA", default=""),
        server_name=".".join(x for x in ["birdbox", APP_NAME] if x),
        integrations=[DjangoIntegration()],
    )

# Rate limiting using django-ratelimit

RATELIMIT_ENABLE = config(
    "RATELIMIT_ENABLE",
    default="True",
    parser=bool,
)
RATELIMIT_USE_CACHE = config(
    "RATELIMIT_USE_CACHE",
    default="default",
    parser=str,
)
RATELIMIT_VIEW = "common.views.rate_limited"
RATELIMIT_DEFAULT_LIMIT = config(
    "RATELIMIT_DEFAULT_LIMIT",
    default="25/m",
    parser=str,
)


# Mozillaverse settings

BASKET_SUBSCRIPTION_URL = config(
    "BASKET_SUBSCRIPTION_URL",
    default="https://basket.mozilla.org/news/subscribe/",
)

BASKET_NEWSLETTER_DATA_URL = config(
    "BASKET_NEWSLETTER_DATA_URL",
    default="https://www.mozilla.org/newsletter/newsletter-all.json",  # Updated regularly by Bedrock
)

BASKET_NEWSLETTER_DATA_TTL_HOURS = config(
    "BASKET_NEWSLETTER_DATA_TTL",
    default="24",
    parser=int,
)

# Set this to False in your .env to disable the pull-down of latest data
# (e.g. if working offline or running tests that don't need it)
BASKET_NEWSLETTER_DATA_DO_SYNC = config(
    "BASKET_NEWSLETTER_DATA_DO_SYNC",
    default="True",
    parser=bool,
)

FALLBACK_NEWSLETTER_DATA_PATH = f"{BIRDBOX_BASE_DIR}/data/basket/basket.mozilla.org.json"

BLOG_PAGINATION_PAGE_SIZE = config(
    "BLOG_PAGINATION_PAGE_SIZE",
    default="6",
    parser=int,
)

# For analytics
GOOGLE_TAG_ID = config("GOOGLE_TAG_ID", default="", parser=str)


# For Mozilla Innovations contact form ONLY
CONTACT_FORM_RECIPIENT_EMAIL = {
    "default": config(
        "CONTACT_FORM_RECIPIENT_EMAIL__DEFAULT",
        default="",
        parser=str,
    ),
    "innovations": config(
        "CONTACT_FORM_RECIPIENT_EMAIL__INNOVATIONS",
        default="innovations@mozilla.com",
        parser=str,
    ),
    "meico": config(
        "CONTACT_FORM_RECIPIENT_EMAIL__MEICO",
        default="meico@mozilla.com",
        parser=str,
    ),
}
