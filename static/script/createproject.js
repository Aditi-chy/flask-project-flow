
document.addEventListener("DOMContentLoaded", function () {
    const userButton = document.getElementById("userButton");
    const userMenu = document.getElementById("userMenu");

    const projectForm = document.getElementById("projectForm");
    const message = document.getElementById("createProjectMessage");
    const submitButton = document.getElementById("createProjectSubmit");

    if (userButton && userMenu) {
        userButton.addEventListener("click", function (event) {
            event.stopPropagation();

            const isOpen = userMenu.hidden;

            userMenu.hidden = !isOpen;
            userButton.setAttribute("aria-expanded", String(isOpen));
        });

        document.addEventListener("click", function (event) {
            if (
                !userButton.contains(event.target) &&
                !userMenu.contains(event.target)
            ) {
                userMenu.hidden = true;
                userButton.setAttribute("aria-expanded", "false");
            }
        });

        document.addEventListener("keydown", function (event) {
            if (event.key === "Escape") {
                userMenu.hidden = true;
                userButton.setAttribute("aria-expanded", "false");
                userButton.focus();
            }
        });
    }

    if (!projectForm || !submitButton || !message) {
        return;
    }

    projectForm.addEventListener("submit", async function (event) {
        event.preventDefault();

        const title = document.getElementById("title").value.trim();

        const description =
            document.getElementById("description").value;

        const duration =
            document.getElementById("duration").value;

        const agency =
            document.getElementById("agency").value.trim();

        const budget =
            document.getElementById("budget").value;

        message.textContent = "";
        message.className = "form-message";

        submitButton.disabled = true;

        try {
            const response = await fetch("/createproject", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    title: title,
                    description: description,
                    duration: duration,
                    agency: agency,
                    budget: budget
                })
            });

            const data = await response.json();

            if (
                response.ok &&
                data.message === "Project created successfully"
            ) {
                message.textContent = "Project created successfully!";
                message.classList.add("success");

                projectForm.reset();

                window.setTimeout(function () {
                    window.location.assign("/dashboard");
                }, 700);

            } else {
                message.textContent =
                    data.alert ||
                    data.message ||
                    "Unable to create project.";

                message.classList.add("error");
            }

        } catch (error) {
            console.error("Error creating project:", error);

            message.textContent =
                "Something went wrong. Please try again.";

            message.classList.add("error");

        } finally {
            submitButton.disabled = false;
        }
    });
});
