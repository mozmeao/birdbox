# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


all: help


clean-local-deps:
	pip freeze | xargs pip uninstall -y

compile-requirements:
	./bin/compile-requirements.sh

install-local-python-deps:
	pip install -r requirements/production.txt

preflight:
	$ npm install
	${MAKE} install-local-python-deps

djserve:
	python birdbox/manage.py runserver


help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo "  compile-requirements   - update Python requirements files"

.PHONY: all clean-local-deps compile-requirements djserve djmanage help install-local-python-deps preflight
