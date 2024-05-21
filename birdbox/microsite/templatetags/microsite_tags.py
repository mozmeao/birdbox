# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from collections import defaultdict
from operator import itemgetter
from typing import Dict, List

from django.conf import settings
from django.template import Library

from product_details import product_details
from wagtail.blocks.struct_block import StructBlock
from wagtail.models import Site

from common.utils import (
    find_streamfield_blocks_by_types,
    get_freshest_newsletter_data,
)

from ..blocks import HeroBlock
from ..models import (
    Footer,
    FormStandardMessages,
    MicrositeSettings,
    Page,
    StructuralPage,
)

register = Library()

_LANGUAGE_LOOKUP = {}


def _get_language_lookup():
    global _LANGUAGE_LOOKUP
    if not _LANGUAGE_LOOKUP:
        # Use mozilla-django-product-details to get a set of localised language names
        _LANGUAGE_LOOKUP = {k: v.get("native", k) for k, v in product_details.languages.items()}
    return _LANGUAGE_LOOKUP


@register.inclusion_tag("microsite/partials/nav.html", takes_context=True)
def navigation(context) -> Dict:
    request = context["request"]
    microsite_settings = MicrositeSettings.load(request_or_site=request)
    homepage = Site.objects.get(is_default_site=True).root_page

    context = {
        "show_nav": microsite_settings.navigation_enabled,
        "nav_theme_class": microsite_settings.navigation_theme,
        "nav_links": [],
        "cta_label": "",
        "cta_url": "",
    }

    if microsite_settings.navigation_generate_nav_from_page_tree:
        context["nav_links"] = [child_page for child_page in homepage.get_children().defer_streamfields().live().public().in_menu()]

    if microsite_settings.navigation_show_cta_button:
        context["cta_label"] = microsite_settings.navigation_cta_button_label
        context["cta_url"] = microsite_settings.navigation_cta_button_url

    return context


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
    OVERRIDES_TO_STOP_CLASS_FROM_PAGE = [
        # Most blocks call this by default, but there are some pages where we want to stop that happening
        "BlogPage",
    ]

    page = context.get("page")
    if page and page.__class__.__name__ not in OVERRIDES_TO_STOP_CLASS_FROM_PAGE:
        return page.specific.page_layout
    return ""


@register.simple_tag(takes_context=True)
def get_layout_modifier_from_page(context) -> str:
    # Generates a modifier class from the page layout class
    # - eg turns "mzp-l-content mzp-t-content-md" into "mzp-u-modifier-md"
    page = context.get("page")
    if page:
        return page.specific.page_layout.replace("mzp-l-content ", "").replace("mzp-t-content", "mzp-u-modifier")
    return ""


def _get_language_name_for_locale(locale_code):
    adjusted_locale_code = {
        "en": "en-US",
        "pt": "pt-PT",
    }.get(locale_code, locale_code)
    return _get_language_lookup().get(adjusted_locale_code, locale_code)


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
    }


@register.simple_tag
def get_form_standard_messages():
    return FormStandardMessages.objects.first()


@register.simple_tag
def newsletter_service_url() -> str:
    return settings.BASKET_SUBSCRIPTION_URL


@register.simple_tag
def seek_dark_theme_class(parent_class_string: str) -> str:
    """Used with a child HTML node to determine whether it should have
    the mzp-t-dark class added to it, based on a class string set on
    a parent/grandparent node.

    See microsite/templates/microsite/blocks/split.html for an example of its use
    """
    DARK_THEME_CLASSNAME = "mzp-t-dark"

    try:
        if DARK_THEME_CLASSNAME in parent_class_string:
            return DARK_THEME_CLASSNAME
    except TypeError:
        pass

    return ""


@register.simple_tag
def block_with_h1_exists_in_page(page: Page) -> bool:
    candidate_blocks = find_streamfield_blocks_by_types(
        page=page,
        target_block_types=(
            HeroBlock,
            # ArticleBlock does NOT contain a H1 any more, it's a H2
        ),
    )
    # If we have more than one candidate block in a page, that's a separate problem
    # but should be caught by Wagtail's own a11y checks
    return len(candidate_blocks) > 0


@register.inclusion_tag("microsite/partials/breadcrumbs.html")
def breadcrumbs(page: Page) -> Dict[str, str]:
    context = defaultdict(list)
    context["show_breadcrumbs"] = page.specific.show_breadcrumbs
    context["page"] = page

    # Exclude the Wagtail-internal site Root page, because that's not a viewable page
    ancestors_up_to_homepage = page.get_ancestors().defer_streamfields().live().public()[1:]
    for ancestor in ancestors_up_to_homepage:
        context["ancestors"].append(
            {
                "title": ancestor.title,
                "url": ancestor.url if not isinstance(ancestor.specific, StructuralPage) else None,
            }
        )

    return context


@register.filter
def is_hero_block(value: StructBlock) -> bool:
    return isinstance(value.block, HeroBlock)
