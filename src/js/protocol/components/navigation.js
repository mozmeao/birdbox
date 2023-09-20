/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

// import MzpNavigation from '@mozilla-protocol/core/protocol/js/navigation';
// import MzpMenu from '@mozilla-protocol/core/protocol/js/menu';

// window.MzpMenu = MzpMenu;

// window.MzpMenu.init();
// MzpNavigation.init();




// Copied from Protocol, to be back-ported along with nav updates.

(function () {
    'use strict';

    var MzpNavigation = {};
    var _navElem;
    var _navItemsLists;
    var _options = {
        onNavOpen: null,
        onNavClose: null
    };
    var _ticking = false;
    var _lastKnownScrollPosition = 0;
    var _animationFrameID = null;
    var _stickyScrollOffset = 300;
    var _wideBreakpoint = '768px';
    var _tallBreakpoint = '600px';
    var _mqLargeNav;
    var _viewport = document.getElementsByTagName('html')[0];

    /**
     * Does the viewport meet the minimum width and height
     * requirements for sticky behavior?
     * @returns {Boolean}
     */
    MzpNavigation.isLargeViewport = function () {
        return _mqLargeNav.matches;
    };

    /**
     * Feature detect for sticky navigation
     * @returns {Boolean}
     */
    MzpNavigation.supportsSticky = function () {
        if (typeof window.MzpSupports !== 'undefined') {
            return (
                window.MzpSupports.matchMedia &&
                window.MzpSupports.classList &&
                window.MzpSupports.requestAnimationFrame &&
                window.MzpSupports.cssFeatureQueries &&
                CSS.supports('position', 'sticky')
            );
        } else {
            return false;
        }
    };

    /**
     * Scroll event listener. No computationally expensive
     * operations such as DOM modifications should happen
     * here. Instead we throttle using `requestAnimationFrame`.
     */
    MzpNavigation.onScroll = function () {
        if (!_ticking) {
            _animationFrameID = window.requestAnimationFrame(
                MzpNavigation.checkScrollPosition
            );
            _ticking = true;
        }
    };

    /**
     * Create sticky state for the navigation.
     */
    MzpNavigation.createSticky = function () {
        _viewport.classList.add('mzp-has-sticky-navigation');
        _animationFrameID = window.requestAnimationFrame(
            MzpNavigation.checkScrollPosition
        );
        window.addEventListener('scroll', MzpNavigation.onScroll, false);
    };

    /**
     * Destroy sticky state for the navigation.
     */
    MzpNavigation.destroySticky = function () {
        _viewport.classList.remove('mzp-has-sticky-navigation');
        _navElem.classList.remove('mzp-is-scrolling');
        _navElem.classList.remove('mzp-is-hidden');
        _lastKnownScrollPosition = 0;

        if (_animationFrameID) {
            window.cancelAnimationFrame(_animationFrameID);
        }
        window.removeEventListener('scroll', MzpNavigation.onScroll, false);
    };

    /**
     * Initialize sticky state for the navigation.
     * Uses `matchMedia` to determine if conditions
     * for sticky navigation are satisfied.
     */
    MzpNavigation.initSticky = function () {
        _mqLargeNav = matchMedia(
            '(min-width: ' +
                _wideBreakpoint +
                ') and (min-height: ' +
                _tallBreakpoint +
                ')'
        );

        _mqLargeNav.addListener(function (mq) {
            if (mq.matches) {
                MzpNavigation.createSticky();
            } else {
                MzpNavigation.destroySticky();
            }
        });

        if (MzpNavigation.isLargeViewport()) {
            MzpNavigation.createSticky();
        }
    };

    /**
     * Implements sticky navigation behavior as
     * user scrolls up and down the viewport.
     */
    MzpNavigation.checkScrollPosition = function () {
        // add styling for when scrolling the viewport
        if (window.scrollY > 0) {
            _navElem.classList.add('mzp-is-scrolling');
        } else {
            _navElem.classList.remove('mzp-is-scrolling');
        }

        // scrolling down
        if (window.scrollY > _lastKnownScrollPosition) {
            // hide the sticky nav shortly after scrolling down the viewport.
            if (window.scrollY > _stickyScrollOffset) {
                // if there's a menu currently open, close it.
                if (typeof window.MzpMenu !== 'undefined') {
                    window.MzpMenu.close();
                }

                _navElem.classList.add('mzp-is-hidden');
            }
        }
        // scrolling up
        else {
            _navElem.classList.remove('mzp-is-hidden');
        }

        _lastKnownScrollPosition = window.scrollY;
        _ticking = false;
    };

    /**
     * Event handler for navigation menu button `click` events.
     */
    MzpNavigation.onClick = function (e) {
        var thisNavItemList = e.target.parentNode.querySelector(
            '.c-navigation-items'
        );

        e.preventDefault();

        // Update button state
        e.target.classList.toggle('mzp-is-active');

        // Update menu state
        thisNavItemList.classList.toggle('mzp-is-open');

        // Update aria-expended state on menu.
        var expanded = thisNavItemList.classList.contains('mzp-is-open')
            ? true
            : false;
        thisNavItemList.setAttribute('aria-expanded', expanded);

        if (expanded) {
            if (typeof _options.onNavOpen === 'function') {
                _options.onNavOpen(thisNavItemList);
            }
        } else {
            if (typeof _options.onNavClose === 'function') {
                _options.onNavClose(thisNavItemList);
            }
        }
    };

    /**
     * Set initial ARIA navigation states.
     */
    MzpNavigation.setAria = function () {
        for (var i = 0; i < _navItemsLists.length; i++) {
            _navItemsLists[i].setAttribute('aria-expanded', false);
        }
    };

    /**
     * Bind navigation event handlers.
     */
    MzpNavigation.bindEvents = function () {
        _navItemsLists = document.querySelectorAll('.c-navigation-items');
        if (_navItemsLists.length > 0) {
            var navButtons = document.querySelectorAll(
                '.c-navigation-menu-button'
            );
            for (var i = 0; i < navButtons.length; i++) {
                navButtons[i].addEventListener(
                    'click',
                    MzpNavigation.onClick,
                    false
                );
            }
            MzpNavigation.setAria();
        }
    };

    /**
     * Initialize menu.
     * @param {Object} options - configurable options.
     */
    MzpNavigation.init = function (options) {
        if (typeof options === 'object') {
            for (var i in options) {
                if (options.hasOwnProperty.call(i)) {
                    _options[i] = options[i];
                }
            }
        }

        MzpNavigation.bindEvents();

        /**
         * Init (optional) sticky navigation.
         * If there are multiple navigation organisms on a single page,
         * assume only the first (and hence top-most) instance can and
         * will be sticky.
         *
         * Do not init sticky navigation if user prefers reduced motion
         */

        _navElem = document.querySelector('.c-navigation');
        var _navIsSticky =
            _navElem &&
            _navElem.classList.contains('mzp-is-sticky') &&
            MzpNavigation.supportsSticky();

        if (_navIsSticky && matchMedia('(prefers-reduced-motion)').matches) {
            _navElem.classList.remove('mzp-is-sticky');
        } else if (_navIsSticky) {
            MzpNavigation.initSticky();
        }
    };

    window.MzpNavigation = MzpNavigation;
})(window.Mzp);


(function () {
    'use strict';

    var MzpMenu = {};
    var _menuOpen = false;
    var _hoverTimeout;
    var _hoverTimeoutDelay = 150;
    var _mqWideNav;
    var _wideBreakpoint = '768px';

    var _options = {
        onMenuOpen: null,
        onMenuClose: null,
        onMenuButtonClose: null
    };

    /**
     * Opens a menu panel.
     * @param {Object} el - DOM element (`.mzp-c-menu-category.mzp-js-expandable`)
     * @param {Boolean} animate - show animation when menu panel opens.
     */
    MzpMenu.open = function (el, animate) {
        if (animate) {
            el.classList.add('mzp-is-animated');
        }

        el.classList.add('mzp-is-selected');

        _menuOpen = true; // For checking menu state on keyup.

        el.querySelector('.c-menu-title').setAttribute('aria-expanded', true);

        if (typeof _options.onMenuOpen === 'function') {
            _options.onMenuOpen(el);
        }
    };

    /**
     * Closes all currently open menu panels.
     * Note: on small screens more than one menu can be open at the same time.
     */
    MzpMenu.close = function () {
        var current = document.querySelectorAll(
            '.c-menu-category.mzp-is-selected'
        );

        for (var i = 0; i < current.length; i++) {
            // The following classes must be removed in the correct order
            // to work around a bug in bedrock's classList polyfill for IE9.
            // https://github.com/mozilla/bedrock/issues/6221 :/
            current[i].classList.remove('mzp-is-selected');
            current[i].classList.remove('mzp-is-animated');

            current[i]
                .querySelector('.c-menu-title')
                .setAttribute('aria-expanded', false);
        }

        _menuOpen = false; // For checking menu state on keyup.

        if (typeof _options.onMenuClose === 'function' && current.length > 0) {
            _options.onMenuClose();
        }

        return current.length > 0;
    };

    MzpMenu.onDocumentKeyUp = function (e) {
        if (e.keyCode === 27 && _menuOpen) {
            MzpMenu.close();
        }
    };

    /**
     * Menu panel close button `click` event handler.
     * @param {Object} e - Event object.
     */
    MzpMenu.onCloseButtonClick = function (e) {
        e.preventDefault();

        if (typeof _options.onMenuButtonClose === 'function') {
            _options.onMenuButtonClose();
        }

        MzpMenu.close();
    };

    /**
     * Toggles the open/closed state of a menu panel.
     * @param {Object} el - DOM element (`.mzp-c-menu-category.mzp-js-expandable`)
     */
    MzpMenu.toggle = function (el) {
        var state = el.classList.contains('mzp-is-selected') ? true : false;

        if (!state) {
            MzpMenu.open(el);
        } else {
            // The following classes must be removed in the correct order
            // to work around a bug in bedrock's classList polyfill for IE9.
            // https://github.com/mozilla/bedrock/issues/6221 :/
            el.classList.remove('mzp-is-selected');
            el.classList.remove('mzp-is-animated');
            el.querySelector('.c-menu-title').setAttribute(
                'aria-expanded',
                false
            );

            if (typeof _options.onMenuClose === 'function') {
                _options.onMenuClose();
            }
        }
    };

    /**
     * Menu `mouseenter` event handler.
     * Opens the menu only when hover intent is shown.
     * Animates only if a menu panel is not already open.
     * @param {Object} e - Event object.
     */
    MzpMenu.onMouseEnter = function (e) {
        clearTimeout(_hoverTimeout);

        _hoverTimeout = setTimeout(function () {
            var current = MzpMenu.close();
            var animate = current ? false : true;

            MzpMenu.open(e.target, animate);
        }, _hoverTimeoutDelay);
    };

    /**
     * Menu `mouseleave` event handler.
     * Closes the menu only when hover intent is shown.
     */
    MzpMenu.onMouseLeave = function () {
        clearTimeout(_hoverTimeout);

        _hoverTimeout = setTimeout(function () {
            MzpMenu.close();
        }, _hoverTimeoutDelay);
    };

    /**
     * Menu `focusout` event handler.
     * Closes the menu when focus moves to an alement outside of the currently open panel.
     */
    MzpMenu.onFocusOut = function () {
        var self = this;

        /**
         * After an element loses focus, `document.activeElement` will always be `body` before
         * moving to the next element. A `setTimeout` of `0` circumvents this issue as it
         * re-queues the JavaScript to run at the end of the current excecution.
         */
        setTimeout(function () {
            // If the menu is open and the newly focused element is not a child, then call close().
            if (
                !self.contains(document.activeElement) &&
                self.classList.contains('mzp-is-selected')
            ) {
                MzpMenu.close();
            }
        }, 0);
    };

    /**
     * Menu link `click` event handler for wide viewports.
     * Closes any currently open menu panels before opening the selected one.
     * @param {Object} e - Event object.
     */
    MzpMenu.onClickWide = function (e) {
        e.preventDefault();
        MzpMenu.close();
        MzpMenu.open(e.target.parentNode);
    };

    /**
     * Menu link `click` event handler for small viewports.
     * Toggles the currently selected menu open open/close state.
     * @param {Object} e - Event object.
     */
    MzpMenu.onClickSmall = function (e) {
        e.preventDefault();
        MzpMenu.toggle(e.target.parentNode);
    };

    /**
     * Convenience function for checking `matchMedia` state.
     * @return {Boolean}
     */
    MzpMenu.isWideViewport = function () {
        return _mqWideNav.matches;
    };

    /**
     * Toggle desktop/mobile navigation using `matchMedia` event handler.
     */
    MzpMenu.handleState = function () {
        _mqWideNav = matchMedia('(min-width: ' + _wideBreakpoint + ')');

        _mqWideNav.addListener(function (mq) {
            MzpMenu.close();

            if (mq.matches) {
                MzpMenu.unbindEventsSmall();
                MzpMenu.bindEventsWide();
            } else {
                MzpMenu.unbindEventsWide();
                MzpMenu.bindEventsSmall();
            }
        });

        if (MzpMenu.isWideViewport()) {
            MzpMenu.bindEventsWide();
        } else {
            MzpMenu.bindEventsSmall();
        }
    };

    /**
     * Bind events for wide viewports.
     */
    MzpMenu.bindEventsWide = function () {
        var items = document.querySelectorAll(
            '.c-menu-category.mzp-js-expandable'
        );
        var link;
        var close;

        for (var i = 0; i < items.length; i++) {
            items[i].addEventListener(
                'mouseenter',
                MzpMenu.onMouseEnter,
                false
            );
            items[i].addEventListener(
                'mouseleave',
                MzpMenu.onMouseLeave,
                false
            );
            items[i].addEventListener('focusout', MzpMenu.onFocusOut, false);

            link = items[i].querySelector('.c-menu-title');
            link.addEventListener('click', MzpMenu.onClickWide, false);

            close = items[i].querySelector('.c-menu-button-close');
            close.addEventListener('click', MzpMenu.onCloseButtonClick, false);
        }

        // close with escape key
        document.addEventListener('keyup', MzpMenu.onDocumentKeyUp, false);
    };

    /**
     * Unbind events for wide viewports.
     */
    MzpMenu.unbindEventsWide = function () {
        var items = document.querySelectorAll(
            '.c-menu-category.mzp-js-expandable'
        );
        var link;
        var close;

        for (var i = 0; i < items.length; i++) {
            items[i].removeEventListener(
                'mouseenter',
                MzpMenu.onMouseEnter,
                false
            );
            items[i].removeEventListener(
                'mouseleave',
                MzpMenu.onMouseLeave,
                false
            );
            items[i].removeEventListener('focusout', MzpMenu.onFocusOut, false);

            link = items[i].querySelector('.c-menu-title');
            link.removeEventListener('click', MzpMenu.onClickWide, false);

            close = items[i].querySelector('.c-menu-button-close');
            close.removeEventListener(
                'click',
                MzpMenu.onCloseButtonClick,
                false
            );
        }

        document.removeEventListener('keyup', MzpMenu.onDocumentKeyUp, false);
    };

    /**
     * Bind events for small viewports.
     */
    MzpMenu.bindEventsSmall = function () {
        var items = document.querySelectorAll(
            '.c-menu-category.mzp-js-expandable .c-menu-title'
        );

        for (var i = 0; i < items.length; i++) {
            items[i].addEventListener('click', MzpMenu.onClickSmall, false);
        }
    };

    /**
     * Unbind events for small viewports.
     */
    MzpMenu.unbindEventsSmall = function () {
        var items = document.querySelectorAll(
            '.c-menu-category.mzp-js-expandable .c-menu-title'
        );

        for (var i = 0; i < items.length; i++) {
            items[i].removeEventListener('click', MzpMenu.onClickSmall, false);
        }
    };

    /**
     * Set initial ARIA menu panel states.
     */
    MzpMenu.setAria = function () {
        var items = document.querySelectorAll(
            '.c-menu-category.mzp-js-expandable .c-menu-title'
        );

        for (var i = 0; i < items.length; i++) {
            items[i].setAttribute('aria-expanded', false);
        }
    };

    /**
     * Enhances the menu for 1st class JS support.
     */
    MzpMenu.enhanceJS = function () {
        var menu = document.querySelectorAll('.c-menu');

        for (var i = 0; i < menu.length; i++) {
            menu[i].classList.remove('mzp-is-basic');
            menu[i].classList.add('mzp-is-enhanced');
        }
    };

    /**
     * Basic feature detect for 1st class menu JS support.
     */
    MzpMenu.isSupported = function () {
        if (typeof window.MzpSupports !== 'undefined') {
            return (
                window.MzpSupports.matchMedia && window.MzpSupports.classList
            );
        } else {
            return false;
        }
    };

    /**
     * Initialize menu.
     * @param {Object} options - configurable options.
     */
    MzpMenu.init = function (options) {
        if (typeof options === 'object') {
            for (var i in options) {
                if (options.hasOwnProperty.call(i)) {
                    _options[i] = options[i];
                }
            }
        }

        if (MzpMenu.isSupported()) {
            MzpMenu.handleState();
            MzpMenu.setAria();
            MzpMenu.enhanceJS();
        }
    };

    window.MzpMenu = MzpMenu;
})();


window.MzpMenu.init();
MzpNavigation.init();
