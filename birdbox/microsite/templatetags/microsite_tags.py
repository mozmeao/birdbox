# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.template import Library

from ..models import Footer

register = Library()


@register.inclusion_tag("microsite/partials/footer.html", takes_context=True)
def site_footer(context):
    request = context["request"]

    footer = Footer.load(request_or_site=request)
    if footer and not footer.display_footer:
        footer = None

    return {"footer": footer}
