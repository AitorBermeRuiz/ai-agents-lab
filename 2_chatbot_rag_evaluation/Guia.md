# 🎓 **Guía de Aprendizaje: Replica tu RAG Chatbot**

## 🎯 **Filosofía: Construye desde Cero, No Copies**

**Estrategia:** Pequeñas victorias → Complejidad gradual → Integración

---

## 📍 **FASE 0: Setup Inicial (30 min)**

### **Paso 0.1: Estructura del Proyecto**

```
mi-chatbot/
├── .env                    # ← Empieza aquí
├── requirements.txt        # ← Lista de librerías
├── knowledge_base/         # ← Tus documentos
│   └── mi_cv.txt
└── tests/                  # ← Para validar cada paso
    └── test_paso1.py
```

### **Paso 0.2: Crear Documentos de Conocimiento**

**TAREA:** Crea `knowledge_base/mi_cv.txt` con tu info real (3-4 párrafos)

**Objetivo:** Tener datos reales para probar

**Validación:** ¿Puedes leer el archivo con Python?

```python
# test_paso1.py - Escribe esto TÚ
# Pista: Usa open() y .read()
```

---

## 🏗️ **FASE 1: RAG Básico - El Buscador (2-3 horas)**

### **¿Por qué empezar aquí?**
- ✅ Es independiente (no necesita el resto)
- ✅ Es visual (ves resultados inmediatos)
- ✅ Entiendes el concepto clave de RAG

### **Paso 1.1: Cargar Documentos**

**OBJETIVO:** Leer todos los archivos .txt de una carpeta

**Conceptos nuevos (busca en Google):**
- `DirectoryLoader` de langchain
- Encoding UTF-8
- Glob patterns

**TAREA:** Crea `rag_v1.py` que:
1. Lea todos los .txt de `knowledge_base/`
2. Imprima cuántos documentos encontró
3. Imprima los primeros 200 caracteres de cada uno

**Validación:** Ejecuta y verifica que imprime tu contenido

**Recursos para buscar:**
- "langchain DirectoryLoader example"
- "python read files from directory"

---

### **Paso 1.2: Dividir en Chunks**

**OBJETIVO:** Dividir textos largos en fragmentos

**Conceptos nuevos:**
- CharacterTextSplitter
- chunk_size, chunk_overlap

**EXPERIMENTO:** 
- Prueba con chunk_size=500, overlap=100
- Prueba con chunk_size=2000, overlap=500
- ¿Cuál funciona mejor para TU contenido?

**TAREA:** Modifica `rag_v1.py` para:
1. Dividir documentos en chunks
2. Imprimir número total de chunks
3. Mostrar 2-3 chunks de ejemplo

**Pregunta reflexiva:** ¿Por qué es necesario dividir? ¿Qué pasa si no lo haces?

---

### **Paso 1.3: Generar Embeddings (Primera Prueba con IA)**

**OBJETIVO:** Convertir texto en vectores

**Conceptos nuevos:**
- Embeddings
- HuggingFaceEmbeddings
- Modelos pre-entrenados

**EXPERIMENTO MANUAL:**
```python
# Crea test_embeddings.py
from langchain_huggingface import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Prueba con 2 frases
texto1 = "Soy desarrollador de Python"
texto2 = "Trabajo con .NET y C#"
texto3 = "Me gusta el chocolate"

vector1 = embeddings.embed_query(texto1)
vector2 = embeddings.embed_query(texto2)
vector3 = embeddings.embed_query(texto3)

# Imprime dimensiones
print(f"Dimensiones: {len(vector1)}")

# Bonus: Calcula similitud (busca cómo calcular cosine similarity)
```

**Pregunta reflexiva:** ¿Cuáles tienen vectores más similares? ¿Por qué?

---

### **Paso 1.4: Crear Vector Database**

**OBJETIVO:** Guardar chunks con sus embeddings en ChromaDB

**Conceptos nuevos:**
- Chroma
- persist_directory
- from_documents

**TAREA:** Modifica `rag_v1.py` para:
1. Crear vectorstore con Chroma
2. Guardar en carpeta `./mi_db`
3. Imprimir confirmación de guardado

**Validación:** 
- ¿Se creó la carpeta `mi_db/`?
- ¿Puedes volver a ejecutar sin error?
- ¿Detecta que la BD ya existe?

---

### **Paso 1.5: Buscar (¡Lo Emocionante!)**

**OBJETIVO:** Hacer tu primera búsqueda semántica

**TAREA:** Crea `buscar.py` que:
1. Cargue la BD existente (sin recrear)
2. Acepte una pregunta por consola
3. Busque los 5 chunks más relevantes
4. Imprima los resultados

**Experimento:**
```bash
python buscar.py
> ¿Qué experiencia tienes con Python?

python buscar.py
> ¿Cuáles son tus proyectos?
```

**Validación crítica:** 
- ¿Encuentra información relevante?
- ¿Qué pasa si preguntas algo que NO está en tus docs?

---

### **🎉 CHECKPOINT 1: RAG Funcional**

**Antes de continuar, debes tener:**
- ✅ Script que carga documentos
- ✅ Script que divide en chunks
- ✅ BD vectorial creada
- ✅ Script de búsqueda funcionando
- ✅ Entiendes QUÉ hace cada parte

**Test final:** ¿Puedes explicarle a alguien cómo funciona el RAG sin mirar código?

---

## 🤖 **FASE 2: Chat Básico - El Generador (2 horas)**

### **¿Por qué ahora?**
Ya tienes el RAG. Ahora necesitas que OpenAI use esa información.

### **Paso 2.1: Primera Llamada a OpenAI (Sin RAG)**

**OBJETIVO:** Hacer tu primera llamada simple

**TAREA:** Crea `chat_v1.py` que:
1. Lea tu API key de .env
2. Haga UNA llamada simple a OpenAI
3. Imprima la respuesta

```python
# Estructura básica (complétala TÚ):
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

# Tu pregunta hardcodeada
mensaje = "¿Qué es Python?"

# Llama a la API (busca la sintaxis correcta)
# response = client.chat.completions.create(...)

# Imprime respuesta
```

**Validación:** ¿Responde correctamente?

---

### **Paso 2.2: Añadir System Prompt**

**OBJETIVO:** Hacer que el bot tenga personalidad

**EXPERIMENTO:** Prueba diferentes system prompts:
1. "Eres un asistente técnico formal"
2. "Eres un mentor amigable que explica con ejemplos"
3. "Eres un experto en Python que responde concisamente"

**Observa:** ¿Cómo cambia el tono de las respuestas?

**TAREA:** Crea un system prompt para TU caso de uso

---

### **Paso 2.3: Integrar RAG con Chat**

**OBJETIVO:** ¡Unir ambas piezas!

**TAREA:** Crea `chat_con_rag.py` que:
1. Reciba una pregunta
2. Use tu `rag_v1.py` para buscar contexto
3. Añada el contexto al mensaje del usuario
4. Llame a OpenAI
5. Imprima respuesta

**Estructura conceptual:**
```
Pregunta Usuario
    ↓
Buscar en RAG (5 chunks)
    ↓
Construir mensaje: "Pregunta + Contexto"
    ↓
OpenAI
    ↓
Respuesta
```

**Validación crítica:**
- Pregunta algo que SÍ está en tus docs
- Pregunta algo que NO está
- ¿Diferencia las respuestas?

---

### **Paso 2.4: Añadir Historial**

**OBJETIVO:** Mantener contexto de conversación

**CONCEPTO:** Cada mensaje debe incluir el historial anterior

**TAREA:** Modifica `chat_con_rag.py` para:
1. Mantener lista de mensajes
2. En cada nueva pregunta, incluir historial
3. Probar conversación multi-turno

**Prueba:**
```
Tú: ¿Qué experiencia tienes con Python?
Bot: [respuesta]

Tú: ¿Y en qué proyectos lo usaste?  # ← Debe entender "lo" = Python
Bot: [respuesta con contexto]
```

---

### **🎉 CHECKPOINT 2: Chat + RAG Funcional**

**Debes tener:**
- ✅ Script que busca en RAG
- ✅ Script que llama a OpenAI
- ✅ Integración: RAG → OpenAI
- ✅ Conversación con historial

**Test:** Mantén una conversación de 3-4 turnos

---

## 🏛️ **FASE 3: Arquitectura - Organizar (1-2 horas)**

### **¿Por qué ahora?**
Ya funciona, pero está desorganizado. Hora de estructurar.

### **Paso 3.1: Crear Clases**

**OBJETIVO:** Convertir scripts en clases reutilizables

**TAREA:** Crea `rag.py` con:
```python
class Retriever:
    def __init__(self):
        # Inicializa embeddings, carga/crea BD
        pass
    
    def search(self, query, k=5):
        # Busca y retorna chunks
        pass
```

**Reto:** Migra tu código de `rag_v1.py` a esta clase

---

### **Paso 3.2: Clase Chat**

**TAREA:** Crea `chat.py` con:
```python
class Chat:
    def __init__(self, name):
        # Inicializa OpenAI client
        pass
    
    def get_system_prompt(self):
        # Retorna tu system prompt
        pass
    
    def chat(self, message, history, context=None):
        # Genera respuesta
        pass
```

---

### **Paso 3.3: Controlador**

**OBJETIVO:** Orquestar Retriever + Chat

**TAREA:** Crea `controller.py` que:
1. Inicialice Retriever y Chat
2. Tenga método `get_response(message, history)`
3. Internamente: busque → genere → retorne

**Validación:** Mismo resultado que antes, pero código más limpio

---

## 🎨 **FASE 4: Interfaz Web (1 hora)**

### **Paso 4.1: Gradio Mínimo**

**OBJETIVO:** Tu primer chatbot visual

**TAREA:** Crea `app.py`:
```python
import gradio as gr
from controller import Controller

controller = Controller(name="Tu Nombre")

def respond(message, history):
    # Llama a controller.get_response()
    # Retorna respuesta
    pass

gr.ChatInterface(respond, type="messages").launch()
```

**Validación:** Abre en navegador y chatea

---

## ✅ **FASE 5: Evaluador (Opcional - 2 horas)**

**Solo si quieres calidad automática:**

### **Paso 5.1: Evaluador Simple**

**OBJETIVO:** Detectar respuestas malas

**TAREA:** Crea `evaluator.py` que:
1. Reciba pregunta + respuesta
2. Llame a Gemini para evaluar
3. Retorne bool: ¿es aceptable?

### **Paso 5.2: Loop de Reintentos**

**TAREA:** Modifica `controller.py` para:
1. Evaluar respuesta
2. Si falla, reintentar con feedback
3. Máximo 2 reintentos

---

## 🔧 **FASE 6: Function Calling (Avanzado - 2-3 horas)**

**Solo si necesitas guardar emails, etc.**

### **Paso 6.1: Definir Herramienta**

**OBJETIVO:** Que OpenAI pueda "llamar funciones"

**Investiga:** OpenAI Function Calling

**TAREA:** Define `tools.py` con:
1. Función `record_email(email)`
2. JSON descriptor de la función
3. Manejo de tool_calls

---

## 📊 **Orden de Prioridades**

```
DEBE HACER (Core):
1. RAG básico funcional              [FASE 1]
2. Chat + RAG integrado              [FASE 2]
3. Clases organizadas                [FASE 3]
4. Interfaz Gradio                   [FASE 4]

DEBERÍA HACER (Calidad):
5. Evaluador                         [FASE 5]

PODRÍA HACER (Extra):
6. Function Calling                  [FASE 6]
7. Caché de respuestas
8. Logging
9. Tests unitarios
```

---

## 🎯 **Estrategia de Aprendizaje**

### **Para Cada Fase:**

1. **Lee documentación** (15 min)
   - Busca en Google los conceptos nuevos
   - Lee docs oficiales de las librerías

2. **Escribe código** (30-60 min)
   - Empieza simple
   - Prueba en consola antes de integrar
   - Usa `print()` para debug

3. **Valida** (10 min)
   - ¿Funciona?
   - ¿Entiendes QUÉ hace?
   - ¿Puedes explicarlo?

4. **Itera** (20 min)
   - Mejora el código
   - Añade validaciones
   - Maneja errores

---

## 🚫 **Errores Comunes a Evitar**

1. **Calcar sin entender**
   - ❌ Copiar todo el código del proyecto
   - ✅ Escribir desde cero cada parte

2. **Querer todo perfecto al inicio**
   - ❌ Empezar con clases, evaluador, tools
   - ✅ Script simple que funciona

3. **No validar cada paso**
   - ❌ Escribir todo y luego probar
   - ✅ Validar cada 30 min

4. **No usar print() para debug**
   - ❌ Asumir que funciona
   - ✅ Imprimir variables en cada paso

5. **No leer errores**
   - ❌ "No funciona" sin leer el error
   - ✅ Leer traceback completo

---

## 🎓 **Recursos de Aprendizaje**

### **Python Específico:**
- Diccionarios: `{"key": "value"}`
- Listas: `[1, 2, 3]`
- List comprehension: `[x for x in lista]`
- Context managers: `with open() as f:`
- Decoradores (para después)

### **Búsquedas Útiles:**
- "langchain DirectoryLoader example"
- "openai python chat completions"
- "gradio chatinterface tutorial"
- "chromadb python quickstart"
- "python dotenv tutorial"

---

## 📝 **Checklist de Progreso**

Marca cuando completes cada uno:

**FASE 1 - RAG:**
- [ ] Leer archivos de carpeta
- [ ] Dividir en chunks
- [ ] Generar embeddings
- [ ] Crear ChromaDB
- [ ] Búsqueda funciona

**FASE 2 - Chat:**
- [ ] Primera llamada OpenAI
- [ ] System prompt personalizado
- [ ] Integrar RAG + Chat
- [ ] Historial conversacional

**FASE 3 - Arquitectura:**
- [ ] Clase Retriever
- [ ] Clase Chat
- [ ] Clase Controller

**FASE 4 - Interfaz:**
- [ ] Gradio básico funciona
- [ ] Conversación fluida

**FASE 5 - Evaluador (Opcional):**
- [ ] Gemini evalúa respuestas
- [ ] Loop de reintentos

---

## 💡 **Última Recomendación**

**No intentes entenderlo todo al inicio.**

- Primera pasada: Haz que funcione
- Segunda pasada: Entiende por qué funciona
- Tercera pasada: Mejora y optimiza

**Objetivo:** En 2-3 días de trabajo, tener un chatbot RAG funcional que realmente entiendas.

---

## ❓ **¿Por Dónde Empezar AHORA MISMO?**

1. Crea la carpeta `mi-chatbot/`
2. Crea `knowledge_base/mi_cv.txt` con tu info
3. Crea `rag_v1.py` vacío
4. Empieza FASE 1, Paso 1.1

**¡No leas más! Empieza a programar.** 🚀

---

¿Quieres que aclare alguna fase específica antes de empezar? ¿O prefieres empezar directamente y me consultas cuando te atasques?