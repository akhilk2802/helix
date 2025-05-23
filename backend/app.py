from flask import Flask
from flask_cors import CORS
from database import db
from routes import register_blueprints
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)
    db.init_app(app)
    
    register_blueprints(app)

    with app.app_context():
        db.create_all()

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)