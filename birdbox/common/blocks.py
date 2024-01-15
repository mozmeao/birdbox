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


DEFAULT_THEMED_COLOR_CLASSNAMES = "mzp-t-light bb-theme-monochrome"


def _get_themed_color_options():
    return (
        (DEFAULT_THEMED_COLOR_CLASSNAMES, "Default monochrome"),
        ("mzp-t-dark bb-theme-monochrome-inverse", "Inverse monochrome"),
        ("mzp-t-light bb-mzp-t-light-themed-color-1", "Light-theme color option 1"),
        ("mzp-t-light bb-mzp-t-light-themed-color-2", "Light-theme color option 2"),
        ("mzp-t-light bb-mzp-t-light-themed-color-3", "Light-theme color option 3"),
        ("mzp-t-light bb-mzp-t-light-themed-color-4", "Light-theme color option 4"),
        ("mzp-t-light bb-mzp-t-light-themed-color-5", "Light-theme color option 5"),
        ("mzp-t-dark bb-mzp-t-dark-themed-color-1", "Dark-theme color option 1"),
        ("mzp-t-dark bb-mzp-t-dark-themed-color-2", "Dark-theme color option 2"),
        ("mzp-t-dark bb-mzp-t-dark-themed-color-3", "Dark-theme color option 3"),
        ("mzp-t-dark bb-mzp-t-dark-themed-color-4", "Dark-theme color option 4"),
        ("mzp-t-dark bb-mzp-t-dark-themed-color-5", "Dark-theme color option 5"),
    )


class ThemedColorBlock(blocks.ChoiceBlock):
    choices = _get_themed_color_options()
    default = DEFAULT_THEMED_COLOR_CLASSNAMES
