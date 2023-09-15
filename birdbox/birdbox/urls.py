# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.utils.module_loading import import_string

# Disabled until we need Search
# from search import views as search_views
from wagtail import urls as wagtail_urls
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls

handler500 = "common.views.server_error_view"
handler404 = "common.views.page_not_found_view"

urlpatterns = [
    path("django-admin/", admin.site.urls),
    path("admin/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
    # Disabled until we need Search
    # path("search/", search_views.search, name="search"),
]


if settings.DEFAULT_FILE_STORAGE == "django.core.files.storage.FileSystemStorage":
    # Serve media files from Django itself - production won't use this
    from django.urls import re_path
    from django.views.static import serve

    urlpatterns = urlpatterns + [
        re_path(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
    ]
    # Note that statics are handled via Whitenoise's middleware

if settings.DEBUG:
    urlpatterns += (
        path("404/", import_string(handler404)),
        path("500/", import_string(handler500)),
    )


urlpatterns = urlpatterns + [
    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's page serving mechanism. This should be the last pattern in
    # the list:
    path("", include(wagtail_urls)),
    # Alternatively, if you want Wagtail pages to be served from a subpath
    # of your site, rather than the site root:
    #    path("pages/", include(wagtail_urls)),
]
