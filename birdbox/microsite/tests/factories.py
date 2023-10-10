# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import factory
import wagtail_factories

from microsite import models


class HomePageFactory(wagtail_factories.PageFactory):
    title = "Test Home Page"
    live = True
    slug = "homepage"

    class Meta:
        model = models.HomePage


class BlogIndexPageFactory(wagtail_factories.PageFactory):
    title = "Blog Index"
    live = True

    class Meta:
        model = models.BlogIndexPage


class BlogPageFactory(wagtail_factories.PageFactory):
    feed_image = factory.SubFactory(
        wagtail_factories.ImageChooserBlockFactory,
    )

    class Meta:
        model = models.BlogPage
