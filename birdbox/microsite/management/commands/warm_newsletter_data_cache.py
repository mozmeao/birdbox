#!/usr/bin/env python
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from sys import stdout

from django.core.management.base import BaseCommand

from common.utils import get_freshest_newsletter_data


def _print(*args):
    stdout.write("\n".join(args) + "\n")


class Command(BaseCommand):
    def handle(self, *args, **options):
        _print("Warming cache with newsletter options")
        get_freshest_newsletter_data()
