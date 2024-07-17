/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

var dntEnabled = require("@mozmeao/dnt-helper");

(function () {
    "use strict";
    const googleTagId = document.documentElement.dataset.gtagId;
    window.dataLayer = window.dataLayer || [];

    // If doNotTrack is not enabled, it is ok to add GTM
    // @see https://bugzilla.mozilla.org/show_bug.cgi?id=1217896 for more details
    // prettier-ignore
    if (typeof dntEnabled === 'function' && !dntEnabled() && googleTagId) {

        (function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
        new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
        j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
        'https://www.googletagmanager.com/gtag/js?id='+i+dl;f.parentNode.insertBefore(j,f);
        })(window,document,'script','dataLayer',googleTagId);

        window.dataLayer = window.dataLayer || [];
        window.gtag = function(){dataLayer.push(arguments);}
        gtag('js', new Date());

        gtag('config', googleTagId);
    }
})();
