# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from unittest import mock

import pytest

from microsite.templatetags.microsite_tags import block_with_h1_exists_in_page


@mock.patch("microsite.templatetags.microsite_tags.find_streamfield_blocks_by_types")
@pytest.mark.django_db
@pytest.mark.parametrize(
    "mocked_helper_retval, expected",
    (
        ([], False),
        (["anything"], True),
        (["anything", "more-than-one-is-unexpected-but-truthy"], True),
    ),
)
def test_block_with_h1_exists_in_page(
    mock_find_streamfield_blocks_by_types,
    mocked_helper_retval,
    expected,
):
    mock_page = mock.Mock()
    mock_find_streamfield_blocks_by_types.return_value = mocked_helper_retval
    assert block_with_h1_exists_in_page(mock_page) == expected
