from models.sequence import Sequence
from database import db

def create_sequence(user_id: int, role: str, tone: str) -> list:
    """
    Create a basic outreach sequence with predefined steps.
    """
    steps = [
        f"Hi, I saw your background and thought you'd be a great fit for a {role} role.",
        f"We're building something exciting and looking for someone with your skill set.",
        f"If you're open to chatting, I’d love to tell you more. Let me know!"
    ]

    sequence_objects = []
    for i, content in enumerate(steps, start=1):
        seq = Sequence(user_id=user_id, step=i, content=content)
        db.session.add(seq)
        sequence_objects.append(seq)

    db.session.commit()

    return [{"step": s.step, "content": s.content} for s in sequence_objects]

def create_sequence(user_id: int, role: str, tone: str) -> list:
    sequence_objects = []
    outreach_pairs = [
        (
            f"Hi, I saw your LinkedIn profile and thought you'd be great for a {role} role.",
            f"Hi, I wanted to reach out via email about a {role} opportunity."
        ),
        (
            f"We're working on something exciting — open to a quick chat on LinkedIn?",
            f"We’d love to tell you more — would you be open to chatting over email?"
        ),
        (
            f"If this sounds interesting, happy to connect!",
            f"If you're curious, I'd love to send more info by email!"
        )
    ]

    for i, (linkedin_msg, email_msg) in enumerate(outreach_pairs, start=1):
        for channel, content in [("linkedin", linkedin_msg), ("email", email_msg)]:
            seq = Sequence(user_id=user_id, step=i, content=content, channel=channel)
            db.session.add(seq)
            sequence_objects.append(seq)

    db.session.commit()

    return [
        {"step": s.step, "channel": s.channel, "content": s.content}
        for s in sequence_objects
    ]

def edit_sequence(step_id: int, new_content: str) -> dict:
    """
    Edit a specific step in the sequence.
    """
    step = Sequence.query.get(step_id)
    if step:
        step.content = new_content
        db.session.commit()
        return {"step": step.step, "content": step.content}
    return {}

def delete_step(step_id: int) -> None:
    """
    Delete a specific step from the sequence.
    """
    step = Sequence.query.get(step_id)
    if step:
        db.session.delete(step)
        db.session.commit()