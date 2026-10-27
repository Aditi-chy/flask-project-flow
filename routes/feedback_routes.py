from flask import Blueprint, request, jsonify
from services.feedback_service import feedback_service

feedback_bp = Blueprint("feedback", __name__)

@feedback_bp.route("/feedback", methods=["POST"])
def feedback():
    data = request.get_json(silent=True)

    response, status_code = feedback_service(data)

    return jsonify(response), status_code