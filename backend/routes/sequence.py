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

@sequence_bp.route("/delete", methods=["DELETE"])
def delete_step():
    try:
        data = request.get_json()

        sequence_id = data.get("sequence_id")
        step = data.get("step")
        channel = data.get("channel")

        # Validate required fields
        if not all([sequence_id, step, channel]):
            return jsonify({"error": "Missing required fields: sequence_id, step, channel"}), 400

        # Query the specific step
        step_record = Sequence.query.filter_by(
            sequence_id=sequence_id,
            step=step,
            channel=channel
        ).first()

        if not step_record:
            return jsonify({
                "error": f"Step {step} with channel '{channel}' not found in sequence {sequence_id}"
            }), 404

        # Delete the record
        db.session.delete(step_record)
        db.session.commit()

        return jsonify({
            "message": f"Step {step} on '{channel}' in sequence {sequence_id} deleted successfully."
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

@sequence_bp.route("/edit", methods=["PUT"])
def edit_step():
    data = request.get_json()
    sequence_id = data.get("sequence_id")
    step = data.get("step")
    channel = data.get("channel")
    new_content = data.get("new_content")

    # Input validation
    if not all([sequence_id, step, channel, new_content]):
        return jsonify({"error": "Missing required fields: sequence_id, step, channel, new_content"}), 400

    try:
        # Find the step to update
        step_record = Sequence.query.filter_by(
            sequence_id=sequence_id,
            step=step,
            channel=channel
        ).first()

        if not step_record:
            return jsonify({"error": f"Step {step} on channel '{channel}' not found in sequence {sequence_id}"}), 404

        # Update the content
        print("update -> ", new_content.strip())
        step_record.content = new_content.strip()
        db.session.commit()

        return jsonify({
            "message": f"Step {step} on {channel} successfully updated.",
            "updated_step": {
                "sequence_id": sequence_id,
                "step": step,
                "channel": channel,
                "content": step_record.content
            }
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to update step: {str(e)}"}), 500
