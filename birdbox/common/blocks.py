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
    # DEPRECATED. Historic Migrations need updating when/if we remove this custom block
    def __init__(self, help_text=None, required=True, **kwargs):
        self.field = forms.CharField(
            help_text=help_text,
            max_length=7,
            required=required,
            widget=forms.TextInput(attrs={"type": "color"}),
        )
        super().__init__(**kwargs)


DEFAULT_THEMED_COLOR_CLASSNAME = "mzp-t-light"


class ThemedColorBlock(blocks.ChoiceBlock):
    choices = (
        (DEFAULT_THEMED_COLOR_CLASSNAME, DEFAULT_THEMED_COLOR_CLASSNAME),
        ("mzp-t-dark", "mzp-t-dark"),
        ("mzp-t-light bb-t-light-color-01", "bb-t-light-color-01"),
        ("mzp-t-dark bb-t-dark-color-01", "bb-t-dark-color-01"),
        ("mzp-t-light bb-t-light-color-02", "bb-t-light-color-02"),
        ("mzp-t-dark bb-t-dark-color-02", "bb-t-dark-color-02"),
        ("mzp-t-light bb-t-light-color-03", "bb-t-light-color-03"),
        ("mzp-t-dark bb-t-dark-color-03", "bb-t-dark-color-03"),
        ("mzp-t-light bb-t-light-color-04", "bb-t-light-color-04"),
        ("mzp-t-dark bb-t-dark-color-04", "bb-t-dark-color-04"),
        ("mzp-t-light bb-t-light-color-05", "bb-t-light-color-05"),
        ("mzp-t-dark bb-t-dark-color-05", "bb-t-dark-color-05"),
        ("mzp-t-light bb-t-light-color-06", "bb-t-light-color-06"),
        ("mzp-t-dark bb-t-dark-color-06", "bb-t-dark-color-06"),
        ("mzp-t-light bb-t-light-color-07", "bb-t-light-color-07"),
        ("mzp-t-dark bb-t-dark-color-07", "bb-t-dark-color-07"),
    )
    default = DEFAULT_THEMED_COLOR_CLASSNAME
