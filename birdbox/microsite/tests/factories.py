# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import wagtail_factories

from microsite import models


class HomePageFactory(wagtail_factories.PageFactory):
    title = "Test Home Page"

    class Meta:
        model = models.HomePage
