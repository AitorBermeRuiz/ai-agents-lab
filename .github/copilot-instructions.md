# Copilot Instructions for `ai-agents-lab`

## Overview

This repository is a personal lab for experimenting with AI agents and multi-agent systems. It contains mini-projects exploring frameworks (CrewAI, LangGraph, AutoGen, OpenAI SDK) and patterns like RAG, tool-calling, and autonomous workflows.

## Architecture

- **1_foundations/**: Contains foundational experiments and notebooks.
- **2_chatbot_rag_evaluation/**: Main RAG chatbot project. Key files:
  - `app.py`: Gradio UI for chat interface.
  - `controller.py`: Orchestrates chat, retrieval, and evaluation.
  - `chat.py`: Handles OpenAI chat logic and tool-calling.
  - `retriever.py`: Loads and splits documents, manages vector DB (Chroma, HuggingFace embeddings).
  - `evaluator.py`: Uses Gemini API to evaluate chatbot responses.
  - `tools.py`: Utility functions for logging user details and unknown questions via Pushover.
  - `knowledge_base/`: Text files with domain knowledge.
  - `career_db/`: Chroma vector DB storage.
  - `tests/`: Contains test scripts (e.g., `test_embeddings.py`).

## Key Patterns

- **RAG Workflow**: User queries are processed by retrieving relevant documents, generating a response, and evaluating its quality. If the response is not acceptable, the agent retries up to 3 times.
- **Tool-Calling**: The chatbot can call custom tools (`record_user_details`, `record_unknown_question`) to log user info or unanswered questions.
- **Evaluation Loop**: Responses are checked for quality using an external LLM (Gemini). Feedback is used to improve answers.
- **Gradio UI**: The main interface is built with Gradio (`app.py`), using a message-based chat format.

## Developer Workflows

- **Run the Chatbot UI**:  
  ```bash
  python app.py
  ```
  (from `2_chatbot_rag_evaluation/`)

- **Environment Variables**:  
  Store API keys in `.env` (OpenAI, Gemini, Pushover).

- **Testing**:  
  Place tests in `tests/`. Example: `test_embeddings.py` for vector DB validation.

- **Add Knowledge**:  
  Place `.txt` files in `knowledge_base/`. The retriever will auto-load them.

## Conventions

- **Chunking**: Documents are split into 500-character chunks with 100 overlap for embedding.
- **Retry Logic**: Chatbot retries up to 3 times if evaluation fails.
- **Logging**: All user details and unknown questions are pushed to Pushover for tracking.

## External Dependencies

- **OpenAI SDK**: For chat completions.
- **Gemini API**: For response evaluation.
- **LangChain**: For document loading, splitting, and embedding.
- **Chroma**: For vector DB storage.
- **Gradio**: For UI.
- **Pushover**: For notifications/logging.

## Example Data Flow

1. User submits a question via Gradio UI.
2. `controller.py` retrieves relevant documents.
3. `chat.py` generates a response, possibly calling tools.
4. `evaluator.py` checks response quality.
5. If unacceptable, chatbot retries with feedback.
6. All user details and unknown questions are logged.

## References

- See `Guia.md` for step-by-step learning and project philosophy.
- See `requirements.txt` for all dependencies.
