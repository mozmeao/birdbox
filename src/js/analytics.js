/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

var dntEnabled = require("@mozmeao/dnt-helper");

(function () {
    "use strict";
    const googleTagId = document.documentElement.dataset.gtmId;
    window.dataLayer = window.dataLayer || [];

    // If doNotTrack is not enabled, it is ok to add GTM
    // @see https://bugzilla.mozilla.org/show_bug.cgi?id=1217896 for more details
    // prettier-ignore
    if (typeof dntEnabled === 'function' && !dntEnabled() && googleTagId) {

        (function(w,d,s,l,i,j,f,dl,k,q){
            w[l]=w[l]||[];w[l].push({'gtm.start': new Date().getTime(),event:'gtm.js'});f=d.getElementsByTagName(s)[0];
            k=i.length;q='//www.googletagmanager.com/gtm.js?id=@&l='+(l||'dataLayer');
            while(k--){j=d.createElement(s);j.async=!0;j.src=q.replace('@',i[k]);f.parentNode.insertBefore(j,f);}
        }(window,document,'script','dataLayer',[googleTagId]));

        // Google tag (gtag.js)
        function gtag(){dataLayer.push(arguments);}
        gtag('js', new Date());
        gtag('config', '{{googleTagId}}');
    }
})();
