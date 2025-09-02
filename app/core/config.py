from pydantic_settings import BaseSettings
from typing import List, Optional
import os
from pathlib import Path

class Settings(BaseSettings):
    # Database
    database_url: str = "postgresql://username:password@localhost:5432/social_support_db"
    database_test_url: str = "postgresql://username:password@localhost:5432/social_support_test_db"
    
    # LLM Configuration
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "llama2:7b"
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    
    # Security
    secret_key: str = "your-secret-key-here"
    encryption_key: str = "your-encryption-key-here"
    pii_masking_enabled: bool = True
    
    # Logging
    log_level: str = "INFO"
    log_file: str = "logs/app.log"
    
    # File Storage
    upload_dir: str = "uploads/"
    max_file_size: int = 10485760  # 10MB
    
    # ML Model
    model_path: str = "models/eligibility_model.pkl"
    feature_scaler_path: str = "models/feature_scaler.pkl"
    
    # Vector Database
    chroma_persist_directory: str = "./chroma_db"
    
    # API Configuration
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    cors_origins: List[str] = ["http://localhost:3000", "http://localhost:8501"]
    
    # Streamlit Configuration
    streamlit_server_port: int = 8501
    streamlit_server_address: str = "localhost"
    
    class Config:
        env_file = ".env"
        case_sensitive = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Ensure directories exist
        Path(self.upload_dir).mkdir(parents=True, exist_ok=True)
        Path(self.chroma_persist_directory).mkdir(parents=True, exist_ok=True)
        Path("logs").mkdir(parents=True, exist_ok=True)
        Path("models").mkdir(parents=True, exist_ok=True)

settings = Settings() 