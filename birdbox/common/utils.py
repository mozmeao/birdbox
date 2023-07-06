# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import json
from typing import Dict, List, Tuple

from django.conf import settings
from django.core.cache import cache
from django.db.utils import OperationalError
from django.forms import Media

import requests
from sentry_sdk import capture_message
from wagtail.fields import StreamValue
from wagtail.models import Page


def get_frontend_media(page: Page) -> List[Media]:
    """For a given Page, return Media objects featuring extra JS and CSS URIs needed
    in the HTML template for that Page"""

    gathered_frontend_media = []

    # find all the streamfields
    streamfields = []
    for fieldname, value in vars(page).items():
        if not fieldname.startswith("_") and type(value) == StreamValue:
            streamfields.append(value)

    def _get_media_for_blocks(block):
        gathered_media = []
        if hasattr(block, "frontend_media"):
            gathered_media.append(block.frontend_media)

        if hasattr(block, "child_blocks"):
            for child_block in block.child_blocks:
                gathered_media += _get_media_for_blocks(child_block)
        return gathered_media

    for sf in streamfields:
        for block in sf.stream_block.child_blocks.values():
            gathered_frontend_media.extend(_get_media_for_blocks(block))

    return gathered_frontend_media


def get_freshest_newsletter_data() -> Dict:
    # If the refresh fails, we still have older records in the DB and they are
    # unlikely to change.

    key = "basket-newsletter-data"
    try:
        data = cache.get(key)
    except OperationalError:
        # During initial setup the cache table won't be available
        data = None
        pass

    if not data:
        try:
            data = requests.get(settings.BASKET_NEWSLETTER_DATA_URL).json()
        except requests.RequestException as ex:
            capture_message(f"Unable to load newsletter data from {settings.BASKET_NEWSLETTER_DATA_URL}, so loading from backup file: {ex}")
            with open(settings.FALLBACK_NEWSLETTER_DATA_PATH, "r") as fp:
                data = json.loads(fp.read())
        try:
            cache.set(key, data, timeout=settings.BASKET_NEWSLETTER_DATA_TTL_HOURS)
        except OperationalError:
            # During initial setup the cache table won't be available
            pass

    return data


def get_freshest_newsletter_options() -> Tuple[Tuple[str, str]]:
    data = get_freshest_newsletter_data()

    retval = []

    # From the newsletters key in the data, we want the ones where
    # they are active and not private
    for newsletter_id, newsletter_data in data.get("newsletters", {}).items():
        if newsletter_data.get("active") is True and newsletter_data.get("private") is False:
            choice = (newsletter_id, newsletter_data.get("title"))
            retval.append(choice)

    return tuple(sorted(retval))
