document.addEventListener("DOMContentLoaded", function () {
    const userMenuButton = document.getElementById("userMenuButton");
    const userDropdown = document.getElementById("userDropdown");

    if (!userMenuButton || !userDropdown) {
        return;
    }

    userMenuButton.addEventListener("click", function (event) {
        event.stopPropagation();

        const isOpen = userDropdown.classList.toggle("show");

        userMenuButton.setAttribute("aria-expanded", String(isOpen));
    });

    document.addEventListener("click", function (event) {
        if (
            !userMenuButton.contains(event.target) &&
            !userDropdown.contains(event.target)
        ) {
            userDropdown.classList.remove("show");
            userMenuButton.setAttribute("aria-expanded", "false");
        }
    });

    document.addEventListener("keydown", function (event) {
        if (event.key === "Escape") {
            userDropdown.classList.remove("show");
            userMenuButton.setAttribute("aria-expanded", "false");
            userMenuButton.focus();
        }
    });
});
