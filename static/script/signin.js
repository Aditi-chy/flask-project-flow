document.addEventListener("DOMContentLoaded", function () {
    const signinForm = document.getElementById("signinForm");
    const usernameInput = document.getElementById("signinUsername");
    const passwordInput = document.getElementById("signinPassword");
    const togglePassword = document.getElementById("togglePassword");
    const signinMessage = document.getElementById("signinMessage");

    if (togglePassword && passwordInput) {
        togglePassword.addEventListener("click", function () {
            const isPasswordHidden = passwordInput.type === "password";

            passwordInput.type = isPasswordHidden ? "text" : "password";

            togglePassword.innerHTML = `
                <span class="material-symbols-outlined">
                    ${isPasswordHidden ? "visibility_off" : "visibility"}
                </span>
            `;

            togglePassword.setAttribute(
                "aria-label",
                isPasswordHidden ? "Hide password" : "Show password"
            );

            togglePassword.setAttribute(
                "aria-pressed",
                String(isPasswordHidden)
            );
        });
    }

    if (signinForm) {
        signinForm.addEventListener("submit", async function (event) {
            event.preventDefault();

            const signinButton = signinForm.querySelector(".signin-button");

            const username = usernameInput.value.trim();
            const password = passwordInput.value;

            signinMessage.textContent = "";
            signinMessage.className = "form-message";

            signinButton.disabled = true;
            signinButton.innerHTML = "Signing in...";

            try {
                const response = await fetch("/signin", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    credentials: "same-origin",
                    body: JSON.stringify({
                        username: username,
                        password: password
                    })
                });

                const data = await response.json();

                if (response.ok && data.message === "Signin successful") {
                    signinMessage.textContent = data.message;
                    signinMessage.classList.add("success");

                    window.location.replace("/dashboard");
                    return;
                }

                signinMessage.textContent =
                    data.alert || data.message || "Sign in failed. Please check your details.";

                signinMessage.classList.add("error");

            } catch (error) {
                console.error("Sign-in error:", error);

                signinMessage.textContent =
                    "Unable to connect to the server. Please try again.";

                signinMessage.classList.add("error");

            } finally {
                signinButton.disabled = false;

                signinButton.innerHTML = `
                    Sign In
                    <span class="material-symbols-outlined">arrow_forward</span>
                `;
            }
        });
    }
});