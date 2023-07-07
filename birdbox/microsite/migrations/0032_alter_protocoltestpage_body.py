# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

# Generated by Django 4.1.10 on 2023-07-07 16:43

from django.db import migrations

import wagtail.blocks
import wagtail.fields
import wagtail.images.blocks
import wagtailstreamforms.blocks


class Migration(migrations.Migration):
    dependencies = [
        ("microsite", "0031_alter_protocoltestpage_body"),
    ]

    operations = [
        migrations.AlterField(
            model_name="protocoltestpage",
            name="body",
            field=wagtail.fields.StreamField(
                [
                    ("paragraph", wagtail.blocks.RichTextBlock(required=False)),
                    ("image", wagtail.images.blocks.ImageChooserBlock(required=False)),
                    (
                        "cards",
                        wagtail.blocks.StructBlock(
                            [
                                (
                                    "layout",
                                    wagtail.blocks.ChoiceBlock(
                                        choices=[
                                            ("mzp-l-card-hero", "5-Card Hero layout"),
                                            ("mzp-l-card-quarter", "4-Card Layout"),
                                            ("mzp-l-card-third", "3-Card Layout"),
                                            ("mzp-l-card-half", "2-Card Layout"),
                                        ]
                                    ),
                                ),
                                (
                                    "cards",
                                    wagtail.blocks.ListBlock(
                                        wagtail.blocks.StructBlock(
                                            [
                                                (
                                                    "size",
                                                    wagtail.blocks.ChoiceBlock(
                                                        choices=[
                                                            ("mzp-c-card-extra-small", "Extra small"),
                                                            ("", "Small"),
                                                            ("mzp-c-card-extra-medium", "Medium"),
                                                            ("mzp-c-card-large", "Large"),
                                                            ("mzp-c-card-extra-large", "Extra Large"),
                                                        ],
                                                        required=False,
                                                    ),
                                                ),
                                                (
                                                    "title",
                                                    wagtail.blocks.CharBlock(
                                                        help_text="Card title with about 30-40 characters", max_length=60, required=True
                                                    ),
                                                ),
                                                (
                                                    "description",
                                                    wagtail.blocks.TextBlock(
                                                        help_text="A description of about 150 characters. Usually we only have room for one or two sentences.",
                                                        max_length=170,
                                                        required=True,
                                                    ),
                                                ),
                                                (
                                                    "cta",
                                                    wagtail.blocks.CharBlock(
                                                        help_text="Call to action with about 30-40 characters", max_length=60, required=False
                                                    ),
                                                ),
                                                (
                                                    "meta_info",
                                                    wagtail.blocks.CharBlock(
                                                        help_text="Meta info at the base of the card", max_length=60, required=False
                                                    ),
                                                ),
                                                (
                                                    "link",
                                                    wagtail.blocks.StructBlock(
                                                        [
                                                            ("page", wagtail.blocks.PageChooserBlock(label="Page", required=False)),
                                                            ("external_url", wagtail.blocks.URLBlock(label="External URL", required=False)),
                                                        ]
                                                    ),
                                                ),
                                                (
                                                    "image_aspect_ratio",
                                                    wagtail.blocks.ChoiceBlock(
                                                        choices=[
                                                            ("mzp-has-aspect-1-1", "1:1"),
                                                            ("mzp-has-aspect-3-2", "3:2"),
                                                            ("mzp-has-aspect-16-9", "16:9"),
                                                        ]
                                                    ),
                                                ),
                                                (
                                                    "card_image",
                                                    wagtail.blocks.StructBlock(
                                                        [
                                                            ("image", wagtail.images.blocks.ImageChooserBlock(required=False)),
                                                            (
                                                                "alt_text",
                                                                wagtail.blocks.CharBlock(
                                                                    label="Alt-text for this image", max_length=250, required=False
                                                                ),
                                                            ),
                                                            (
                                                                "decorative_only",
                                                                wagtail.blocks.BooleanBlock(
                                                                    default=False, label="Is this image decorative only?", required=False
                                                                ),
                                                            ),
                                                            (
                                                                "width",
                                                                wagtail.blocks.IntegerBlock(
                                                                    label="Specific image width in px (optional)", min_value=0, required=False
                                                                ),
                                                            ),
                                                            (
                                                                "height",
                                                                wagtail.blocks.IntegerBlock(
                                                                    label="Specific image height in px (optional)", min_value=0, required=False
                                                                ),
                                                            ),
                                                            (
                                                                "rendition_spec",
                                                                wagtail.blocks.CharBlock(
                                                                    blank=True,
                                                                    default="original",
                                                                    help_text="Lots of options available. See <a href='https://docs.wagtail.org/en/stable/topics/images.html#available-resizing-methods'>Wagtail docs on image sizing</a> Defaults to 'original'",
                                                                    max_length=256,
                                                                ),
                                                            ),
                                                        ],
                                                        required=False,
                                                    ),
                                                ),
                                                ("tag", wagtail.blocks.CharBlock(max_length=48, required=False)),
                                            ]
                                        ),
                                        collapsed=True,
                                        help_text="<a href='https://protocol.mozilla.org/components/detail/card-layout--overview.html'>Protocol docs for card-layout</a>.",
                                    ),
                                ),
                            ],
                            help_text="Layout wrapper for Cards. <a href='https://protocol.mozilla.org/components/detail/card-layout--overview.html'>Protocol docs for card-layout</a>.",
                            label="Card group",
                            required=False,
                        ),
                    ),
                    (
                        "split",
                        wagtail.blocks.StructBlock(
                            [
                                (
                                    "layout_variant",
                                    wagtail.blocks.ChoiceBlock(
                                        choices=[
                                            ("", "Standard"),
                                            ("mzp-l-split-reversed", "Reversed"),
                                            ("mzp-t-dark mzp-t-background-secondary", "Dark Background"),
                                        ],
                                        required=False,
                                    ),
                                ),
                                (
                                    "content_size",
                                    wagtail.blocks.ChoiceBlock(
                                        blank=True,
                                        choices=[("mzp-t-content-md", "Medium"), ("mzp-t-content-lg", "Large"), ("mzp-t-content-xl", "Extra-large")],
                                    ),
                                ),
                                ("title", wagtail.blocks.CharBlock(max_length=120, required=True)),
                                ("text", wagtail.blocks.TextBlock(max_length=500, required=True)),
                                (
                                    "cta_button",
                                    wagtail.blocks.StructBlock(
                                        [
                                            ("page", wagtail.blocks.PageChooserBlock(label="Page", required=False)),
                                            ("external_url", wagtail.blocks.URLBlock(label="External URL", required=False)),
                                            ("button_text", wagtail.blocks.CharBlock(max_length=50)),
                                        ],
                                        required=False,
                                    ),
                                ),
                                (
                                    "image",
                                    wagtail.blocks.StructBlock(
                                        [
                                            ("image", wagtail.images.blocks.ImageChooserBlock(required=False)),
                                            ("alt_text", wagtail.blocks.CharBlock(label="Alt-text for this image", max_length=250, required=False)),
                                            (
                                                "decorative_only",
                                                wagtail.blocks.BooleanBlock(default=False, label="Is this image decorative only?", required=False),
                                            ),
                                            (
                                                "width",
                                                wagtail.blocks.IntegerBlock(
                                                    label="Specific image width in px (optional)", min_value=0, required=False
                                                ),
                                            ),
                                            (
                                                "height",
                                                wagtail.blocks.IntegerBlock(
                                                    label="Specific image height in px (optional)", min_value=0, required=False
                                                ),
                                            ),
                                            (
                                                "rendition_spec",
                                                wagtail.blocks.CharBlock(
                                                    blank=True,
                                                    default="original",
                                                    help_text="Lots of options available. See <a href='https://docs.wagtail.org/en/stable/topics/images.html#available-resizing-methods'>Wagtail docs on image sizing</a> Defaults to 'original'",
                                                    max_length=256,
                                                ),
                                            ),
                                        ],
                                        required=True,
                                    ),
                                ),
                            ],
                            help_text="<a href='https://protocol.mozilla.org/components/detail/split--default.html'>Protocol docs for split</a>.  Not all options supported",
                            label="Split content",
                            required=False,
                        ),
                    ),
                    (
                        "columns",
                        wagtail.blocks.StructBlock(
                            [
                                (
                                    "column_layout",
                                    wagtail.blocks.ChoiceBlock(
                                        choices=[
                                            ("mzp-l-content", "One column"),
                                            ("mzp-l-content mzp-l-columns mzp-t-columns-two", "Two column"),
                                            ("mzp-l-content mzp-l-columns mzp-t-columns-three", "Three column"),
                                            ("mzp-l-content mzp-l-columns mzp-t-columns-four", "Four column"),
                                        ]
                                    ),
                                ),
                                (
                                    "content",
                                    wagtail.blocks.StreamBlock(
                                        [
                                            (
                                                "picto",
                                                wagtail.blocks.StructBlock(
                                                    [
                                                        (
                                                            "layout",
                                                            wagtail.blocks.ChoiceBlock(
                                                                choices=[
                                                                    ("", "Standard"),
                                                                    ("mzp-t-picto-center", "Centered"),
                                                                    ("mzp-t-picto-side", "Side"),
                                                                ],
                                                                required=False,
                                                            ),
                                                        ),
                                                        (
                                                            "image",
                                                            wagtail.blocks.StructBlock(
                                                                [
                                                                    ("image", wagtail.images.blocks.ImageChooserBlock(required=False)),
                                                                    (
                                                                        "alt_text",
                                                                        wagtail.blocks.CharBlock(
                                                                            label="Alt-text for this image", max_length=250, required=False
                                                                        ),
                                                                    ),
                                                                    (
                                                                        "decorative_only",
                                                                        wagtail.blocks.BooleanBlock(
                                                                            default=False, label="Is this image decorative only?", required=False
                                                                        ),
                                                                    ),
                                                                    (
                                                                        "width",
                                                                        wagtail.blocks.IntegerBlock(
                                                                            label="Specific image width in px (optional)", min_value=0, required=False
                                                                        ),
                                                                    ),
                                                                    (
                                                                        "height",
                                                                        wagtail.blocks.IntegerBlock(
                                                                            label="Specific image height in px (optional)",
                                                                            min_value=0,
                                                                            required=False,
                                                                        ),
                                                                    ),
                                                                    (
                                                                        "rendition_spec",
                                                                        wagtail.blocks.CharBlock(
                                                                            blank=True,
                                                                            default="original",
                                                                            help_text="Lots of options available. See <a href='https://docs.wagtail.org/en/stable/topics/images.html#available-resizing-methods'>Wagtail docs on image sizing</a> Defaults to 'original'",
                                                                            max_length=256,
                                                                        ),
                                                                    ),
                                                                ],
                                                                help_text="Picto block images should usually be a small icon, but larger images or (eventually) even videos can be accommodated in some layouts",
                                                                required=True,
                                                            ),
                                                        ),
                                                        ("heading", wagtail.blocks.CharBlock(max_length=100, required=False)),
                                                        (
                                                            "body",
                                                            wagtail.blocks.TextBlock(
                                                                help_text="Don’t use this component for long-form content; it’s only for blurbs.",
                                                                max_length=150,
                                                                required=False,
                                                            ),
                                                        ),
                                                    ],
                                                    required=False,
                                                ),
                                            )
                                        ],
                                        help_text="Only blocks that can fit/flow well in a multi-column layout are allowed here - e.g. Picto",
                                    ),
                                ),
                            ],
                            help_text="Column layout wrapper. <a href='https://protocol.mozilla.org/components/detail/columns--overview.html'>Protocol docs for columns</a>.. Has sub-components. <a href='https://protocol.mozilla.org/components/detail/picto--default.html'>Protocol docs for picto</a>.",
                            label="Column block",
                            required=False,
                        ),
                    ),
                    (
                        "article",
                        wagtail.blocks.StructBlock(
                            [
                                ("header", wagtail.blocks.CharBlock(help_text="Rendered as a H1", max_length=250)),
                                (
                                    "intro_para",
                                    wagtail.blocks.CharBlock(
                                        help_text="Rendered as a single styled paragraph element  (<p>). 2000 chars max, but less is better.",
                                        max_length=1000,
                                    ),
                                ),
                                (
                                    "body",
                                    wagtail.blocks.RichTextBlock(
                                        features=["h2", "h3", "bold", "italic", "strikethrough", "code", "blockquote", "link", "ol", "ul"]
                                    ),
                                ),
                            ],
                            help_text="<a href='https://protocol.mozilla.org/components/detail/article.html'>Protocol docs for article</a>.",
                            label="Article block",
                            required=False,
                        ),
                    ),
                    (
                        "newsletter_form",
                        wagtail.blocks.StructBlock(
                            [
                                (
                                    "newsletter",
                                    wagtail.blocks.MultipleChoiceBlock(
                                        choices=[
                                            ("about-addons", "Add-ons Developer Newsletter"),
                                            ("about-mozilla", "Mozilla Community"),
                                            ("ambassadors", "Firefox Student Ambassadors"),
                                            ("app-dev", "Developer Newsletter"),
                                            ("common-voice", "Common Voice"),
                                            ("developer-events", "Developer Events"),
                                            ("didthat-waitlist", "DidThat Waitlist"),
                                            ("firefox-accounts-journey", "Firefox Account Tips"),
                                            ("firefox-desktop", "Firefox for desktop"),
                                            ("firefox-friends", "Firefox Friends"),
                                            ("firefox-ios", "Firefox iOS"),
                                            ("firefox-os", "Firefox OS smartphone owner?"),
                                            ("firefox-sweepstakes", "Firefox Sweepstakes"),
                                            ("firefox-welcome", "Firefox Welcome"),
                                            ("game-developer-conference", "Game Developer Conference"),
                                            ("graceland-waitlist", "Graceland Waitlist"),
                                            ("guardian-vpn-waitlist", "Mozilla VPN Waitlist"),
                                            ("hubs", "Hubs"),
                                            ("inhuman", "Inhuman Ads"),
                                            ("internet-health-report", "Internet Health Report"),
                                            ("knowledge-is-power", "Knowledge is Power"),
                                            ("maker-party", "Maker Party"),
                                            ("mdnplus", "MDN"),
                                            ("member-comm", "Firefox Membership: Community Minded"),
                                            ("member-idealo", "Firefox Membership: Ideologically Engaged"),
                                            ("member-tech", "Firefox Membership: Tech-Forward"),
                                            ("member-tk", "Firefox Membership: TK"),
                                            ("miti", "Mozilla Information Trust Initiative"),
                                            ("mixed-reality", "Mixed Reality"),
                                            ("mobile", "Firefox for Android"),
                                            ("mozilla-accounts", "Firefox Accounts"),
                                            ("mozilla-ai-challenge", "Responsible AI Challenge"),
                                            ("mozilla-and-you", "Firefox News"),
                                            ("mozilla-fellowship-awardee-alumni", "Mozilla Fellowship & Awardee Alumni"),
                                            ("mozilla-festival", "Mozilla Festival"),
                                            ("mozilla-foundation", "Mozilla News"),
                                            ("mozilla-general", "Mozilla"),
                                            ("mozilla-innovation", "Innovation at Mozilla"),
                                            ("mozilla-leadership-network", "Mozilla Leadership Network"),
                                            ("mozilla-learning-network", "Mozilla Learning Network"),
                                            ("mozilla-phone", "Mozillians"),
                                            ("mozilla-rally", "Mozilla Rally News"),
                                            ("mozilla-technology", "Mozilla Labs"),
                                            ("mozilla-welcome", "Mozilla Welcome"),
                                            ("open-innovation-challenge", "Open Innovation Challenge"),
                                            ("open-leadership", "Open Leadership"),
                                            ("relay-phone-masking-waitlist", "Relay Phone Masking Waitlist"),
                                            ("relay-vpn-bundle-waitlist", "Relay VPN Bundle Waitlist"),
                                            ("relay-waitlist", "Firefox Relay Waitlist"),
                                            ("security-privacy-news", "Security and Privacy News from Mozilla"),
                                            ("shape-web", "Shape of the Web"),
                                            ("take-action-for-the-internet", "Take Action for the Internet"),
                                            ("test-pilot", "New Product Testing"),
                                            ("view-source-conference-global", "View Source Conference Global"),
                                            ("view-source-conference-north-america", "View Source Conference North America"),
                                            ("webmaker", "Webmaker"),
                                        ],
                                        help_text="Which newsletter(s) should be selectable? See <a href='https://www.mozilla.org/newsletter/newsletter-all.json'>Basket for details and available locales</a>",
                                    ),
                                ),
                                ("title", wagtail.blocks.CharBlock(default="Love the Web?", max_length=50)),
                                (
                                    "tagline",
                                    wagtail.blocks.CharBlock(default="Get the Mozilla newsletter and help us keep it open and free.", max_length=100),
                                ),
                                (
                                    "accompanying_image",
                                    wagtail.blocks.StructBlock(
                                        [
                                            ("image", wagtail.images.blocks.ImageChooserBlock(required=False)),
                                            ("alt_text", wagtail.blocks.CharBlock(label="Alt-text for this image", max_length=250, required=False)),
                                            (
                                                "decorative_only",
                                                wagtail.blocks.BooleanBlock(default=False, label="Is this image decorative only?", required=False),
                                            ),
                                            (
                                                "width",
                                                wagtail.blocks.IntegerBlock(
                                                    label="Specific image width in px (optional)", min_value=0, required=False
                                                ),
                                            ),
                                            (
                                                "height",
                                                wagtail.blocks.IntegerBlock(
                                                    label="Specific image height in px (optional)", min_value=0, required=False
                                                ),
                                            ),
                                            (
                                                "rendition_spec",
                                                wagtail.blocks.CharBlock(
                                                    blank=True,
                                                    default="original",
                                                    help_text="Lots of options available. See <a href='https://docs.wagtail.org/en/stable/topics/images.html#available-resizing-methods'>Wagtail docs on image sizing</a> Defaults to 'original'",
                                                    max_length=256,
                                                ),
                                            ),
                                        ],
                                        help_text="NB: Needs to match background colour (for now - working on a no-image variation)",
                                        required=True,
                                    ),
                                ),
                                ("success_title", wagtail.blocks.CharBlock(default="Thanks!", max_length=50)),
                                (
                                    "sucess_message",
                                    wagtail.blocks.CharBlock(
                                        default="If you haven’t previously confirmed a subscription to a Mozilla-related newsletter you may have to do so. Please check your inbox or your spam filter for an email from us.",
                                        max_length=200,
                                    ),
                                ),
                            ],
                            label="Newsletter signup form",
                            required=False,
                        ),
                    ),
                    (
                        "custom_form",
                        wagtail.blocks.StructBlock(
                            [
                                ("form", wagtailstreamforms.blocks.FormChooserBlock()),
                                (
                                    "form_action",
                                    wagtail.blocks.CharBlock(
                                        help_text='The form post action. "" or "." for the current page or a url', required=False
                                    ),
                                ),
                                (
                                    "form_reference",
                                    wagtailstreamforms.blocks.InfoBlock(
                                        help_text="This form will be given a unique reference once saved", required=False
                                    ),
                                ),
                            ],
                            icon="radio-empty",
                            required=False,
                        ),
                    ),
                ],
                use_json_field=True,
            ),
        ),
    ]
