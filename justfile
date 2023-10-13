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

compile-requirements:
	./bin/compile-requirements.sh

docker-compile-requirements: build-python-builder
    docker-compose run compile-requirements

createsuperuser:
    python birdbox/manage.py createsuperuser

run-local:
    npm start

collectstatic:
	python birdbox/manage.py collectstatic --no-input

djshell:
	python birdbox/manage.py shell

docker-shell:
    docker-compose exec app bash

docker-manage-py *ARGS:
    docker-compose exec app python birdbox/manage.py {{ARGS}}

install-local-python-deps:
	pip install -r requirements/production.txt
	pip install -r requirements/dev.txt
	pip install -r requirements/test.txt

docker-preflight:
	docker-compose exec app python birdbox/manage.py createcachetable
	docker-compose exec app python birdbox/manage.py migrate

preflight:
	npm install
	{{JUST}} install-local-python-deps
	python birdbox/manage.py createcachetable
	python birdbox/manage.py migrate

showmigrations *ARGS:
	python birdbox/manage.py showmigrations {{ARGS}}

makemigrations *ARGS:
	python birdbox/manage.py makemigrations {{ARGS}}

migrate *ARGS:
	python birdbox/manage.py migrate {{ARGS}}

make-superuser:
	python birdbox/manage.py createsuperuser

manage-py *ARGS:
    python birdbox/manage.py {{ARGS}}

test *ARGS:
    echo "If these tests fail, complaining about missing statics, run 'just collectstatic' first"
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
	@echo "  clean-local-deps                 - uninstall Python dependencies. Not for Docker"
	@echo "  collectstatic                    - locally, run collectstatic. Not for Docker"
	@echo "  compile-requirements             - update Python requirements files directly on your machine"
	@echo "  createsuperuser                  - bootstrap a Django admin user. Not for Docker"
	@echo "  createsuperuser                  - locally, create a superuser to log in with. Not for Docker"
	@echo "  djshell                          - run a local Django shell. Not for Docker"
	@echo "  docker-compile-requirements      - update Python requirements files via Docker"
	@echo "  docker-manage-py SOME_COMMAND    - run manage.py SOME_COMMAND in an already running Docker container"
	@echo "  docker-preflight                 - install essentials in the Docker container before running"
	@echo "  docker-shell                     - start a bash shell in an already running Docker container"
	@echo "  export-local-data                - export LOCAL sqlite DB and media for loading elsewhere. Not for Docker"
	@echo "  import-local-data                - import LOCAL sqlite DB and media from elsewhere. Not for Docker"
	@echo "  install-local-python-deps        - install Python requirements"
	@echo "  makemigrations                   - make new Django migrations if needed. Not for Docker"
	@echo "  manage-py                        - run manage.py SOME_COMMAND on your onw machine"
	@echo "  migrate                          - apply Django migrations if needed. Not for Docker"
	@echo "  preflight                        - install essentials before running. Not for Docker"
	@echo "  run-local                        - run the site locally using webpack, watching and recompiling CSS and JS"
	@echo "  showmigrations                   - show state of Django migrations. Not for Docker"
	@echo "  test                             - run all tests that can be run locally. Not for Docker"
