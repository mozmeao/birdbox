# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.templatetags.static import static
from django.utils.html import format_html_join
from django.utils.safestring import mark_safe

from wagtail import hooks


@hooks.register("insert_editor_js")
def patch_in_dynamic_theme_color_names():
    # Each theme has a set of custom/specific colors associated with it,
    # sharing the same CSS classnames, but varying based on theme.
    # microsite.blocks.ColorThemBlock has values which are the CSS classes to use
    # and, by default, the _label_ for each option is, basically, the CSS class
    # name. To make the editor experience better, we swap in theme-specific
    # human-friendly labels when the editing UI is rendered, based on the
    # theme selected for the birdbox site

    from microsite.models import MicrositeSettings

    try:
        settings = MicrositeSettings.objects.first()
        theme_name = settings.site_theme
    except AttributeError:
        theme_name = "mozilla"

    js_files = [
        "js/color-theme-block-labels.js",
    ]
    js_includes = format_html_join("\n", '<script src="{0}"></script>', ((static(filename),) for filename in js_files))

    return js_includes + mark_safe(
        """
        <script>
            window.addEventListener("DOMContentLoaded", () => {
                window.Birdbox.themeColorLabelFixup("%s");
            });
        </script>
        """
        % theme_name  # noqa: F522 F524  # Old-style formatting needed to avoid breaking hook rendering
    )
