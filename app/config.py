import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "LLM Semantic Caching Proxy"
    similarity_threshold: float = 0.88
    embedding_model_name: str = "all-MiniLM-L6-v2"
    upstream_delay_sec: float = 0.35  # Simulates LLM generation latency

    class Config:
        env_file = ".env"


settings = Settings()