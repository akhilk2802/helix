from flask import Blueprint, request, jsonify
from services.agent_core import handle_chat

chat_bp = Blueprint("chat", __name__)

@chat_bp.route("/", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        user_id = data.get("user_id")
        user_message = data.get("message")

        if not user_id or not user_message:
            return jsonify({"error": "user_id and message are required"}), 400

        # Delegate chat handling to agent core
        response_data = handle_chat(user_id, user_message)

        return jsonify(response_data), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500