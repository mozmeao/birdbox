/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

import {
    checkEmailValidity,
    clearFormErrors,
    errorList,
    disableFormFields,
    enableFormFields,
    postToEmailServer,
} from "./form-utils";

// import "@mozilla-protocol/core/protocol/js/protocol-newsletter.min.js";
import MzpNewsletter from "@mozilla-protocol/core/protocol/js/newsletter";

let form;
let isBuilderPage;
let isMIECO;
let isInnovationPage;

const EmailForm = {
    handleFormError: (msg) => {
        let error;

        enableFormFields(form);

        switch (msg) {
            case errorList.EMAIL_INVALID_ERROR:
                error = form.querySelector(".error-email-invalid");
                break;
            case errorList.PRIVACY_POLICY_ERROR:
                error = form.querySelector(".error-privacy-policy");
                break;
            case errorList.NEWSLETTER_ERROR:
                error = form.querySelector(".error-newsletter-checkbox");
                break;
            case errorList.NAME_REQUIRED:
                error = form.querySelector(".error-name-required");
                break;
            default:
                error = form.querySelector(".error-try-again-later");
        }

        if (error) {
            const errorContainer = form.querySelector(".mzp-c-form-errors");
            errorContainer.classList.remove("hidden");
            errorContainer.style.display = "block";
            error.classList.remove("hidden");
        }
    },

    handleFormSuccess: () => {
        form.classList.add("hidden");
        const thanks = document.getElementById("newsletter-thanks");
        thanks.style.display = "block";
    },

    validateFields: () => {
        const email = form.querySelector('input[type="email"]').value;
        const name = form.querySelector('input[id="name"]').value;
        const privacy = !!form.querySelector('input[name="privacy"]:checked');
        const newsletters = form.querySelectorAll(
            'input[name="interests"]:checked'
        );

        // Really basic client side email validity check.
        if (!checkEmailValidity(email)) {
            EmailForm.handleFormError(errorList.EMAIL_INVALID_ERROR);
            return false;
        }

        // Confirm privacy policy is checked
        if (!privacy) {
            EmailForm.handleFormError(errorList.PRIVACY_POLICY_ERROR);
            return false;
        }

        // Confirm name is required on MIECO page
        if (!name && isMIECO) {
            EmailForm.handleFormError(errorList.NAME_REQUIRED);
            return false;
        }

        // the form on the builder page already includes a newsletter so these aren't required
        if (newsletters.length === 0 && !isBuilderPage) {
            EmailForm.handleFormError(errorList.NEWSLETTER_ERROR);
            return false;
        }

        return true;
    },

    submit: (e) => {
        const csrfToken = form.querySelector(
            '[name="csrfmiddlewaretoken"]'
        ).value;
        const email = form.querySelector('input[type="email"]').value;
        const url = form.getAttribute("action");
        const interests = Array.from(
            form.querySelectorAll('input[name="interests"]:checked')
        )
            .map((interests) => `${interests.value}`)
            .join(",");

        e.preventDefault();
        e.stopPropagation();

        // Disable form fields until POST has completed.
        disableFormFields(form);

        // Clear any prior messages that might have been displayed.
        clearFormErrors(form);

        // Perform client side form field validation.
        if (!EmailForm.validateFields()) {
            return;
        }

        if (isBuilderPage) {
            const newsletters =
                interests.length > 0
                    ? `mozilla-builder, ${interests}`
                    : "mozilla-builder";
            const params = { email, newsletters };
            postToEmailServer(
                url,
                params,
                EmailForm.handleFormSuccess,
                EmailForm.handleFormError,
                csrfToken
            );
        } else {
            const name = form.querySelector('input[id="name"]').value;
            const description = form.querySelector("textarea").value;

            const params = {
                email,
                name,
                description,
                interests,
            };

            if (isMIECO) {
                // The MIECO page will only send form info to email server -> mieco@mozilla.com
                postToEmailServer(
                    url,
                    { ...params, message_id: "mieco" },
                    EmailForm.handleFormSuccess,
                    EmailForm.handleFormError,
                    csrfToken
                );
            }
            if (isInnovationPage) {
                // On the innovation landing page the user can do the following in the form:
                //    - Sign up for the mozilla-innovation newsletter
                //    - Send an interest email to innovations@mozilla.com
                //    - They can also both of the above options

                const website = form.querySelector('input[name="website"]');
                if (interests.includes("newsletter")) {
                    postToEmailServer(
                        url,
                        {
                            ...params,
                            newsletters: "mozilla-innovation",
                            message_id: "innovations",
                        },
                        EmailForm.handleFormSuccess,
                        EmailForm.handleFormError,
                        csrfToken
                    );
                }

                if (interests.includes("collaboration")) {
                    postToEmailServer(
                        url,
                        {
                            ...params,
                            website: website.value || "",
                            message_id: "innovations",
                        },
                        EmailForm.handleFormSuccess,
                        EmailForm.handleFormError,
                        csrfToken
                    );
                }
            }
        }
    },

    handleCheckboxChange: ({ target }) => {
        const description = document.querySelector(".description");
        if (target.checked) {
            description.style.display = "block";
        } else {
            description.style.display = "none";
        }
    },

    init: () => {
        form = document.getElementById("newsletter-form");
        isBuilderPage = form.classList.contains("builders-form");
        isMIECO = form.classList.contains("mieco-form");
        isInnovationPage = form.classList.contains("innovations-form");

        if (!form) {
            return;
        }

        if (isInnovationPage) {
            const checkbox = form.querySelector("input#collaboration");

            if (checkbox?.checked) {
                const description = document.querySelector(".description");
                description.style.display = "block";
            }

            checkbox.addEventListener(
                "change",
                EmailForm.handleCheckboxChange,
                false
            );
        }

        form.addEventListener("submit", EmailForm.submit, false);
    },
};

EmailForm.init();
MzpNewsletter.init();
