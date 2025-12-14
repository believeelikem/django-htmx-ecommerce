document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector("#form");
    if (form) {
        checkFormState(form);
    }
});

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

// core logic: always works on the form passed in
function checkFormState(form, currentField = null) {
    if (!form) return;

    const requiredFields = form.querySelectorAll("input[required], textarea[required], select[required]");
    const submitBtn = form.querySelector("#add-btn-1");
    if (!submitBtn || !requiredFields.length) return;

    const emptyFields = Array.from(requiredFields).filter(f => !f.value.trim());

    const errors = errorSelectors
        .map(sel => form.querySelector(sel))
        .filter(Boolean);

    const hasErrors = errors.some(err => err.innerText.trim() !== "");

    if (emptyFields.length === 0 && !hasErrors) {
        submitBtn.disabled = false;
        submitBtn.style.opacity = "1";
    } else {
        submitBtn.disabled = true;
        submitBtn.style.opacity = "0.5";
    }

    if (currentField) {
        if (emptyFields.length === 1 && emptyFields[0] === currentField) {
            currentField.style.borderColor = "green";
        } else {
            currentField.style.borderColor = "";
        }
    }
}

// attach listeners via delegation so swaps don't break anything
document.body.addEventListener("input", (e) => {
    const form = e.target.closest("#form");
    if (!form) return;

    // make sure this is one of the required fields
    if (e.target.matches("input[required], textarea[required], select[required]")) {
        checkFormState(form, e.target);
    }
});

document.body.addEventListener("change", (e) => {
    const form = e.target.closest("#form");
    if (!form) return;

    if (e.target.matches("input[required], textarea[required], select[required]")) {
        checkFormState(form, e.target);
    }
});

// when htmx swaps content, re-evaluate the form state
document.body.addEventListener("htmx:afterSwap", (evt) => {
    const target = evt.detail?.target;
    if (!target) return;

    // if the form itself or something containing it was swapped
    const form =
        target.matches("#form")
            ? target
            : target.querySelector("#form");

    if (form) {
        checkFormState(form);
        return;
    }

    // if only an error <small> got swapped
    if (errorSelectors.some(sel => target.matches(sel) || target.querySelector(sel))) {
        const formEl = document.querySelector("#form");
        if (formEl) checkFormState(formEl);
    }
});
