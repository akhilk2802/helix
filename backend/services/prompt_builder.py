

def build_prompt(user_id: int, user_message: str, history: list) -> str:
    """
    Build a prompt by combining recent chat history with the user's current message.
    """
    prompt = "You are Helix, an intelligent recruiter assistant.\n"
    prompt += "You help recruiters craft personalized outreach sequences based on their intent.\n"
    prompt += "Maintain context and avoid asking redundant questions.\n\n"
    prompt += "Chat History:\n"

    for msg in history:
        role = "Recruiter" if msg.role == "user" else "Helix"
        prompt += f"{role}: {msg.content}\n"

    prompt += f"\nRecruiter: {user_message}\n"
    prompt += "Helix:"
    return prompt