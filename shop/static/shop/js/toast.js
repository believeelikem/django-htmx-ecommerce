(() => {
  const MAX_TOASTS = 4;

  function trimToMax() {
    const stack = document.querySelector("#toast-stack");
    if (!stack) return;
    const toasts = Array.from(stack.querySelectorAll("[data-toast]"));
    // newest are at the top, so remove extras from the bottom
    toasts.slice(MAX_TOASTS).forEach(t => t.remove());
  }

  function initToast(toast) {
    if (toast.dataset.init === "1") return;
    toast.dataset.init = "1";

    // entrance animation
    requestAnimationFrame(() => toast.classList.add("is-in"));

    const timeoutMs = parseInt(toast.dataset.timeout || "5000", 10);
    let timer = null;
    let start = Date.now();
    let remaining = timeoutMs;

    const removeToast = () => {
      toast.classList.remove("is-in");
      toast.classList.add("is-out");
      // wait for transition
      setTimeout(() => toast.remove(), 260);
    };

    const arm = () => {
      start = Date.now();
      timer = setTimeout(removeToast, remaining);
    };

    const pause = () => {
      if (!timer) return;
      clearTimeout(timer);
      timer = null;
      remaining -= (Date.now() - start);
      if (remaining < 0) remaining = 0;
    };

    const resume = () => {
      if (timer) return;
      arm();
    };

    toast.addEventListener("mouseenter", pause);
    toast.addEventListener("mouseleave", resume);

    arm();
    trimToMax();
  }

  function initAll() {
    document.querySelectorAll("[data-toast]").forEach(initToast);
    trimToMax();
  }

  // Initial load
  document.addEventListener("DOMContentLoaded", initAll);

  // HTMX: after content is swapped in (including OOB inserts)
  document.addEventListener("htmx:afterSwap", initAll);
  document.addEventListener("htmx:oobAfterSwap", initAll);
})();
