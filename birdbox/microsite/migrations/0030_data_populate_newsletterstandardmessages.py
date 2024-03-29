# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

# Generated by Django 4.1.9 on 2023-07-06 21:03

from django.db import migrations


def forwards(apps, schema_editor):
    NewsletterStandardMessages = apps.get_model("microsite", "NewsletterStandardMessages")
    # Spin up a new record, with the default values from the model fields
    NewsletterStandardMessages.objects.get_or_create()


def backwards(apps, schema_editor):
    NewsletterStandardMessages = apps.get_model("microsite", "NewsletterStandardMessages")
    NewsletterStandardMessages.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ("microsite", "0029_newsletterstandardmessages"),
    ]

    operations = [migrations.RunPython(forwards, backwards)]
