from database import get_db
from queries import get_user_by_id, update_user_query


def profile_service(user_id):
    conn = None
    cursor = None

    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)

        user = get_user_by_id(cursor, user_id)

        return user, 200 if user is not None else 404

    finally:
        if cursor is not None:
            cursor.close()

        if conn is not None:
            conn.close()


def update_profile_service(user_id, name, email):
    conn = None
    cursor = None

    try:
        conn = get_db()
        cursor = conn.cursor()

        update_user_query(cursor, user_id, name, email)

        conn.commit()

        return {"message": "Profile updated successfully."}, 200

    except Exception:
        if conn is not None:
            conn.rollback()

        return {"message": "Unable to update profile."}, 500

    finally:
        if cursor is not None:
            cursor.close()

        if conn is not None:
            conn.close()