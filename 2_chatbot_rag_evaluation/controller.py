from chat import Chat
from retriever import Retriever
from evaluator import Evaluator
class ChatbotController:
    def __init__(self):
        self.chat = Chat()
        self.retriever = Retriever()
        self.evaluator = Evaluator(name="Aitor Bermejo")
    
    def get_response(self, message, history = []):
        relevant_documents = self.retriever.get_relevant_documents(message)
        reply = self.chat.chat(message, history, context=relevant_documents)
        evaluation = self.evaluator.evaluate(reply, message, history)

        retry_count = 0
        while not evaluation.is_acceptable and retry_count < 3:
            print("Retrying due to failed evaluation...")
            reply = self.chat.rerun(reply, message, history, evaluation.feedback)
            evaluation = self.evaluator.evaluate(reply, message, history)
            retry_count += 1

        return reply



        