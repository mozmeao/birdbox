#!/bin/bash

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

set -exo pipefail

# We need this installed, but we don't want it to live in the main requirements
# We will need to periodically review this pinning

pip install -U pip
pip install pip-tools
pip-compile --generate-hashes --no-header
