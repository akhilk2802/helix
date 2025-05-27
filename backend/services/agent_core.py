import os
import json
import openai
from services.helpers import handle_delete_sequence, handle_edit_sequence, handle_create_sequence, save_to_log, get_session_messages, build_message_history, extract_tool_call
from services.functions_schema import get_tool_schemas
from services.vector_store import store_message_in_memory, retrieve_similar_memory
from sockets.socketio_instance import socketio

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_llm_response(messages):
    
    client = openai.OpenAI()
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=messages,
        functions=get_tool_schemas(),
        function_call="auto"
    )

    return response


def handle_chat(user_id, message, rec_name, company_name, session_id, sid=None):

    save_to_log(user_id, session_id, "recruiter", message) # Save to Postgres
    store_message_in_memory(user_id, session_id, message) # Save to ChromaDB for memory
    history = get_session_messages(user_id, session_id) # Get memory from current session - from postgres
    similar_memory = retrieve_similar_memory(user_id, message) # Get similar memory if any in the ChromaDB
    
    # print("similtar memory -> ", similar_memory)

    memory_text = "\n".join(similar_memory)
    messages = build_message_history(history, rec_name, company_name) # Brain of the AI - with prev messages and content

    response = generate_llm_response(messages)
    # print("Response -> ", response)
    tool_call = extract_tool_call(response) # Extract the intent of the message

    # print("tool_call -> ", tool_call)

    if not tool_call:
        response_message = response.choices[0].message.content
        return {
            "intent": None,
            "arguments": {},
            "agent": response_message
        }

    tool_name = tool_call.name
    args = json.loads(tool_call.arguments)

    # print("tool_name -> ", tool_name)
    # print("args -> ", args)

    socketio.emit("tool_call", {
        "tool": tool_name,
        "session_id": session_id,
        "user_id": user_id
    }, to=sid)


    if tool_name == "create_sequence":
        return handle_create_sequence(user_id, company_name, session_id, rec_name, **args)
    elif tool_name == "edit_sequence":  
        return handle_edit_sequence(user_id, session_id, **args)
    elif tool_name == "delete_step":
        return handle_delete_sequence(user_id, session_id, **args)


    return {
        "intent": None,
        "arguments": {},
        "agent": response.choices[0].message.content or "I’m not sure what to do with that."
    }