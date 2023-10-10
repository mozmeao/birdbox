# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from datetime import date

import pytest
import wagtail_factories

from microsite.models import HomePage
from microsite.tests.factories import BlogIndexPageFactory, BlogPageFactory, HomePageFactory


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


@pytest.fixture
def homepage(bootstrap_minimal_site):
    return HomePage.objects.get()


@pytest.fixture
def minimal_site_with_blog(bootstrap_minimal_site):
    homepage = HomePage.objects.get()

    blog_index = BlogIndexPageFactory(
        parent=homepage,
    )

    BlogPageFactory(
        parent=blog_index,
        title="blog post 1",
        date=date(2023, 5, 1),
    )
    BlogPageFactory(
        parent=blog_index,
        title="blog post 2 (featured)",
        date=date(2023, 5, 11),
        is_featured=True,
    )
    BlogPageFactory(
        parent=blog_index,
        title="blog post 3",
        date=date(2023, 6, 12),
    )
