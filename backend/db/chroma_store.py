from db.postgres_store import get_chunks_by_ids, get_chunk_id
from embedding.summarize import get_embedding
from chromadb.config import Settings
from typing import Dict, List 
import chromadb
import hashlib

client = chromadb.PersistentClient(path='./chroma_storage')

collection = client.get_or_create_collection(name="code_chunks")

def store_embedding(chunk: Dict):
    chunk_id = get_chunk_id(chunk)

    metadata = {
        "file_path": chunk["file_path"],
        "start_line": chunk["start_line"],
        "end_line": chunk["end_line"],
        "summary": chunk["summary"],
        "type": chunk["type"],
    }

    collection.add(
        ids=[chunk_id],
        embeddings=[chunk["embedding"]],
        metadatas=[metadata],
        documents=[chunk["text"]]
    )
    
# embed a user query and grab the top k matching chunks
def search_codebase(user_query: str, k: int = 5):
    top_chunks = []
    query_embedding = get_embedding(user_query)
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k,
        include=["metadatas", "documents"]
    )

    top_k_ids = results["ids"][0]
    for i in range(len(top_k_ids)):
        metadata = results["metadatas"][0][i]
        metadata["text"] = results["documents"][0][i] 
        top_chunks.append(metadata)

    return top_chunks