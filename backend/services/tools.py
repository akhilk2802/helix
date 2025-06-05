# services/sequence_manager.py

from models.sequence import Sequence
from database import db
from services.llm_agent import call_llm
import json
import uuid

def generate_sequence_id():
    return str(uuid.uuid4())[:4]

def fetch_latest_sequence(user_id, session_id):
    query = Sequence.query.filter_by(user_id=user_id)
    if session_id:
        query = query.filter_by(session_id=session_id)
    return query.order_by(Sequence.created_at.desc()).first()

def fetch_sequence_list(user_id, session_id, sequence_id):
    sequence = Sequence.query.filter_by(
        user_id=user_id, 
        session_id=session_id,
        sequence_id=sequence_id
    ).order_by(Sequence.step, Sequence.channel).all()

    return [{
        "sequence_id": s.sequence_id,
        "step": s.step,
        "channel": s.channel,
        "content": s.content
    } for s in sequence]

def create_sequence(rec_name, company_name, session_id, user_id, role, city, years_of_experience, additional_context=None):
    prompt = (
        f"You are Helix, an intelligent recruiter assistant helping a recruiter named {rec_name}.\n"
        f"Do not introduce yourself as Helix.\n"
        f"Generate a warm and professional 3-step recruiting sequence tailored for both LinkedIn and Email.\n"
        f"The candidate role is: {role}, based in {city}, with {years_of_experience} years of experience for {company_name}.\n"
        f"Return a JSON array with exactly 3 steps. Each step should have:\n"
        f"- 'step' (integer),\n- 'linkedin' (string),\n- 'email' (string).\n"
    )

    if additional_context:
        prompt += f"Additional context: {additional_context}\n"

    prompt += f"Use [Candidate's Name] as a placeholder if not already provided.\nEmails should be signed off by {rec_name}.\n"

    llm_response = call_llm(prompt)
    try:
        steps = json.loads(llm_response)
    except Exception as e:
        return {"error": "Failed to parse LLM output."}

    sequence_id = generate_sequence_id()
    result = []
    for step in steps:
        step_num = int("".join(filter(str.isdigit, str(step["step"]))))
        for channel in ["linkedin", "email"]:
            content = step[channel]
            seq = Sequence(
                user_id=user_id, session_id=session_id,
                sequence_id=sequence_id, step=step_num,
                channel=channel, content=content
            )
            db.session.add(seq)
            result.append({"sequence_id": sequence_id, "step": step_num, "channel": channel, "content": content})
    db.session.commit()
    return result

def edit_sequence(user_id, session_id, step=None, channel=None, mode="update", modification_instruction=None, new_content=None):
    results = []
    latest = fetch_latest_sequence(user_id, session_id)
    if not latest:
        return {"status": ["No sequences found for the user."]}
    sequence_id = latest.sequence_id

    if mode == "append":
        steps = Sequence.query.filter_by(user_id=user_id, sequence_id=sequence_id).order_by(Sequence.step.asc(), Sequence.channel.asc()).all()
        step_list = [{"step": s.step, "channel": s.channel, "content": s.content} for s in steps]
        last_step = db.session.query(db.func.max(Sequence.step)).filter_by(user_id=user_id, sequence_id=sequence_id).scalar() or 0
        new_step = last_step + 1

        print("modification_instruction -> ", modification_instruction)
        print("new_content -> ", new_content)

        prompt = (
            f"Add a new step to this sequence:\n{json.dumps(step_list, indent=2)}\n"
            f"Instruction: {modification_instruction}\n"
            f"New Requirements: {new_content}\n"
            f"Return a JSON object with exactly three keys: 'step', 'email', and 'linkedin'.\n"
            f"- 'step' should be an integer.\n"
            f"- 'email' should contain the email content.\n"
            f"- 'linkedin' should contain the LinkedIn message.\n"
            f"Do not include a 'channel' field. Return only this JSON object."
        )
        llm_response = call_llm(prompt).strip()
        try:
            parsed = json.loads(llm_response)
        except Exception as e:
            return {"status": [f"Failed to parse LLM response: {e}"], "raw_response": llm_response}
        
        print("llm_response -> ", llm_response)

        channels_to_append = [channel] if channel in ["linkedin", "email"] else ["linkedin", "email"]
        print("channel requested by the user -> ", channel)
        print("channels to append -> ", channels_to_append)

        for ch in channels_to_append:
            seq = Sequence(
                user_id=user_id, session_id=session_id, sequence_id=sequence_id,
                step=new_step, channel=ch, content=parsed.get(ch, "")
            )
            db.session.add(seq)
            results.append(f"Appended step {new_step} on {ch}")

        db.session.commit()

    elif mode == "update":
        for ch in [channel] if channel else ["linkedin", "email"]:
            step_to_update = Sequence.query.filter_by(
                user_id=user_id, sequence_id=sequence_id, step=step, channel=ch
            ).first()
            if not step_to_update:
                results.append(f"Step {step} on {ch} not found.")
                continue

            prompt = f"""Rewrite the following message:\n\"\"\"{step_to_update.content}\"\"\"\n"""
            if modification_instruction:
                prompt += f"Instruction: {modification_instruction}\n"
            if new_content:
                prompt += f"New Requirements: {new_content}\n"
            step_to_update.content = call_llm(prompt).strip()
            results.append(f"Updated step {step} on {ch}.")

        db.session.commit()

    return {
        "status": results,
        "sequence_list": fetch_sequence_list(user_id, session_id, sequence_id)
    }

def delete_step(user_id, session_id, step=None, channel=None):
    results = []
    latest = fetch_latest_sequence(user_id, session_id)
    if not latest:
        return {"status": ["No sequences found for the user."]}

    sequence_id = latest.sequence_id
    if step is None:
        return {"status": ["Step number is required."]}

    for ch in [channel] if channel else ["email", "linkedin"]:
        deleted_count = Sequence.query.filter_by(
            user_id=user_id, session_id=session_id, sequence_id=sequence_id,
            step=step, channel=ch
        ).delete()
        results.append(f"Deleted step {step} on {ch}" if deleted_count else f"Step {step} on {ch} not found")

    db.session.commit()
    return {
        "status": results,
        "sequence_list": fetch_sequence_list(user_id, session_id, sequence_id)
    }