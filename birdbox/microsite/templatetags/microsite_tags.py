# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.template import Library

from ..models import Footer, MicrositeSettings

register = Library()


@register.inclusion_tag("microsite/partials/footer.html", takes_context=True)
def site_footer(context):
    request = context["request"]

    footer = Footer.load(request_or_site=request)
    if footer and not footer.display_footer:
        footer = None

    return {"footer": footer}


@register.inclusion_tag("microsite/partials/global_css_tag.html", takes_context=True)
def global_css_tag(context):
    request = context["request"]
    microsite_settings = MicrositeSettings.load(request_or_site=request)
    filepath = f"css/protocol-{microsite_settings.site_theme}-theme.css"
    return {"filepath": filepath}


@register.inclusion_tag("microsite/partials/favicons.html", takes_context=True)
def favicon_links(context):
    request = context["request"]

    microsite_settings = MicrositeSettings.load(request_or_site=request)

    _base_path = f"img/favicons/{microsite_settings.site_theme}/"

    apple_icon_path = _base_path + "apple-touch-icon.png"
    large_favicon_path = _base_path + "favicon-196x196.png"
    favicon_path = _base_path + "favicon.ico"

    return {
        "apple_icon_path": apple_icon_path,
        "large_favicon_path": large_favicon_path,
        "favicon_path": favicon_path,
    }
