document.addEventListener("DOMContentLoaded", function () {
    const signupForm = document.getElementById("signupForm");
    const passwordInput = document.getElementById("signupPassword");
    const togglePassword = document.getElementById("togglePassword");
    const signupMessage = document.getElementById("signupMessage");

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

    if (signupForm) {
        signupForm.addEventListener("submit", async function (event) {
            event.preventDefault();

            const signupButton = signupForm.querySelector(".signup-button");

            const name = document.getElementById("signupName").value.trim();
            const username = document.getElementById("signupUsername").value.trim();
            const email = document.getElementById("signupEmail").value.trim();
            const password = passwordInput.value;

            signupMessage.textContent = "";
            signupMessage.className = "form-message";

            signupButton.disabled = true;
            signupButton.innerHTML = "Creating account...";

            try {
                const response = await fetch("/signup", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({
                        name: name,
                        username: username,
                        email: email,
                        password: password
                    })
                });

                const data = await response.json();

                if (!response.ok) {
                    signupMessage.textContent =
                        data.alert || "Registration failed. Please try again.";

                    signupMessage.classList.add("error");
                    return;
                }

                if (data.message === "User registered successfully") {
                    signupMessage.textContent = data.message;
                    signupMessage.classList.add("success");

                    signupForm.reset();

                    setTimeout(function () {
                        window.location.href = "/signin-page";
                    }, 1000);
                } else {
                    signupMessage.textContent =
                        data.alert || "Something went wrong. Please try again.";

                    signupMessage.classList.add("error");
                }

            } catch (error) {
                console.error(error);

                signupMessage.textContent =
                    "Unable to connect to the server. Please try again.";

                signupMessage.classList.add("error");

            } finally {
                signupButton.disabled = false;

                signupButton.innerHTML = `
                    Create account
                    <span class="material-symbols-outlined">arrow_forward</span>
                `;
            }
        });
    }
});