# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from unittest import mock

from django.test import override_settings

from microsite import context_processors


@override_settings(GOOGLE_TAG_ID="ThisIsATest")
def test_google_tag():
    assert context_processors.google_tag(mock.Mock()) == {
        "GOOGLE_TAG_ID": "ThisIsATest",
    }
