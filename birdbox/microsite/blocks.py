# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


"""Custom Wagtail blocks that map to Protocol components, intended for use in a StreamField"""

from django import forms
from django.conf import settings
from django.db.models import TextChoices
from django.templatetags.static import static
from django.utils.module_loading import import_string
from django.utils.safestring import mark_safe

from wagtail import blocks as wagtail_blocks
from wagtail.contrib.table_block.blocks import TableBlock
from wagtail.embeds.blocks import EmbedBlock
from wagtail.images.blocks import ImageChooserBlock

from birdbox.protocol_links import get_docs_link
from common.blocks import AccessibleImageBlock, AccessibleImageBlockBase, ThemedColorBlock
from common.utils import get_freshest_newsletter_options
from microsite.forms import CONTACT_FORM_CHOICES


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


class SplitBlockVariants(TextChoices):
    SPLIT_BLOCK_STANDARD = "", "Standard"
    SPLIT_BLOCK_REVERSED = "mzp-l-split-reversed", "Reversed"
    SPLIT_BLOCK_NARROW_BODY = "mzp-l-split-body-narrow", "Narrow body"
    SPLIT_BLOCK_NARROW_BODY_REVERSED = "mzp-l-split-body-narrow mzp-l-split-reversed", "Narrow body, reversed"
    SPLIT_BLOCK_WIDE_BODY = "mzp-l-split-body-wide", "Wide body"
    SPLIT_BLOCK_WIDE_BODY_REVERSED = "mzp-l-split-body-wide mzp-l-split-reversed", "Wide body, reversed"
    SPLIT_BLOCK_DARK_BACKGROUND = "mzp-t-dark mzp-t-background-secondary", "Dark Background"


class SplitBlockSizes(TextChoices):
    SPLIT_BLOCK_SIZE_MEDIUM = "mzp-t-content-md", "Medium"
    SPLIT_BLOCK_SIZE_LARGE = "mzp-t-content-lg", "Large"
    SPLIT_BLOCK_SIZE_EXTRA_LARGE = "mzp-t-content-xl", "Extra-large"


class LayoutSizes(TextChoices):
    LAYOUT_SIZE_NONE = "", "N/A"
    LAYOUT_SIZE_MEDIUM = "mzp-t-content-md", "Medium"
    LAYOUT_SIZE_LARGE = "mzp-t-content-lg", "Large"
    LAYOUT_SIZE_EXTRA_LARGE = "mzp-t-content-xl", "Extra-large"


class PictoLayoutOptions(TextChoices):
    PICTO_LAYOUT_STANDARD = "", "Standard"
    PICTO_LAYOUT_CENTERED = "mzp-t-picto-center", "Centered"
    PICTO_LAYOUT_SIDE = "mzp-t-picto-side", "Side"


class SocialIconChoices(TextChoices):
    # The two values for each choice are the static URL path and the display name
    SOCIAL_FIREFOX = "firefox", "Firefox"
    SOCIAL_GITHUB = "github", "Github"
    SOCIAL_INSTAGRAM = "instagram", "Instagram"
    SOCIAL_LINKEDIN = "linkedin", "LinkedIn"
    SOCIAL_MASTODON = "mastodon", "Mastodon"
    SOCIAL_POCKET = "pocket", "Pocket"
    SOCIAL_SPOTIFY = "spotify", "Spotify"
    SOCIAL_TIKTOK = "tiktok", "TikTok"
    SOCIAL_TWITTER = "twitter", "Twitter"
    SOCIAL_YOUTUBE = "youtube", "YouTube"


class ColumnOptions(TextChoices):
    COLUMN_LAYOUT_ONE_COLUMN = " ", "One column"
    COLUMN_LAYOUT_TWO_COLUMN = "mzp-l-columns mzp-t-columns-two", "Two column"
    COLUMN_LAYOUT_THREE_COLUMN = "mzp-l-columns mzp-t-columns-three", "Three column"
    COLUMN_LAYOUT_FOUR_COLUMN = "mzp-l-columns mzp-t-columns-four", "Four column"


class ThemeOptions(TextChoices):
    THEME_LIGHT = "mzp-t-light", "Light theme"
    THEME_DARK = "mzp-t-dark", "Dark theme"


class HeadingLevelOptions(TextChoices):
    HEADING_LEVEL_H2 = "h2", "Heading Level 2"
    HEADING_LEVEL_H3 = "h3", "Heading Level 3"
    HEADING_LEVEL_H4 = "h4", "Heading Level 4"


class HeadingSizeOptions(TextChoices):
    HEADING_SIZE_LG = "", "Large"
    HEADING_SIZE_MD = "mzp-u-title-md", "Medium"
    HEADING_SIZE_SM = "mzp-u-title-sm", "Small"


class HeadingAlignmentOptions(TextChoices):
    SECTION_HEADING_ALIGNMENT_DEFAULT = "", "Default"
    SECTION_HEADING_ALIGNMENT_CENTER = "t-align-center", "Center"


class HeroLayoutOptions(TextChoices):
    HERO_LAYOUT_DEFAULT = "hero-section-default", "Default layout"
    HERO_LAYOUT_CENTERED = "hero-section-centered", "Centered layout"


class TableWidthOptions(TextChoices):
    TABLE_WIDTH_DEFAULT = "bb-table-width-default", "Default width"
    TABLE_WIDTH_FULL = "bb-table-width-full", "Full width"


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
    rel = wagtail_blocks.CharBlock(
        max_length=100,
        required=False,
        help_text="Optional 'rel' attribute. If blank, no attribute will be set",
    )

    class Meta:
        icon = "site"
        value_class = LinkStructValue


class LabelledLinkBlock(LinkBlock):
    label = wagtail_blocks.CharBlock(
        max_length=100,
        required=False,
    )


class CTAButtonBlock(LinkBlock):
    button_text = wagtail_blocks.CharBlock(
        max_length=50,
        required=False,
    )


class CardBlock(wagtail_blocks.StructBlock):
    class Meta:
        template = "microsite/blocks/card.html"

    @property
    def frontend_media(self):
        "Custom property that lets us selectively include CSS"
        return forms.Media(css={"all": [static("css/protocol-card.css")]})

    title = wagtail_blocks.CharBlock(
        required=False,
        max_length=60,
        help_text="Card title with about 30-40 characters",
    )
    description = wagtail_blocks.TextBlock(
        required=False,
        max_length=350,
        help_text="A description ideally around 150 characters, max 350. Usually we only have room for one or two sentences.",
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
    size = wagtail_blocks.ChoiceBlock(
        choices=CardSizes.choices,
        default=CardSizes.SMALL,
        required=False,  # so that we can set SMALL, which is actually an empty string
    )
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
        icon = "copy"

    @property
    def frontend_media(self):
        "Custom property that lets us selectively include CSS"
        return forms.Media(css={"all": [static("css/protocol-card.css")]})

    layout = wagtail_blocks.ChoiceBlock(
        label="Layout style",
        choices=CardLayoutOptions.choices,
        default=CardLayoutOptions.CARD_LAYOUT_3,
    )

    layout_size = wagtail_blocks.ChoiceBlock(
        choices=LayoutSizes.choices,
        default=LayoutSizes.LAYOUT_SIZE_NONE,
        blank=True,
        required=False,  # to allow for default/empty/large option
    )

    cards = wagtail_blocks.ListBlock(
        CardBlock(),
        help_text=get_docs_link("card-layout"),
        collapsed=True,
    )


class SectionHeadingBlock(wagtail_blocks.StructBlock):
    class Meta:
        template = "microsite/blocks/section_heading.html"
        icon = "title"

    @property
    def frontend_media(self):
        "Custom property that lets us selectively include CSS"
        return forms.Media(css={"all": [static("css/protocol-section-heading.css")]})

    heading_level = wagtail_blocks.ChoiceBlock(
        choices=HeadingLevelOptions.choices,
        default=HeadingLevelOptions.HEADING_LEVEL_H2,
        help_text=mark_safe(
            "Remember to respect best practices around hierarchy of heading level: "
            "<a href='https://developer.mozilla.org/docs/Web/HTML/Element/Heading_Elements#usage_notes'>See MDN</a>"
        ),
    )

    heading_size = wagtail_blocks.ChoiceBlock(
        choices=HeadingSizeOptions.choices,
        default=HeadingSizeOptions.HEADING_SIZE_LG,
        help_text=mark_safe("Sets the display size of the heading independent of the heading level (h2, h3, or h4)."),
        blank=True,
        required=False,  # to allow for default/empty/large option
    )

    alignment = wagtail_blocks.ChoiceBlock(
        choices=HeadingAlignmentOptions.choices,
        default=HeadingAlignmentOptions.SECTION_HEADING_ALIGNMENT_CENTER,
        blank=True,
        required=False,  # to allow for default/empty/centered option
    )

    text = wagtail_blocks.TextBlock(
        max_length=120,
        required=True,
    )


class SplitBlock(wagtail_blocks.StructBlock):
    class Meta:
        template = "microsite/blocks/split.html"

    @property
    def frontend_media(self):
        "Custom property that lets us selectively include CSS"
        return forms.Media(css={"all": [static("css/protocol-split.css")]})

    layout_variant = wagtail_blocks.ChoiceBlock(
        choices=SplitBlockVariants.choices,
        default=SplitBlockVariants.SPLIT_BLOCK_STANDARD,
        required=False,  # so that we can set SPLIT_BLOCK_STANDARD, which is actually an empty string
    )
    content_size = wagtail_blocks.ChoiceBlock(
        choices=SplitBlockSizes.choices,
        blank=True,
    )
    title = wagtail_blocks.CharBlock(
        max_length=120,
        required=True,
    )

    text = wagtail_blocks.RichTextBlock(
        features=settings.RICHTEXT_FEATURES__SIMPLE,
        max_length=650,
        required=True,
        help_text="Ideally less than 500 chars. 650 max.",
    )
    cta_button = CTAButtonBlock(required=False)
    image = AccessibleImageBlock(required=True)


class FooterColumnBlock(wagtail_blocks.StructBlock):
    @property
    def frontend_media(self):
        "Custom property that lets us selectively include CSS"
        return forms.Media(
            css={"all": [static("css/protocol-footer-css.css")]},
            js=[static("js/protocol-footer-js.js")],
        )

    # For use in the models.Footer.content Streamfield,
    # so has no template of its own
    title = wagtail_blocks.CharBlock(
        label="Column title - e.g. 'Company' or 'Support'",
        max_length=50,
        required=False,
    )
    links = wagtail_blocks.ListBlock(
        LabelledLinkBlock(),
        collapsed=False,
    )


class FooterSocialLinkBlock(wagtail_blocks.StructBlock):
    @property
    def frontend_media(self):
        "Custom property that lets us selectively include CSS"
        return forms.Media(
            css={"all": [static("css/protocol-footer-css.css")]},
            js=[static("js/protocol-footer-js.js")],
        )

    icon = wagtail_blocks.ChoiceBlock(
        choices=SocialIconChoices.choices,
    )
    url = wagtail_blocks.URLBlock(
        required=True,
    )
    data_label = wagtail_blocks.CharBlock(
        max_length=50,
        required=True,
        help_text='Service name and handle - e.g. "Twitter (@mozilla)"',
    )
    rel = wagtail_blocks.CharBlock(
        max_length=100,
        required=False,
        help_text="Optional 'rel' attribute. If blank, no attribute will be set",
    )


class FooterSocialLinksGroupBlock(wagtail_blocks.StructBlock):
    # For use in the models.Footer.content Streamfield,
    # so has no template of its own
    title = wagtail_blocks.CharBlock(
        label="Social links section title - e.g. 'Follow @mozilla'",
        max_length=50,
        required=False,
    )
    links = wagtail_blocks.ListBlock(
        FooterSocialLinkBlock(),
        label="Social links",
        max_num=6,
        collapsed=False,
    )


class FooterAfterMatterLinksBlock(wagtail_blocks.StructBlock):
    @property
    def frontend_media(self):
        "Custom property that lets us selectively include CSS"
        return forms.Media(
            css={"all": [static("css/protocol-footer-css.css")]},
            js=[static("js/protocol-footer-js.js")],
        )

    links = wagtail_blocks.ListBlock(
        LabelledLinkBlock(),
        max_num=10,
        collapsed=False,
    )
    legal_text = wagtail_blocks.RichTextBlock(
        features=["link"],
    )


class PictoBlock(wagtail_blocks.StructBlock):
    class Meta:
        template = "microsite/blocks/picto.html"

    @property
    def frontend_media(self):
        "Custom property that lets us selectively include CSS"
        return forms.Media(
            css={"all": [static("css/protocol-picto.css")]},
        )

    layout = wagtail_blocks.ChoiceBlock(
        choices=PictoLayoutOptions.choices,
        default=PictoLayoutOptions.PICTO_LAYOUT_STANDARD,
        required=False,  # so that we can set PICTO_LAYOUT_STANDARD, which is actually an empty string
    )
    image = AccessibleImageBlock(
        required=True,
        help_text=(
            "Picto block images should usually be a small icon, but larger images or (eventually) even videos can be accommodated in some layouts"
        ),
    )
    heading = wagtail_blocks.CharBlock(
        max_length=100,
        required=False,
    )
    body = wagtail_blocks.RichTextBlock(
        features=settings.RICHTEXT_FEATURES__SIMPLE,
        max_length=500,
        required=False,
        help_text="Don’t use this component for long-form content; it’s only for blurbs.",
    )


class PictoWithLinkBlock(PictoBlock):
    link = LabelledLinkBlock(
        required=False,
    )


class StackOfPictosBlock(wagtail_blocks.StructBlock):
    class Meta:
        template = "microsite/blocks/stack_of_pictos.html"

    @property
    def frontend_media(self):
        "Custom property that lets us selectively include CSS"
        return forms.Media(
            css={
                "all": [
                    static("css/birdbox-picto-stack.css"),
                ]
            },
        )

    title = wagtail_blocks.CharBlock(
        required=False,
        max_length=100,
    )
    pictos = wagtail_blocks.ListBlock(
        PictoBlock(),
        collapsed=False,
    )


class ColumnContentBlock(wagtail_blocks.StreamBlock):
    stack_of_pictos = StackOfPictosBlock(
        required=False,
    )
    picto = PictoBlock(
        required=False,
    )
    picto_with_link = PictoWithLinkBlock(
        required=False,
    )
    text = wagtail_blocks.RichTextBlock(
        features=settings.RICHTEXT_FEATURES__LIMITED,
    )


class ColumnBlock(wagtail_blocks.StructBlock):
    """The multi-column layout made available as a block, wrapping various content items
    that need structure around them.

    This block will support 1 to 4 columns
    """

    class Meta:
        template = "microsite/blocks/column.html"

    @property
    def frontend_media(self):
        "Custom property that lets us selectively include CSS"
        return forms.Media(
            css={
                "all": [
                    static("css/protocol-columns.css"),
                    static("css/protocol-picto.css"),
                    static("css/birdbox-picto-stack.css"),
                ]
            },
        )

    title = wagtail_blocks.CharBlock(
        required=False,
        max_length=100,
    )

    layout_size = wagtail_blocks.ChoiceBlock(
        choices=LayoutSizes.choices,
        default=LayoutSizes.LAYOUT_SIZE_NONE,
        blank=True,
        required=False,  # to allow for default/empty/large option
    )

    column_layout = wagtail_blocks.ChoiceBlock(
        choices=ColumnOptions.choices,
        default=ColumnOptions.COLUMN_LAYOUT_TWO_COLUMN,
        required=True,
    )

    color_theme = ThemedColorBlock(
        required=True,
    )

    content = ColumnContentBlock(
        help_text="Only blocks that can fit/flow well in a multi-column layout are allowed here - e.g. Picto",
    )


class ArticleBlock(wagtail_blocks.StructBlock):
    class Meta:
        template = "microsite/blocks/article.html"
        icon = "doc-full-inverse"

    @property
    def frontend_media(self):
        "Custom property that lets us selectively include CSS"
        return forms.Media(
            css={"all": [static("css/birdbox-article.css")]},
        )

    title = wagtail_blocks.CharBlock(
        max_length=150,
        required=False,
    )
    heading_level = wagtail_blocks.ChoiceBlock(
        choices=HeadingLevelOptions.choices,
        default=HeadingLevelOptions.HEADING_LEVEL_H2,
        help_text=mark_safe(
            "Remember to respect best practices around hierarchy of heading level: "
            "<a href='https://developer.mozilla.org/docs/Web/HTML/Element/Heading_Elements#usage_notes'>See MDN</a>"
        ),
    )
    heading_size = wagtail_blocks.ChoiceBlock(
        choices=HeadingSizeOptions.choices,
        default=HeadingSizeOptions.HEADING_SIZE_LG,
        help_text=mark_safe("Sets the display size of the heading independent of the heading level (h2, h3, or h4)."),
        blank=True,
        required=False,  # to allow for default/empty/large option
    )
    alignment = wagtail_blocks.ChoiceBlock(
        choices=HeadingAlignmentOptions.choices,
        default=HeadingAlignmentOptions.SECTION_HEADING_ALIGNMENT_CENTER,
        blank=True,
        required=False,  # to allow for default/empty/centered option
    )

    intro_para = wagtail_blocks.CharBlock(
        max_length=1000,
        help_text="Rendered as a single styled paragraph element. 2000 chars max, but less is better.",
        required=False,
    )
    body = wagtail_blocks.RichTextBlock(
        features=settings.RICHTEXT_FEATURES__ARTICLE,
    )


class CaptionedImageBlock(AccessibleImageBlock):
    @property
    def frontend_media(self):
        "Custom property that lets us selectively include CSS"
        return forms.Media(
            css={"all": [static("css/birdbox-captioned-image.css")]},
        )

    class Meta:
        template = "microsite/blocks/captioned_image.html"
        icon = "doc-full"

    image_caption = wagtail_blocks.CharBlock(
        max_length=250,
        required=False,
    )
    image_credit = wagtail_blocks.CharBlock(
        max_length=250,
        required=False,
    )


class NewsletterFormBlock(wagtail_blocks.StructBlock):
    class Meta:
        template = "microsite/blocks/newsletter.html"
        icon = "mail"

    @property
    def frontend_media(self):
        "Custom property that lets us selectively include CSS"
        return forms.Media(
            css={"all": [static("css/protocol-newsletter-form.css")]},
            js=[static("js/newsletter-form.js")],
        )

    newsletter = wagtail_blocks.MultipleChoiceBlock(
        choices=get_freshest_newsletter_options(),
        help_text=mark_safe(
            "Which newsletter(s) should be selectable? "
            f"See <a href='{settings.BASKET_NEWSLETTER_DATA_URL}'>Basket for details and available locales</a>",
        ),
    )
    title = wagtail_blocks.CharBlock(
        default="Love the Web?",
        max_length=50,
    )
    tagline = wagtail_blocks.CharBlock(
        default="Get the Mozilla newsletter and help us keep it open and free.",
        max_length=100,
    )
    accompanying_image = AccessibleImageBlock(
        required=True,
        help_text="NB: Needs to match background colour (for now - working on a no-image variation)",
    )
    success_title = wagtail_blocks.CharBlock(
        default="Thanks!",
        max_length=50,
    )
    success_message = wagtail_blocks.CharBlock(
        default=(
            "If you haven’t previously confirmed a subscription to a "
            "Mozilla-related newsletter you may have to do so. "
            "Please check your inbox or your spam filter for an email from us."
        ),
        max_length=200,
    )


class VideoEmbedBlock(wagtail_blocks.StructBlock):
    class Meta:
        template = "microsite/blocks/video_embed.html"
        icon = "media"

    @property
    def frontend_media(self):
        "Custom property that lets us selectively include CSS"
        return forms.Media(css={"all": [static("css/protocol-video.css")]})

    video = EmbedBlock(
        required=True,
    )


class BiographyBlock(wagtail_blocks.StructBlock):
    class Meta:
        template = "microsite/blocks/biography.html"
        icon = "user"

    # Frontend_media comes from the parent block that uses this block

    name = wagtail_blocks.CharBlock(
        max_length=100,
    )
    bio = wagtail_blocks.RichTextBlock(
        features=settings.RICHTEXT_FEATURES__BIO,
    )
    meta_info = wagtail_blocks.CharBlock(
        max_length=50,
        required=False,
        help_text="Supplementary contextual info, this person's dept or project",
    )
    website = wagtail_blocks.URLBlock(
        required=False,
    )
    website_link_label = wagtail_blocks.CharBlock(
        max_length=50,
        required=False,
    )
    image = AccessibleImageBlock(
        required=False,
    )


class BiographyGridBlock(wagtail_blocks.StructBlock):
    class Meta:
        template = "microsite/blocks/biography_grid.html"
        icon = "group"

    @property
    def frontend_media(self):
        "Custom property that lets us selectively include CSS"
        return forms.Media(
            css={
                "all": [
                    static("css/protocol-card.css"),
                    static("css/birdbox-biography-grid.css"),
                ]
            }
        )

    title = wagtail_blocks.CharBlock(
        max_length=150,
        required=False,
    )
    heading_level = wagtail_blocks.ChoiceBlock(
        choices=HeadingLevelOptions.choices,
        default=HeadingLevelOptions.HEADING_LEVEL_H2,
        help_text=mark_safe(
            "Remember to respect best practices around hierarchy of heading level: "
            "<a href='https://developer.mozilla.org/docs/Web/HTML/Element/Heading_Elements#usage_notes'>See MDN</a>"
        ),
    )
    heading_size = wagtail_blocks.ChoiceBlock(
        choices=HeadingSizeOptions.choices,
        default=HeadingSizeOptions.HEADING_SIZE_LG,
        help_text=mark_safe("Sets the display size of the heading independent of the heading level (h2, h3, or h4)."),
        blank=True,
        required=False,  # to allow for default/empty/large option
    )
    standfirst = wagtail_blocks.TextBlock(
        max_length=500,
        required=False,
    )
    theme = wagtail_blocks.ChoiceBlock(
        choices=ThemeOptions.choices,
        required=True,
        default=ThemeOptions.THEME_LIGHT,
    )
    people = wagtail_blocks.ListBlock(
        BiographyBlock(),
        collapsed=False,
    )


class CalloutBlockBase(wagtail_blocks.StructBlock):
    @property
    def frontend_media(self):
        "Custom property that lets us selectively include CSS"
        return forms.Media(css={"all": [static("css/protocol-callout.css")]})

    headline = wagtail_blocks.CharBlock(
        max_length=100,
        required=True,
        help_text="Around 50 chars ideally. Max 100",
    )
    body = wagtail_blocks.RichTextBlock(
        features=settings.RICHTEXT_FEATURES__SIMPLE,
        max_length=1000,
        required=True,
        help_text="Around 150 chars ideally. 400 is pushing it. Max is 1000 but think about how it'll look on mobile, too",
    )
    cta = CTAButtonBlock(
        required=True,
    )
    theme = wagtail_blocks.ChoiceBlock(
        choices=ThemeOptions.choices,
        required=True,
        default=ThemeOptions.THEME_LIGHT,
    )


class CalloutBlock(CalloutBlockBase):
    class Meta:
        template = "microsite/blocks/callout.html"
        icon = "comment"


class CompactCalloutBlock(CalloutBlockBase):
    class Meta:
        template = "microsite/blocks/compact_callout.html"
        icon = "comment"


class HeroBlock(wagtail_blocks.StructBlock):
    """This is not a core Protocol component, but is based on work done
    for MEICO"""

    class Meta:
        template = "microsite/blocks/hero.html"

    @property
    def frontend_media(self):
        "Custom property that lets us selectively include CSS"
        return forms.Media(css={"all": [static("css/birdbox-hero.css")]})

    teaser = wagtail_blocks.CharBlock(
        max_length=150,
        required=False,
        help_text="Up to 150 characters, appears above the main heading",
    )
    main_heading = wagtail_blocks.CharBlock(
        max_length=75,
        required=True,
        help_text="Up to 75 characters. Will be the H1 of the page it's used in",
    )
    standfirst = wagtail_blocks.TextBlock(
        max_length=400,
        required=False,
        help_text="Up to 400 characters",
    )
    background_image = ImageChooserBlock(
        required=False,
        help_text="Optional but recommended - needs to be something that will fill well",
    )
    call_to_action = LabelledLinkBlock(
        required=False,
        help_text="Link for an optional button at the base of the hero",
    )
    color_theme = ThemedColorBlock(
        required=True,
    )
    layout = wagtail_blocks.ChoiceBlock(
        choices=HeroLayoutOptions.choices,
        required=True,
        default=HeroLayoutOptions.HERO_LAYOUT_DEFAULT,
    )


class DetailsBlock(wagtail_blocks.StructBlock):
    # Individual block for https://protocol.mozilla.org/components/detail/details-component--default.html
    # This block is used either in a streamfield that's specifically for a page
    # that contains only Detail blocks, or in an ExpandingDetailsBlock in a
    # StreamField in any page

    class Meta:
        template = "microsite/blocks/details.html"

    # No custom frontend_media needed - the JS is already in the main bundle and
    # there is no related CSS

    heading = wagtail_blocks.CharBlock(
        max_length=75,
        required=True,
        help_text="Up to 75 characters. Will be the H3 of the page it's used in",
    )

    body = wagtail_blocks.RichTextBlock(
        features=settings.RICHTEXT_FEATURES__DETAIL,
    )


class ExpandingDetailsBlock(wagtail_blocks.StructBlock):
    class Meta:
        icon = "collapse-down"
        template = "microsite/blocks/expanding_details.html"

    # No custom frontend_media needed - the JS is already in the main bundle and
    # there is no related CSS

    preamble = wagtail_blocks.RichTextBlock(
        features=settings.RICHTEXT_FEATURES__DETAIL,
        required=False,
        help_text="Optional rich-text to go before the section. Not standard Protocol",
    )

    details = wagtail_blocks.ListBlock(
        DetailsBlock(),
        collapsed=False,
        help_text="Each Details Block will be rendered as an expandable section",
    )


class ContactFormBlock(wagtail_blocks.StructBlock):
    # A contact form is CURRENTLY a very heavily modified version of
    # the newsletter form, due to the need to backport and existing site
    # into Birdbox, which overrode the newsletter behaviour
    class Meta:
        # For now, the Contact form is VERY opinionated and does what
        # we needed for Future.m.o - we need to make a generic alternative
        template = "microsite/blocks/futuremo_contact_form.html"
        icon = "mail"

    @property
    def frontend_media(self):
        return forms.Media(
            css={
                "all": [
                    static("css/protocol-newsletter-form.css"),
                    static("css/birdbox-contact-form.css"),
                ]
            },
            js=[static("js/futuremo-contact-form-js.js")],
        )

    form_type = wagtail_blocks.ChoiceBlock(
        choices=CONTACT_FORM_CHOICES,
        help_text="Note: the recipient address for the form is defined in code, not in the CMS",
    )
    title = wagtail_blocks.CharBlock(
        max_length=120,
    )
    tagline = wagtail_blocks.TextBlock(
        max_length=500,
        required=False,
    )
    submit_button_text = wagtail_blocks.CharBlock(
        default="Submit",
        max_length=120,
    )
    aftermatter_text = wagtail_blocks.CharBlock(
        default="We will only send you Mozilla-related information",
        required=False,
        max_length=120,
    )
    success_title = wagtail_blocks.CharBlock(
        default="Thanks!",
        max_length=120,
    )
    success_message = wagtail_blocks.CharBlock(
        default=(
            "If you haven’t previously confirmed a subscription to a "
            "Mozilla-related newsletter you may have to do so. "
            "Please check your inbox or your spam filter for an email from us."
        ),
        max_length=200,
    )
    accompanying_image = AccessibleImageBlock(
        required=False,
        help_text="NB: Needs to match background colour (for now - working on a no-image variation)",
    )

    def get_context(self, value, parent_context=None):
        context = parent_context or {}
        form_class = import_string(value.get("form_type"))
        context.update(
            {
                "contact_form": form_class(),
            }
        )
        return context


class HeadedTableBlock(wagtail_blocks.StructBlock):
    """IMPORTANT: if you include this block in a StreamField and the streamfield
    is set to collapsed=True, the table will not be visible to edit unless the
    browser window is resized slightly. This is ticketed at
    https://github.com/wagtail/wagtail/issues/8611 but help-text should be added
    to make it clear for the end user until the bug is fixed.
    """

    class Meta:
        template = "microsite/blocks/headed_table.html"
        icon = "table"

    @property
    def frontend_media(self):
        return forms.Media(
            css={"all": [static("css/birdbox-headed-table.css")]},
        )

    title = wagtail_blocks.CharBlock(
        max_length=50,
        required=False,
    )
    intro = wagtail_blocks.RichTextBlock(
        required=False,
        features=settings.RICHTEXT_FEATURES__SIMPLE,
    )

    table = TableBlock(
        table_options={
            "contextMenu": [
                "row_above",
                "row_below",
                "---------",
                "col_left",
                "col_right",
                "---------",
                "remove_row",
                "remove_col",
                "---------",
                "undo",
                "redo",
                "---------",
                "copy",
                "cut",
                "---------",
                "alignment",
            ],
        }
    )
    table_width = wagtail_blocks.ChoiceBlock(
        choices=TableWidthOptions.choices,
        default=TableWidthOptions.TABLE_WIDTH_DEFAULT,
    )


class CaptionedImageLayoutBlock(wagtail_blocks.StructBlock):
    class Meta:
        template = "microsite/blocks/captioned_image_layout.html"

    @property
    def frontend_media(self):
        "Custom property that lets us selectively include CSS"
        return forms.Media(
            css={
                "all": [
                    static("css/birdbox-captioned-image.css"),
                    static("css/birdbox-captioned-image-layout.css"),
                    static("css/protocol-card.css"),
                ]
            }
        )

    title = wagtail_blocks.CharBlock(
        max_length=100,
        rquired=False,
    )

    layout = wagtail_blocks.ChoiceBlock(
        choices=CardLayoutOptions.choices,
        default=CardLayoutOptions.CARD_LAYOUT_3,
    )

    cards = wagtail_blocks.ListBlock(
        CaptionedImageBlock(),
        help_text=get_docs_link("card-layout"),
        collapsed=True,
    )


class HorizontalImageBlock(AccessibleImageBlockBase):
    color_theme = ThemedColorBlock(
        required=True,
    )

    disable_bottom_spacing = wagtail_blocks.BooleanBlock(
        default=True,
        required=False,
    )

    class Meta:
        template = "microsite/blocks/horizontal_image.html"
        icon = "image"

    @property
    def frontend_media(self):
        "Custom property that lets us selectively include CSS"
        return forms.Media(
            css={"all": [static("css/birdbox-horizontal-image.css")]},
        )
