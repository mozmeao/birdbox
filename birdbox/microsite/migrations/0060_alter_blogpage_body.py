# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

# Generated by Django 4.2.5 on 2023-09-15 13:37

from django.db import migrations

import wagtail.blocks
import wagtail.embeds.blocks
import wagtail.fields
import wagtail.images.blocks


class Migration(migrations.Migration):
    dependencies = [
        ("microsite", "0059_alter_footer_social_links"),
    ]

    operations = [
        migrations.AlterField(
            model_name="blogpage",
            name="body",
            field=wagtail.fields.StreamField(
                [
                    (
                        "blogtext",
                        wagtail.blocks.RichTextBlock(
                            features=["h2", "h3", "bold", "italic", "strikethrough", "code", "blockquote", "link", "ol", "ul"],
                            label="Text block for blog post",
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
                                ("width", wagtail.blocks.IntegerBlock(label="Specific image width in px (optional)", min_value=0, required=False)),
                                ("height", wagtail.blocks.IntegerBlock(label="Specific image height in px (optional)", min_value=0, required=False)),
                                (
                                    "rendition_spec",
                                    wagtail.blocks.CharBlock(
                                        blank=True,
                                        default="original",
                                        help_text="Lots of options available. See <a href='https://docs.wagtail.org/en/stable/topics/images.html#available-resizing-methods'>Wagtail docs on image sizing</a> Defaults to 'original'",
                                        max_length=256,
                                    ),
                                ),
                                ("image_caption", wagtail.blocks.CharBlock(max_length=250, required=False)),
                                ("image_credit", wagtail.blocks.CharBlock(max_length=250, required=False)),
                            ],
                            label="Mid-body image",
                            required=False,
                        ),
                    ),
                    (
                        "video",
                        wagtail.blocks.StructBlock(
                            [("video", wagtail.embeds.blocks.EmbedBlock(required=True))], label="Mid-body video", required=False
                        ),
                    ),
                ],
                use_json_field=True,
            ),
        ),
    ]
