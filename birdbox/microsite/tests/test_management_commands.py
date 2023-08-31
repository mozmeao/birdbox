# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.core.management import call_command

import pytest

from microsite.models import Footer


@pytest.mark.django_db
def test_bootstrap_footer__needs_commit_arg():
    assert Footer.objects.count() == 0
    call_command("bootstrap_footer", commit=False)
    assert Footer.objects.count() == 0
    call_command("bootstrap_footer")
    assert Footer.objects.count() == 0


@pytest.mark.django_db
def test_bootstrap_footer__max_count():
    assert Footer.objects.count() == 0
    call_command("bootstrap_footer", commit=True)
    assert Footer.objects.count() == 1
    footer1 = Footer.objects.get()

    call_command("bootstrap_footer", commit=True)
    assert Footer.objects.count() == 1
    footer2 = Footer.objects.get()
    assert footer1 != footer2


@pytest.mark.django_db
def test_bootstrap_footer__smoke_test():
    assert Footer.objects.count() == 0
    call_command("bootstrap_footer", commit=True)
    assert Footer.objects.count() == 1

    footer = Footer.objects.get()

    assert footer.display_footer is True

    assert footer.columns[0].value["title"] == "Company"
    assert footer.columns[1].value["title"] == "Resources"
    assert footer.columns[2].value["title"] == "Support"
    assert footer.columns[3].value["title"] == "Developers"

    # spot check
    assert len(footer.columns[3].value["links"]) == 7
    fifth_link = footer.columns[3].value["links"][4]
    assert fifth_link.get("external_url") == "https://www.mozilla.org/firefox/channel/android/#nightly"
    assert fifth_link.get("label") == "Firefox Nightly for Android"
    assert fifth_link.get("page") is None
    assert fifth_link.get("rel") is None
