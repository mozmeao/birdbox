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

from django.utils.log import DEFAULT_LOGGING

import dj_database_url
import sentry_sdk
from everett.manager import ConfigEnvFileEnv, ConfigManager, ConfigOSEnv, ListOf
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.logging import ignore_logger
from wagtail.embeds.oembed_providers import vimeo, youtube

config = ConfigManager(
    [
        ConfigOSEnv(),
        ConfigEnvFileEnv(".env"),
    ]
)

APP_NAME = config("APP_NAME", default="birdbox")
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BIRDBOX_BASE_DIR = os.path.dirname(PROJECT_DIR)
ROOT_DIR = Path(__file__).resolve().parents[3]

DEBUG = config("DEBUG", default="False", parser=bool)


def path_from_root(*args):
    return abspath(str(ROOT_DIR.joinpath(*args)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# Application definition

INSTALLED_APPS = [
    "wagtail.contrib.forms",
    "wagtail.contrib.redirects",
    "wagtail.contrib.settings",
    "wagtail.contrib.table_block",
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
    "mozilla_django_oidc",  # needs to be loaded after django.contrib.auth
    "product_details",
    "wagtailmarkdown",
    "wagtailstreamforms",  # Has to come ahead of any custom apps that might extend it
    "generic_chooser",  # Needed by wagtailstreamforms - see https://github.com/labd/wagtailstreamforms/issues/216
    "common",
    "microsite",
    "wagtailmetadata",
]

MIDDLEWARE = [
    "common.middleware.remove_vary_on_cookie_for_statics",  # Must go above SessionMiddleware so that it runs last on the response
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    # In case someone has their Auth0 revoked while logged in, revalidate it:
    "mozilla_django_oidc.middleware.SessionRefresh",
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
GS_OBJECT_PARAMETERS = {
    "cache_control": "max-age=2592000, public, immutable",
    # 2592000 == 30 days 1 month age
}


if GS_BUCKET_NAME and GS_PROJECT_ID:
    DEFAULT_FILE_STORAGE = "storages.backends.gcloud.GoogleCloudStorage"
    GS_DEFAULT_ACL = "publicRead"
    GS_FILE_OVERWRITE = False


# Password validation, if users are signing in with passwords - see OIDC setup, below, too
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

WHITENOISE_ROOT = config(
    "WHITENOISE_ROOT",
    default=path_from_root("root_files"),
)

# Default age duration for static assets without an MD5 hash in their filename.
# (Which shouldn't be accessed in production anyway)
WHITENOISE_MAX_AGE = 24 * 60 * 60  # 24 hours

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
    default="http://birdbox.mozilla.org",
)

BASE_SITE_URL = config(
    "BASE_SITE_URL",
    default=WAGTAILADMIN_BASE_URL,
)


WAGTAILEMBEDS_FINDERS = [
    # Only these two for now - others need to be confirmed to be cookie-approprite
    {
        "class": "common.embed.YouTubeNoCookieEmbedFinder",
        "providers": [
            youtube,
        ],
    },
    {
        "class": "wagtail.embeds.finders.oembed",
        "providers": [
            vimeo,
        ],
    },
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

RICHTEXT_FEATURES__LIMITED = [
    # Order here is the order used in the editor UI
    "h3",
    "h4",
    "bold",
    "italic",
    "strikethrough",
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

# Robots.txt - also see production.py for where we may allow it to be rendered

ENGAGE_ROBOTS = config("ENGAGE_ROBOTS", parser=bool, default="False")

# Customise the size of the social-sharing card image
WAGTAILMETADATA_IMAGE_FILTER = "fill-1200x630"

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
    default="False",
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
    default="300/m",
    parser=str,
)

# django-watchman
WATCHMAN_DISABLE_APM = True
WATCHMAN_CHECKS = (
    "watchman.checks.caches",
    "watchman.checks.databases",
)

# Security settings (see `manage.py check --deploy`)

SECURE_SSL_REDIRECT = config(
    "SECURE_SSL_REDIRECT",
    default="False",  # Deliberately off by default - we don't need to upgrade at the app level
    parser=bool,
)
if config("USE_SECURE_PROXY_HEADER", default="False", parser=bool):
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Only necessary if SECURE_SSL_REDIRECT is set to True at the app level, which we shouldn't
# need anyway
SECURE_REDIRECT_EXEMPT = [
    r"^healthz/$",
    r"^readiness/$",
]

CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SESSION_COOKIE_SECURE = True
X_FRAME_OPTIONS = "DENY"

# Set header Strict-Transport-Security header
SECURE_HSTS_SECONDS = config("SECURE_HSTS_SECONDS", default="0", parser=int)
# Configure via env var

# We do NOT want to roll all subdomains into the same HSTS setting
# > Only set this to True if you are certain that all subdomains of your domain should be served exclusively via SSL.
SECURE_HSTS_INCLUDE_SUBDOMAINS = False


# Custom CSRF failure view to show custom CSRF messaging
CSRF_FAILURE_VIEW = "common.views.csrf_failure"

# Authentication with Mozilla OpenID Connect / Auth0

LOGIN_ERROR_URL = "/admin/"
LOGIN_REDIRECT_URL_FAILURE = "/admin/"
LOGIN_REDIRECT_URL = "/admin/"
LOGOUT_REDIRECT_URL = "/admin/"

OIDC_RP_SIGN_ALGO = "RS256"

# How frequently do we check with the provider that the authenticated CMS user
# still exists and is authorised? It's 15 mins by default, but we're extending
# this. Why? It looks like renewal of an expired "lease" appears to give us a
# fresh CSRF token, which means pages that are edited over a period greater
# than this timeframe will fail to save because they feature the old token in
# their page and POST payload.
# So, we're going with a longer lease, with the minor trade-off that a revoked
# SSO account can still remain active within the CMS for up to an hour

OIDC_RENEW_ID_TOKEN_EXPIRY_SECONDS = config(
    "OIDC_RENEW_ID_TOKEN_EXPIRY_SECONDS",
    default="86400",  # 24 hours
    parser=int,
)

OIDC_CREATE_USER = False  # We don't want drive-by signups

OIDC_RP_CLIENT_ID = config("OIDC_RP_CLIENT_ID", default="", parser=str)
OIDC_RP_CLIENT_SECRET = config("OIDC_RP_CLIENT_SECRET", default="", parser=str)

OIDC_OP_AUTHORIZATION_ENDPOINT = "https://auth.mozilla.auth0.com/authorize"
OIDC_OP_TOKEN_ENDPOINT = "https://auth.mozilla.auth0.com/oauth/token"
OIDC_OP_USER_ENDPOINT = "https://auth.mozilla.auth0.com/userinfo"
OIDC_OP_DOMAIN = "auth.mozilla.auth0.com"
OIDC_OP_JWKS_ENDPOINT = "https://auth.mozilla.auth0.com/.well-known/jwks.json"

# If True (which should only be for local work in your .env), then show
# username and password fields when signing up, not the SSO button
USE_SSO_AUTH = config("USE_SSO_AUTH", default="True", parser=bool)

if USE_SSO_AUTH:
    AUTHENTICATION_BACKENDS = (
        # Deliberately OIDC or no entry by default
        "mozilla_django_oidc.auth.OIDCAuthenticationBackend",
    )
else:
    AUTHENTICATION_BACKENDS = (
        # Regular username + password auth
        "django.contrib.auth.backends.ModelBackend",
    )

# Note that AUTHENTICATION_BACKENDS is overridden in tests, so take care
# to check/amend those if you add additional auth backends

# Extra Wagtail config to disable password usage (SSO should be the only route)
# https://docs.wagtail.org/en/v4.2.4/reference/settings.html#wagtail-password-management-enabled
# Don't let users change or reset their password
if USE_SSO_AUTH:
    WAGTAIL_PASSWORD_MANAGEMENT_ENABLED = False
    WAGTAIL_PASSWORD_RESET_ENABLED = False

    # Don't require a password when creating a user,
    # and blank password means cannot log in unless SSO
    WAGTAILUSERS_PASSWORD_ENABLED = False

# EXTRA LOGGING
DEFAULT_LOGGING["loggers"]["mozilla_django_oidc"] = {
    "handlers": ["console"],
    "level": "INFO",
}

# Custom code in birdbox.microsite.models.BirdboxBasePage limits what page models
# can be added - allowing us to configure deployments of Birdbox to behave
# differently while still all sharing the same common codebase.
ALLOWED_PAGE_MODELS = config(
    "ALLOWED_PAGE_MODELS",
    default="__all__",
    parser=ListOf(str),
)

WAGTAILMARKDOWN = {
    "autodownload_fontawesome": False,
    "allowed_tags": [
        "p",
        "div",
        "span",
        "h2",
        "h3",
        "h4",
        "h5",
        "h6",
        "tt",
        "pre",
        "em",
        "strong",
        "ul",
        "sup",
        "li",
        "dl",
        "dd",
        "dt",
        "code",
        "img",
        "a",
        "table",
        "tr",
        "th",
        "td",
        "tbody",
        "caption",
        "colgroup",
        "thead",
        "tfoot",
        "blockquote",
        "ol",
        "hr",
        "br",
    ],
    "allowed_styles": [],  # a list of CSS attributes - nothing allowed
    "allowed_attributes": {  # optional. a dict with HTML tag as key and a list of attributes as value
        "a": [
            "href",
            "target",
            "rel",
            "title",
        ],
        "img": [
            "src",
            "alt",
            "title",
        ],
    },
    "allowed_settings_mode": "override",  # optional. Possible values: "extend" or "override". Defaults to "extend".
    "extensions": [],  # optional. a list of python-markdown supported extensions
    "extension_configs": {},  # optional. a dictionary with the extension name as key, and its configuration as value
    "extensions_settings_mode": "extend",  # optional. Possible values: "extend" or "override". Defaults to "extend".
}


# Content Security Policy settings via django-csp
# http://django-csp.readthedocs.io/en/latest/configuration.html

CSP_ENABLED = config("CSP_ENABLED", default="False", parser=bool)

_CSP_SELF_ONLY = "'self'"

if CSP_ENABLED:
    MIDDLEWARE.append("csp.middleware.CSPMiddleware")
    CSP_EXCLUDE_URL_PREFIXES = (
        # Until https://github.com/wagtail/wagtail/issues/1288 is resolved, exclude the Wagtail admin
        "/admin/",
    )

    CSP_REPORT_ONLY = config("CSP_REPORT_ONLY", default="True", parser=bool)
    CSP_REPORT_URI = config("CSP_REPORTING_ENDPOINT", default="")

    # Remember to quote 'self', 'unsafe-inline', 'unsafe-eval', or 'none'
    # e.g.: CSP_DEFAULT_SRC = "'self'" - without quotes they will not work as intended.

    CSP_DEFAULT_SRC = config("CSP_DEFAULT_SRC", default=_CSP_SELF_ONLY)

    CSP_SCRIPT_SRC = config("CSP_SCRIPT_SRC", default=_CSP_SELF_ONLY)
    CSP_STYLE_SRC = config("CSP_STYLE_SRC", default="'self' 'unsafe-inline'")

    CSP_MEDIA_SRC = config("CSP_MEDIA_SRC", default=_CSP_SELF_ONLY)

    # CSP_IMG_SRC will be set in production with details of the relevant cloud bucket
    CSP_IMG_SRC = config("CSP_IMG_SRC", default="'self' data:")
    CSP_FONT_SRC = config("CSP_FONT_SRC", default=_CSP_SELF_ONLY)

    CSP_CHILD_SRC = config("CSP_CHILD_SRC", default=_CSP_SELF_ONLY)
    CSP_FRAME_SRC = config("CSP_FRAME_SRC", default=_CSP_SELF_ONLY)
    CSP_CONNECT_SRC = config("CSP_CONNECT_SRC", default=_CSP_SELF_ONLY)

    CSP_BASE_URI = config(
        "CSP_BASE_URI",
        default="'none'",  # https://csp.withgoogle.com/docs/strict-csp.html
    )
    CSP_OBJECT_SRC = config(
        "CSP_OBJECT_SRC",
        default="'none'",  # Deny by default - https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy/object-src
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


# For Mozilla Innovations contact form ONLY. Values are set by env vars in k8s
CONTACT_FORM_RECIPIENT_EMAIL = {
    "default": config(
        "CONTACT_FORM_RECIPIENT_EMAIL__DEFAULT",
        default="",
        parser=str,
    ),
    "innovations": config(
        "CONTACT_FORM_RECIPIENT_EMAIL__INNOVATIONS",
        default="",
        parser=str,
    ),
    "mieco": config(
        "CONTACT_FORM_RECIPIENT_EMAIL__MIECO",
        default="",
        parser=str,
    ),
}
