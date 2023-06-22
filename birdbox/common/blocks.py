# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from wagtail import blocks as wagtail_blocks
from wagtail.images import blocks as wagtailimages_blocks


class AccessibleImageBlock(wagtail_blocks.StructBlock):
    "Custom Image wrapper with increased a11y provision"
    image = wagtailimages_blocks.ImageChooserBlock(
        required=False,
    )
    alt_text = wagtail_blocks.CharBlock(
        label="Alt-text for this image",
        max_length=250,
        required=False,
    )
    decorative_only = wagtail_blocks.BooleanBlock(
        label="Is this image decorative only?",
        default=False,
        required=False,
    )
