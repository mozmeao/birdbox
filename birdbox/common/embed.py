# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from typing import Dict, List, Optional

from bs4 import BeautifulSoup
from wagtail.embeds.finders.oembed import OEmbedFinder
from wagtail.embeds.oembed_providers import youtube


class YouTubeNoCookieEmbedFinder(OEmbedFinder):
    """
    EmbedFinder that ensures YouTube videos are embedded on the
    youtube-nocookie.com domain for greater privacy
    """

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

    def _update_html(self, embed_html, original_url):
        """Replace the oembed-generated iframe with one we control more,
        and ensure it's using the youtube-nocookie.com domain"""

        soup = BeautifulSoup(embed_html, features="html5lib")

        # NB: no try/except here. This is called during the page building/editing
        # step, so we want this to fail hard, to stop bad embeds being used/published

        iframe_tag = soup.find_all("iframe")
        iframe_tag = iframe_tag[0]

        # We could work out the embed URL from the original, but it's in the iframe,
        # so we might as well get it and reuse it in the replacement iframe contnent
        src_attr = iframe_tag["src"]

        # drop all querystrings
        src_attr = src_attr.split("?")[0]
        # swap out the domain
        src_attr = src_attr.replace(
            "youtube.com",
            "youtube-nocookie.com",
        )
        iframe_tag["src"] = src_attr

        # Redefine only minimal permissions for iframe
        iframe_tag["allow"] = "fullscreen; encrypted-media"
        iframe_tag["allowfullscreen"] = ""

        # Also drop in a direct link into the iframe
        link_tag = soup.new_tag("a", href=original_url)
        link_tag.string = "Watch the video"  # TODO: mark up for L10N
        p_tag = soup.new_tag("p")
        p_tag.append(link_tag)
        return str(iframe_tag)

    def find_embed(self, *args: List, **kwargs: Dict) -> Dict:
        result = super().find_embed(*args, **kwargs)
        if "html" in result:
            result["html"] = self._update_html(
                embed_html=result["html"],
                original_url=args[0],
            )
        return result
