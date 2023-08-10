#!/bin/bash

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

# IMPORTANT: RUN THIS FROM THE ROOT DIRECTORY ideally as `just import-packaged-data-to-local`

set -xeuo pipefail

# TODO: handle running from the non-ideal working dir

ZIP_FILE_PATH=$1

if [[ ! -f "$ZIP_FILE_PATH" ]];
then
    echo "Missing mandatory arguments: path to zip of exported data."
    exit 1
fi

BIRDBOX_ARCHIVE_REGEX="^[\w\d\_\/\~]*\/(birdbox_\d*)\.zip$"

BIRDBOX_ROOT_DIR=$(pwd)

DB_PATH_ROOT="${BIRDBOX_ROOT_DIR}/birdbox/data/"
MEDIA_PATH="${BIRDBOX_ROOT_DIR}/birdbox/media/"

NOW=$(date +%s)

WORKING_PATH="/tmp/birdbox_incoming_${NOW}"

mkdir $WORKING_PATH

echo "Unzipping file to ${WORKING_PATH}"

unzip $ZIP_FILE_PATH -d $WORKING_PATH

echo "Copying files into your local project"

cp -v "${WORKING_PATH}/birdbox.sqlite3" $DB_PATH_ROOT
cp -Rv "${WORKING_PATH}/images" $MEDIA_PATH
cp -Rv "${WORKING_PATH}/original_images" $MEDIA_PATH

cd $BIRDBOX_ROOT_DIR

echo "All done"
