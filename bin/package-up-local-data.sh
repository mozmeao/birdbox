#!/bin/bash

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

# IMPORTANT: RUN THIS FROM THE ROOT DIRECTORY ideally as `just package-local-data`

set -euo pipefail

# TODO: handle running from the non-ideal working dir

ORIGINAL_DIR=$(pwd)

DB_PATH="./birdbox/data/birdbox.sqlite3"
MEDIA_PATH="./birdbox/media/"

NOW=$(date +%s)

OUTPUT_DIR="birdbox_${NOW}"
OUTPUT_PATH="/tmp/${OUTPUT_DIR}"

mkdir $OUTPUT_PATH

echo "Copying from ${DB_PATH} and ${MEDIA_PATH} to ${OUTPUT_PATH}"

cp -r $DB_PATH $OUTPUT_PATH
cp -r $MEDIA_PATH $OUTPUT_PATH

echo "Zipping ${OUTPUT_PATH}"

cd /tmp/
# Zip up all the files and subdirs but omit the actual parent dir:
(cd "${OUTPUT_DIR}/" && zip -r -8 "../${OUTPUT_DIR}.zip" .)

echo "The data bundle you need is at ${OUTPUT_PATH}.zip"

cd $ORIGINAL_DIR

echo "All done"
