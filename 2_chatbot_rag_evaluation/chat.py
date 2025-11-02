import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from tools import record_user_details, record_unknown_question

load_dotenv(override=True)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL = "gpt-4o-mini"
NAME = "Aitor Bermejo"

# Tool schemas
RECORD_USER_DETAILS_SCHEMA = {
    "name": "record_user_details",
    "description": "Use this tool to record that a user is interested in being in touch and provided an email address",
    "parameters": {
        "type": "object",
        "properties": {
            "email": {
                "type": "string",
                "description": "The email address of this user"
            },
            "name": {
                "type": "string",
                "description": "The user's name, if they provided it"
            },
            "notes": {
                "type": "string",
                "description": "Any additional information about the conversation that's worth recording to give context"
            }
        },
        "required": ["email"],
        "additionalProperties": False
    }
}

RECORD_UNKNOWN_QUESTION_SCHEMA = {
    "name": "record_unknown_question",
    "description": "Always use this tool to record any question that couldn't be answered as you didn't know the answer",
    "parameters": {
        "type": "object",
        "properties": {
            "question": {
                "type": "string",
                "description": "The question that couldn't be answered"
            }
        },
        "required": ["question"],
        "additionalProperties": False
    }
}

TOOL_FUNCTIONS = {
    "record_user_details": record_user_details,
    "record_unknown_question": record_unknown_question,
}

TOOLS = [
    {"type": "function", "function": RECORD_USER_DETAILS_SCHEMA},
    {"type": "function", "function": RECORD_UNKNOWN_QUESTION_SCHEMA}
]


class Chat:
    def __init__(self, name=NAME):
        self.openai = OpenAI()
        self.name = name

    def system_prompt(self):
        return (f"""
                You are acting as {self.name}. You are answering questions on {self.name}'s website, particularly questions related to {self.name}'s career, background, skills, and experience.
                You are given a summary of {self.name}'s background and LinkedIn profile which you should use as the only source of truth to answer questions. 
                Interpret and answer based strictly on the information provided.
                You should never generate or write code. If asked to write code or build an app, explain whether {self.name}'s experience or past projects are relevant to the task, 
                and what approach {self.name} would take. If {self.name} has no relevant experience, politely acknowledge that.
                If a project is mentioned, specify whether it's a personal project or a professional one. Be professional and engaging — 
                the tone should be warm, clear, and appropriate for a potential client or future employer.
                If you don't know the answer to any question, use your record_unknown_question tool to record the question that you couldn't answer, even if it's about something trivial or unrelated to career. \
                If the user is engaging in discussion, try to steer them towards getting in touch via email; ask for their email and record it using your record_user_details tool.
                """
            )
        
    def handle_tool_calls(self, tool_calls):
        results = []
        for call in tool_calls:
            tool_name = call.function.name
            arguments = json.loads(call.function.arguments)
            print(f"Tool called: {tool_name}", flush=True)
            func = TOOL_FUNCTIONS.get(tool_name)
            result = func(**arguments) if func else {}
            results.append({
                "role": "tool",
                "content": json.dumps(result),
                "tool_call_id": call.id
            })
        return results

    def _execute_with_tools(self, messages):
        """Ejecuta la llamada a OpenAI manejando tool calls en un bucle."""
        done = False
        while not done:
            response = self.openai.chat.completions.create(
                model=MODEL,
                messages=messages,
                tools=TOOLS,
                max_tokens=500,
                temperature=0.5
            )
            
            if response.choices[0].finish_reason == "tool_calls":
                message = response.choices[0].message
                tool_calls = message.tool_calls
                results = self.handle_tool_calls(tool_calls)
                messages.append(message)
                messages.extend(results)
            else:
                done = True
                
        return response.choices[0].message.content

    def chat(self, question, history=[], context=None):
        if context:
            question += f"\n\nUse the following context to answer the question if helpful:\n{context}"

        messages = [
            {"role": "system", "content": self.system_prompt()}
        ] + history + [
            {"role": "user", "content": question}
        ]
        
        return self._execute_with_tools(messages)

    def rerun(self, original_reply, message, history, feedback):
        updated_prompt = self.system_prompt()
        updated_prompt += (
            "\n\n## Previous answer rejected\n"
            "You just tried to reply, but the quality control rejected your reply.\n"
            f"## Your attempted answer:\n{original_reply}\n\n"
            f"## Reason for rejection:\n{feedback}\n"
        )
        
        messages = [
            {"role": "system", "content": updated_prompt}
        ] + history + [
            {"role": "user", "content": message}
        ]
        
        return self._execute_with_tools(messages)