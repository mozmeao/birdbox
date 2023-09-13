# Birdbox

A system to create a quick-deploy, easily customisable, CMS-backed microsite service

STATUS: Very much WIP

LICENSE: [Mozilla Public License Version 2.0](LICENSE)

----

## Running locally, for development of Birdbox itself

### Directly on your machine

_This mode uses sqlite for the DB and stores uploaded media on your machine_

* Install the `just` taskrunner (Docs [here](https://github.com/casey/just); spoiler: `brew install just`)
* Check out the repo
* `cd` path/to/birdbox
* Create then activate a virtual environment (`pyenv` + `pyenv-virtualenv` is recommended, but not required - see [Bedrock docs](https://bedrock.readthedocs.io/en/latest/install.html#local-installation) for installation details)

    ```
    pyenv virtualenv 3.10 birdbox
    pyenv activate birdbox
    ```

* `just preflight` to install Python and JS dependencies, run migrations (against a simple SQLite DB for local dev), create a cache table
* To make an admin user `just createsuperuser`
* To run the local webpack bundler + django runserver: `just run-local` or `npm start` (both do the same thing)
* Go to http://localhost:8000 for the default Wagtail site, and http://localhost:8000/admin/ for the CMS UI
* Ideally you will now load in set of sample pages - see Local development tips, below

Main Wagtail admin/editor docs are at https://guide.wagtail.org/en-latest/


### On your machine, via Docker

We expect most active development to happen directly on 'bare metal' but it's possible to build  and use Docker containers to run Birdbox locally, avoiding the virtualenv and local dependency steps.

Dockerized Birdbox uses a separate Postgres container for its database, not sqlite, so does not (currently) support the exporting and importing of local state.

* Install the `just` taskrunner (Docs [here](https://github.com/casey/just); spoiler: `brew install just`)
* Have Docker desktop and Docker Compose installed
* Check out the repo
* `cd` path/to/birdbox
* Build the needed containers: `docker-compose build assets app`
* Run the app container: `docker-compose up app` then go to http://localhost:8080 -- note that at the moment you'll start with the default, empty, Wagtail site

To run commands in the docker containers, there are a couple of convenience helpers:

* `just docker-preflight` - the same preflighting steps as for local, just run in Docker
* `just docker-shell` - run a bash shell in an already-running Docker container
* `just docker-manage-py SOME_COMMAND` - run Django's manage.py script in the already-running docker container, with SOME_COMMAND passed as extra args. e.g. `just docker-manage-py makemigrations`

To that end, if you're setting up a new Docker build locally, you'll want to do the following just
to get Wagtail running, but with no content. This is the equivalent of `just preflight`:

```
just docker-preflight
just docker-manage-py createsuperuser
just docker-manage-py bootstrap_footer
```

#### Cloud storage with local Docker build

When using Docker locally, it's possible to configure birdbox to use cloud storage, as we do on a deployed site.

To do this, copy ./docker/envfiles/local.env.example as local.env and add the relevant env vars. The link in the example file to Django-storages documentation shows what to set and also links to how to get the GCS credentials. For local use of Docker with GCS, you'll need to put those credentiuals somewhere that the Docker container can reach them - that's what the local-credentials directory is for: copy the relevant JSON credentials into there and update the  `GOOGLE_APPLICATION_CREDENTIALS` var in `local.env`` file to match.

Once that's done, it should Just Work.


## Deployment instructions

TO COME

## Real-world use instructions

(i.e. making a new site using Birdbox as a template project)

TO COME

----

## Local development tips

### How To: import and export local data

For local development, we use sqlite as our database, in part because it makes it easier to give another developer a copy of your state, which they can load in to be able to work with the same content you have. This is particularly useful for code review.

(Note that it's not just the database we need to share around: we also need media files that line up with the records in the relevant DB table.)

1. To export a zip file of your local DB and images:

    `just export-local-data`

    ...and note where the zip file is generated. Send that file to a colleague as needed. Note that it is zipped but not password-protected.

2. To load in a zip file of DB and image data

    `just import-local-data /path/to/file.zip`

    This will replace your DB file and load in all the images, overwriting existing files. Note that it does not drop image files that aren't in the zip of data.


----
## How To: Add a new StreamField component based on a Protocol component

(This assumes you know your way around Wagtail - if not, please at least review the [Wagtail quick start](https://docs.wagtail.org/en/stable/getting_started/index.html))

1. Define a new block in Python in `microsite/blocks.py` with the fields/content items that the Protocol component needs (eg title, description, image)
2. Add a new HTML template fragment for the new block in `microsite/templates/blocks/`
    * Base the markup on the HTML in the Protocol docs' examples
    * Remember to circle back and reference the template in the Python block definition
3. If JS or CSS is needed for the component, configure webpack to build it - see `src/css/protocol/card.scss` as an example
    * Remember to circle back to the Python nlock definition to set the `frontend_media` property so that this CSS/JS gets included when needed
4. Find the page (in `microsite.models`) with a StreamField that you want the new component to be available in. Add it to the list of blocks that are available.
5. `make makemigrations` then `make migrate` to get the DB up to speed
6. In the Wagtail CMS admin, amend an instance of the relevant page to use your new block - you should be able to see it in the live preview. Usually it takes a bit of tweaking to get the page to look as you intend.
7. If you need to add custom CSS to override what's in Protocol, add to `src/css/birdbox-protocol-overrides.css`

----

