# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


from django.test import RequestFactory

import pytest

from microsite.models import BlogIndexPage, BlogPage

# Wondering where some of these arguments are coming from, they may be
# pytest fixtures declared in conftest.py


@pytest.mark.django_db
def test_live_vs_draft_blog_post_visibility__live_view(
    client,
    minimal_site_with_blog,
):
    index = BlogIndexPage.objects.get()

    bp1, bp2_featured, bp3 = BlogPage.objects.live().all()

    # Fake a request for live/non-preview viewing
    request = RequestFactory().get("/blog-index/")
    request.is_preview = False

    # 1. Show that all three are visible and in results
    context = index.get_context(request)
    assert context["featured_post"] == bp2_featured
    assert [x for x in context["non_featured_posts"]] == [bp3, bp1]

    # 2. Make the featured one draft
    bp2_featured.unpublish()
    bp2_featured.save()
    context = index.get_context(request)
    assert context["featured_post"] is None
    assert [x for x in context["non_featured_posts"]] == [bp3, bp1]

    # 3. Make a different one draft
    bp1.unpublish()
    bp1.save()
    context = index.get_context(request)
    assert context["featured_post"] is None
    assert [x for x in context["non_featured_posts"]] == [bp3]


@pytest.mark.django_db
def test_live_vs_draft_blog_post_visibility__draft_view(
    client,
    minimal_site_with_blog,
):
    index = BlogIndexPage.objects.get()

    bp1, bp2_featured, bp3 = BlogPage.objects.live().all()

    # Fake a request for PREVIEW viewing
    request = RequestFactory().get("/blog-index/")
    request.is_preview = True

    # 1. Show that all three are visible and in results
    context = index.get_context(request)
    assert context["featured_post"] == bp2_featured
    assert [x for x in context["non_featured_posts"]] == [bp3, bp1]

    # 2. Make the featured one draft - should remain visible
    bp2_featured.unpublish()
    bp2_featured.save()
    context = index.get_context(request)
    assert context["featured_post"] == bp2_featured
    assert [x for x in context["non_featured_posts"]] == [bp3, bp1]

    # 3. Make a different one draft - still should be visible
    bp1.unpublish()
    bp1.save()
    context = index.get_context(request)
    assert context["featured_post"] == bp2_featured
    assert [x for x in context["non_featured_posts"]] == [bp3, bp1]
