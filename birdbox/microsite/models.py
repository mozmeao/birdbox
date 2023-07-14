# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


from django.core.exceptions import ValidationError
from django.db.models import BooleanField, CharField, Model, TextChoices
from django.utils.safestring import mark_safe

from wagtail.admin.panels import FieldPanel
from wagtail.blocks import RichTextBlock
from wagtail.contrib.settings.models import BaseGenericSetting, register_setting
from wagtail.fields import StreamField
from wagtail.images.blocks import ImageChooserBlock
from wagtail.models import LockableMixin, Page
from wagtail.snippets.models import register_snippet
from wagtailstreamforms.blocks import WagtailFormBlock

from birdbox.protocol_links import get_docs_link

from .blocks import (
    ArticleBlock,
    CardLayoutBlock,
    ColumnBlock,
    FooterAfterMatterLinksBlock,
    FooterColumnBlock,
    FooterSocialLinksGroupBlock,
    NewsletterFormBlock,
    SplitBlock,
    VideoEmbedBlock,
)


class ProtocolLayout(TextChoices):
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
        default=ProtocolLayout.LARGE,
        max_length=64,
        help_text=mark_safe(f'Optional layout wrapper <i>– only for components that need one</i>. {get_docs_link("layout")}'),
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
                    help_text=mark_safe(f'{get_docs_link("split")}  Not all options supported'),
                ),
            ),
            (
                "columns",
                ColumnBlock(
                    label="Column block",
                    required=False,
                    help_text=mark_safe(f'Column layout wrapper. {get_docs_link("columns")}. Has sub-components. {get_docs_link("picto")}'),
                ),
            ),
            (
                "article",
                ArticleBlock(
                    label="Article block",
                    required=False,
                    help_text=get_docs_link("article"),
                ),
            ),
            (
                "newsletter_form",
                NewsletterFormBlock(
                    label="Newsletter signup form",
                    required=False,
                ),
            ),
            (
                "custom_form",
                WagtailFormBlock(
                    required=False,
                    icon="radio-empty",
                ),
            ),
            (
                "video",
                VideoEmbedBlock(
                    required=False,
                    icon="media",
                ),
            ),
        ],
        block_counts={
            "newsletter_form": {"max_num": 1},
        },
        use_json_field=True,
        collapsed=True,
    )

    content_panels = BaseProtocolPage.content_panels + [
        FieldPanel("body"),
    ]


@register_setting(icon="list-ul", order=2)
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
        collapsed=True,
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
        collapsed=True,
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
        collapsed=True,
    )

    panels = [
        FieldPanel("display_footer"),
        FieldPanel("columns"),
        FieldPanel("social_links"),
        FieldPanel("aftermatter"),
    ]

    class Meta:
        verbose_name = "Configure Footer"


class BrandChoices(TextChoices):
    MOZORG_BRAND = "mozilla", "Mozilla.org theme"
    FIREFOX_BRAND = "firefox", "Firefox theme"


@register_setting(icon="globe", order=1)
class MicrositeSettings(BaseGenericSetting):
    site_theme = CharField(
        max_length=64,
        choices=BrandChoices.choices,
        default=BrandChoices.MOZORG_BRAND,
        help_text="Choose the design theme for this site. Changes will be immediately applied - there is no preview",
    )

    class Meta:
        verbose_name = "General site settings"


@register_snippet
class NewsletterStandardMessages(LockableMixin, Model):
    # TODO: Support L10N via wagtail-localize
    "Singleton-like snippet where we hold common messages, ready for L10N"

    form_error_email_invalid = CharField(
        blank=False,
        max_length=150,
        default="Please enter a valid email address",
    )
    form_error_select_contry = CharField(
        blank=False,
        max_length=150,
        default="Please select a country or region",
    )
    form_error_select_languge = CharField(
        blank=False,
        max_length=150,
        default="Please select a language",
    )
    form_error_newsletter_checkbox = CharField(
        blank=False,
        max_length=150,
        default="Please check at least one of the newsletter options",
    )
    form_error_privacy_policy = CharField(
        blank=False,
        max_length=150,
        default="You must agree to the privacy notice",
    )
    form_error_try_again_later = CharField(
        blank=False,
        max_length=150,
        default="We are sorry, but there was a problem with our system. Please try again later!",
    )
    form_label_your_email_address = CharField(
        blank=False,
        max_length=150,
        default="Your email address",
    )
    form_label_country = CharField(
        blank=False,
        max_length=150,
        default="Country",
    )
    form_label_language = CharField(
        blank=False,
        max_length=150,
        default="Language",
    )
    form_label_info_sought = CharField(
        verbose_name="Form label for 'I want information about:'",
        blank=False,
        max_length=150,
        default="I want information about:",
    )
    form_label_format = CharField(
        blank=False,
        max_length=150,
        default="Format",
    )
    form_label_privacy = CharField(
        blank=False,
        max_length=150,
        default='I’m okay with Mozilla handling my info as explained in <a href="https://www.mozilla.org/privacy/websites/">this Privacy Notice</a>',
    )
    form_label_submit_label = CharField(
        blank=False,
        max_length=150,
        default="Sign up now",
    )
    form_label_submit_note = CharField(
        blank=False,
        max_length=150,
        default="We will only send you Mozilla-related information.",
    )

    class Meta:
        verbose_name_plural = "Newsletter Standard Messages - only one must exist"

    def __str__(self):
        return "Newsletter Boilerplate Wording"

    def save(self, *args, **kwargs):
        _model = self.__class__
        if _model.objects.exclude(pk=self.pk).exists():
            raise ValidationError("There can be only one instance of Newsletter Standard Messages")
        return super().save(*args, **kwargs)
