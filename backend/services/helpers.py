from models.messageLog import MessageLog
from models.sequence import Sequence
from services.tools import create_sequence, edit_sequence, delete_step
from database import db

def save_to_log(user_id: int, session_id: str, role: str, content: str):
    try:
        log = MessageLog(user_id=user_id, session_id=session_id, role=role, content=content)
        db.session.add(log)
        db.session.commit()
    except Exception as e:
        print("Error saving to log:", e)

def get_session_messages(user_id, session_id):
    return (
        MessageLog.query
        .filter_by(
            user_id=user_id, 
            session_id=session_id
            )
        .order_by(MessageLog.timestamp.asc())
        .all()
    )

def build_message_history(history, rec_name, company_name, memory_text=None):

    brain = (
        f"You are Helix, a smart recruiter assistant for {rec_name} working at {company_name}.\n"
    )

    if memory_text:
        brain += f"\nHere is what the recruiter has previously said:\n{memory_text}\n"
        brain += "Avoid repeating or re-asking anything already mentioned except the required fields like City, Years of Experience, and Role. Since these three information will change for every role"

    messages = [{"role": "system", "content": brain}]

    if not history:
        messages.append({"role": "recruiter", "content": "Let's begin."})

    for msg in history:
        role = "user" if msg.role == "recruiter" else "assistant"
        messages.append({"role": role, "content": msg.content})

    return messages


def extract_tool_call(response):
    if response.choices and response.choices[0].message.function_call:
        return response.choices[0].message.function_call
    return None

def handle_create_sequence(user_id, company_name, session_id, rec_name, **args):

    sequence_result = create_sequence(rec_name, company_name, session_id, user_id, **args)
    summary = f"Created outreach sequence for {args['role']} in {args['city']}."
    save_to_log(user_id, session_id, "agent", summary)

    # return sequence_result

    return {
        "intent": "create_sequence",
        "arguments": args,
        "agent": summary,
        "sequence": sequence_result
    }

def handle_edit_sequence(user_id, session_id, **args):
    response = edit_sequence(user_id, session_id, **args)
    results = response.get("status")
    sequence_list = response.get("sequence_list")

    summary = "Edited sequence: " + " ".join(results)

    # save_to_log(user_id, session_id, "agent", summary)

    return {
        "intent": "edit_sequence",
        "agent": summary,
        "sequence": sequence_list
    }

def handle_delete_sequence(user_id, session_id, **args):
    response = delete_step(user_id, session_id, **args)
    summary = ", ".join(response.get("status", []))
    sequence_list = response.get("sequence_list")

    save_to_log(user_id, session_id, "agent", f"Deleted sequence step(s): {summary}")

    return {
        "intent": "delete_sequence",
        "agent": summary,
        "sequence": sequence_list
    }


