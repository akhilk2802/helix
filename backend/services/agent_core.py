from services.prompt_builder import build_prompt
from services.llm_agent import call_llm
from services.tools import create_sequence, edit_sequence, delete_step
from models.messageLog import MessageLog
from database import db

def save_to_log(user_id: int, role: str, content: str):
    log = MessageLog(user_id=user_id, role=role, content=content)
    db.session.add(log)
    db.session.commit()

def get_recent_messages(user_id: int, limit: int = 10):
    return (
        MessageLog.query
        .filter_by(user_id=user_id)
        .order_by(MessageLog.timestamp.desc())
        .limit(limit)
        .all()[::-1]
    )

def handle_chat(user_id: int, message: str):
    # Step 1: Save user message to message log
    save_to_log(user_id, "user", message)

    # Step 2: Get chat history (if implementing memory)
    history = get_recent_messages(user_id)

    # Step 3: Build prompt using history + user message
    prompt = build_prompt(user_id, message, history)

    print("prompt -> ", prompt)

    # Step 4: Get LLM response
    llm_response = call_llm(prompt)

    # Step 5: (Optional) Tool detection logic
    tool_called = None
    sequence_result = []

    # Example hardcoded detection (replace with actual parsing logic)
    lowered = message.lower()

    if "create" in lowered and "sequence" in lowered:
        tool_called = "create_sequence"
        sequence_result = create_sequence(user_id=user_id, role="backend engineer", tone="friendly")
    
    elif "edit" in lowered and "step" in lowered:
        tool_called = "edit_sequence"
        step_id = 1  # TODO: Extract step ID dynamically
        new_content = "Updated content from user message"  # TODO: Extract content
        sequence_result = [edit_sequence(step_id=step_id, new_content=new_content)]

    elif "delete" in lowered and "step" in lowered:
        tool_called = "delete_step"
        step_id = 1  # TODO: Extract step ID dynamically
        delete_step(step_id=step_id)
        sequence_result = []

    # Step 6: Save agent message to log
    save_to_log(user_id, "agent", llm_response)

    # Step 7: Return structured response
    return {
        "response": llm_response,
        "tool_called": tool_called,
        "sequence": sequence_result
    }