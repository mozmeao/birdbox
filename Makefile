# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


all: help


clean-local-deps:
	pip freeze | xargs pip uninstall -y

compile-requirements:
	./bin/compile-requirements.sh

djshell:
	python birdbox/manage.py shell

install-local-python-deps:
	pip install -r requirements/production.txt

preflight:
	$ npm install
	${MAKE} install-local-python-deps
	python birdbox/manage.py createcachetable

makemigrations:
	python birdbox/manage.py makemigrations

migrate:
	python birdbox/manage.py migrate


help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo "  compile-requirements       - update Python requirements files"
	@echo "  clean-local-deps           - uninstall Python dependencies"
	@echo "  djshell                    - run a local Django shell"
	@echo "  install-local-python-deps  - install Python requirements"
	@echo "  preflight                  - install essentials before running"
	@echo "  makemigrations             - make new Django migrations if needed"
	@echo "  migrate                    - apply Django migrations if needed"

.PHONY: all clean-local-deps compile-requirements djshell help install-local-python-deps makemigrations migrate preflight
