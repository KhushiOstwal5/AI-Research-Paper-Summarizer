import json
from pathlib import Path
from typing import Any, Dict, List


class HistoryManager:
    def __init__(self, file_path: str | Path):
        self.file_path = Path(file_path)
        self.file_path.parent.mkdir(parents=True, exist_ok=True)

    def load_history(self) -> List[Dict[str, Any]]:
        if not self.file_path.exists():
            return []
        try:
            with self.file_path.open("r", encoding="utf-8") as handle:
                payload = json.load(handle)
                return payload if isinstance(payload, list) else []
        except (json.JSONDecodeError, OSError):
            return []

    def save_history(self, entries: List[Dict[str, Any]]) -> None:
        with self.file_path.open("w", encoding="utf-8") as handle:
            json.dump(entries, handle, indent=2, default=str)

    def add_entry(self, question: str, answer: str) -> None:
        payload = self.load_history()
        payload.append({"question": question, "answer": answer})
        self.save_history(payload)
