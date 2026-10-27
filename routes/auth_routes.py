from flask import Blueprint, request, jsonify, redirect
from services.auth_service import signup_service, signin_service, signout_service

auth_bp = Blueprint("auth", __name__)

#signup
@auth_bp.route("/signup", methods=["POST"])
def signup():
    data = request.get_json(silent=True)
    response, status_code = signup_service(data)
    return jsonify(response), status_code

#signin
@auth_bp.route("/signin", methods=["POST"])
def signin():
    data = request.get_json(silent=True)
    response, status_code = signin_service(data)
    return jsonify(response), status_code

#signout
@auth_bp.route("/signout", methods=["GET"])
def signout():
    session_response, status_code = signout_service()
    return redirect("/")