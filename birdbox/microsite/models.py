# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


from django.db.models import CharField, TextChoices
from django.utils.safestring import mark_safe

from wagtail.admin.edit_handlers import FieldPanel
from wagtail.blocks import RichTextBlock
from wagtail.fields import StreamField
from wagtail.images.blocks import ImageChooserBlock
from wagtail.models import Page

from birdbox.protocol_links import get_docs_link


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
            # TO COME: custom blocks for all the protocol components
        ],
        use_json_field=True,
    )

    content_panels = BaseProtocolPage.content_panels + [
        FieldPanel("body"),
    ]
