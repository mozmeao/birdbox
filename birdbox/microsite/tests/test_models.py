# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from unittest import mock

from django.test import override_settings

import pytest

from microsite.models import (
    CacheAwareAbstractBasePage,
    GeneralPurposePage,
    HomePage,
    StructuralPage,
)


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


@pytest.mark.django_db
@pytest.mark.parametrize(
    "config, page_class, success_expected",
    (
        ("__all__", GeneralPurposePage, True),  # same as default
        ("microsite.InnovationsContentPage,microsite.StructuralPage,microsite.GeneralPurposePage", StructuralPage, True),
        ("microsite.GeneralPurposePage", GeneralPurposePage, True),
        ("microsite.GeneralPurposePage,microsite.InnovationsContentPage", GeneralPurposePage, True),
        ("microsite.InnovationsContentPage,microsite.GeneralPurposePage", GeneralPurposePage, True),
        ("microsite.InnovationsContentPage,microsite.SomeOtherPageClass", GeneralPurposePage, False),
        ("microsite.SomeOtherPageClass", GeneralPurposePage, False),
        ("microsite.InnovationsContentPage,microsite.SomeOtherPageClass", StructuralPage, False),
    ),
)
def test_can_create_at(
    config,
    page_class,
    success_expected,
    bootstrap_minimal_site,
):
    home_page = HomePage.objects.get()
    with override_settings(ALLOWED_PAGE_MODELS=config.split(",")):
        assert page_class.can_create_at(home_page) == success_expected
