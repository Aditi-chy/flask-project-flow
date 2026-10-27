import re
from flask import session
from werkzeug.security import generate_password_hash, check_password_hash
from database import get_db
from queries import create_user, get_user_by_username

#signup
def signup_service(data):

    if not isinstance(data, dict):
        return {"alert": "Please provide valid JSON data"}, 400

    name = data.get("name")
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not all(
        isinstance(value, str) and value.strip()
        for value in [name, username, email, password]
    ):
        return {"alert": "Please provide all data"}, 400

#removes unnecessary spaces from the beginning and end.
    name = name.strip()
    username = username.strip()
    email = email.strip().lower() #lower() used to create lower case for email address

    if len(name) > 30:
        return {"alert": "Name must not exceed 30 characters"}, 400

    if len(username) < 3 or len(username) > 10:
        return {"alert": "Username must be between 3 and 10 characters"}, 400

    email_pattern = r"^[\w.+-]+@[\w-]+(?:\.[\w-]+)+$"

    if not re.match(email_pattern, email):
        return {"alert": "Please provide a valid email address"}, 400

    if len(password) < 8:
        return {"alert": "Password must be at least 8 characters long"}, 400

    if len(password) > 30:
        return {"alert": "Password must not exceed 30 characters"}, 400

    password_hash = generate_password_hash(password) #create a random hash password so that password is not easily detected

    conn = None
    cursor = None

    try:
        conn = get_db()
        cursor = conn.cursor()

        create_user(
            cursor, name, username, email, password_hash
        )

        conn.commit()

        return {"message": "User registered successfully"}, 201

    except Exception as e:
        if conn:
            conn.rollback()

        if getattr(e, "errno", None) == 1062:
            return {"alert": "Username or email already exists"}, 409

        return {"alert": "Registration failed due to a server error"}, 500

    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()

#signin
def signin_service(data):

    if not isinstance(data, dict):
        return {"alert": "Please provide valid JSON data"}, 400

    username = data.get("username")
    password = data.get("password")

    if not isinstance(username, str) or not username.strip():
        return {"alert": "Please provide a valid username"}, 400

    if not isinstance(password, str) or not password:
        return {"alert": "Please provide a valid password"}, 400

    username = username.strip()

    if len(username) < 3 or len(username) > 10:
        return {"alert": "Username must be between 3 and 10 characters"}, 400

    conn = None
    cursor = None

    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)

        user = get_user_by_username(cursor, username)

        if not user or not check_password_hash(
            user["password"], password
        ):
            return {"alert": "Invalid username or password"}, 401

        session.clear()
        session["user_id"] = user["user_id"]
        session["name"] = user["name"]
        session["username"] = user["username"]

        return {
            "message": "Signin successful",
            "userid": user["user_id"]
        }, 200

    except Exception as e:
        print("Signin error:", e)
        return {"alert": "Signin failed due to a server error"}, 500

    finally:
        if cursor is not None:
            cursor.close()

        if conn is not None:
            conn.close()

#signout
def signout_service():
    session.clear()
    return {"message": "Signout successful"}, 200