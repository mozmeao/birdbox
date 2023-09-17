# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django import forms

from wagtail import blocks, blocks as wagtail_blocks
from wagtail.images import blocks as wagtailimages_blocks


class AccessibleImageBlockBase(wagtail_blocks.StructBlock):
    "Custom Image wrapper with increased a11y provision"
    image = wagtailimages_blocks.ImageChooserBlock(
        required=False,
    )
    alt_text = wagtail_blocks.CharBlock(
        label="Alt-text for this image",
        max_length=250,
        required=False,
    )
    decorative_only = wagtail_blocks.BooleanBlock(
        label="Is this image decorative only?",
        default=False,
        required=False,
    )

    class Meta:
        abstract = True


class AccessibleImageBlock(AccessibleImageBlockBase):
    pass


class ColorBlock(blocks.FieldBlock):
    def __init__(self, help_text=None, required=True, **kwargs):
        self.field = forms.CharField(
            help_text=help_text,
            max_length=7,
            required=required,
            widget=forms.TextInput(attrs={"type": "color"}),
        )
        super().__init__(**kwargs)
