# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


JUST := just_executable()

all: help

clean-local-deps:
	pip freeze | xargs pip uninstall -y

compile-requirements:
	./bin/compile-requirements.sh

run-local:
    npm start

djshell:
	python birdbox/manage.py shell

install-local-python-deps:
	pip install -r requirements/production.txt

preflight:
	npm install
	{{JUST}} install-local-python-deps
	python birdbox/manage.py createcachetable
	python birdbox/manage.py migrate
	python birdbox/manage.py update_product_details

makemigrations ARGS:
	python birdbox/manage.py makemigrations {{ARGS}}

migrate:
	python birdbox/manage.py migrate

make-superuser:
	python birdbox/manage.py createsuperuser

export-local-data:
    ./bin/package-up-local-data.sh

import-local-data ARGS:
    ./bin/import-packaged-data-to-local.sh {{ARGS}}

help:
	@echo "Please use \`just <target>' where <target> is one of"
	@echo "  clean-local-deps           - uninstall Python dependencies"
	@echo "  compile-requirements       - update Python requirements files"
	@echo "  createsuperuser            - bootstrap a Django admin user"
	@echo "  djshell                    - run a local Django shell"
	@echo "  install-local-python-deps  - install Python requirements"
	@echo "  export-local-data          - export sqlite DB and media for loading elsewhere"
	@echo "  import-local-data          - import sqlite DB and media for loading elsewhere"
	@echo "  preflight                  - install essentials before running"
	@echo "  makemigrations             - make new Django migrations if needed"
	@echo "  migrate                    - apply Django migrations if needed"
