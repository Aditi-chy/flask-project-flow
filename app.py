import os
from flask import Flask, render_template, session, redirect, url_for
from routes.auth_routes import auth_bp
from routes.feedback_routes import feedback_bp
from routes.project_routes import project_bp
from routes.page_routes import pages_bp
from services.project_service import get_user_projects

app = Flask(__name__)

# Session configuration (generates random secret key)
app.config["SECRET_KEY"] = os.environ.get(
    "SECRET_KEY",
    "dev-only-change-this-secret-key"
)

app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

#Blueprints- Instead of writing hundreds of routes in one single file, 
# a Blueprint allows you to group related features together 
# (such as authentication, user profiles, or an admin dashboard) 
# and plug them into your main Flask app later
# Register Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(feedback_bp)
app.register_blueprint(project_bp)
app.register_blueprint(pages_bp)

# Signup page
@app.route("/")
def home():
    return render_template("signup.html")

# Signin page
@app.route("/signin-page")
def signin_page():
    return render_template("signin.html")

# Dashboard page
@app.route("/dashboard")
def dashboard():
    user_id = session.get("user_id")

    if user_id is None:
        return redirect(url_for("signin_page"))

    projects = get_user_projects(user_id)

    return render_template(
        "dashboard.html",
        projects=projects
    )

# Create project page
@app.route("/create-project-page")
def create_project_page():
    if session.get("user_id") is None:
        return redirect(url_for("signin_page"))

    return render_template("createproject.html")

# Project details page
@app.route("/project-page")
def project_page():
    if session.get("user_id") is None:
        return redirect(url_for("signin_page"))

    return render_template("projectdetails.html")

if __name__ == "__main__":
    app.run(debug=True)