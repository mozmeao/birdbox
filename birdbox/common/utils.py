# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from typing import List

from django.forms import Media

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
