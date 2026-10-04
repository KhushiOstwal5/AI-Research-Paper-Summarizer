from pathlib import Path

import streamlit as st

from app.config import settings
from app.schemas import ChatEntry
from app.services.history_manager import HistoryManager
from app.services.pdf_extractor import extract_text_from_pdf
from app.services.rag import RAGChatEngine
from app.services.summarizer import summarize_text


st.set_page_config(page_title=settings.app_title, page_icon="📄", layout="wide")


def initialize_state() -> None:
    if "paper_text" not in st.session_state:
        st.session_state.paper_text = ""
    if "paper_summary" not in st.session_state:
        st.session_state.paper_summary = ""
    if "paper_title" not in st.session_state:
        st.session_state.paper_title = "No paper uploaded"
    if "rag_engine" not in st.session_state:
        st.session_state.rag_engine = RAGChatEngine()
    if "history" not in st.session_state:
        st.session_state.history = []
    if "history_manager" not in st.session_state:
        st.session_state.history_manager = HistoryManager(Path("storage/history.json"))


initialize_state()


def render_sidebar() -> None:
    st.sidebar.title("AI Research Paper Summarizer")
    st.sidebar.caption("Upload a PDF to analyze and ask questions about it.")

    uploaded_file = st.sidebar.file_uploader("Upload a PDF", type=["pdf"])
    if uploaded_file is not None:
        try:
            uploaded_path = Path("storage") / uploaded_file.name
            uploaded_path.parent.mkdir(parents=True, exist_ok=True)
            uploaded_path.write_bytes(uploaded_file.getvalue())

            extracted_text = extract_text_from_pdf(uploaded_path)
            summary = summarize_text(extracted_text)
            title = uploaded_file.name.replace(".pdf", "").replace("_", " ").title()

            st.session_state.paper_text = extracted_text
            st.session_state.paper_summary = summary
            st.session_state.paper_title = title
            st.session_state.rag_engine = RAGChatEngine()
            st.session_state.rag_engine.build_from_text(extracted_text)

            st.sidebar.success(f"Loaded: {uploaded_file.name}")
            st.sidebar.info(f"Extracted {len(extracted_text.split())} words")
        except Exception as exc:  # pragma: no cover - UI safety
            st.sidebar.error(f"Unable to process PDF: {exc}")

    if st.sidebar.button("Clear session"):
        st.session_state.paper_text = ""
        st.session_state.paper_summary = ""
        st.session_state.paper_title = "No paper uploaded"
        st.session_state.rag_engine = RAGChatEngine()
        st.session_state.history = []
        st.sidebar.success("Session cleared.")


def render_main() -> None:
    st.title("📚 Research Paper Analyzer")
    st.subheader(st.session_state.paper_title)

    if not st.session_state.paper_text:
        st.info("Upload a PDF from the sidebar to begin")
        return

    summary_col, insight_col = st.columns([2, 1])

    with summary_col:
        st.markdown("### Summary")
        st.write(st.session_state.paper_summary)

    with insight_col:
        st.markdown("### Paper insights")
        st.metric("Words extracted", len(st.session_state.paper_text.split()))
        st.metric("Chunks indexed", len(st.session_state.rag_engine.chunks))
        st.caption("The app answers questions based on the uploaded paper text.")

    st.markdown("---")
    st.markdown("### Ask a question about the paper")
    question = st.text_input(
        "Type your question",
        placeholder="e.g. What is the main contribution of this paper?",
    )

    if st.button("Ask") and question.strip():
        answer = st.session_state.rag_engine.answer(question.strip())
        st.session_state.history.append(ChatEntry(question=question.strip(), answer=answer))
        st.session_state.history_manager.save_history(st.session_state.history)
        st.markdown("#### Answer")
        st.write(answer)

    if st.session_state.history:
        st.markdown("---")
        st.markdown("### Chat history")
        for idx, entry in enumerate(reversed(st.session_state.history[-10:])):
            with st.container():
                st.markdown(f"**Q{len(st.session_state.history) - idx}:** {entry.question}")
                st.write(entry.answer)
                st.caption(f"{entry.created_at.strftime('%Y-%m-%d %H:%M:%S')}")


render_sidebar()
render_main()
