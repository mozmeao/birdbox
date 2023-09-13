#!/bin/bash

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

set -exo pipefail

python birdbox/manage.py collectstatic --noinput --clear

# See Bedrock's build_staticfiles.sh if we want to link unhashed to hashed to
# reduce Docker image space
