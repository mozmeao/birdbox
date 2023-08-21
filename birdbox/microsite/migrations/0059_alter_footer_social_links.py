# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

# Generated by Django 4.1.10 on 2023-08-31 19:11

from django.db import migrations

import wagtail.blocks
import wagtail.fields


class Migration(migrations.Migration):
    dependencies = [
        ("microsite", "0058_alter_footer_aftermatter_alter_footer_columns_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="footer",
            name="social_links",
            field=wagtail.fields.StreamField(
                [
                    (
                        "socials",
                        wagtail.blocks.StructBlock(
                            [
                                (
                                    "title",
                                    wagtail.blocks.CharBlock(
                                        label="Social links section title - e.g. 'Follow @mozilla'", max_length=50, required=False
                                    ),
                                ),
                                (
                                    "links",
                                    wagtail.blocks.ListBlock(
                                        wagtail.blocks.StructBlock(
                                            [
                                                (
                                                    "icon",
                                                    wagtail.blocks.ChoiceBlock(
                                                        choices=[
                                                            ("firefox", "Firefox"),
                                                            ("github", "Github"),
                                                            ("instagram", "Instagram"),
                                                            ("linkedin", "LinkedIn"),
                                                            ("mastodon", "Mastodon"),
                                                            ("pocket", "Pocket"),
                                                            ("spotify", "Spotify"),
                                                            ("tiktok", "TikTok"),
                                                            ("twitter", "Twitter"),
                                                            ("youtube", "YouTube"),
                                                        ]
                                                    ),
                                                ),
                                                ("url", wagtail.blocks.URLBlock(required=True)),
                                                (
                                                    "data_label",
                                                    wagtail.blocks.CharBlock(
                                                        help_text='Service name and handle - e.g. "Twitter (@mozilla)"', max_length=50, required=True
                                                    ),
                                                ),
                                                (
                                                    "rel",
                                                    wagtail.blocks.CharBlock(
                                                        help_text="Optional 'rel' attribute. If blank, no attribute will be set",
                                                        max_length=100,
                                                        required=False,
                                                    ),
                                                ),
                                            ]
                                        ),
                                        collapsed=False,
                                        label="Social links",
                                        max_num=6,
                                    ),
                                ),
                            ]
                        ),
                    )
                ],
                blank=True,
                help_text="Add an group of social links (optional)",
                null=True,
                use_json_field=True,
            ),
        ),
    ]
