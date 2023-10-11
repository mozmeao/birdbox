# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

"""Custom middleware for Birdbox"""

from http import HTTPStatus

from django.conf import settings

from django_ratelimit import ALL
from django_ratelimit.core import is_ratelimited
from django_ratelimit.exceptions import Ratelimited


def rate_limiter(get_response):
    """Enforces rate-limiting on all views.

    Custom wrapper for django-ratelimit so we can use it with Wagtail.

    Why are we rate-limiting ALL views and not just those that the CDN won't
    be cacheing? Here's the logic:

    * Most production traffic spikes will be handled by the CDN.
    * However, querystrings on requests (either deliberately if/when we add search,
    or via abuse) can lead to CDN cache misses
    * We can't decorate the main Wagtail page-serving view with django-ratelimit, but
    we can use middleware to do perform rate-limiting checks, using django-ratelimit's
    core helpers
    * However, django-ratelimit's API/helpers need a request object because they
    rate-limit based on a view func, not a path from the URL, so we can't easily target
    specific Wagtail-served pages for rate limiting

    With all that in mind, including the fact the CDN will cache pages, we rate-limit
    ALL the pages served by the site. In the wild, once the CDN is warm, we should
    only be rate-limiting abuse.

    The limit set will be one which should not impair real-world content curation via
    /admin/ either.

    """

    def middleware(request):
        # Set an arbitrary catch-all group name, because we need to provide
        # a group because we don't have the view func available here.
        group = "all_requests"

        old_limited = getattr(request, "limited", False)
        ratelimited = is_ratelimited(
            request=request,
            group=group,
            key="ip",
            rate=settings.RATELIMIT_DEFAULT_LIMIT,
            increment=True,
            method=ALL,  # ie include GET, not just ratelimit.UNSAFE methods
        )
        request.limited = ratelimited or old_limited
        if ratelimited:
            raise Ratelimited()

        response = get_response(request)
        return response

    return middleware


def set_remote_addr_from_forwarded_for(get_response):
    """
    Middleware that sets REMOTE_ADDR based on HTTP_X_FORWARDED_FOR, if the
    latter is set. This is useful if you're sitting behind a reverse proxy

    TODO: consider switching to https://pypi.org/project/django-xff/
    """

    def middleware(request):
        forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if forwarded_for:
            # HTTP_X_FORWARDED_FOR can be a comma-separated list of IPs.
            # The client's claimed IP will be the first in the list, as CDN etc
            # append to the end.
            forwarded_for = forwarded_for.split(",")[0].strip()
            request.META["REMOTE_ADDR"] = forwarded_for

        response = get_response(request)
        return response

    return middleware


def remove_vary_on_cookie_for_statics(get_response):
    """We're using whitenoise to serve static assets, but Django is setting the
    `Vary: Cookie` header on static assets, which is stoppping the CDN from
    caching them effectively.

    This middleware needs to go before SessionMiddleware so that it can
    selectively prune back the Vary: Cookie header which that middleware sets.
    """

    VARY_HEADER_KEY = "Vary"
    COOKIE_VALUE = "Cookie"

    def middleware(request):
        response = get_response(request)
        if response.status_code == HTTPStatus.OK and request.path.startswith(settings.STATIC_URL):
            for key, value in list(response.headers.items()):
                if key.lower() == VARY_HEADER_KEY.lower():
                    split_values = [x.strip() for x in value.split(",")]
                    if split_values == [COOKIE_VALUE]:
                        del response.headers[key]
                    elif COOKIE_VALUE in split_values:
                        split_values.pop(split_values.index(COOKIE_VALUE))
                        response.headers[key] = ", ".join(split_values)
        return response

    return middleware
