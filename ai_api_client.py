import json
import os
import re

from dotenv import load_dotenv
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from llama_index.core.settings import Settings
from llama_index.embeddings.google_genai import GoogleGenAIEmbedding
from llama_index.embeddings.together import TogetherEmbedding
from llama_index.llms.gemini import Gemini
from llama_index.llms.together import TogetherLLM

load_dotenv()

selected_model_together = 'meta-llama/Llama-3.3-70B-Instruct-Turbo-Free'
document_dir = os.getenv("DOCUMENT_DIR")

# Global storage for models and index
cached_index = None
cached_model = None


def completion_to_prompt(completion: str) -> str:
    return f"[INST] {completion} [/INST]"


def clean_response(response: str) -> str:
    """Remove tags do modelo e JSONs desnecessários"""
    # Remover tags como [INST] e [/INST]
    response = re.sub(r"\[/?INST\]", "", response).strip()

    # Tentar remover JSONs inesperados
    response = re.sub(r"\{.*?\}", "", response).strip()

    # Garante que a string não seja escapada em Unicode (\u00e7 → ç)
    return response.encode('latin-1').decode('unicode-escape')


def initialize_index():
    """Loads documents and initializes the index once."""
    global cached_index
    if cached_index is None:
        documents = SimpleDirectoryReader(document_dir).load_data()
        cached_index = VectorStoreIndex.from_documents(documents)
    return cached_index


def initialize_model(model_name: str, api_key: str):
    """Initializes the model and embeddings once and reuses them."""
    global cached_model
    if cached_model is None or cached_model != model_name:
        if "gemini" in model_name:
            Settings.llm = Gemini(
                model=model_name,
                api_key=api_key,
                temperature=0.8,
                max_tokens=256,
                top_p=0.7,
                top_k=50,
                is_chat_model=False,
                completion_to_prompt=completion_to_prompt
            )
            Settings.embed_model = GoogleGenAIEmbedding(
                api_key=api_key,
                model_name="text-embedding-004",
                embed_batch_size=100,
            )
        else:
            Settings.llm = TogetherLLM(
                model_name,
                temperature=0.8,
                max_tokens=256,
                top_p=0.7,
                top_k=50,
                is_chat_model=False,
                completion_to_prompt=completion_to_prompt
            )
            Settings.embed_model = TogetherEmbedding("togethercomputer/m2-bert-80M-8k-retrieval")
        cached_model = model_name


def run_rag_completion(query_text: str, model_name: str):
    """Handles RAG completion using the selected model."""
    api_key = os.getenv("GEMINI_API_KEY") if "gemini" in model_name else os.getenv("TOGETHER_API_KEY")

    if not api_key:
        raise ValueError("API key is missing. Please set the necessary environment variables.")

    initialize_model(model_name, api_key)
    index = initialize_index()
    response = index.as_query_engine(similarity_top_k=5).query(query_text)

    return clean_response(str(response))


def ai_client_query(message, model):
    """Processes user queries using the appropriate model."""
    try:
        return run_rag_completion(message, model)
    except Exception as e:
        return "Erro interno, tente novamente..."
