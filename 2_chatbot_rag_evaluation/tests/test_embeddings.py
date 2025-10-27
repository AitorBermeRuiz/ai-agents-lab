import numpy as np
from langchain_huggingface import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)
# TIENE QUE ESTAR EN INGLES. MODELO NO SOPORTA TEXTO EN ESPAÑOL Y SE EMPIEZA A VOLVER LOCO.
texto1 = "I am a Python developer"
texto2 = "I work with .NET and C#"
texto3 = "I like chocolate"

vector1 = embeddings.embed_query(texto1)
vector2 = embeddings.embed_query(texto2)
vector3 = embeddings.embed_query(texto3)

def cos_sim(a, b):
    a = np.array(a)
    b = np.array(b)
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

s12 = cos_sim(vector1, vector2)
s13 = cos_sim(vector1, vector3)
s23 = cos_sim(vector2, vector3)

pairs = [("texto1", "texto2", s12), ("texto1", "texto3", s13), ("texto2", "texto3", s23)]
most_similar = max(pairs, key=lambda x: x[2]) # key=lambda x: x[2] es necesário por que tenemos una tupla. Con esto le indicamos que tome el valor 2

# Imprime dimensiones
print(f"Sim(texto1, texto2): {s12:.4f}")
print(f"Sim(texto1, texto3): {s13:.4f}")
print(f"Sim(texto2, texto3): {s23:.4f}")
print(f"Más similares: {most_similar[0]} y {most_similar[1]} con similitud {most_similar[2]:.4f}") # :.4f indica que haya 4 decimales