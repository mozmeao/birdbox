# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from typing import Dict, List

from django.template import Library
from django.template.loader import render_to_string

from microsite.models import Footer

from ..utils import get_frontend_media

register = Library()


@register.simple_tag(takes_context=True)
def frontend_media_for_page(context, page) -> Dict[str, List[str]]:
    """Gather the frontend CSS and JS associated with any Protocol-styled
    blocks in the page"""

    request = context["request"]

    css_files = []
    js_files = []

    if hasattr(page, "specific"):
        for media_obj in get_frontend_media(page.specific):
            css_files.extend(set([x for x in media_obj.render_css()]))
            js_files.extend(set([x for x in media_obj.render_js()]))

    # See if we need to gather footer media too
    footer = Footer.load(request_or_site=request)
    if footer and footer.display_footer:
        for media_obj in get_frontend_media(footer):
            css_files.extend(set([x for x in media_obj.render_css()]))
            js_files.extend(set([x for x in media_obj.render_js()]))

    return {
        "css": render_to_string(
            "templatetags/css_frontend_media.html",
            {
                "css_files": set(css_files),
            },
        ),
        "js": render_to_string(
            "templatetags/js_frontend_media.html",
            {
                "js_files": set(js_files),
            },
        ),
    }


@register.simple_tag
def get_alt_text_for_accessible_image_block(block_data):
    """Complements common.blocks.AccessibleImageBlock, which
    should be the block_data passed in.

    If the block is for a non-decorative image, we try to use custom
    alt-text, else fall back to the image's title, which is what
    Wagtail also uses by default"""

    retval = ""
    if not block_data.get("decorative_only"):
        retval = block_data.get("alt_text")
        if not retval:
            retval = getattr(block_data.get("image"), "title", "")
    return retval


@register.simple_tag
def gather_field_errors(form):
    errors = []
    for field in form.visible_fields():
        if field.errors:
            combined_errors = ";".join(field.errors)
            errors.append(f"{field.label}: {combined_errors}")

    return errors
