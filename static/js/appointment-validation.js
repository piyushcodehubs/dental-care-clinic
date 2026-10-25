
document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("appointment-form");
    if (!form) return;

    const email = document.getElementById("patient-email");
    const phone = document.getElementById("patient-phone");
    const emailError = document.getElementById("email-error");
    const phoneError = document.getElementById("phone-error");
    const formError = document.getElementById("form-error");

    let submitted = false;

    function showError(input, errorElement, message) {
        input.classList.add("validation-invalid");
        input.classList.remove("validation-valid");
        input.setAttribute("aria-invalid", "true");
        errorElement.textContent = message;
    }

    function showValid(input, errorElement) {
        input.classList.remove("validation-invalid");
        input.classList.add("validation-valid");
        input.setAttribute("aria-invalid", "false");
        errorElement.textContent = "";
    }

    function validateEmail() {
        const value = email.value.trim();

        if (!value) {
            showError(email, emailError, "Email address is required.");
            return false;
        }

        if (
            value.length > 254 ||
            !/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(value)
        ) {
            showError(
                email,
                emailError,
                "Please enter a valid email address."
            );
            return false;
        }

        showValid(email, emailError);
        return true;
    }

    function validatePhone() {
        let value = phone.value.trim().replace(/[\s()-]/g, "");

        if (value.startsWith("+91")) {
            value = value.slice(3);
        } else if (value.startsWith("91") && value.length === 12) {
            value = value.slice(2);
        }

        if (!value) {
            showError(phone, phoneError, "Phone number is required.");
            return false;
        }

        if (!/^[6-9]\d{9}$/.test(value)) {
            showError(
                phone,
                phoneError,
                "Enter a valid 10-digit Indian mobile number."
            );
            return false;
        }

        showValid(phone, phoneError);
        return true;
    }

    email.addEventListener("input", () => {
        if (email.dataset.touched || submitted) validateEmail();
    });

    phone.addEventListener("input", () => {
        if (phone.dataset.touched || submitted) validatePhone();
    });

    email.addEventListener("blur", () => {
        email.dataset.touched = "true";
        validateEmail();
    });

    phone.addEventListener("blur", () => {
        phone.dataset.touched = "true";
        validatePhone();
    });

    form.addEventListener("submit", event => {
        submitted = true;

        const emailValid = validateEmail();
        const phoneValid = validatePhone();

        const otherRequired = [
            ...form.querySelectorAll("[required]")
        ].filter(field => field !== email && field !== phone);

        let otherValid = true;

        otherRequired.forEach(field => {
            if (!field.checkValidity()) {
                field.setAttribute("aria-invalid", "true");
                otherValid = false;
            } else {
                field.removeAttribute("aria-invalid");
            }
        });

        if (!emailValid || !phoneValid || !otherValid) {
            event.preventDefault();

            formError.textContent =
                "Please correct the highlighted fields before submitting.";

            const firstInvalid = form.querySelector(
                ".validation-invalid, [aria-invalid='true']"
            );

            firstInvalid?.focus();
        } else {
            formError.textContent = "";
        }
    });
});
