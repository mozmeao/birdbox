/*
* This Source Code Form is subject to the terms of the Mozilla Public
* License, v. 2.0. If a copy of the MPL was not distributed with this
* file, You can obtain one at https://mozilla.org/MPL/2.0/.
*/

/* These mappings let us give descriptive names to CSS classes when we surface
* them in the Wagtail editor. If you change the value of the relevant class in
* src/css/protocol-{THEME-NAME}-theme-colors.scss, you may need to update here, too
*/

const colorLabels = {
    "mozilla": {
        "mzp-t-light": "White",
        "mzp-t-dark": "Black/Ink",
        "bb-t-light-color-01": "Light Gray",
        "bb-t-dark-color-01": "Dark Gray",
        "bb-t-light-color-02": "Pink",
        "bb-t-dark-color-02": "Red",
        "bb-t-light-color-03": "Light Yellow",
        "bb-t-dark-color-03": "Dark Yellow",
        "bb-t-light-color-04": "Light Orange",
        "bb-t-dark-color-04": "Dark Orange",
        "bb-t-light-color-05": "Light Green",
        "bb-t-dark-color-05": "Dark Green",
        "bb-t-light-color-06": "Light Blue",
        "bb-t-dark-color-06": "Dark Blue",
        "bb-t-light-color-07": "Light Violet",
        "bb-t-dark-color-07": "Dark Violet",
    },
    "firefox": {
        "mzp-t-light": "White",
        "mzp-t-dark": "Black/Ink",
        "bb-t-light-color-01": "Light Gray",
        "bb-t-dark-color-01": "Dark Gray",
        "bb-t-light-color-02": "Pink",
        "bb-t-dark-color-02": "Red",
        "bb-t-light-color-03": "Light Yellow",
        "bb-t-dark-color-03": "Dark Yellow",
        "bb-t-light-color-04": "Light Orange",
        "bb-t-dark-color-04": "Dark Orange",
        "bb-t-light-color-05": "Light Green",
        "bb-t-dark-color-05": "Dark Green",
        "bb-t-light-color-06": "Light Blue",
        "bb-t-dark-color-06": "Dark Blue",
        "bb-t-light-color-07": "Light Violet",
        "bb-t-dark-color-07": "Dark Violet",
    },
    "innovation": {
        "mzp-t-light": "White",
        "mzp-t-dark": "Black",
        "bb-t-light-color-01": "Light Gray",
        "bb-t-dark-color-01": "Dark Gray",
        "bb-t-light-color-02": "Pink",
        "bb-t-dark-color-02": "Red",
        "bb-t-light-color-03": "Light Yellow",
        "bb-t-dark-color-03": "Dark Yellow",
        "bb-t-light-color-04": "Light Orange",
        "bb-t-dark-color-04": "Dark Orange",
        "bb-t-light-color-05": "Light Green",
        "bb-t-dark-color-05": "Dark Green",
        "bb-t-light-color-06": "Light Blue",
        "bb-t-dark-color-06": "Dark Blue",
        "bb-t-light-color-07": "Light Violet",
        "bb-t-dark-color-07": "Dark Violet",
    },
}

var fixupHelper = function(themeName){
    const themeColorOptionElements = document.querySelectorAll("[data-contentpath='color_theme'] option");
    const newLabels = colorLabels[themeName];
    Array.from(themeColorOptionElements).forEach(
        item => {
            if (newLabels.hasOwnProperty(item.label)){
                item.label=newLabels[item.label]
            }
        }
    )
};


window.Birdbox = window.Birdbox || {};

window.Birdbox.themeColorLabelFixup = fixupHelper
