#!/bin/bash

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

# Bundling a few apt-get commands to grease the wheels and save some space

set -e

apt-get update
apt-get install -y --no-install-recommends "$@"
rm -rf /var/lib/apt/lists/*
