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


# PICK UP HERE PREFIXING THE CLASSNAMES WITH mzp-t-light or mzp-t-dark


DEFAULT_THEMED_COLOR_CLASSNAMES = "mzp-t-light"


def _get_themed_color_options():
    return (
        (DEFAULT_THEMED_COLOR_CLASSNAMES, "White"),
        ("mzp-t-dark", "Black/Ink"),
        ("mzp-t-light bb-t-light-color-01", "Light Gray"),
        ("mzp-t-dark bb-t-dark-color-01", "Dark Gray"),
        ("mzp-t-light bb-t-light-color-02", "Pink"),
        ("mzp-t-dark bb-t-dark-color-02", "Red"),
        ("mzp-t-light bb-t-light-color-03", "Light Yellow"),
        ("mzp-t-dark bb-t-dark-color-03", "Dark Yellow"),
        ("mzp-t-light bb-t-light-color-04", "Light Orange"),
        ("mzp-t-dark bb-t-dark-color-04", "Dark Orange"),
        ("mzp-t-light bb-t-light-color-05", "Light Green"),
        ("mzp-t-dark bb-t-dark-color-05", "Dark Green"),
        ("mzp-t-light bb-t-light-color-06", "Light Blue"),
        ("mzp-t-dark bb-t-dark-color-06", "Dark Blue"),
        ("mzp-t-light bb-t-light-color-07", "Light Violet"),
        ("mzp-t-dark bb-t-dark-color-07", "Dark Violet"),
    )


class ThemedColorBlock(blocks.ChoiceBlock):
    choices = _get_themed_color_options()
    default = DEFAULT_THEMED_COLOR_CLASSNAMES
