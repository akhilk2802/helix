from flask import Blueprint, request, jsonify
from models.sequence import Sequence
from database import db

sequence_bp = Blueprint("sequence", __name__)

@sequence_bp.route("/", methods=["POST"])
def create_sequence():
    data = request.get_json()
    user_id = data.get("user_id")
    step = data.get("step")
    content = data.get("content")

    sequence = Sequence(user_id=user_id, step=step, content=content)
    db.session.add(sequence)
    db.session.commit()

    return jsonify({"message": "Sequence step created", "id": sequence.id}), 201

@sequence_bp.route("/<int:user_id>", methods=["GET"])
def get_sequences_by_user(user_id):
    sequences = Sequence.query.filter_by(user_id=user_id).all()
    result = [
        {"id": s.id, "step": s.step, "content": s.content, "created_at": s.created_at.isoformat()}
        for s in sequences
    ]
    return jsonify(result), 200 