# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

# Hyperlinks to the relevant Protcol component, so that we can easily reference them in help text in the CMS Admin

# Constants are named after the name they have in the sidbar of https://protocol.mozilla.org

from django.utils.safestring import mark_safe

links = {
    "layout": "https://protocol.mozilla.org/components/detail/content-container--default.html",
    "card-layout": "https://protocol.mozilla.org/components/detail/card-layout--overview.html",
    "card": "https://protocol.mozilla.org/components/detail/card--overview.html",
    "split": "https://protocol.mozilla.org/components/detail/split--default.html",
    "footer": "https://protocol.mozilla.org/components/detail/footer.html",
}


def get_docs_link(link_name):
    try:
        return mark_safe(f"<a href='{links[link_name.lower()]}'>See Protocol docs</a>.")
    except KeyError:
        return None
