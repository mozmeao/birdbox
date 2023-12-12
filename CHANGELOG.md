# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased

No changes

## [1.2.1]

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
