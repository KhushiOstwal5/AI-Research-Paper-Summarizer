from dataclasses import dataclass, field
from datetime import datetime
from typing import List


@dataclass
class PaperDocument:
    document_id: str
    filename: str
    title: str
    text: str
    summary: str
    chunks: List[str] = field(default_factory=list)
    uploaded_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class ChatEntry:
    question: str
    answer: str
    created_at: datetime = field(default_factory=datetime.utcnow)
