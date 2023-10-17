# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from urllib.parse import urlparse

from everett.manager import ListOf

from .base import *  # noqa
from .base import config

DEBUG = False

CSRF_TRUSTED_ORIGINS = config("CSRF_TRUSTED_ORIGINS", parser=ListOf(str))

ALLOWED_HOSTS = []
if BASE_SITE_URL:
    ALLOWED_HOSTS.append(urlparse(BASE_SITE_URL).hostname)
if WAGTAILADMIN_BASE_URL and (WAGTAILADMIN_BASE_URL != BASE_SITE_URL):
    ALLOWED_HOSTS.append(urlparse(WAGTAILADMIN_BASE_URL).hostname)

SECRET_KEY = config("SECRET_KEY", parser=str)

ENGAGE_ROBOTS = config(
    "ENGAGE_ROBOTS",
    parser=bool,
    default=str(BASE_SITE_URL in ALLOWED_HOSTS),
)
