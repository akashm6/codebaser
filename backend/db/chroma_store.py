from chromadb.config import Settings
from typing import Dict
import chromadb
import hashlib

client = chromadb.PersistentClient(path='./chroma_storage')

collection = client.get_or_create_collection(name="code_chunks")

def get_chunk_id(chunk: Dict) -> str:
    base = f"{chunk['file_path']}:{chunk['start_line']}-{chunk['end_line']}"
    return hashlib.sha256(base.encode()).hexdigest()

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