from pydantic import BaseModel
from openai import OpenAI
import os
from dotenv import load_dotenv

MODEL = "gemini-2.5-flash"

class Evaluation(BaseModel):
    question: str
    response: str
    is_acceptable: bool
    feedback: str = "No Feedback returned"

class Evaluator:
    def __init__(self, name="", model=MODEL):
        load_dotenv(override=True)
        api_key = os.getenv("GOOGLE_API_KEY")
        self.gemini = OpenAI(api_key=api_key, base_url="https://generativelanguage.googleapis.com/v1beta/openai/")
        self.name = name
        self.model = model

    def _evaluator_system_prompt(self):
        return f"You are an evaluator that decides whether a response to a question is acceptable. \
            You are provided with a conversation between a User and an Agent. Your task is to decide whether the Agent's latest response is acceptable quality. \
            The Agent is playing the role of {self.name} and is representing {self.name} on their website. \
            The Agent has been instructed to be professional and engaging, as if talking to a potential client or future employer who came across the website. \
            The Agent has been provided with context on {self.name} in the form of their summary, experience and CV. \
            With this context, please evaluate the latest response, replying with whether the response is acceptable and your feedback."

    def _evaluator_user_prompt(self, reply, message, history):
        return f"Here's the conversation between the User and the Agent: \n\n{history}\n\n" \
               f"Here's the latest message from the User: \n\n{message}\n\n" \
               f"Here's the latest response from the Agent: \n\n{reply}\n\n" \
               "Please evaluate the response, replying with whether it is acceptable and your feedback."
        
    def evaluate(self, reply, message, history) -> Evaluation:
        message=[
            {"role": "system", "content": self._evaluator_system_prompt()} 
            ] + [
            {"role": "user", "content": self._evaluator_user_prompt(reply, message, history)}
        ]
        response = self.gemini.beta.chat.completions.parse(model=self.model, messages=message, response_format=Evaluation)
        return response.choices[0].message.parsed
