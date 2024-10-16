########
# Python dependencies builder
#
FROM python:3.11-slim-bookworm AS python-builder

WORKDIR /app
ENV LANG=C.UTF-8
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/app/venv/bin:$PATH"

COPY docker/bin/apt-install.sh /usr/local/bin/
RUN apt-install.sh \
    build-essential \
    libpq-dev \
    libffi-dev \
    libjpeg62-turbo-dev \
    zlib1g-dev \
    libwebp-dev \
    imagemagick

RUN python -m venv /app/venv

COPY requirements/production.txt ./requirements/

# Install Python deps
RUN pip install --require-hashes --no-cache-dir -r requirements/production.txt


########
# assets builder and webpack dev server
#
FROM node:18-slim AS assets

ENV PATH=/app/node_modules/.bin:$PATH
WORKDIR /app

# copy dependency definitions
COPY package.json package-lock.json ./

# install dependencies
RUN npm ci

# copy supporting files and media
COPY .prettierignore webpack.config.js webpack.static.config.js ./
COPY ./src ./src

RUN npm run build


########
# django app container
#
FROM python:3.11-slim-bookworm AS app-base

# Extra python env
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV PATH="/app/venv/bin:$PATH"

# add non-priviledged user
RUN adduser --uid 1000 --disabled-password --gecos '' --no-create-home webdev

WORKDIR /app
EXPOSE 8000
CMD ["./bin/run.sh"]

COPY docker/bin/apt-install.sh /usr/local/bin/
RUN apt-install.sh gettext libxslt1.1 git curl

# copy in Python environment
COPY --from=python-builder /app/venv /app/venv

# changes infrequently
COPY ./bin ./bin
COPY ./docker ./docker
COPY LICENSE ./
# TODO: add newrelic.ini and contribute.json to the COPY below

# We don't have anything in the repo with this, but we need it for revision.txt
RUN mkdir ./root_files

# changes more frequently
COPY ./birdbox ./birdbox
COPY ./src ./src


########
# expanded webapp image for testing and dev
#
FROM app-base AS devapp

CMD ["./bin/run-tests.sh"]

COPY requirements/* ./requirements/
COPY ./pyproject.toml ./
RUN pip install --require-hashes --no-cache-dir -r requirements/dev.txt
RUN pip install --require-hashes --no-cache-dir -r requirements/test.txt

RUN bin/run-sync-all.sh

RUN chown webdev:webdev -R .

USER webdev

# build args
ARG GIT_SHA=latest
ENV GIT_SHA=${GIT_SHA}


########
# final image for deployment
#
FROM app-base AS release

RUN bin/run-sync-all.sh

COPY --from=assets /app/birdbox/birdbox/static/ /app/birdbox/birdbox/static/

RUN honcho run --env docker/envfiles/prod.env docker/bin/build_staticfiles.sh

# Change User
RUN chown webdev:webdev -R .
USER webdev

# build args
ARG GIT_SHA=latest
ENV GIT_SHA=${GIT_SHA}

RUN echo "${GIT_SHA}" > ./root_files/revision.txt
