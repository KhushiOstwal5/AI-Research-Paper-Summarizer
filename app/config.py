from dataclasses import dataclass
from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv()


@dataclass
class Settings:
    app_title: str = "AI Research Paper Summarizer"
    openai_api_key: Optional[str] = None
    max_history_items: int = 20
    max_chunk_length: int = 700
    similarity_threshold: float = 0.05

    @classmethod
    def from_env(cls) -> "Settings":
        return cls(
            app_title=os.getenv("APP_TITLE", "AI Research Paper Summarizer"),
            openai_api_key=os.getenv("OPENAI_API_KEY"),
            max_history_items=int(os.getenv("MAX_HISTORY_ITEMS", "20")),
            max_chunk_length=int(os.getenv("MAX_CHUNK_LENGTH", "700")),
            similarity_threshold=float(os.getenv("SIMILARITY_THRESHOLD", "0.05")),
        )


settings = Settings.from_env()
