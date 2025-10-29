import os
from dotenv import load_dotenv
from openai import OpenAI
from rag_v1 import Rag_V1


load_dotenv(override=True)


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL = "gpt-4o-mini"
NAME = "Aitor Bermejo"

class Chat:
    def __init__(self, name=NAME):
        self.openai = OpenAI()
        self.name = name
        self.rag = Rag_V1()

    
    
    def system_prompt(self):
        return (f"""
                You are acting as {self.name}. You are answering questions on {self.name}'s website, particularly questions related to {self.name}'s career, background, skills, and experience.
                You are given a summary of {self.name}'s background and LinkedIn profile which you should use as the only source of truth to answer questions. 
                Interpret and answer based strictly on the information provided.
                You should never generate or write code. If asked to write code or build an app, explain whether {self.name}'s experience or past projects are relevant to the task, 
                and what approach {self.name} would take. If {self.name} has no relevant experience, politely acknowledge that.
                If a project is mentioned, specify whether it's a personal project or a professional one. Be professional and engaging — 
                the tone should be warm, clear, and appropriate for a potential client or future employer.
                If a visitor engages in a discussion, try to steer them towards getting in touch via email. Ask for their email and record it using your record_user_details tool.
                Only accept inputs that follow the standard email format (like name@example.com). Do not confuse emails with phone numbers or usernames. If in doubt, ask for clarification.
                If you don't know the answer, just say so.
                """
            )
        
    def chat(self, question, history = []):


        # 1. Buscamos documentos relevantes.
        relevant_documents = self.rag.get_relevant_documents(question)
        if relevant_documents:
            question += f"\n\n Use the following context to answer the question if helpful:\n {relevant_documents}"

        # 2. Generamos respuesta.
        response = self.openai.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": self.system_prompt()},
                {"role": "user", "content": question}
            ],
            max_tokens=500, temperature=0.5,
        )
        return response.choices[0].message.content


if __name__ == "__main__":
# Start the chat interface
    chatbot = Chat(name="Aitor Bermejo")

    history = []
    print("ChatBot started! Type 'exit' to quit.")
    while True:
        question = input("\nYou: ")
        
        if question.lower() in ['exit', 'quit', 'q']:
            print("Goodbye!")
            break

        response = chatbot.chat(question, history)
        history.append({"role": "user", "content": question})
        history.append({"role": "assistant", "content": response})
        print(f"\nBot: {response}")



        