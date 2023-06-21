# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

"""Custom Wagtail blocks that map to Protocol components, intended for use in a StreamField"""

from django.db.models import TextChoices

from wagtail import blocks as wagtail_blocks
from wagtail.images import blocks as wagtailimages_blocks


class AspectRatios(TextChoices):
    ASPECT_1_1 = "mzp-has-aspect-1-1", "1:1"
    ASPECT_3_2 = "mzp-has-aspect-3-2", "3:2"
    ASPECT_16_9 = "mzp-has-aspect-16-9", "16:9"


class CardSizes(TextChoices):
    EXTRA_SMALL = "mzp-c-card-extra-small", "Extra small"
    SMALL = "", "Small"
    MEDIUM = "mzp-c-card-extra-medium", "Medium"
    LARGE = "mzp-c-card-large", "Large"
    EXTRA_LARGE = "mzp-c-card-extra-large", "Extra Large"


class LinkStructValue(wagtail_blocks.StructValue):
    def url(self):
        external_url = self.get("external_url")
        page = self.get("page")
        if external_url:
            return external_url
        elif page:
            return page.url


class LinkBlock(wagtail_blocks.StructBlock):
    "Block that allows linking to ether a Wagtail Page or an external URL"
    page = wagtail_blocks.PageChooserBlock(label="page", required=False)
    external_url = wagtail_blocks.URLBlock(label="external URL", required=False)

    class Meta:
        icon = "site"
        value_class = LinkStructValue


class CardBlock(wagtail_blocks.StructBlock):
    template = "microsite/blocks.card.html"

    size = wagtail_blocks.ChoiceBlock(
        choices=CardSizes.choices,
        default=CardSizes.SMALL,
    )
    title = wagtail_blocks.CharBlock(
        required=True,
        max_length=60,
        help_text="Card title with about 30-40 characters",
    )
    description = wagtail_blocks.TextBlock(
        required=True,
        max_length=170,
        help_text="A description of about 150 characters. Usually we only have room for one or two sentences.",
    )
    cta = wagtail_blocks.CharBlock(
        required=False,
        max_length=60,
        help_text="Call to action with about 30-40 characters",
    )
    meta_info = wagtail_blocks.CharBlock(
        required=False,
        max_length=60,
        help_text="Meta info at the base of the card",
    )
    link = LinkBlock()
    image_aspect_ratio = wagtail_blocks.ChoiceBlock(
        choices=AspectRatios.choices,
        default=AspectRatios.ASPECT_3_2,
    )
    image = wagtailimages_blocks.ImageChooserBlock(
        required=False,
    )
    tags = wagtail_blocks.ListBlock(
        wagtail_blocks.CharBlock(label="tag"),
    )

    @property
    def has_video(self):
        # TODO: update this when we support video
        return False


class CardLayout(wagtail_blocks.StructBlock):
    assert False, "WRITE ME"
