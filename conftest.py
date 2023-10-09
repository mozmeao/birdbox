# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import pytest
import wagtail_factories

from microsite.tests.factories import HomePageFactory


@pytest.fixture
def bootstrap_minimal_site(
    client,
    homepage=None,
):
    if homepage is None:
        homepage = HomePageFactory()

    return wagtail_factories.SiteFactory(
        root_page=homepage,
        hostname=client._base_environ()["SERVER_NAME"],
    )
