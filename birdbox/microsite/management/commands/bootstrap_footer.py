#!/usr/bin/env python
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import json
import os
from sys import stdout

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.transaction import atomic

from wagtail.blocks import ListBlock
from wagtail.blocks.list_block import ListValue
from wagtail.core.rich_text import RichText

from microsite.blocks import FooterSocialLinkBlock, LabelledLinkBlock
from microsite.models import Footer


def _print(*args):
    stdout.write("\n".join(args) + "\n")


class DryRunException(Exception):
    pass


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "--commit",
            action="store_true",
            help="Commit changes to the Footer to the database. Without this, does a dry run that confirms the footer config file is OK.",
        )

    def handle(self, *args, **options):
        """
        Delete the existing Footer setting and replace it with
        a default set of content based on Mozilla.org
        """
        try:
            self._rebuild_footer(inert=not options["commit"])
        except DryRunException as e:
            spacer = "*" * 64
            _print(spacer, e.args[0], spacer)

    def _pprint_data(self, sv):
        collected = []
        for block in sv:
            for key, value in block.value.items():
                if type(value) == ListValue:
                    collected.append(f"{key}: \n")
                    for val in value:
                        collected.append(" ".join([f"{k}: {v} |" for k, v in val.items() if v]))
                        collected.append("\n")
                else:
                    collected.append(f"\n{key}: {value}\n")

        return "".join(collected)

    @atomic
    def _rebuild_footer(self, inert):
        if inert:
            _print("No --commit parameter passed. No changes will be stored")

        result = Footer.objects.all().delete()
        if result[0] > 0:
            message = "Deleted existing Footer in order to replace it"
            _print("=" * len(message), message, "=" * len(message))
        else:
            message = "No existing Footer record found in the database"
            _print("=" * len(message), message, "=" * len(message))

        footer_data_path = os.path.join(
            settings.PROJECT_DIR,
            "../data/footer/mozilla.json",
        )
        _print(f"Loading footer data from {footer_data_path}", "=" * 90)

        # Load the data from a JSON file that's based on a peek at the
        # JSONField data in the DB after manually adding a couple of entries

        with open(footer_data_path) as fp:
            data = json.loads(fp.read())

        footer = Footer()

        for column_data in data["columns"]:
            lv = ListValue(ListBlock(LabelledLinkBlock()))
            for item in column_data["value"]["links"]:
                lv.append(item["value"])
            footer.columns.append(
                (
                    "grouped_links",
                    {
                        "title": column_data["value"]["title"],
                        "links": lv,
                    },
                )
            )

        for social_data in data["social_links"]:
            lv = ListValue(ListBlock(FooterSocialLinkBlock()))
            for item in social_data["value"]["links"]:
                lv.append(item["value"])
            footer.social_links.append(
                (
                    "socials",
                    {
                        "title": social_data["value"]["title"],
                        "links": lv,
                    },
                )
            )

        for aftermatter_data in data["aftermatter"]:
            lv = ListValue(ListBlock(LabelledLinkBlock()))
            for item in aftermatter_data["value"]["links"]:
                lv.append(item["value"])
            footer.aftermatter.append(
                (
                    "content",
                    {"links": lv, "legal_text": RichText(aftermatter_data["value"]["legal_text"])},
                )
            )

        footer.save()

        footer.refresh_from_db()  # just to be sure
        _print("\nData loaded:\n")
        _print("Columns", self._pprint_data(footer.columns))
        _print("Social links", self._pprint_data(footer.social_links))
        _print("Aftermatter", self._pprint_data(footer.aftermatter))

        if inert:
            # Because this method is decorated with @atomic we can throw
            # an exeception here to trigger a rollback
            raise DryRunException("Not committing changes - dry run only")
