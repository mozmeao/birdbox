# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

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
