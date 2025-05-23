from .chat import chat_bp
from .sequence import sequence_bp
from .user import user_bp

def register_blueprints(app):
    app.register_blueprint(chat_bp, url_prefix="/api/chat")
    app.register_blueprint(sequence_bp, url_prefix="/api/sequence")
    app.register_blueprint(user_bp, url_prefix="/api/user")