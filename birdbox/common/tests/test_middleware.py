# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from copy import deepcopy
from unittest import mock

from django.conf import settings
from django.core.cache import cache
from django.http import HttpResponse
from django.test import RequestFactory, TestCase, override_settings

import pytest
from django_ratelimit.exceptions import Ratelimited

from common.middleware import (
    rate_limiter,
    remove_vary_on_cookie_for_statics,
    set_remote_addr_from_forwarded_for,
)


@override_settings(RATELIMIT_ENABLE=True, RATELIMIT_DEFAULT_LIMIT="2/m")
class RateLimiterMiddlewareTests(TestCase):
    def tearDown(self):
        cache.clear()

    def test_rate_limiter_middleware_is_enabled(self):
        for expected_middleware in [
            "common.middleware.rate_limiter",
            "django_ratelimit.middleware.RatelimitMiddleware",
        ]:
            assert expected_middleware in settings.MIDDLEWARE

    def test_rate_limiter__works_for_all_http_methods(self):
        factory = RequestFactory()

        for method in ["get", "post", "put", "delete", "head", "options"]:
            with self.subTest(label=method):
                # django-ratelimit uses the default cache. Invalidating it between
                # attempts means subtests will not interfere with each other
                cache.clear()

                mock_get_response = mock.Mock(name="get_response")
                fake_request = getattr(factory, method)("/", REMOTE_ADDR="127.0.0.1")
                middleware_func = rate_limiter(mock_get_response)

                # First time, no problem
                middleware_func(fake_request)
                assert mock_get_response.call_count == 1

                # Second time, no problem
                middleware_func(fake_request)
                assert mock_get_response.call_count == 2

                # Third time: rate-limited problem
                with self.assertRaises(Ratelimited):
                    middleware_func(fake_request)
                assert mock_get_response.call_count == 2  # ie, didn't get called again

    @override_settings(RATELIMIT_DEFAULT_LIMIT="3/m")  # 3 per min max
    def test_rate_limiter__definitely_separates_by_ip(self):
        factory = RequestFactory()

        mock_get_response = mock.Mock(name="get_response")
        middleware_func = rate_limiter(mock_get_response)

        # Four calls from different IPs: all fine
        cache.clear()  # reset any previous rate limiting
        for i, ip in enumerate(["127.0.0.1", "127.0.0.2", "127.0.0.3", "127.0.0.4"]):
            fake_request = factory.get("/", REMOTE_ADDR=ip)
            middleware_func(fake_request)
            assert mock_get_response.call_count == 1 + i

        # Four calls from SAME IP: fourth will be limited
        cache.clear()  # reset any previous rate limiting

        assert fake_request.META["REMOTE_ADDR"] == "127.0.0.4"

        middleware_func(fake_request)
        middleware_func(fake_request)
        middleware_func(fake_request)
        with self.assertRaises(Ratelimited):
            middleware_func(fake_request)


class RemoteAddressMiddlewareTests(TestCase):
    def test_set_remote_addr_from_forwarded_for_middleware_is_enabled(self):
        assert "common.middleware.set_remote_addr_from_forwarded_for" in settings.MIDDLEWARE

    def test_set_remote_addr_from_forwarded_for_middleware(self):
        remote_addr = "172.24.24.24"
        cases = [
            {
                "x_forwarded_for_string": "172.31.255.255",
                "expected_ip": "172.31.255.255",
            },
            {
                "x_forwarded_for_string": "172.31.255.255, 172.16.1.1",
                "expected_ip": "172.31.255.255",
            },
            {
                "x_forwarded_for_string": "172.31.255.255, 172.16.1.1, 172.16.128.128",
                "expected_ip": "172.31.255.255",
            },
            {"x_forwarded_for_string": "", "expected_ip": remote_addr},
            {"x_forwarded_for_string": None, "expected_ip": remote_addr},
        ]

        factory = RequestFactory()

        mock_get_response = mock.Mock(name="get_response")
        middleware_func = set_remote_addr_from_forwarded_for(mock_get_response)

        for case in cases:
            mock_get_response.reset_mock()
            with self.subTest(label=case):
                xff = case["x_forwarded_for_string"]
                if xff is None:
                    kwargs = dict(REMOTE_ADDR=remote_addr)
                else:
                    kwargs = dict(REMOTE_ADDR=remote_addr, HTTP_X_FORWARDED_FOR=xff)
                fake_request = factory.get("/", **kwargs)
                middleware_func(fake_request)

                updated_request = mock_get_response.call_args_list[0][0][0]
                self.assertEqual(updated_request.META["REMOTE_ADDR"], case["expected_ip"])


_HEADERS___SIMPLE_VARY_ON_COOKIE = {
    "Content-Type": "image/png",
    "Access-Control-Allow-Origin": "*",
    "Cache-Control": "public, max-age=3600",
    "Vary": "Cookie",
    "Last-Modified": "Wed, 27 Sep 2023 13:24:03 GMT",
    "ETag": '"65142cf3-1cee"',
    "Content-Length": "1780",
    "X-Content-Type-Options": "nosniff",
    "Referrer-Policy": "same-origin",
    "Cross-Origin-Opener-Policy": "same-origin",
    "X-Frame-Options": "DENY",
}
_HEADERS___COMPLEX_VARY_ON_COOKIE = deepcopy(_HEADERS___SIMPLE_VARY_ON_COOKIE)
_HEADERS___COMPLEX_VARY_ON_COOKIE["Vary"] = "Accept-Encoding, Cookie"

_HEADERS__WITHOUT_SIMPLE_VARY_ON_COOKIE = deepcopy(_HEADERS___SIMPLE_VARY_ON_COOKIE)
del _HEADERS__WITHOUT_SIMPLE_VARY_ON_COOKIE["Vary"]

_HEADERS__WITHOUT_COMPLEX_VARY_ON_COOKIE = deepcopy(_HEADERS___COMPLEX_VARY_ON_COOKIE)
_HEADERS__WITHOUT_COMPLEX_VARY_ON_COOKIE["Vary"] = "Accept-Encoding"


@pytest.mark.parametrize(
    "request_path, original_headers, status_code, expected_headers",
    (
        (
            "/",
            _HEADERS___SIMPLE_VARY_ON_COOKIE,
            200,
            _HEADERS___SIMPLE_VARY_ON_COOKIE,
        ),
        (
            "/some-non-static-path/",
            _HEADERS___COMPLEX_VARY_ON_COOKIE,
            200,
            _HEADERS___COMPLEX_VARY_ON_COOKIE,
        ),
        (
            "/static/test.png",
            _HEADERS___SIMPLE_VARY_ON_COOKIE,
            200,
            _HEADERS__WITHOUT_SIMPLE_VARY_ON_COOKIE,
        ),
        (
            "/static/path/to/test.png",
            _HEADERS___COMPLEX_VARY_ON_COOKIE,
            200,
            _HEADERS__WITHOUT_COMPLEX_VARY_ON_COOKIE,
        ),
        (
            "/static/path/to/test.png",
            _HEADERS___SIMPLE_VARY_ON_COOKIE,
            404,
            _HEADERS___SIMPLE_VARY_ON_COOKIE,
        ),
        (
            "/static/path/to/test.png",
            _HEADERS___COMPLEX_VARY_ON_COOKIE,
            404,
            _HEADERS___COMPLEX_VARY_ON_COOKIE,
        ),
        (
            "/static/path/to/test.png",
            _HEADERS___SIMPLE_VARY_ON_COOKIE,
            301,
            _HEADERS___SIMPLE_VARY_ON_COOKIE,
        ),
        (
            "/static/path/to/test.png",
            _HEADERS___COMPLEX_VARY_ON_COOKIE,
            302,
            _HEADERS___COMPLEX_VARY_ON_COOKIE,
        ),
    ),
    ids=(
        "Not a static path, no change to simple Vary: Cookie header",
        "Not a static path, no change to complex Vary: Cookie header",
        "Static path, dropping of simple Vary: Cookie header",
        "Static path, change to complex Vary: Cookie header",
        "Static path, but 404 so no change; simple Vary: Cookie header",
        "Static path, but 404 so no change; complex Vary: Cookie header",
        "Static path, but 301 so no change; simple Vary: Cookie header",  # very artificial headers for a 302
        "Static path, but 302 so no change; complex Vary: Cookie header",  # very artificial headers for a 302
    ),
)
def test_remove_vary_on_cookie_for_statics(
    request_path,
    original_headers,
    status_code,
    expected_headers,
):
    mock_get_response = mock.Mock(name="get_response")
    middleware_func = remove_vary_on_cookie_for_statics(mock_get_response)

    fake_request = RequestFactory().get(request_path)
    fake_response = HttpResponse("", headers=original_headers, status=status_code)
    mock_get_response.return_value = fake_response

    response = middleware_func(fake_request)

    mock_get_response.assert_called_once_with(fake_request)
    assert response.headers == expected_headers
