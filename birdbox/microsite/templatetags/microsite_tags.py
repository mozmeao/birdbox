# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from operator import itemgetter
from typing import Dict, List

from django.conf import settings
from django.template import Library

from product_details import product_details

from common.utils import get_freshest_newsletter_data

from ..models import Footer, MicrositeSettings, NewsletterStandardMessages

register = Library()

# Use mozilla-django-product-details to get a set of localised language names
LANGUAGE_LOOKUP = {k: v.get("native", k) for k, v in product_details.languages.items()}


@register.inclusion_tag("microsite/partials/footer.html", takes_context=True)
def site_footer(context) -> Dict:
    request = context["request"]

    footer = Footer.load(request_or_site=request)
    if footer and not footer.display_footer:
        footer = None

    return {"footer": footer}


@register.inclusion_tag("microsite/partials/global_css_tag.html", takes_context=True)
def global_css_tag(context) -> Dict:
    request = context["request"]
    microsite_settings = MicrositeSettings.load(request_or_site=request)
    filepath = f"css/protocol-{microsite_settings.site_theme}-theme.css"
    return {"filepath": filepath}


@register.inclusion_tag("microsite/partials/favicons.html", takes_context=True)
def favicon_links(context) -> Dict:
    request = context["request"]

    microsite_settings = MicrositeSettings.load(request_or_site=request)

    _base_path = f"img/favicons/{microsite_settings.site_theme}/"

    apple_icon_path = _base_path + "apple-touch-icon.png"
    large_favicon_path = _base_path + "favicon-196x196.png"
    favicon_path = _base_path + "favicon.ico"

    return {
        "apple_icon_path": apple_icon_path,
        "large_favicon_path": large_favicon_path,
        "favicon_path": favicon_path,
    }


@register.simple_tag(takes_context=True)
def get_layout_class_from_page(context) -> str:
    page = context.get("page")
    if page:
        return page.specific.page_layout
    return ""


def _get_language_name_for_locale(locale_code):
    adjusted_locale_code = {
        "en": "en-US",
        "pt": "pt-PT",
    }.get(locale_code, locale_code)
    return LANGUAGE_LOOKUP.get(adjusted_locale_code, locale_code)


@register.inclusion_tag("microsite/blocks/partials/_newsletter_fieldsets.html", takes_context=True)
def newsletter_form_fieldset(context, newsletter_slugs: List[str]) -> Dict:
    newsletter_data = get_freshest_newsletter_data()

    country_choices = sorted(
        # TODO: localise me, taking the locale code from context
        iter(product_details.get_regions(locale="en").items()),
        key=itemgetter(1),
    )
    language_choices = set()
    newsletter_choices = set()

    for slug in newsletter_slugs:
        if selected_newsletter := newsletter_data.get("newsletters", {}).get(slug):
            newsletter_choices.add(
                (slug, selected_newsletter.get("title", slug)),
            )

            specific_newsletter_languages = set()
            for locale_code in selected_newsletter.get("languages", []):
                specific_newsletter_languages.add(
                    (locale_code, _get_language_name_for_locale(locale_code)),
                )

            if language_choices:
                language_choices = language_choices.union(specific_newsletter_languages)
            else:
                language_choices = specific_newsletter_languages

    return {
        "request": context["request"],
        "countries": sorted(country_choices, key=lambda x: x[1]),
        "languages": sorted(language_choices, key=lambda x: x[1]),
        "newsletters": sorted(newsletter_choices, key=lambda x: x[1]),
        "standard_messages": NewsletterStandardMessages.objects.first(),
    }


@register.simple_tag
def newsletter_service_url():
    return settings.BASKET_SUBSCRIPTION_URL
