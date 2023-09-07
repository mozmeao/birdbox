#!/bin/bash
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

# use honcho to inject the proper env vars
honcho run --env docker/envfiles/prod.env ./bin/sync-all.sh
