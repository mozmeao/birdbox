/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

import MzpSupports from '@mozilla-protocol/core/protocol/js/supports';
import MzpUtils from '@mozilla-protocol/core/protocol/js/utils';
import MzpDetails from '@mozilla-protocol/core/protocol/js/details';

window.MzpSupports = MzpSupports;
window.MzpUtils = MzpUtils;
window.MzpDetails = MzpDetails;

// check if details is supported, if not, init this as a polyfill
if (typeof window.MzpSupports !== 'undefined') {
    // not supported, add support
    if (!window.MzpSupports.details) {
        window.MzpDetails.init('summary');
    }
}

// init generic class indicating headings should be made into open/close component
window.MzpDetails.init('.mzp-c-details > h2');
window.MzpDetails.init('.mzp-c-details > h3');
window.MzpDetails.init('.mzp-c-details > h4');
window.MzpDetails.init('.mzp-c-details > h5');
window.MzpDetails.init('.mzp-c-details > h6');
