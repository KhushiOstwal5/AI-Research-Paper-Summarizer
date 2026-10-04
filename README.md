# AI Research Paper Summarizer

AI-powered research paper analyzer with PDF extraction, AI summarization, embeddings, RAG-based chat, and history management.

## Features
- Upload research paper PDFs
- Extract text from PDF documents
- Generate concise summaries
- Split content into chunks and index it using TF-IDF
- Ask context-aware questions from the uploaded paper
- Keep a session history of conversations

## Stack
- Python
- Streamlit
- PyPDF
- scikit-learn
- NumPy

## Project structure
- `app/` - Streamlit app and service modules
- `app/services/` - PDF extraction, summarization, embeddings and RAG logic

## Setup

1. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/macOS
   .venv\Scripts\activate     # Windows
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the app:
   ```bash
   streamlit run app/main.py
   ```

4. Upload a PDF and ask questions about the paper.

## Notes
This project uses a lightweight local retrieval pipeline for summarization and question answering. It is designed to run on a local machine without needing an external API for the core retrieval workflow.
