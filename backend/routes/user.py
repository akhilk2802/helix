from flask import Blueprint, request, jsonify
from models.user import User
from database import db

user_bp = Blueprint("user", __name__)

@user_bp.route("/", methods=["POST"])
def create_user():
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    preferences = data.get("preferences", {})

    user = User(name=name, email=email, preferences=preferences)
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User created", "user_id": user.id}), 201

@user_bp.route("/", methods=["GET"])
def get_users():
    users = User.query.all()
    result = [
        {"id": u.id, "name": u.name, "email": u.email, "preferences": u.preferences} for u in users
    ]
    return jsonify(result), 200