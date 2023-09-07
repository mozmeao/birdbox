# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from everett.manager import ListOf

from .base import *  # noqa
from .base import config

DEBUG = False

ALLOWED_HOSTS = config("ALLOWED_HOSTS", parser=ListOf(str))
SECRET_KEY = config("SECRET_KEY", parser=str)
