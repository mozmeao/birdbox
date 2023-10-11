# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import random
import string

from locust import between, task
from locust.contrib.fasthttp import FastHttpUser


def get_asset_paths(add_cachebreaker=False) -> list:
    """Return the JS and CSS bundle paths for the site -- at the moment we have
    no need for code splitting, etc

    While production uses django-whitenoise to serve files with a cachebreaking
    hash, the files are also available via their unhashed filename.
    If we want to, we can ask for them after appending a random cachebreaker
    param as a querystring to ensure we get a fresh set every time we run the
    load tests
    """

    if add_cachebreaker:
        cachebreaker = f"?v={random.random()}"
    else:
        cachebreaker = ""

    return [
        f"/static/js/protocol-base.js{cachebreaker}",
        f"/static/js/protocol-footer-js.js{cachebreaker}",
        f"/static/css/protocol-columns.css{cachebreaker}",
        f"/static/css/protocol-mozilla-theme.css{cachebreaker}",
        f"/static/css/protocol-footer-css.css{cachebreaker}",
    ]


def get_random_string(length=9):
    return "".join(random.choice(string.ascii_lowercase) for i in range(length))


class FutureMOQuickstartUser(FastHttpUser):
    wait_time = between(5, 9)

    @task(6)
    def view_homepage(self):
        self.client.get("/")
        for asset_path in get_asset_paths():
            self.client.get(asset_path)

    @task(4)
    def view_mieco_page(self):
        self.client.get("/mieco/")
        for asset_path in get_asset_paths():
            self.client.get(asset_path)

    @task(4)
    def view_builders_challenge(self):
        self.client.get("/builders-challenge/")
        for asset_path in get_asset_paths():
            self.client.get(asset_path)
