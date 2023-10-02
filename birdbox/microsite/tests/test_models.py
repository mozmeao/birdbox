# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from unittest import mock

import pytest

from microsite.models import CacheAwareAbstractBasePage, HomePage


@mock.patch("microsite.models.HomePage.get_view_restrictions")
@pytest.mark.django_db
@pytest.mark.parametrize(
    "fake_restrictions, expected_headers",
    (
        ([], None),
        ([mock.Mock()], "max-age=0, no-cache, no-store, must-revalidate, private"),
    ),
)
def test_cache_control_headers_on_pages_with_view_restrictions(
    mock_get_view_restrictions,
    fake_restrictions,
    expected_headers,
    client,
    bootstrap_minimal_site,
):
    mock_get_view_restrictions.return_value = fake_restrictions

    page = HomePage.objects.get()  # made by the bootstrap_minimal_site fixture

    # Confirm we're using the base page
    assert isinstance(page, CacheAwareAbstractBasePage)

    response = client.get("/")

    assert response.get("Cache-Control") == expected_headers
