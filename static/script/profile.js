const editButton = document.getElementById("edit-profile");
const cancelButton = document.getElementById("cancel-edit");
const editForm = document.getElementById("edit-profile-form");

const profileView = document.getElementById("profile-view");
const profileActions = document.getElementById("profile-actions");

const profileName = document.getElementById("profile-name");
const profileEmail = document.getElementById("profile-email");

const nameInput = document.getElementById("edit-name");
const emailInput = document.getElementById("edit-email");

const profileMessage = document.getElementById("profile-message");

editButton.addEventListener("click", () => {
    profileView.style.display = "none";
    profileActions.style.display = "none";
    editForm.style.display = "block";

    profileMessage.textContent = "";
    nameInput.focus();
});

cancelButton.addEventListener("click", () => {
    editForm.style.display = "none";
    profileView.style.display = "grid";
    profileActions.style.display = "flex";

    nameInput.value = profileName.textContent;
    emailInput.value = profileEmail.textContent.trim();

    profileMessage.textContent = "";
});

editForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const name = nameInput.value.trim();
    const email = emailInput.value.trim();

    if (!name || !email) {
        profileMessage.textContent = "Name and email are required.";
        return;
    }

    try {
        const response = await fetch("/profile/update", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                name: name,
                email: email
            })
        });

        const data = await response.json();

        if (!response.ok) {
            profileMessage.textContent =
                data.message || "Unable to update profile.";
            return;
        }

        profileName.textContent = name;
        profileEmail.textContent = email;

        editForm.style.display = "none";
        profileView.style.display = "grid";
        profileActions.style.display = "flex";

        profileMessage.textContent = "";

    } catch (error) {
        profileMessage.textContent =
            "Something went wrong. Please try again.";
    }
});