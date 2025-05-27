from flask import Blueprint, request, jsonify
from models.user import User
from database import db

user_bp = Blueprint("user", __name__)

@user_bp.route("/signup", methods=["POST"])
def create_user():
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    company = data.get("company")

    user = User(name=name, email=email, company=company, password=password)
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User created", "user_id": user.id}), 201

@user_bp.route("/login", methods=["POST"])
def login_user():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400
    
    user = User.query.filter_by(email=email, password=password).first()

    if user:
        return jsonify({
            "message": "Login successful",
            "user": {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "company": user.company
            }
        }), 200
    else:
        return jsonify({"error": "Invalid email or password"}), 401

@user_bp.route("/", methods=["GET"])
def get_users():
    users = User.query.all()
    result = [
        {"id": u.id, "name": u.name, "email": u.email, "preferences": u.preferences} for u in users
    ]
    return jsonify(result), 200