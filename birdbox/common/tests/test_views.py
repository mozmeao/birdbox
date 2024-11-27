# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.conf import settings
from django.test import override_settings
from django.urls import path, reverse

import pytest
from django_ratelimit.exceptions import Ratelimited

from common.views import rate_limited

# Make the rate_limited view available to this test only without needing DEBUG=True.
urlpatterns = [
    path(
        r"test-rate-limited/",
        rate_limited,
        {"exception": Ratelimited()},
        name="test-rl-view",
    )
]


@pytest.mark.urls(__name__)
@pytest.mark.django_db
def test_rate_limited__does_not_get_cached_at_cdn(client):
    resp = client.get(reverse("test-rl-view"))
    assert resp["Cache-Control"] == "max-age=0, no-cache, no-store, must-revalidate, private"


@pytest.mark.parametrize(
    "engage_robots,expected_content",
    (
        (True, b"User-agent: *\nAllow: /"),
        (False, b"User-agent: *\nDisallow: /"),
    ),
)
@pytest.mark.django_db
@pytest.mark.urls("birdbox.urls")
def test_robots_txt(client, engage_robots, expected_content):
    with override_settings(ENGAGE_ROBOTS=engage_robots):
        resp = client.get("/robots.txt")
        assert resp.content == expected_content


@pytest.mark.django_db
def test_csrf_view_is_custom_one():
    assert settings.CSRF_FAILURE_VIEW == "common.views.csrf_failure"


@pytest.mark.django_db
@pytest.mark.parametrize(
    "path",
    (
        "/builders/",
        "/builders/some/deeper/path/",
    ),
)
def test_builders_redirect(path, client):
    resp = client.get(path, follow=False)
    assert resp.headers["location"] == "https://builders.mozilla.org"


@pytest.mark.django_db
def test_builders_redirect_does_not_affect_anyting_else(client, minimal_site_with_blog):
    from microsite.models import BlogPage

    bp1, bp2_featured, bp3 = BlogPage.objects.live().all()

    resp = client.get(bp1.url, follow=False)
    assert resp.status_code == 200

    resp = client.get(bp2_featured.url, follow=False)
    assert resp.status_code == 200

    resp = client.get(bp3.url, follow=False)
    assert resp.status_code == 200
