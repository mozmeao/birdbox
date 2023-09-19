# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import json

from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.module_loading import import_string
from django.views.decorators.http import require_POST

from jsonview.decorators import json_view


@json_view
@require_POST
def handle_contact_form(request, form_class_name):
    """
    This form accepts a POST request and, if the form is valid, will send
    an email with the data included in the email.
    """
    try:
        json_data = json.loads(request.body.decode("utf-8"))
    except json.decoder.JSONDecodeError:
        return {"error": 400, "message": "Error decoding JSON"}, 400

    form_class = import_string(f"microsite.forms.{form_class_name}")

    # Special manipulation for interests field
    if "interests" in json_data:
        json_data["interests"] = json_data["interests"].split(",")

    form = form_class(data=json_data)

    if not form.is_valid():
        return {"error": 400, "message": f"Invalid form data: {form.errors}"}, 400

    email_msg = render_to_string(
        "microsite/emails/contact.txt",
        {"data": form.cleaned_data},
        request=request,
    )
    email_sub = form.email_subject

    email = EmailMessage(
        subject=email_sub,
        body=email_msg,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[form.recipient_email],
    )

    try:
        email.send()
    except Exception as e:
        return {"error": 400, "message": str(e)}, 400

    return {"status": "ok"}, 200
