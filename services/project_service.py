from decimal import Decimal, InvalidOperation
from flask import session
from database import get_db
from queries import (
    create_project_query, get_projects_by_user, get_project_by_id, update_project_query, delete_project_query
)

# Create project
def create_project_service(data):
    if not isinstance(data, dict):
        return {"alert": "Please provide valid JSON data"}, 400

    title = data.get("title")
    description = data.get("description")
    duration = data.get("duration")
    agency = data.get("agency")
    budget = data.get("budget")

    if not isinstance(title, str) or not title.strip():
        return {"alert": "Please provide a valid project title"}, 400

    title = title.strip()

    if len(title) > 20:
        return {"alert": "Title must not exceed 20 characters"}, 400

    if not isinstance(description, str) or not description.strip():
        return {"alert": "Please provide a project description"}, 400

    description = description.strip()

    if not isinstance(agency, str) or not agency.strip():
        return {"alert": "Please provide a valid agency"}, 400

    agency = agency.strip()

    if len(agency) > 20:
        return {"alert": "Agency must not exceed 20 characters"}, 400

    if isinstance(duration, bool) or not isinstance(duration, (int, str)):
        return {"alert": "Duration must be a positive whole number"}, 400

    if isinstance(duration, str):
        duration = duration.strip()

        if not duration.isdigit():
            return {"alert": "Duration must be a positive whole number"}, 400

        duration = int(duration)

    if duration <= 0:
        return {"alert": "Duration must be greater than zero"}, 400

    if isinstance(budget, bool) or not isinstance(budget, (int, float, str)):
        return {"alert": "Budget must be a valid number"}, 400

    try:
        budget = Decimal(str(budget).strip())

        if not budget.is_finite() or budget < 0:
            return {"alert": "Budget must be a non-negative number"}, 400

        if budget.as_tuple().exponent < -2:
            return {"alert": "Budget can have at most 2 decimal places"}, 400

        if budget >= Decimal("100000000"):
            return {"alert": "Budget exceeds the allowed limit"}, 400

    except (InvalidOperation, ValueError):
        return {"alert": "Budget must be a valid number"}, 400

    user_id = session.get("user_id")

    if user_id is None:
        return {"alert": "Please sign in before creating a project"}, 401

    conn = None
    cursor = None

    try:
        conn = get_db()
        cursor = conn.cursor()

        create_project_query(
            cursor, user_id, title, description, duration, agency, budget
        )

        conn.commit()

        return {"message": "Project created successfully"}, 201

    except Exception as e:
        if conn is not None:
            conn.rollback()

        print("Error creating project:", e)

        return {"alert": "Project creation failed due to a server error"}, 500

    finally:
        if cursor is not None:
            cursor.close()

        if conn is not None:
            conn.close()

# View projects
def viewproject_service():
    user_id = session.get("user_id")

    if user_id is None:
        return {"alert": "Please sign in to view your projects"}, 401

    conn = None
    cursor = None

    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)

        projects = get_projects_by_user(cursor, user_id)
        project_list = []

        for project in projects:
            project_list.append({
                "project_id": project["project_id"],
                "title": project["title"],
                "description": project["description"],
                "duration": project["duration"],
                "agency": project["agency"],
                "budget": float(project["budget"])
                    if project["budget"] is not None else None,
                "status": project["status"] or "Not Started",
                "created_at": project["created_at"].strftime("%Y-%m-%d")
                    if project["created_at"] else None
            })

        return {"projects": project_list}, 200

    except Exception as e:
        print("Error retrieving projects:", e)

        return {
            "alert": "Failed to retrieve projects due to a server error"
        }, 500

    finally:
        if cursor is not None:
            cursor.close()

        if conn is not None:
            conn.close()

# Get projects for a user
def get_user_projects(user_id):
    conn = None
    cursor = None

    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)

        projects = get_projects_by_user(cursor, user_id)

        for project in projects:
            if project["budget"] is not None:
                project["budget"] = float(project["budget"])

            if not project.get("status"):
                project["status"] = "Not Started"

        return projects

    finally:
        if cursor is not None:
            cursor.close()

        if conn is not None:
            conn.close()

# Project details
def projectdetails_service(project_id):
    if not project_id:
        return {"alert": "Please provide a project ID."}, 400

    user_id = session.get("user_id")

    if user_id is None:
        return {"alert": "Please sign in to view project details."}, 401

    conn = None
    cursor = None

    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)

        project = get_project_by_id(cursor, project_id, user_id)

        if not project:
            return {"message": "Project not found."}, 404

        created_at = project["created_at"]

        return {
            "project_id": project["project_id"],
            "title": project["title"],
            "description": project["description"],
            "duration": project["duration"],
            "agency": project["agency"],
            "budget": float(project["budget"])
                if project["budget"] is not None else None,
            "status": project["status"] or "Not Started",
            "created_at": created_at.isoformat() if created_at else None
        }, 200

    except Exception as e:
        print("Error retrieving project details:", e)

        return {"message": "Unable to load project details."}, 500

    finally:
        if cursor is not None:
            cursor.close()

        if conn is not None:
            conn.close()

# Update project
def updateproject_service(project_id, data):
    if not project_id:
        return {"alert": "Please provide project ID"}, 400

    user_id = session.get("user_id")

    if user_id is None:
        return {"alert": "Please sign in to update your project"}, 401

    if not isinstance(data, dict):
        return {"alert": "Please provide project data"}, 400

    title = data.get("title")
    description = data.get("description")
    duration = data.get("duration")
    agency = data.get("agency")
    budget = data.get("budget")
    status = data.get("status", "Not Started")

    allowed_statuses = {
        "Not Started",
        "In Progress",
        "On Hold",
        "Completed"
    }

    if status not in allowed_statuses:
        return {"alert": "Invalid project status"}, 400

    if not isinstance(title, str) or not title.strip():
        return {"alert": "Please provide a valid project title"}, 400

    title = title.strip()

    if len(title) > 20:
        return {"alert": "Title must not exceed 20 characters"}, 400

    if not isinstance(description, str) or not description.strip():
        return {"alert": "Please provide a project description"}, 400

    description = description.strip()

    if not isinstance(agency, str) or not agency.strip():
        return {"alert": "Please provide a valid agency"}, 400

    agency = agency.strip()

    if len(agency) > 20:
        return {"alert": "Agency must not exceed 20 characters"}, 400

    if isinstance(duration, bool) or not isinstance(duration, (int, str)):
        return {"alert": "Duration must be a positive whole number"}, 400

    if isinstance(duration, str):
        duration = duration.strip()

        if not duration.isdigit():
            return {"alert": "Duration must be a positive whole number"}, 400

        duration = int(duration)

    if duration <= 0:
        return {"alert": "Duration must be greater than zero"}, 400

    if isinstance(budget, bool) or not isinstance(budget, (int, float, str)):
        return {"alert": "Budget must be a valid number"}, 400

    try:
        budget = Decimal(str(budget).strip())

        if not budget.is_finite() or budget < 0:
            return {"alert": "Budget must be a non-negative number"}, 400

        if budget.as_tuple().exponent < -2:
            return {"alert": "Budget can have at most 2 decimal places"}, 400

        if budget >= Decimal("100000000"):
            return {"alert": "Budget exceeds the allowed limit"}, 400

    except (InvalidOperation, ValueError):
        return {"alert": "Budget must be a valid number"}, 400

    conn = None
    cursor = None

    try:
        conn = get_db()
        cursor = conn.cursor()

        update_project_query(
            cursor, title, description, duration, agency, budget, status, project_id, user_id
        )

        if cursor.rowcount == 0:
            conn.rollback()

            return {
                "message": "Project not found or no changes were made"
            }, 404

        conn.commit()

        return {
            "message": "Project updated successfully",
            "status": status
        }, 200

    except Exception as e:
        if conn is not None:
            conn.rollback()

        print("Error updating project:", e)

        return {"alert": "Failed to update project"}, 500

    finally:
        if cursor is not None:
            cursor.close()

        if conn is not None:
            conn.close()

# Delete project
def deleteproject_service(project_id):
    if not project_id:
        return {"alert": "please provide project id"}, 400

    user_id = session.get("user_id")

    if user_id is None:
        return {
            "alert": "Please sign in to delete your project"
        }, 401

    conn = None
    cursor = None

    try:
        conn = get_db()
        cursor = conn.cursor()

        delete_project_query(cursor, project_id, user_id)

        if cursor.rowcount == 0:
            conn.rollback()

            return {"message": "project not found"}, 404

        conn.commit()

        return {
            "message": "project deleted sucessfully"
        }, 200

    except Exception as e:
        if conn is not None:
            conn.rollback()

        print("Error deleting project:", e)

        return {"alert": "Failed to delete project"}, 500

    finally:
        if cursor is not None:
            cursor.close()

        if conn is not None:
            conn.close()