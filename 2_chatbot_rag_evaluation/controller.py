import asyncio
from chat import Chat
from retriever import Retriever
from evaluator import Evaluator


class ChatbotController:
    def __init__(self):
        self.chat = Chat()
        self.retriever = Retriever()
        self.evaluator = Evaluator(name="Aitor Bermejo")

    async def get_response(self, message, history=None):
        if history is None:
            history = []

        # Run sync retriever in thread to avoid blocking
        relevant_documents = await asyncio.to_thread(
            self.retriever.get_relevant_documents, message
        )
        reply = await self.chat.chat(message, history, context=relevant_documents)
        evaluation = await self.evaluator.evaluate(reply, message, history)

        retry_count = 0
        while not evaluation.is_acceptable and retry_count < 3:
            print("Retrying due to failed evaluation...")
            reply = await self.chat.rerun(reply, message, history, evaluation.feedback)
            evaluation = await self.evaluator.evaluate(reply, message, history)
            retry_count += 1

        return reply



        