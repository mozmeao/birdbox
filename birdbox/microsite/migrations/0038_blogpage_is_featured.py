# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

# Generated by Django 4.1.10 on 2023-07-17 09:29

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("microsite", "0037_alter_blogpage_feed_image"),
    ]

    operations = [
        migrations.AddField(
            model_name="blogpage",
            name="is_featured",
            field=models.BooleanField(
                default=False, help_text="Only one post be featured. If multiple are selected, the newest post wins, making switchover easier"
            ),
        ),
    ]
