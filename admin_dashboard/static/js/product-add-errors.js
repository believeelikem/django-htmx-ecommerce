document.addEventListener("DOMContentLoaded", () => {
    initProductForm();
});

// Shared config & state
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

let form = null;
let requiredFields = [];
let submitBtn = null;

// This is your original logic, just moved out so we can call it again
const checkFormState = (currentField = null) => {
    if (!form || !submitBtn || !requiredFields.length) return;

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

// Your original setup logic, now reusable
function initProductForm() {
    form = document.querySelector("form");
    if (!form) {
        return;
    }

    requiredFields = form.querySelectorAll("input[required], textarea[required], select[required]");
    submitBtn = document.querySelector("#add-btn-1");

    if (!submitBtn) {
        return;
    }

    // Listen to input events (same behavior as before)
    requiredFields.forEach(field => {
        field.addEventListener("input", () => checkFormState(field));
    });

    // Initialize button state
    checkFormState();
}

// HTMX: run the same setup when content is swapped in
document.body.addEventListener("htmx:afterSwap", (evt) => {
    const target = evt.detail && evt.detail.target ? evt.detail.target : null;
    if (!target) return;

    // If the main content area (containing the form) was swapped, re-init form logic
    if (target.matches(".admin-layout__main") || target.querySelector("form")) {
        initProductForm();
        return;
    }

    // Only recalc if an error element was updated (your original intent)
    if (errorSelectors.some(sel => target.matches(sel) || target.querySelector(sel))) {
        checkFormState();
    }
});
