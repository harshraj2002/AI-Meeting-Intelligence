import chromadb
from chromadb.config import Settings
from typing import List, Dict, Any
from config import config

class VectorStoreService:
    def __init__(self):
        self.client = chromadb.PersistentClient(
            path=config.CHROMA_PERSIST_DIR,
            settings=Settings(anonymized_telemetry=False)
        )
        self.collection = self.client.get_or_create_collection("meetings")
    
    async def add_meeting(self, meeting_id: str, transcript: str, metadata: Dict[str, Any]):
        """Add meeting transcript to vector store"""
        # Split transcript into chunks for better search
        chunks = self._chunk_transcript(transcript)
        
        documents = []
        metadatas = []
        ids = []
        
        for i, chunk in enumerate(chunks):
            documents.append(chunk)
            metadatas.append({
                "meeting_id": meeting_id,
                "chunk_index": i,
                **metadata
            })
            ids.append(f"{meeting_id}_chunk_{i}")
        
        self.collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
    
    async def search_meetings(self, query: str, n_results: int = 5) -> List[Dict[str, Any]]:
        """Search meetings by content"""
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        
        return [
            {
                "meeting_id": metadata["meeting_id"],
                "content": document,
                "metadata": metadata
            }
            for document, metadata in zip(results["documents"][0], results["metadatas"][0])
        ]
    
    def _chunk_transcript(self, transcript: str, chunk_size: int = 1000) -> List[str]:
        """Split transcript into overlapping chunks"""
        words = transcript.split()
        chunks = []
        
        for i in range(0, len(words), chunk_size // 2):
            chunk = " ".join(words[i:i + chunk_size])
            if chunk:
                chunks.append(chunk)
        
        return chunks