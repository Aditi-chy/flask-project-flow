from flask import session
from database import get_db
from queries import create_feedback

def feedback_service(data):
    if not isinstance(data, dict):
        return {"error": "Invalid request data."}, 400

    name = data.get("name", "")
    email = data.get("email", "")
    message = data.get("message", "")

    if not all(
        isinstance(value, str)
        for value in [name, email, message]
    ):
        return {"error": "Invalid input data."}, 400

    name = name.strip()
    email = email.strip()
    message = message.strip()

    if not name or not email or not message:
        return {"error": "Please fill in all fields."}, 400

    if len(name) > 100 or len(email) > 150:
        return {"error": "Name or email is too long."}, 400

    if (
        "@" not in email
        or "." not in email.rsplit("@", 1)[-1]
        or email.startswith("@")
    ):
        return {
            "error": "Please enter a valid email address."
        }, 400

    conn = None
    cursor = None

    try:
        conn = get_db()
        cursor = conn.cursor()

        user_id = session.get("user_id")

        create_feedback(
            cursor, user_id, name, email, message
        )

        conn.commit()

        return {
            "message": (
                "Thank you! Your feedback has been submitted "
                "successfully."
            )
        }, 201

    except Exception as e:
        if conn is not None:
            conn.rollback()

        print("Error submitting feedback:", e)

        return {
            "error": (
                "Unable to submit your feedback. Please try again."
            )
        }, 500

    finally:
        if cursor is not None:
            cursor.close()

        if conn is not None:
            conn.close()