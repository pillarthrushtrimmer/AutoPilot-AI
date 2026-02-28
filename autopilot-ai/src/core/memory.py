"""AutoPilot AI — Memory Manager (ChromaDB)."""

from __future__ import annotations
import hashlib, os
from datetime import datetime
import chromadb
from chromadb.config import Settings

class MemoryManager:
    def __init__(self, persist_dir: str = "./data/memory"):
        os.makedirs(persist_dir, exist_ok=True)
        self.client = chromadb.PersistentClient(path=persist_dir, settings=Settings(anonymized_telemetry=False))
        self.collection = self.client.get_or_create_collection("autopilot_memory", metadata={"hnsw:space": "cosine"})

    async def store(self, task: str, result: str) -> None:
        doc_id = hashlib.sha256(f"{task}:{result[:100]}".encode()).hexdigest()[:16]
        self.collection.upsert(ids=[doc_id], documents=[f"Task: {task}\nResult: {result[:2000]}"],
                               metadatas=[{"task": task[:500], "timestamp": datetime.now().isoformat()}])

    async def recall(self, query: str, top_k: int = 5) -> list[str]:
        if self.collection.count() == 0:
            return []
        r = self.collection.query(query_texts=[query], n_results=min(top_k, self.collection.count()))
        return r["documents"][0] if r["documents"] else []

    async def clear(self) -> None:
        self.client.delete_collection("autopilot_memory")
        self.collection = self.client.get_or_create_collection("autopilot_memory")
