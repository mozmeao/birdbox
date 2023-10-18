/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

// Needs dnt-helper.js to be executed first and window.Mozilla.googleTagId to be set

(function () {
    "use strict";

    // dnt-helper.js sets the window.Mozilla namespace
    var GOOGLE_TAG_ID = window.Mozilla.googleTagId;

    // If doNotTrack is not enabled, it is ok to add GTM
    // @see https://bugzilla.mozilla.org/show_bug.cgi?id=1217896 for more details
    // prettier-ignore
    if (typeof Mozilla.dntEnabled === 'function' && !Mozilla.dntEnabled() && GOOGLE_TAG_ID) {

        window.dataLayer = window.dataLayer || [];

        (function(w,d,s,l,i,j,f,dl,k,q){
            w[l]=w[l]||[];w[l].push({'gtm.start': new Date().getTime(),event:'gtm.js'});f=d.getElementsByTagName(s)[0];
            k=i.length;q='//www.googletagmanager.com/gtm.js?id=@&l='+(l||'dataLayer');
            while(k--){j=d.createElement(s);j.async=!0;j.src=q.replace('@',i[k]);f.parentNode.insertBefore(j,f);}
        }(window,document,'script','dataLayer',[GOOGLE_TAG_ID]));

        // Google tag (gtag.js)
        if (!window.Mozilla.dntEnabled()) {
            function gtag(){dataLayer.push(arguments);}
            gtag('js', new Date());
            gtag('config', '{{GOOGLE_TAG_ID}}');
        }
    }
})();
