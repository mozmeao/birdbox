# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.utils.safestring import mark_safe

from wagtail import hooks


@hooks.register("insert_editor_js")
def patch_in_dynamic_theme_color_name():
    # Each theme has a set of custom/specific colors associated with it,
    # sharing the same CSS classnames, but varying based on theme.
    # common.blocks.ThemedColorBlock has values which are the CSS classes to use
    # and, by default, the _label_ for each option is, basically, the CSS class
    # name.
    # To make the editor experience better, we swap in theme-specific
    # human-friendly labels when the editing UI is rendered (see
    # common.blocks.ThemedColorBlockAdapter) based on the
    # theme selected for the birdbox site. This hook ensure the currently
    # selected theme is available as a data-attr on the `body` node

    from microsite.models import MicrositeSettings

    try:
        settings = MicrositeSettings.objects.first()
        theme_name = settings.site_theme
    except AttributeError:
        theme_name = "mozilla"

    return mark_safe(
        """
        <div id="bb-site-theme" data-site-theme="%s"></div>
        """
        % theme_name  # noqa: F522 F524  # Old-style formatting needed to avoid breaking hook rendering
    )
