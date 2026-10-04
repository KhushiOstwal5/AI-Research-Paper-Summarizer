import re
from typing import List


def split_into_sentences(text: str) -> List[str]:
    sentences = re.split(r"(?<=[.!?])\s+", text.strip())
    return [sentence.strip() for sentence in sentences if sentence.strip()]


def sentence_score(sentence: str) -> float:
    words = re.findall(r"\b[a-zA-Z]+\b", sentence.lower())
    if not words:
        return 0.0
    keyword_score = len(words)
    title_like = 1 if sentence[:1].isupper() else 0
    return keyword_score * 0.7 + title_like * 2.0


def summarize_text(text: str, max_sentences: int = 5) -> str:
    """Generate a lightweight, deterministic summary from paper text."""
    sentences = split_into_sentences(text)
    if not sentences:
        return "No text could be extracted from the uploaded PDF."

    if len(sentences) <= max_sentences:
        return " ".join(sentences)

    scored = sorted(
        ((sentence_score(sentence), sentence) for sentence in sentences),
        key=lambda item: item[0],
        reverse=True,
    )

    selected = [sentence for _, sentence in scored[:max_sentences]]
    selected.sort(key=lambda sentence: sentences.index(sentence))
    summary = " ".join(selected)
    return summary if summary.strip() else " ".join(sentences[:max_sentences])
