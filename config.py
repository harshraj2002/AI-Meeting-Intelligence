import os
from pathlib import Path

class Config:
    # Database
    DATABASE_URL = "sqlite:///./meetings.db"
    
    # File Storage
    UPLOAD_DIR = Path("uploads")
    PROCESSED_DIR = Path("processed")
    
    # AI Components
    OLLAMA_BASE_URL = "http://localhost:11434"
    OLLAMA_MODEL = "llama3.2"
    
    # ChromaDB
    CHROMA_PERSIST_DIR = "./chroma_db"
    
    # API
    MAX_UPLOAD_SIZE = 100 * 1024 * 1024  # 100MB
    ALLOWED_EXTENSIONS = {'.mp3', '.wav', '.mp4', '.avi', '.mov', '.m4a', '.flac'}

config = Config()