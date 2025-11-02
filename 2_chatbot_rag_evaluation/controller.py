from chat import Chat
from retriever import Retriever

class ChatbotController:
    def __init__(self):
        self.chat = Chat()
        self.retriever = Retriever()
    
    def get_response(self, message, history = []):
        relevant_documents = self.retriever.get_relevant_documents(message)
        reply = self.chat.chat(message, history, context=relevant_documents)
        return reply



        