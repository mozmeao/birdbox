# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


from django.db.models import BooleanField, CharField, TextChoices
from django.utils.safestring import mark_safe

from wagtail.admin.panels import FieldPanel
from wagtail.blocks import RichTextBlock
from wagtail.contrib.settings.models import BaseGenericSetting, register_setting
from wagtail.fields import StreamField
from wagtail.images.blocks import ImageChooserBlock
from wagtail.models import Page

from birdbox.protocol_links import get_docs_link

from .blocks import (
    CardLayoutBlock,
    FooterAfterMatterLinksBlock,
    FooterColumnBlock,
    FooterSocialLinksGroupBlock,
    SplitBlock,
)


class ProtocolLayout(TextChoices):
    DEFAULT = "mzp-l-content", "Default"
    SMALL = "mzp-l-content mzp-t-content-sm", "Small"
    MEDIUM = "mzp-l-content mzp-t-content-md", "Medium"
    LARGE = "mzp-l-content mzp-t-content-lg", "Large"
    EXTRA_LARGE = "mzp-l-content mzp-t-content-xl", "Extra Large"


class BaseProtocolPage(Page):
    """Abstract wagtail.Page subclass that features fields we want on _all_ pages,
    in order to support Protocol - e.g. layout style.

    Note that other prefs happen at a site level, such as Brand selection."""

    class Meta:
        abstract = True

    page_layout = CharField(
        choices=ProtocolLayout.choices,
        blank=True,
        max_length=64,
        help_text=mark_safe(f'Optional layout wrapper for the entire page. {get_docs_link("layout")}'),
    )
    settings_panels = Page.settings_panels + [
        FieldPanel("page_layout"),
    ]


class ProtocolTestPage(BaseProtocolPage):
    "General-purpose page was a way to test out all Protocol-compliant components and options"

    # title comes from the base Page class

    body = StreamField(
        [
            ("paragraph", RichTextBlock(required=False)),
            ("image", ImageChooserBlock(required=False)),
            # MORE TO COME: custom blocks for all the configured protocol components
            (
                "cards",
                CardLayoutBlock(
                    label="Card group",
                    required=False,
                    help_text=mark_safe(f'Layout wrapper for Cards. {get_docs_link("card-layout")}'),
                ),
            ),
            (
                "split",
                SplitBlock(
                    label="Split content",
                    required=False,
                    help_text=mark_safe(f'Split block. {get_docs_link("split")}  Not all options supported'),
                ),
            ),
        ],
        use_json_field=True,
    )

    content_panels = BaseProtocolPage.content_panels + [
        FieldPanel("body"),
    ]


@register_setting(icon="list-ul", order=1)
class Footer(BaseGenericSetting):
    # Rather than model this as a Snippet + some singleton hackery and _then_
    # have a separate Setting to decide whether to use it, we do it in one place

    display_footer = BooleanField(
        verbose_name="Display footer in this site?",
        default=True,
    )

    columns = StreamField(
        [
            ("grouped_links", FooterColumnBlock(label="Column of links")),
        ],
        block_counts={
            "grouped_links": {"max_num": 6},
        },
        blank=True,
        null=True,
        help_text="Add up to six columns of links OR five + social links",
        use_json_field=True,
    )

    social_links = StreamField(
        [
            ("socials", FooterSocialLinksGroupBlock()),
        ],
        block_counts={
            "socials": {"max_num": 1},
        },
        blank=True,
        null=True,
        help_text="Add an group of social links (optional)",
        use_json_field=True,
    )

    aftermatter = StreamField(
        [
            ("content", FooterAfterMatterLinksBlock()),
        ],
        block_counts={
            "content": {"max_num": 1},
        },
        blank=True,
        null=True,
        help_text="Add one aftermatter block; this is important for legal links etc",
        use_json_field=True,
    )

    panels = [
        FieldPanel("display_footer"),
        FieldPanel("columns"),
        FieldPanel("social_links"),
        FieldPanel("aftermatter"),
    ]

    class Meta:
        verbose_name = "Sitewide footer"
