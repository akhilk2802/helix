import chromadb
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction
import os

CHROMA_DB_HOST = os.getenv("CHROMA_DB_HOST")
CHROMA_DB_PORT = os.getenv("CHROMA_DB_PORT")

# Connect to the running HTTP server
client = chromadb.HttpClient(host=CHROMA_DB_HOST, port=CHROMA_DB_PORT)

collection = client.get_or_create_collection(
    name="helix_memory",
    embedding_function=OpenAIEmbeddingFunction(api_key=os.getenv("OPENAI_API_KEY"))
)

def store_message_in_memory(user_id: int, session_id: str, message: str):
    doc_id = f"{user_id}:{session_id}:{hash(message)}"
    metadata = {"user_id": user_id, "session_id": session_id}
    collection.add(documents=[message], metadatas=[metadata], ids=[doc_id])

def retrieve_similar_memory(user_id: int, query: str, k: int = 3):
    results = collection.query(
        query_texts=[query],
        n_results=k,
        where={"user_id": user_id}
    )
    return results.get("documents", [[]])[0]