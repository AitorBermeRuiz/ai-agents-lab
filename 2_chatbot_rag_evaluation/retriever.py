import os
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DIRECTORY_NAME = os.path.join(BASE_DIR, "knowledge_base")
DB_NAME = os.path.join(BASE_DIR, "career_db")

class Retriever:
    def __init__(self, directory_name=DIRECTORY_NAME, db_name=DB_NAME ):
        self.directory_name = directory_name
        self.db_name = db_name
        self.retriever = None
        self.embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        self.init_or_load_db()

    def load_documents(self):
        # Ensure directory exists to avoid FileNotFoundError
        os.makedirs(self.directory_name, exist_ok=True)
        loader = DirectoryLoader(self.directory_name, glob="*.txt", loader_cls=TextLoader, loader_kwargs={"encoding": "utf-8"})
        documents = loader.load()
        print(f"Cargados {len(documents)} documentos\n\n")
        return documents

    def init_or_load_db(self):
        if os.path.exists(self.db_name):
            # Cargar DB existente
            vectorstore = Chroma(
                persist_directory=self.db_name,
                embedding_function=self.embeddings
            )
            print(f"Vectorstore loaded from {self.db_name}")
            print(f"Vectorstore contains {vectorstore._collection.count()} documents\n\n")
        else:
            # Crear nuevo DB
            documents = self.load_documents()
            if len(documents) == 0:
                # Initialize an empty vectorstore to avoid errors
                vectorstore = Chroma(
                    persist_directory=self.db_name,
                    embedding_function=self.embeddings
                )
                print(f"Vectorstore initialized empty at {self.db_name}\n\n")
            else:
                text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=100)
                documents_split = text_splitter.split_documents(documents)
                print(f"Total number of chunks: {len(documents_split)}")

                vectorstore = Chroma.from_documents(
                    documents_split, 
                    self.embeddings, 
                    persist_directory=self.db_name
                )
                print(f"Vectorstore created at {self.db_name}\n\n")
                print(f"Vectorstore created with {vectorstore._collection.count()} documents\n\n")
        
        # Lógica común para ambos casos (cargar o crear)
        self.retriever = vectorstore.as_retriever(search_kwargs={"k": 25})
        
    def get_relevant_documents(self, msg: str):
        docs = self.retriever.invoke(msg)
        return [doc.page_content for doc in docs]
