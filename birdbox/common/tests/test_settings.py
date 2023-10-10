# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.conf import settings

import pytest

from birdbox.settings.base import set_whitenoise_headers


@pytest.mark.parametrize(
    "input_headers, input_url, input_path, expected_headers",
    (
        (
            {},
            "/static/images/file.png",
            "local/file/path.jpg",
            {"Cache-Control": "public, max-age=30758400"},
        ),
        (
            {},
            "/media/file.png",
            "local/media/files/file.png",
            {},
        ),
        (
            {"special": "header-not-to-be-touched"},
            "/media/file.png",
            "local/media/files/file.png",
            {"special": "header-not-to-be-touched"},
        ),
        (
            {"special": "header-not-to-be-touched"},
            "/static/images/file.png",
            "local/file/path.jpg",
            {
                "special": "header-not-to-be-touched",
                "Cache-Control": "public, max-age=30758400",
            },
        ),
    ),
    ids=[
        "Static gets long cache time",
        "Media (which should be irrelevant to whitenoise) is skipped anyway",
        "Other headers are not touched",
        "Statics get cache header added to existing ones",
    ],
)
def test_set_whitenoise_headers(
    input_headers,
    input_url,
    input_path,
    expected_headers,
):
    set_whitenoise_headers(
        headers=input_headers,
        path=input_path,
        url=input_url,
    )
    assert input_headers == expected_headers


def test_whitenoise_add_headers_is_set():
    assert settings.WHITENOISE_ADD_HEADERS_FUNCTION == set_whitenoise_headers
