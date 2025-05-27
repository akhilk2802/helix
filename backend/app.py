from flask import Flask
from flask_cors import CORS
from database import db
from routes import register_blueprints
from config import Config
from flask_socketio import SocketIO
from sockets.chat_socket import register_chat_sockets
from sockets.socketio_instance import socketio


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    CORS(app, supports_credentials=True)
    db.init_app(app)
    
    register_blueprints(app)

    socketio.init_app(app)

    with app.app_context():
        db.create_all()

    return app

app = create_app()
register_chat_sockets(socketio)

if __name__ == "__main__":
    # app.run(debug=True)
    socketio.run(app, debug=True)