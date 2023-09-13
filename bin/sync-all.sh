#!/bin/bash
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

./birdbox/manage.py createcachetable
./birdbox/manage.py migrate
./birdbox/manage.py warm_newsletter_data_cache
