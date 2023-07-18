# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from typing import List

from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import (
    CASCADE,
    SET_NULL,
    BooleanField,
    CharField,
    DateField,
    ForeignKey,
    Model,
    TextChoices,
)
from django.templatetags.static import static
from django.utils.html import strip_tags
from django.utils.safestring import mark_safe

from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from taggit.models import TaggedItemBase
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.blocks import RichTextBlock
from wagtail.contrib.settings.models import BaseGenericSetting, register_setting
from wagtail.fields import StreamField
from wagtail.models import LockableMixin, Page
from wagtail.snippets.models import register_snippet
from wagtailstreamforms.blocks import WagtailFormBlock

from birdbox.protocol_links import get_docs_link

from .blocks import (
    ArticleBlock,
    BiographyGridBlock,
    CaptionedImageBlock,
    CardLayoutBlock,
    ColumnBlock,
    FooterAfterMatterLinksBlock,
    FooterColumnBlock,
    FooterSocialLinksGroupBlock,
    NewsletterFormBlock,
    SplitBlock,
    VideoEmbedBlock,
)

RICHTEXT_FEATURES_BLOGPAGE = []


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
            (
                "captioned_image",
                CaptionedImageBlock(
                    required=False,
                ),
            ),
            (
                "biography_grid",
                BiographyGridBlock(
                    required=False,
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


class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey(
        "BlogPage",
        related_name="tagged_items",
        on_delete=CASCADE,
    )


class BlogPage(BaseProtocolPage):
    # title and slug come from the superclass
    standfirst = CharField(
        max_length=500,
        blank=True,
    )
    body = StreamField(
        [
            (
                "blogtext",
                RichTextBlock(
                    features=settings.RICHTEXT_FEATURES__BLOGPAGE,
                    label="Text block for blog post",
                    required=False,
                ),
            ),
            (
                "image",
                CaptionedImageBlock(
                    label="Mid-body image",
                    required=False,
                ),
            ),
            (
                "video",
                VideoEmbedBlock(
                    label="Mid-body video",
                    required=False,
                ),
            ),
        ]
    )
    date = DateField("Post date")
    authors = ParentalManyToManyField("auth.User", blank=True)
    custom_authors_text = CharField(
        max_length=150,
        blank=True,
        help_text="If set, will override any automatic author name(s) from the linked users",
    )
    header_image = ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=SET_NULL,
        related_name="+",
        help_text="Optional image at the top of the page",
    )
    header_image_alt_text = CharField(
        max_length=500,
        blank=True,
    )
    feed_image = ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=False,
        on_delete=SET_NULL,
        related_name="+",
        help_text="16:9 image to use in the blog list view",
    )
    feed_image_alt_text = CharField(
        max_length=500,
        blank=True,
    )

    is_featured = BooleanField(
        default=False,
        help_text="Only one post be featured. If multiple are selected, the newest post wins, making switchover easier",
    )

    tags = ClusterTaggableManager(
        through=BlogPageTag,
        blank=True,
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("standfirst"),
                FieldPanel("body"),
            ],
            "Content",
        ),
        MultiFieldPanel(
            [
                FieldPanel("header_image"),
                FieldPanel("header_image_alt_text"),
            ],
            "Header image",
        ),
        MultiFieldPanel(
            [
                FieldPanel("date"),
                FieldPanel("authors"),
                FieldPanel("custom_authors_text"),
            ],
        ),
    ]

    promote_panels = [
        MultiFieldPanel(
            Page.promote_panels,
        ),
        FieldPanel("is_featured"),
        MultiFieldPanel(
            [
                FieldPanel("feed_image"),
                FieldPanel("feed_image_alt_text"),
            ],
            "Feed Image",
        ),
        FieldPanel("tags"),
    ]

    # Parent page / subpage type rules
    parent_page_types = ["BlogIndexPage"]
    # subpage_types = []

    @property
    def frontend_media(self):
        "Custom property that lets us selectively include CSS"
        return forms.Media(
            css={
                "all": [
                    static("css/birdbox-blog.css"),
                ]
            },
        )

    def get_preview_text(self):
        if self.standfirst:
            return self.standfirst
        return strip_tags(self.body.render_as_block())

    def get_author_info(self):
        if author := self.custom_authors_text:
            return author
        return ",".join([author.get_full_name() for author in self.authors.all()])

    def get_feed_image_details(self):
        return {
            "image": self.feed_image,
            "alt_text": self.feed_image_alt_text,
        }


class BlogIndexPage(BaseProtocolPage):
    # No additional fields needed

    read_more_cta_label = CharField(
        max_length=50,
        default="Read more",
    )

    content_panels = Page.content_panels + [
        FieldPanel("read_more_cta_label"),
    ]

    @property
    def frontend_media(self):
        "Custom property that lets us selectively include CSS"
        return forms.Media(
            css={
                "all": [
                    static("css/birdbox-blog.css"),
                    static("css/protocol-card.css"),
                ]
            },
        )

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        # add featured post to the context:
        context["featured_post"] = self.get_specific_featured_post()

        # now paginate the rest
        non_featured_posts = self.get_non_featured_ordered_posts()
        paginator = Paginator(non_featured_posts, settings.BLOG_PAGINATION_PAGE_SIZE)
        page = request.GET.get("page")
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)

        context["non_featured_posts"] = posts
        return context

    def get_non_featured_ordered_posts(self, exclude_featured_post=True):
        posts = BlogPage.objects.child_of(self).specific().order_by("-date")
        if exclude_featured_post:
            if featured_post := self.get_specific_featured_post():
                posts = posts.exclude(id=featured_post.id)
        return posts

    def get_specific_featured_post(self) -> List[BlogPage]:
        base_qs = BlogPage.objects.child_of(self).live().order_by("-date")
        return base_qs.filter(is_featured=True).first()


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
