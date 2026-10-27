from flask import Blueprint, session, redirect, url_for, render_template
from services.profile_service import profile_service, update_profile_service

pages_bp = Blueprint("pages", __name__)


@pages_bp.route("/profile")
def profile_page():
    if session.get("user_id") is None:
        return redirect(url_for("signin_page"))

    user, status = profile_service(session["user_id"])

    if user is None:
        session.clear()
        return redirect(url_for("signin_page"))

    return render_template("profile.html", user=user)


@pages_bp.route("/profile/update", methods=["POST"])
def update_profile():
    if session.get("user_id") is None:
        return {
            "message": "Please sign in first."
        }, 401

    from flask import request

    data = request.get_json(silent=True)

    if not data:
        return {
            "message": "Invalid request."
        }, 400

    name = data.get("name", "").strip()
    email = data.get("email", "").strip()

    if not name or not email:
        return {
            "message": "Name and email are required."
        }, 400

    response, status_code = update_profile_service(
        session["user_id"],
        name,
        email
    )

    return response, status_code


@pages_bp.route("/about")
def about_page():
    if session.get("user_id") is None:
        return redirect(url_for("signin_page"))

    return render_template("about.html")


@pages_bp.route("/contact")
def contact_page():
    if session.get("user_id") is None:
        return redirect(url_for("signin_page"))

    return render_template("contact.html")