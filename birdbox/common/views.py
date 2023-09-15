# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.shortcuts import render


def server_error_view(request, template_name="500.html"):
    """500 error handler that runs context processors."""
    return render(request, template_name, status=500)


def page_not_found_view(request, exception=None, template_name="404.html"):
    """404 error handler that runs context processors."""
    return render(request, template_name, status=404)
