# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from copy import deepcopy
from unittest import mock

from common.embed import YouTubeNoCookieEmbedFinder


@mock.patch("common.embed.OEmbedFinder.find_embed")
def test_YouTubeNoCookieEmbedFinder_rewrites_embed(mock_find_embed):
    oembed_result = {
        "title": "Title of an example video from YouTube.",
        "author_name": "Example Author",
        "provider_name": "YouTube",
        "type": "video",
        "thumbnail_url": "https://i.ytimg.com/vi/ExampleVideoID/hqdefault.jpg",
        "width": 356,
        "height": 200,
        "html": '<iframe width="356" height="200" src="https://www.youtube.com/embed/ExampleVideoID?feature=oembed" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen title="Title of an example video from YouTube."></iframe>',  # noqa: E501
    }
    mock_find_embed.return_value = oembed_result
    finder = YouTubeNoCookieEmbedFinder()

    updated_result = finder.find_embed("https://www.youtube.com/watch/?v=ExampleVideoID")
    expected_result = deepcopy(oembed_result)

    expected_result[
        "html"
    ] = '<iframe allow="encrypted-media; fullscreen" allowfullscreen frameborder="0" src="https://www.youtube-nocookie.com/embed/ExampleVideoID" title="Title of an example video from YouTube."></iframe>'  # noqa: E501

    assert updated_result == expected_result


@mock.patch("common.embed.OEmbedFinder.find_embed")
def test_YouTubeNoCookieEmbedFinder_no_match_found(mock_find_embed):
    # Unlikely to happen, but covering the path
    mock_find_embed.return_value = {"no_html_key": "oh dear"}
    finder = YouTubeNoCookieEmbedFinder()
    updated_result = finder.find_embed("https://www.youtube.com/watch/?v=ExampleVideoID")
    assert updated_result == {"no_html_key": "oh dear"}
