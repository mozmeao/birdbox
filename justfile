# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


JUST := just_executable()

all: help

build-python-builder:
    # build the lowest-level Docker image in our multi-stage build
    docker-compose build builder

clean-local-deps:
	pip freeze | xargs pip uninstall -y

compile-requirements: build-python-builder
    docker-compose run compile-requirements

compile-requirements-locally:
	./bin/compile-requirements.sh

run-local:
    npm start

djshell:
	python birdbox/manage.py shell

install-local-python-deps:
	pip install -r requirements/production.txt
	pip install -r requirements/test.txt

preflight:
	npm install
	{{JUST}} install-local-python-deps
	python birdbox/manage.py createcachetable
	python birdbox/manage.py migrate
	python birdbox/manage.py update_product_details

makemigrations *ARGS:
	python birdbox/manage.py makemigrations {{ARGS}}

migrate:
	python birdbox/manage.py migrate

make-superuser:
	python birdbox/manage.py createsuperuser

test *ARGS:
    DJANGO_SETTINGS_MODULE=birdbox.settings.test \
    BASKET_NEWSLETTER_DATA_DO_SYNC=false \
        pytest birdbox {{ARGS}} \
        --cov-config=.coveragerc \
        --cov-report=html \
        --cov-report=term-missing \
        --cov-report=xml:python_coverage/coverage.xml \
        --cov=.


export-local-data:
    ./bin/package-up-local-data.sh

import-local-data ARGS:
    ./bin/import-packaged-data-to-local.sh {{ARGS}}

help:
	@echo "Please use \`just <target>' where <target> is one of"
	@echo "  clean-local-deps               - uninstall Python dependencies"
	@echo "  compile-requirements           - update Python requirements files via Docker"
	@echo "  compile-requirements-locally   - update Python requirements files directly on your machine"
	@echo "  createsuperuser                - bootstrap a Django admin user"
	@echo "  djshell                        - run a local Django shell"
	@echo "  install-local-python-deps      - install Python requirements"
	@echo "  export-local-data              - export sqlite DB and media for loading elsewhere"
	@echo "  import-local-data              - import sqlite DB and media for loading elsewhere"
	@echo "  preflight                      - install essentials before running"
	@echo "  makemigrations                 - make new Django migrations if needed"
	@echo "  migrate                        - apply Django migrations if needed"
	@echo "  test                           - run all tests that can be run locally"