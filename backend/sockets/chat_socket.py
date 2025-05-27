from flask_socketio import SocketIO, emit
from flask import request
from services.agent_core import handle_chat

def register_chat_sockets(socketio: SocketIO):

    @socketio.on("send_message")
    def handle_socket_chat(data):
        try:
            user_id = data.get("user_id")
            session_id = data.get("session_id")
            user_message = data.get("message")
            user_name = data.get("rec_name")
            company_name = data.get("company")

            if not user_id or not user_message:
                socketio.emit("chat_error", {"error": "Missing required fields"})
                return

            # Run the existing handle_chat logic
            response_data = handle_chat(
                user_id=user_id,
                message=user_message,
                rec_name=user_name,
                company_name=company_name,
                session_id=session_id,
                sid=request.sid
            )

            # Emit back to frontend
            socketio.emit("receive_message", {
                "message": user_message,
                "response": response_data
            }, to=request.sid)

        except Exception as e:
            socketio.emit("chat_error", {"error": str(e)}, to=request.sid)