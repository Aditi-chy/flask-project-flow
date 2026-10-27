from flask import Blueprint, request, jsonify

from services.project_service import (
    create_project_service, viewproject_service, projectdetails_service, updateproject_service, deleteproject_service
)

project_bp = Blueprint("project", __name__)

@project_bp.route("/createproject", methods=["POST"])
def create_project():
    data = request.get_json(silent=True)
    response, status_code = create_project_service(data)
    return jsonify(response), status_code

@project_bp.route("/viewproject", methods=["GET"])
def viewproject():
    response, status_code = viewproject_service()
    return jsonify(response), status_code

@project_bp.route("/projectdetails", methods=["GET"])
def projectdetails():
    project_id = request.args.get("project_id")

    response, status_code = projectdetails_service(project_id)
    return jsonify(response), status_code

@project_bp.route("/updateproject", methods=["PUT"])
def updateproject():
    project_id = request.args.get("project_id")
    data = request.get_json(silent=True)

    response, status_code = updateproject_service(project_id, data)
    return jsonify(response), status_code

@project_bp.route("/deleteproject", methods=["DELETE"])
def deleteproject():
    project_id = request.args.get("project_id")

    response, status_code = deleteproject_service(project_id)
    return jsonify(response), status_code