# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django import forms
from django.conf import settings
from django.urls import reverse
from django.utils.translation import gettext as _


class ContactFormBase(forms.Form):
    email = forms.EmailField(required=True, label=_("Your email"))
    name = forms.CharField(max_length=200, label=_("Name"))
    description = forms.CharField(
        label="Your message",
        widget=forms.Textarea,
        max_length=2000,
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["description"].widget.attrs.update(
            {
                "placeholder": _("What would you like to collaborate on?"),
            }
        )

        self.email_subject = "Website contact submission"
        self.recipient_email = settings.CONTACT_FORM_RECIPIENT_EMAIL["default"]

    def get_action_url(self):
        return reverse("handle-contact-form", args=[self.__class__.__name__])


class GenericContactForm(ContactFormBase):
    # TODO: implement this with JS that isn't as opionated as the futuremo ones
    pass


class InnovationsContactForm(ContactFormBase):
    interests = forms.MultipleChoiceField(
        label=("What are you interested in learning more about?"),
        choices=(
            ("newsletter", _("Innovation Updates")),
            ("collaboration", _("Collaborate with us")),
        ),
        widget=forms.CheckboxSelectMultiple(),
    )

    website = forms.URLField(label=_("Website"))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["description"].widget.attrs.update(
            {
                "placeholder": _("What would you like to collaborate on?"),
            }
        )
        self.fields["website"].widget.attrs.update(
            {
                "placeholder": _("ex: mozilla.org"),
            }
        )
        self.order_fields(["name", "email", "interests", "description", "website"])
        self.email_subject = "Innovations Interest Form"
        self.recipient_email = settings.CONTACT_FORM_RECIPIENT_EMAIL["innovations"]

        self.root_css_class = "c-innovation-newsletter"
        self.form_type = "innovations-form"  # used to set a key class for behaviour


class MEICOContactForm(ContactFormBase):
    interests = forms.MultipleChoiceField(
        label=("What are you interested in learning more about?"),
        choices=(
            ("application", _("Application")),
            ("collaboration", _("Collaboration")),
            ("other", _("Other")),
        ),
        widget=forms.CheckboxSelectMultiple(),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["description"].widget.attrs.update(
            {
                "placeholder": _("What would you like us to contact you about?"),
            }
        )
        self.order_fields(["name", "email", "interests", "description"])
        self.email_subject = "MIECO Interest Form"
        self.recipient_email = settings.CONTACT_FORM_RECIPIENT_EMAIL["mieco"]

        # self.root_css_class is not needed for this form
        self.form_type = "mieco-form"  # used to set a key class for behaviour


class BuildersChallengeForm(ContactFormBase):
    interests = forms.MultipleChoiceField(
        label=("What are you interested in learning more about?"),
        choices=(
            (
                "mozilla-technology",
                _("Topics like AI and machine learning, the metaverse, extended reality (XR) and the future of the web."),
            ),
        ),
        widget=forms.CheckboxSelectMultiple(),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # no extra fields, just an email field for newsletter signups; no message sending
        del self.fields["description"]

        self.root_css_class = "TODO"
        self.form_type = "builders-form"  # used to set a key class for behaviour


CONTACT_FORM_CHOICES = (
    # (
    #     # Disabled for now
    #     "microsite.forms.GenericContactForm",
    #     "General contact form",
    # ),
    (
        "microsite.forms.InnovationsContactForm",
        "Innovations site contact form",
    ),
    (
        "microsite.forms.MEICOContactForm",
        "MIECO contact form",
    ),
    (
        "microsite.forms.BuildersChallengeForm",
        "Builders Challenge form",
    ),
)
