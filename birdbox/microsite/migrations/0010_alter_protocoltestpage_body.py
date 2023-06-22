# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

# Generated by Django 4.1.9 on 2023-06-22 21:58

from django.db import migrations

import wagtail.blocks
import wagtail.fields
import wagtail.images.blocks


class Migration(migrations.Migration):
    dependencies = [
        ("microsite", "0009_alter_protocoltestpage_body"),
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
                                                            ("alt_text", wagtail.blocks.CharBlock(max_length=250, required=False)),
                                                            ("decorative_only", wagtail.blocks.BooleanBlock(default=False)),
                                                        ],
                                                        required=False,
                                                    ),
                                                ),
                                                ("tag", wagtail.blocks.CharBlock(max_length=48, required=False)),
                                            ]
                                        )
                                    ),
                                ),
                            ],
                            label="Card group",
                            required=False,
                        ),
                    ),
                ],
                use_json_field=True,
            ),
        ),
    ]
