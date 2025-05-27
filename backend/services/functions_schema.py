from typing import List, Dict

# This defines the available function call schemas for the OpenAI model

def get_tool_schemas() -> List[Dict]:
    return [
        {
            "name": "create_sequence",
            "description": "Only use this to generate a brand new 3-step recruiting sequence from scratch based on job role and location.",
            "parameters": {
                "type": "object",
                "properties": {
                "role": {
                    "type": "string",
                    "description": "The job title or position (e.g., 'frontend engineer')"
                },
                "city": {
                    "type": "string",
                    "description": "The city the candidate should be based in (e.g., 'Dallas')"
                },
                "years_of_experience": {
                    "type": "number",
                    "description": "How many years of experience the candidate should have"
                },
                "additional_context": {
                    "type": "string",
                    "description": "Optional. Any extra relevant info for the job or any information about the recruiter itself (e.g., 'remote role, cloud experience, growth team')"
                }
                },
                "required": ["role", "city", "years_of_experience"]
            }
        },
        {
            "name": "edit_sequence",
            "description": "Edit an existing step or append a new step to a recruiting sequence. Use this function when the recruiter wants to make a step more friendly, clear, detailed, or add a new one.",
            "parameters": {
                "type": "object",
                "properties": {
                    "step": {
                        "type": "integer",
                        "description": "The step number to edit or insert. For append, use the next available step number. For insert, use a step between existing ones."
                    },
                    "channel": {
                        "type": "string",
                        "description": "Channel to edit: 'email' or 'linkedin'. If omitted, applies to both.",
                        "nullable": True
                    },
                    "modification_instruction": {
                        "type": "string",
                        "description": "Instruction for how to change the content, e.g., 'make it more enthusiastic', 'add compensation details'"
                    },
                    "new_content": {
                        "type": "string",
                        "description": "Optional new message content or specific text to insert"
                    },
                    "mode": {
                        "type": "string",
                        "enum": ["update", "append", "insert"],
                        "description": "Choose 'update' to modify an existing step, 'append' to add to the end, or 'insert' to add between steps"
                    }
                },
                "required": ["mode"]
            }
        },
        {
            "name": "delete_step",
            "description": "Permanently delete a specific step from the most recent recruiting sequence. Only use this if the user clearly asks to remove a step.",
            "parameters": {
                "type": "object",
                "properties": {
                "step": {
                    "type": "integer",
                    "description": "The step number to delete"
                },
                "channel": {
                    "type": "string",
                    "description": "The channel ('email' or 'linkedin') where the step should be deleted. If not provided, delete the step for all channels."
                }
                },
                "required": ["step"]
            }
        }
    ]