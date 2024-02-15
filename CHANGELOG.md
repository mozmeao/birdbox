# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased

### Changed

* Update YouTube video embeds to use the youtube-nocookie.com domain instead of regular youtube.com
* Do not load analytics JS (if allowed based on DNT) on 40x pages
* Dependency updates for security and stability
* Configure wagtail-markdown so that bleach does not strip anchor element attributes
* Configure wagtail-markdown so that bleach does not strip img element attributes
* Dependency updates

## [1.3.0]

### Added

* Make callout text into richtext, with a limited set of features; increase limit to 1000 chars
* Support for specific per-page social-sharing images, at a reasonable size (#255)

### Changed

* Switch wagtailstreamforms from our fork to the official release, now it has Django 5.2 compat
* Increase length of split block's rich-text-area to 650 chars

## [1.2.0]

### Changed

* Swap TextBlock for RichTextBlock in Picto and Split components (#225)

## [1.1.0]

### Added

* Support an allowlist of page types that may be added to a site (#222)
* Add tests badge to Readme
* Add GHAs to push to stage and prod from Github itself (#220)

### Changed

* Bump Wagtail to 5.2.1 + psycopg and sentry-sdk (#215)
* Update ratelimiting middleware to HTTP 400 badly formatted IPs while still raising other ValueErrors (#216)
* Bump up default OIDC session to 24 hours, to avoid awkward re-auths (#217)
* Increase character counts on card description field (#224)
* Minor Readme change to test end-to-end deployment process
* Update example env with better CSP; upgrade everett to get bugfix release related to CSP strings (#211)

## [1.0.0]

Initial MVP release with page types and behaviour suited to building out future.mozilla.org. Too much to sensibly list here.
