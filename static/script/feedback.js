document.addEventListener("DOMContentLoaded", function () {
    const contactForm = document.getElementById("contactForm");
    const contactStatus = document.getElementById("contactStatus");
    const submitButton = contactForm.querySelector(
        "button[type='submit']"
    );

    contactForm.addEventListener("submit", async function (event) {
        event.preventDefault();

        const name = document.getElementById("contactName").value.trim();
        const email = document.getElementById("contactEmail").value.trim();
        const message = document.getElementById("contactMessage").value.trim();

        contactStatus.textContent = "";
        contactStatus.className = "";

        if (!name || !email || !message) {
            contactStatus.textContent = "Please fill in all fields.";
            contactStatus.classList.add("error");
            return;
        }

        submitButton.disabled = true;
        contactStatus.textContent = "Submitting your feedback...";

        try {
            const response = await fetch("/feedback", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    name: name,
                    email: email,
                    message: message
                })
            });

            const result = await response.json();

            if (!response.ok) {
                throw new Error(
                    result.error || "Unable to submit your feedback."
                );
            }

            contactStatus.textContent = result.message;
            contactStatus.classList.add("success");

            contactForm.reset();

        } catch (error) {
            contactStatus.textContent =
                error.message || "Something went wrong. Please try again.";

            contactStatus.classList.add("error");

        } finally {
            submitButton.disabled = false;
        }
    });
});