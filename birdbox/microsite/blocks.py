# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

"""Custom Wagtail blocks that map to Protocol components, intended for use in a StreamField"""

from django import forms
from django.conf import settings
from django.db.models import TextChoices
from django.templatetags.static import static
from django.utils.safestring import mark_safe

from wagtail import blocks as wagtail_blocks
from wagtail.embeds.blocks import EmbedBlock

from birdbox.protocol_links import get_docs_link
from common.blocks import AccessibleImageBlock
from common.utils import get_freshest_newsletter_options


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
    SPLIT_BLOCK_DARK_BACKGROUND = "mzp-t-dark mzp-t-background-secondary", "Dark Background"


class SplitBlockSizes(TextChoices):
    SPLIT_BLOCK_SIZE_MEDIUM = "mzp-t-content-md", "Medium"
    SPLIT_BLOCK_SIZE_LARGE = "mzp-t-content-lg", "Large"
    SPLIT_BLOCK_SIZE_EXTRA_LARGE = "mzp-t-content-xl", "Extra-large"


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
    COLUMN_LAYOUT_ONE_COLUMN = "mzp-l-content", "One column"
    COLUMN_LAYOUT_TWO_COLUMN = "mzp-l-content mzp-l-columns mzp-t-columns-two", "Two column"
    COLUMN_LAYOUT_THREE_COLUMN = "mzp-l-content mzp-l-columns mzp-t-columns-three", "Three column"
    COLUMN_LAYOUT_FOUR_COLUMN = "mzp-l-content mzp-l-columns mzp-t-columns-four", "Four column"


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


class LabelledLinkBlock(LinkBlock):
    label = wagtail_blocks.CharBlock(
        max_length=100,
    )


class CTAButtonBlock(LinkBlock):
    button_text = wagtail_blocks.CharBlock(
        max_length=50,
    )


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
        collapsed=True,
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
    text = wagtail_blocks.TextBlock(
        max_length=500,
        required=True,
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
        collapsed=True,
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
        collapsed=True,
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
        collapsed=True,
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
    body = wagtail_blocks.TextBlock(
        max_length=150,
        required=False,
        help_text="Don’t use this component for long-form content; it’s only for blurbs.",
    )


class ColumnContentBlock(wagtail_blocks.StreamBlock):
    picto = PictoBlock(
        required=False,
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
                ]
            },
        )

    column_layout = wagtail_blocks.ChoiceBlock(
        choices=ColumnOptions.choices,
        default=ColumnOptions.COLUMN_LAYOUT_TWO_COLUMN,
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
            css={"all": [static("css/protocol-article.css")]},
        )

    header = wagtail_blocks.CharBlock(
        max_length=250,
        help_text="Rendered as a H1",
    )
    intro_para = wagtail_blocks.CharBlock(
        max_length=1000,
        help_text="Rendered as a single styled paragraph element  (<p>). 2000 chars max, but less is better.",
    )
    body = wagtail_blocks.RichTextBlock(
        features=settings.RICHTEXT_FEATURES__ARTICLE,
    )


class CaptionedImageBlock(AccessibleImageBlock):
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
    sucess_message = wagtail_blocks.CharBlock(
        default=(
            "If you haven’t previously confirmed a subscription to a Mozilla-related newsletter you may have to do so. "
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
