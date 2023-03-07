# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


all: help

compile-requirements:
	./bin/compile-requirements.sh

help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo "  compile-requirements   - update Python requirements files"

.PHONY: all compile-requirements help
