# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from typing import Dict, List, Optional

from django.template.loader import render_to_string

from bs4 import BeautifulSoup
from wagtail.embeds.finders.oembed import OEmbedFinder
from wagtail.embeds.oembed_providers import youtube


class YouTubeNoCookieEmbedFinder(OEmbedFinder):
    """
    EmbedFinder that ensures YouTube videos are embedded on the
    youtube-nocookie.com domain for greater privacy
    """

    template_name = "common/partials/_youtube_nocookie_embed.html"

    def __init__(
        self,
        providers: Optional[List[Dict]] = None,
        options: Optional[Dict] = None,
    ):
        super().__init__(
            # Force the provider to YT only; ignore inputs,
            # but keep supporting options
            providers=[youtube],
            options=options,
        )

    def _get_cookieless_embed_html(self, embed_html, title, original_url):
        """Replace the oembed-generated iframe with one we control more,
        and ensure it's using the youtube-nocookie.com domain"""

        # NB: no try/except here. This is called during the page building/editing
        # step, so we want this to fail hard, to stop bad embeds being used/published

        # We could work out the embed URL from the original, but it's in the iframe,
        # so we might as well get it and reuse it in the replacement iframe contnent

        soup = BeautifulSoup(
            embed_html,
            features="html5lib",  # Wagtail requires html5lib, so it'll be available
        )
        iframe_tag = soup.find_all("iframe")
        embed_url = iframe_tag[0]["src"]

        # drop all querystrings
        embed_url = embed_url.split("?")[0]

        # swap the domain for a cookieless one
        embed_url = embed_url.replace(
            "youtube.com",
            "youtube-nocookie.com",
        )

        return render_to_string(
            self.template_name,
            {
                "embed_url": embed_url,
                "embed_title": title,
                "original_url": original_url,
            },
        ).strip()

    def find_embed(self, *args: List, **kwargs: Dict) -> Dict:
        # Call the Oembed endpoint to get the data we need (specifically: title,
        # video embed URL in an iframe, thumbnail url (in the future)), but then
        # rejig the HTML to be a stripped-back, cookieless embed.
        result = super().find_embed(*args, **kwargs)

        # Relevant keys in `result`: html, thumbnail_url, title

        if "html" in result:
            result["html"] = self._get_cookieless_embed_html(
                embed_html=result["html"],
                title=result["title"],
                original_url=args[0],
            )
        return result
