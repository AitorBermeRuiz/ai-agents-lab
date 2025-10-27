from rag_v1 import Rag_V1

class ChatBot:
    def __init__(self):
        self.rag = Rag_V1()

    def find_relevant_question_documents(self, question: str):
        """Get relevant documents for a given question."""
        return self.rag.get_relevant_documents(question)
    
    def start_chat(self):
        """Start an interactive terminal chat session."""
        print("ChatBot started! Type 'exit' to quit.")
        while True:
            # Get user input
            question = input("\nYou: ")
            
            # Check for exit command
            if question.lower() in ['exit', 'quit', 'q']:
                print("Goodbye!")
                break
                
            # Get and display relevant documents
            try:
                results = self.find_relevant_question_documents(question)
                if not results:
                    print("\nNo relevant documents found.")
                    continue
                    
                print("\nRelevant information:")
                for i, doc in enumerate(results, 1):
                    print(f"\n--- Document {i} ---")
                    print(doc)
            except Exception as e:
                print(f"\nAn error occurred: {e}")

if __name__ == "__main__":
    # Start the chat interface
    chatbot = ChatBot()
    chatbot.start_chat()