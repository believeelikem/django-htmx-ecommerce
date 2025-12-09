document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector("form");
    const requiredFields = form.querySelectorAll("input[required], textarea[required], select[required]");
    const submitBtn = document.querySelector("#add-btn-1");

    const errorSelectors = [
        ".product-errors-name",
        ".product-errors-category",
        ".product-errors-tag",
        ".product-errors-quantity",
        ".product-errors-size",
        ".product-errors-color",
        ".product-errors-price",
        ".product-errors-image",
        ".product-errors-description"
    ];

    const checkFormState = (currentField = null) => {
        const emptyFields = Array.from(requiredFields).filter(f => !f.value.trim());
        const errors = Array.from(errorSelectors).map(sel => document.querySelector(sel));
        const hasErrors = errors.some(err => err && err.innerText.trim() !== "");

        // Enable/disable button
        if (emptyFields.length === 0 && !hasErrors) {
            submitBtn.disabled = false;
            submitBtn.style.opacity = "1";
        } else {
            submitBtn.disabled = true;
            submitBtn.style.opacity = "0.5";
        }

        // Optional: highlight last empty field
        if (currentField) {
            if (emptyFields.length === 1 && emptyFields[0] === currentField) {
                currentField.style.borderColor = "green";
            } else {
                currentField.style.borderColor = "";
            }
        }
    };

    // Listen to input events
    requiredFields.forEach(field => {
        field.addEventListener("input", () => checkFormState(field));
    });

    // Listen to HTMX swaps for live validation
    document.body.addEventListener("htmx:afterSwap", (evt) => {
        // Only recalc if an error element was updated
        if (errorSelectors.some(sel => evt.target.matches(sel))) {
            checkFormState();
        }
    });

    // Initialize button state
    checkFormState();
});
