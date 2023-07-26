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
from django.shortcuts import redirect
from django.templatetags.static import static
from django.utils.html import strip_tags
from django.utils.safestring import mark_safe

from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from taggit.models import TaggedItemBase
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.blocks import RichTextBlock
from wagtail.contrib.settings.models import BaseGenericSetting, register_setting
from wagtail.fields import RichTextField, StreamField
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
    CompactCalloutBlock,
    ExpandingDetailsBlock,
    FooterAfterMatterLinksBlock,
    FooterColumnBlock,
    FooterSocialLinksGroupBlock,
    HeroBlock,
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
    menu_icon = ForeignKey(
        "wagtailimages.Image",
        blank=True,
        null=True,
        on_delete=SET_NULL,
        related_name="+",
        help_text="Icon to accompany an entry in the navigation menu. Optional.",
    )
    menu_description = CharField(
        blank=True,
        max_length=200,
        help_text="Text to accompany an entry in the navigation menu. Optional.",
    )

    settings_panels = Page.settings_panels + [
        FieldPanel("page_layout"),
        MultiFieldPanel(
            [
                FieldPanel("show_in_menus"),  # From base page. TODO: avoid duplication
                FieldPanel("menu_icon"),
                FieldPanel("menu_description"),
            ],
            "Menu options",
        ),
    ]

    # Crudely drop the show_in_menus section. TODO: make this more elegant and less brittle
    promote_panels = Page.promote_panels[:-1]

    def has_menu_icon(self):
        return bool(self.menu_icon)

    def get_children_for_nav(self):
        "Only return children that may be shown in a nav menu"
        return self.get_children().specific().filter(show_in_menus=True)


class StructuralPage(BaseProtocolPage):
    """A page used to create structure within a page tree, akin to a 'folder' under/in which other pages live.
    Not directly viewable - will redirect to its parent page if called"""

    # Minimal fields on this model - only exactly what we need
    # `title` and `slug` fields come from BaseProtocolPage->Page

    is_structural_page = True

    # TO COME: guard rails on page heirarchy
    # subpage_types = []

    settings_panels = Page.settings_panels + [
        FieldPanel("show_in_menus"),
    ]
    promote_panels = []

    def serve_preview(self, request, mode_name="irrelevant"):
        # Regardless of mode_name, always redirect to the parent page
        return redirect(self.get_parent().get_full_url())

    def serve(self, request):
        return redirect(self.get_parent().get_full_url())


class GeneralPurposePage(BaseProtocolPage):
    """General-purpose page with most of the components available in it."""

    # title comes from the base Page class
    content = StreamField(
        [
            (
                "hero",
                HeroBlock(
                    required=False,
                    label_format="Hero: {main_heading}",
                    help_text="Not the core Protocol component",
                ),
            ),
            (
                "split",
                SplitBlock(
                    label="Split content",
                    label_format="Split: {title}",
                    required=False,
                    help_text=mark_safe(f'{get_docs_link("split")}  Not all options supported'),
                ),
            ),
            (
                "cards",
                CardLayoutBlock(
                    label="Card group",
                    label_format="Card group",  # Can't add more detials to this 'collapsed'-mode label
                    required=False,
                    help_text=mark_safe(f'Layout wrapper for Cards. {get_docs_link("card-layout")}'),
                ),
            ),
            (
                "columns",
                ColumnBlock(
                    label="Column block",
                    label_format="Column block: {column_layout}",
                    required=False,
                    help_text=mark_safe(f'Column layout wrapper. {get_docs_link("columns")}. Has sub-components. {get_docs_link("picto")}'),
                ),
            ),
            (
                "newsletter_form",
                NewsletterFormBlock(
                    label="Newsletter signup form",
                    label_format="Newsletter: {title}",
                    required=False,
                ),
            ),
            (
                "custom_form",
                WagtailFormBlock(
                    label_format="Custom form",
                    required=False,
                    icon="radio-empty",
                ),
            ),
            (
                "video",
                VideoEmbedBlock(
                    label="Video embed",
                    label_format="Video embed: {video}",
                    required=False,
                    icon="media",
                ),
            ),
            (
                "captioned_image",
                CaptionedImageBlock(
                    label_format="Captioned image: {image_caption}",
                    required=False,
                ),
            ),
            (
                "biography_grid",
                BiographyGridBlock(
                    label_format="Biography grid: {title}",
                    required=False,
                ),
            ),
            (
                "compact_callout",
                CompactCalloutBlock(
                    required=False,
                    label_format="Compact callout: {headline}",
                    help_text=get_docs_link("compact-callout"),
                ),
            ),
        ],
        block_counts={
            "hero": {"max_num": 1},
            "newsletter_form": {"max_num": 1},
        },
        use_json_field=True,
        collapsed=True,
    )

    content_panels = BaseProtocolPage.content_panels + [
        FieldPanel("content"),
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        title_field = self._meta.get_field("title")

        title_field.help_text = (
            "The page title as you'd like it to be seen by the public. "
            "(However, this will not be displayed in the page if a block is "
            "added that has its own H1-level heading field, such as a Hero)"
        )


class FAQPage(BaseProtocolPage):
    """FAQ-focused page which leans heavily on the DetailsExpanderBlock."""

    # title comes from the base Page class
    introduction = RichTextField(
        features=settings.RICHTEXT_FEATURES__ARTICLE,
        blank=True,
        help_text="Optional intro for the page",
    )

    content = StreamField(
        [
            (
                "details",
                ExpandingDetailsBlock(
                    required=False,
                    label_format="Expandable details: {preamble}",
                    help_text=get_docs_link("details"),
                ),
            ),
        ],
        blank=True,
        use_json_field=True,
    )

    content_panels = BaseProtocolPage.content_panels + [
        FieldPanel("introduction"),
        FieldPanel("content"),
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        title_field = self._meta.get_field("title")

        title_field.help_text = (
            "The page title as you'd like it to be seen by the public. "
            "(However, this will not be displayed in the page if a block is "
            "added that has its own H1-level heading field, such the Article)"
        )


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
        verbose_name="Featured Post CTA button label",
        max_length=50,
        default="Read more",
        help_text="Only shown if you mark a post as featured",
    )

    content_panels = Page.content_panels + [
        FieldPanel("read_more_cta_label"),
    ]

    subpage_types = [
        BlogPage,
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
        collapsed=False,
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
        collapsed=False,
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
        collapsed=False,
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

    navigation_enabled = BooleanField(
        default=True,
        verbose_name="Show nav bar on site?",
    )
    navigation_generate_nav_from_page_tree = BooleanField(
        default=True,
        help_text="Note that this will only go two levels deep",
        verbose_name="Automatically generate nav from page heirarchy?",
    )
    navigation_show_cta_button = BooleanField(
        default=False,
        help_text="HIDDEN ON MOBILE VIEWPORT. Button requires label and URL, below, to be set. ",
        verbose_name="Show CTA button in top nav?",
    )
    navigation_cta_button_label = CharField(
        max_length=100,
        verbose_name="CTA button label",
        blank=True,
    )
    navigation_cta_button_url = CharField(
        max_length=500,
        verbose_name="CTA button URL",
        blank=True,
    )

    panels = [
        FieldPanel("site_theme"),
        MultiFieldPanel(
            [
                FieldPanel("navigation_enabled"),
                FieldPanel("navigation_generate_nav_from_page_tree"),
                MultiFieldPanel(
                    [
                        FieldPanel("navigation_show_cta_button"),
                        FieldPanel("navigation_cta_button_label"),
                        FieldPanel("navigation_cta_button_url"),
                    ],
                    "CTA button",
                ),
            ],
            "Site Navigation config",
        ),
    ]

    class Meta:
        verbose_name = "Site settings"


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


class ProtocolTestPage(BaseProtocolPage):
    """DEVELOPMNENT ONLY. General-purpose page was a way to test out all
    Protocol-compliant components and options

    DO NOT USE IN PRODUCTION
    """

    # title comes from the base Page class

    body = StreamField(
        [
            # MORE TO COME: custom blocks for all the configured protocol components
            (
                "cards",
                CardLayoutBlock(
                    label="Card group",
                    label_format="Card group",  # Can't add more detials to this 'collapsed'-mode label
                    required=False,
                    help_text=mark_safe(f'Layout wrapper for Cards. {get_docs_link("card-layout")}'),
                ),
            ),
            (
                "split",
                SplitBlock(
                    label="Split content",
                    label_format="Split: {title}",
                    required=False,
                    help_text=mark_safe(f'{get_docs_link("split")}  Not all options supported'),
                ),
            ),
            (
                "columns",
                ColumnBlock(
                    label="Column block",
                    label_format="Column block: {column_layout}",
                    required=False,
                    help_text=mark_safe(f'Column layout wrapper. {get_docs_link("columns")}. Has sub-components. {get_docs_link("picto")}'),
                ),
            ),
            (
                "article",
                ArticleBlock(
                    label="Article block",
                    label_format="Article: {header}",
                    required=False,
                    help_text=get_docs_link("article"),
                ),
            ),
            (
                "newsletter_form",
                NewsletterFormBlock(
                    label="Newsletter signup form",
                    label_format="Newsletter: {title}",
                    required=False,
                ),
            ),
            (
                "custom_form",
                WagtailFormBlock(
                    label_format="Custom form",
                    required=False,
                    icon="radio-empty",
                ),
            ),
            (
                "video",
                VideoEmbedBlock(
                    label="Video embed",
                    label_format="Video embed: {video}",
                    required=False,
                    icon="media",
                ),
            ),
            (
                "captioned_image",
                CaptionedImageBlock(
                    label_format="Captioned image: {image_caption}",
                    required=False,
                ),
            ),
            (
                "biography_grid",
                BiographyGridBlock(
                    label_format="Biography grid: {title}",
                    required=False,
                ),
            ),
            (
                "compact_callout",
                CompactCalloutBlock(
                    required=False,
                    label_format="Compact callout: {headline}",
                    help_text=get_docs_link("compact-callout"),
                ),
            ),
            (
                "hero",
                HeroBlock(
                    required=False,
                    label_format="Hero: {main_heading}",
                    help_text="Not the core Protocol component",
                ),
            ),
            (
                "details",
                ExpandingDetailsBlock(
                    required=False,
                    label_format="Expandable details: {preamble}",
                    help_text=get_docs_link("details"),
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
