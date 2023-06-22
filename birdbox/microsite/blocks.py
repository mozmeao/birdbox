# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

"""Custom Wagtail blocks that map to Protocol components, intended for use in a StreamField"""

from django import forms
from django.db.models import TextChoices
from django.templatetags.static import static

from wagtail import blocks as wagtail_blocks

from birdbox.protocol_links import get_docs_link
from common.blocks import AccessibleImageBlock


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


class CardLayoutOptions(TextChoices):
    CARD_LAYOUT_5_HERO = "mzp-l-card-hero", "5-Card Hero layout"
    CARD_LAYOUT_4 = "mzp-l-card-quarter", "4-Card Layout"
    CARD_LAYOUT_3 = "mzp-l-card-third", "3-Card Layout"
    CARD_LAYOUT_2 = "mzp-l-card-half", "2-Card Layout"


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
    page = wagtail_blocks.PageChooserBlock(label="Page", required=False)
    external_url = wagtail_blocks.URLBlock(label="External URL", required=False)

    class Meta:
        icon = "site"
        value_class = LinkStructValue


class CardBlock(wagtail_blocks.StructBlock):
    class Meta:
        template = "microsite/blocks/card.html"

    @property
    def frontend_media(self):
        "Custom property that lets us selectively include CSS"
        return forms.Media(css={"all": [static("css/protocol-card.css")]})

    size = wagtail_blocks.ChoiceBlock(
        choices=CardSizes.choices,
        default=CardSizes.SMALL,
        required=False,  # so that we can set SMALL, which is actually an empty string
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
    card_image = AccessibleImageBlock(required=False)
    tag = wagtail_blocks.CharBlock(
        max_length=48,
        required=False,
    )

    @property
    def has_video(self):
        # TODO: update this when we support video
        return False


class CardLayoutBlock(wagtail_blocks.StructBlock):
    class Meta:
        template = "microsite/blocks/card_layout.html"

    @property
    def frontend_media(self):
        "Custom property that lets us selectively include CSS"
        return forms.Media(css={"all": [static("css/protocol-card.css")]})

    layout = wagtail_blocks.ChoiceBlock(
        choices=CardLayoutOptions.choices,
        default=CardLayoutOptions.CARD_LAYOUT_3,
    )

    cards = wagtail_blocks.ListBlock(
        CardBlock(),
        help_text=get_docs_link("card-layout"),
    )
