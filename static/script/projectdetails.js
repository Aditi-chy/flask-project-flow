document.addEventListener("DOMContentLoaded", function () {
    const params = new URLSearchParams(window.location.search);
    const projectId = params.get("project_id");

    const userButton = document.getElementById("userButton");
    const userMenu = document.getElementById("userMenu");

    const projectTitle = document.getElementById("projectTitle");
    const detailsHeading = document.getElementById("detailsHeading");
    const detailsDescription = document.getElementById("detailsDescription");
    const detailsDuration = document.getElementById("detailsDuration");
    const detailsAgency = document.getElementById("detailsAgency");
    const detailsBudget = document.getElementById("detailsBudget");
    const detailsCreatedAt = document.getElementById("detailsCreatedAt");
    const detailsStatus = document.getElementById("detailsStatus");
    const detailsMessage = document.getElementById("detailsMessage"); // for displaying message like loading or please fill all the details

    const editPanel = document.getElementById("editProjectPanel");
    const editForm = document.getElementById("editProjectForm");
    const editButton = document.getElementById("editProjectButton");
    const cancelButton = document.getElementById("cancelEditButton");
    const saveButton = document.getElementById("saveProjectButton");
    const deleteButton = document.getElementById("deleteProjectButton");
    const editStatus = document.getElementById("editStatus");

    const allowedStatuses = [
        "Not Started",
        "In Progress",
        "On Hold",
        "Completed"
    ];

    let currentProject = null;
//for displaying message like loading or please fill all the details
    function showMessage(message, type = "") { 
        detailsMessage.textContent = message;
        detailsMessage.className = "details-message";

        if (type) {
            detailsMessage.classList.add(type);
        }
    }
// display date of project creation
    function formatDate(value) {
    if (!value) return "—";

    const date = new Date(value);

    if (Number.isNaN(date.getTime())) {
        return String(value);
    }

    return date.toLocaleDateString("en-IN", {
        day: "numeric",
        month: "long",
        year: "numeric"
    });
    }
    function displayProject(project) {
        currentProject = project;

        const status = allowedStatuses.includes(project.status)
            ? project.status
            : "Not Started";

        projectTitle.textContent = project.title || "Project Details";
        detailsHeading.textContent = project.title || "Project Overview";

        detailsDescription.textContent =
            project.description || "No description provided.";

        detailsDuration.textContent = project.duration
            ? `${project.duration} months`
            : "—";

        detailsAgency.textContent = project.agency || "—";

        const budget = Number(project.budget);

        detailsBudget.textContent =
            project.budget !== null &&
            project.budget !== undefined &&
            project.budget !== "" &&
            Number.isFinite(budget)
                ? `₹${budget.toLocaleString("en-IN", {
                    minimumFractionDigits: 2,
                    maximumFractionDigits: 2
                })}`
                : "—";

        detailsCreatedAt.textContent = formatDate(project.created_at);

        if (detailsStatus) {
            detailsStatus.textContent = status;
            detailsStatus.className =
                "project-status status-" +
                status.toLowerCase().replaceAll(" ", "-");
        }

        document.getElementById("editTitle").value = project.title || "";

        document.getElementById("editDescription").value =
            project.description || "";

        document.getElementById("editDuration").value =
            project.duration ?? "";

        document.getElementById("editAgency").value =
            project.agency || "";

        document.getElementById("editBudget").value =
            project.budget ?? "";

        if (editStatus) {
            editStatus.value = status;
        }

        currentProject.status = status;
    }

    async function loadProject() {
        if (!projectId) {
            showMessage("Project ID is missing from the URL.", "error");

            projectTitle.textContent = "Project Not Found";
            detailsHeading.textContent = "Project Not Found";

            detailsDescription.textContent =
                "Return to the dashboard and select a project.";

            editButton.disabled = true;
            deleteButton.disabled = true;
            return;
        }

        try {
            showMessage("Loading project details...");

            const response = await fetch(
                `/projectdetails?project_id=${encodeURIComponent(projectId)}`
            );

            const data = await response.json();

            if (!response.ok) {
                throw new Error(
                    data.alert || data.message || "Could not load project."
                );
            }

            displayProject(data);
            showMessage("");

        } catch (error) {
            showMessage(
                error.message || "Unable to load project details.",
                "error"
            );

            projectTitle.textContent = "Unable to Load Project";
            detailsHeading.textContent = "Project Details";

            detailsDescription.textContent =
                "Please return to the dashboard and try again.";

            editButton.disabled = true;
            deleteButton.disabled = true;
        }
    }

    if (userButton && userMenu) {
        userButton.addEventListener("click", function (event) {
            event.stopPropagation();

            userMenu.hidden = !userMenu.hidden;

            userButton.setAttribute(
                "aria-expanded",
                String(!userMenu.hidden)
            );
        });

        document.addEventListener("click", function (event) {
            if (
                !userMenu.contains(event.target) &&
                !userButton.contains(event.target)
            ) {
                userMenu.hidden = true;
                userButton.setAttribute("aria-expanded", "false");
            }
        });

        document.addEventListener("keydown", function (event) {
            if (event.key === "Escape") {
                userMenu.hidden = true;
                userButton.setAttribute("aria-expanded", "false");
            }
        });
    }

    editButton.addEventListener("click", function () {
        if (!currentProject) return;

        editPanel.hidden = false;
        editButton.hidden = true;
        showMessage("");

        editPanel.scrollIntoView({
            behavior: "smooth",
            block: "start"
        });

        document.getElementById("editTitle").focus();
    });

    cancelButton.addEventListener("click", function () {
        if (currentProject) {
            displayProject(currentProject);
        }

        editPanel.hidden = true;
        editButton.hidden = false;
        showMessage("");
    });

    editForm.addEventListener("submit", async function (event) {
        event.preventDefault();

        if (!currentProject) return;

        const updated = {
            title: document.getElementById("editTitle").value.trim(),
            description: document.getElementById("editDescription").value.trim(),
            duration: document.getElementById("editDuration").value,
            agency: document.getElementById("editAgency").value.trim(),
            budget: document.getElementById("editBudget").value,
            status: editStatus ? editStatus.value : currentProject.status
        };

        if (
            !updated.title ||
            !updated.description ||
            !updated.duration ||
            !updated.agency ||
            updated.budget === ""
        ) {
            showMessage("Please fill in all fields.", "error");
            return;
        }
// status of the project wether it is on hold not started working or completed
        if (!allowedStatuses.includes(updated.status)) {
            showMessage("Please select a valid project status.", "error");
            return;
        }

        if (
            Number(updated.duration) < 1 ||
            !Number.isInteger(Number(updated.duration)) ||
            !Number.isFinite(Number(updated.budget)) ||
            Number(updated.budget) < 0
        ) {
            showMessage("Enter a valid duration and budget.", "error");
            return;
        }

        saveButton.disabled = true;
        saveButton.textContent = "Saving...";
        showMessage("");
// PUT function is used to update project
        try {
            const response = await fetch(
                `/updateproject?project_id=${encodeURIComponent(projectId)}`,
                {
                    method: "PUT",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify(updated)
                }
            );

            const data = await response.json();

            if (!response.ok) {
                throw new Error(
                    data.alert || data.message || "Update failed."
                );
            }

            displayProject({
                ...currentProject,
                ...updated,
                duration: Number(updated.duration),
                budget: Number(updated.budget)
            });

            editPanel.hidden = true;
            editButton.hidden = false;

            showMessage(
                data.message || "Project updated successfully.",
                "success"
            );

        } catch (error) {
            showMessage(
                error.message || "Unable to update project.",
                "error"
            );

        } finally {
            saveButton.disabled = false;

            saveButton.innerHTML =
                '<span class="material-symbols-rounded">save</span> Save Changes';
        }
    });

    deleteButton.addEventListener("click", async function () {
        if (!currentProject) return;

        if (
            !confirm(
                `Are you sure you want to delete "${currentProject.title}"?`
            )
        ) {
            return;
        }

        deleteButton.disabled = true;
        deleteButton.textContent = "Deleting...";

        try {
            const response = await fetch(
                `/deleteproject?project_id=${encodeURIComponent(projectId)}`,
                { method: "DELETE" }
            );

            const data = await response.json();

            if (!response.ok) {
                throw new Error(
                    data.alert || data.message || "Delete failed."
                );
            }

            window.location.href = "/dashboard";

        } catch (error) {
            showMessage(
                error.message || "Unable to delete project.",
                "error"
            );

            deleteButton.disabled = false;

            deleteButton.innerHTML =
                '<span class="material-symbols-rounded">delete</span> Delete Project';
        }
    });

    loadProject();
});
