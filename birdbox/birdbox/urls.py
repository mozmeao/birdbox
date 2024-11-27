# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.conf import settings
from django.contrib import admin
from django.http import HttpResponse, HttpResponseForbidden
from django.urls import include, path, re_path
from django.utils.module_loading import import_string
from django.views.defaults import permission_denied

from django_ratelimit.exceptions import Ratelimited

# Disabled until we need Search
# from search import views as search_views
from wagtail import urls as wagtail_urls
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls
from watchman import views as watchman_views

from common.views import csrf_failure, rate_limited, redirect_view
from microsite import urls as microsite_urls

handler500 = "common.views.server_error_view"
handler404 = "common.views.page_not_found_view"


# Custom 403 handling, sending either a rate-limited response or a regular Forbidden
def handler403(request, exception=None):
    if isinstance(exception, Ratelimited):
        return rate_limited(request, exception)
    return permission_denied(request, exception)


urlpatterns = [
    path("oidc/", include("mozilla_django_oidc.urls")),
    path("django-admin/", admin.site.urls),
    path("admin/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
    path("healthz/", watchman_views.ping, name="watchman.ping"),
    path("readiness/", watchman_views.status, name="watchman.status"),
    re_path("^builders/", redirect_view, {"dest": "https://builders.mozilla.org"}),
    path("", include(microsite_urls)),
    path(
        "robots.txt",
        lambda r: HttpResponse(
            f"User-agent: *\n{'Allow' if settings.ENGAGE_ROBOTS else 'Disallow'}: /",
            content_type="text/plain",
        ),
    ),
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
        path("403/", permission_denied, {"exception": HttpResponseForbidden()}),
        path("csrf_403/", csrf_failure, {}),
        path("429/", rate_limited, {"exception": Ratelimited()}),
        path("500/", import_string(handler500)),
    )


urlpatterns = urlpatterns + [
    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's page serving mechanism. This should be the last pattern in
    # the list:
    path("", include(wagtail_urls)),
]
