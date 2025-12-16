document.addEventListener("click", (e) => {
const modal = document.querySelector("#modal");
if (!modal) return;

if (e.target.matches("[data-close='true']")) {
    modal.classList.add("closing");
    modal.addEventListener("animationend", () => modal.remove(), { once: true });
}
});

document.addEventListener("keydown", (e) => {
if (e.key === "Escape") {
    const modal = document.querySelector("#modal");
    if (!modal) return;
    modal.classList.add("closing");
    modal.addEventListener("animationend", () => modal.remove(), { once: true });
}
});

