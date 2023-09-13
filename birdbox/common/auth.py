# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.conf import settings
from django.core.exceptions import SuspiciousOperation

from mozilla_django_oidc.auth import OIDCAuthenticationBackend


class BirdboxOIDCAuthenticationBackend(OIDCAuthenticationBackend):
    """Subclass of the main OIDC auth backend that bootstraps any expected
    admin users from env vars, so that we can set up a Birdbox site
    without needing to shell into a running container."""

    def _check_for_and_create_admin_users(self):
        for email in settings.BIRDBOX_ADMIN_USER_EMAILS:
            if email.endswith(f"@{settings.BIRDBOX_ADMIN_EMAIL_DOMAIN}"):
                user, _ = self.UserModel.objects.get_or_create(
                    email=email,
                    username=email,
                    is_superuser=True,
                    is_staff=True,
                )
                if user.has_usable_password():
                    user.set_unusable_password()
                    user.save()
            else:
                msg = (
                    f"The email address '{email}' in "
                    "settings.BIRDBOX_ADMIN_USER_EMAILS was alleged to be for "
                    "an administrator but didn't belong to the approved "
                    f"domain {settings.BIRDBOX_ADMIN_EMAIL_DOMAIN}"
                )
                raise SuspiciousOperation(msg)

    def get_or_create_user(self, access_token, id_token, payload):
        # Before we see if there is an account for the authenticating user,
        # we need to bootstrap the admin(s) that the site knows
        self._check_for_and_create_admin_users()

        return super().get_or_create_user(
            access_token,
            id_token,
            payload,
        )
