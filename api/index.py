import os
import re
import tempfile
from pathlib import Path
from typing import Dict, List
from uuid import uuid4
import logging
import time

import fitz  # PyMuPDF
import numpy as np
import requests
from dotenv import load_dotenv
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from groq import Groq
from pydantic import BaseModel


def _ensure_temp_dir():
    # On Vercel, only /tmp is writable
    tmp_dir = Path("/tmp")
    tmp_dir.mkdir(parents=True, exist_ok=True)
    os.environ["TMPDIR"] = str(tmp_dir)
    tempfile.tempdir = str(tmp_dir)


_ensure_temp_dir()
load_dotenv()

logging.basicConfig(
    level=os.environ.get("LOG_LEVEL", "INFO").upper(),
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)
logger = logging.getLogger("paperly")

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise RuntimeError("Missing GROQ_API_KEY environment variable")

client = Groq(api_key=GROQ_API_KEY)

EMBEDDING_DIM = 1024  # Cohere embed-english-v3.0


def embed_text(texts: List[str]) -> np.ndarray:
    logger.info("Embedding %d texts with Cohere API...", len(texts))
    cohere_api_key = os.environ.get("COHERE_API_KEY")
    if not cohere_api_key:
        raise RuntimeError("Missing COHERE_API_KEY environment variable")
    
    response = requests.post(
        "https://api.cohere.ai/v1/embed",
        headers={
            "Authorization": f"Bearer {cohere_api_key}",
            "Content-Type": "application/json",
            "X-Client-Name": "paperly"
        },
        json={
            "texts": texts,
            "model": "embed-english-v3.0",
            "input_type": "search_document"
        }
    )
    response.raise_for_status()
    data = response.json()
    embeddings = data["embeddings"]
    logger.info("Embeddings generated")
    return np.array(embeddings, dtype=np.float32)


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
    words = text.split()
    chunks: List[str] = []
    step = max(1, chunk_size - overlap)
    for i in range(0, len(words), step):
        chunk = " ".join(words[i : i + chunk_size])
        if chunk.strip():
            chunks.append(chunk)
    return chunks


def clean_extracted_text(text: str) -> str:
    text = re.sub(r"\n\s*\n", "\n\n", text)
    text = re.sub(r"(?<!\n)\n(?!\n)", " ", text)
    text = re.sub(r"-\s+", "", text)
    text = re.sub(r" {2,}", " ", text)
    return text.strip()


def extract_clean_text_from_pdf_bytes(pdf_bytes: bytes) -> str:
    text = ""
    pdf_document = fitz.open(stream=pdf_bytes, filetype="pdf")
    for page in pdf_document:
        text += page.get_text() + "\n"
    return clean_extracted_text(text)


class SessionState:
    def __init__(self):
        self.embeddings: np.ndarray = None
        self.chunks: List[str] = []


SESSIONS: Dict[str, SessionState] = {}


def build_index(session: SessionState, paper_text: str) -> None:
    chunks = chunk_text(paper_text)
    if not chunks:
        raise ValueError("No text chunks produced from PDF")
    embeddings = embed_text(chunks)
    session.embeddings = np.array(embeddings)
    session.chunks = chunks


def retrieve_top_chunks(session: SessionState, user_query: str, top_k: int = 3) -> str:
    if session.embeddings is None or len(session.embeddings) == 0:
        return ""
    query_embedding = embed_text([user_query])[0]
    # Cosine similarity using numpy
    dot_product = np.dot(session.embeddings, query_embedding)
    norms = np.linalg.norm(session.embeddings, axis=1) * np.linalg.norm(query_embedding)
    similarities = dot_product / norms
    top_indices = np.argsort(similarities)[-top_k:][::-1]
    retrieved = [session.chunks[idx] for idx in top_indices if 0 <= idx < len(session.chunks)]
    return "\n\n".join(retrieved)


def groq_answer(context: str, question: str) -> str:
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are a helpful AI assistant. Answer the user's question based on the provided context.",
            },
            {
                "role": "user",
                "content": f"Context: {context}\n\nQuestion: {question}",
            },
        ],
        model="llama-3.1-8b-instant",
        temperature=0.2,
        max_tokens=600,
    )
    return chat_completion.choices[0].message.content


def groq_summarize(context: str) -> str:
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": "You are an expert research assistant. Summarize research papers based ONLY on the retrieved chunks.",
            },
            {"role": "user", "content": f"Summarize this research paper:\n{context}"},
        ],
        temperature=0.2,
        max_tokens=600,
    )
    return response.choices[0].message.content


app = FastAPI(title="Paperly API")


@app.middleware("http")
async def request_logging_middleware(request, call_next):
    request_id = str(uuid4())
    start = time.perf_counter()
    logger.info(
        "request.start id=%s method=%s path=%s content_type=%s",
        request_id,
        request.method,
        request.url.path,
        request.headers.get("content-type"),
    )
    try:
        response = await call_next(request)
    except Exception:
        logger.exception("request.error id=%s method=%s path=%s", request_id, request.method, request.url.path)
        raise
    finally:
        duration_ms = (time.perf_counter() - start) * 1000
        logger.info(
            "request.end id=%s method=%s path=%s duration_ms=%.1f",
            request_id,
            request.method,
            request.url.path,
            duration_ms,
        )
    response.headers["X-Request-Id"] = request_id
    return response


@app.exception_handler(Exception)
async def unhandled_exception_handler(request, exc):
    logger.exception("unhandled_exception path=%s", request.url.path)
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ProcessResponse(BaseModel):
    session_id: str


class ChatRequest(BaseModel):
    session_id: str
    question: str


class ChatResponse(BaseModel):
    answer: str


class SummarizeRequest(BaseModel):
    session_id: str


class SummarizeResponse(BaseModel):
    summary: str


@app.get("/api/health")
def health():
    logger.info("health.check")
    return {"ok": True}


@app.post("/api/process", response_model=ProcessResponse)
async def process_paper(file: UploadFile = File(...)):
    logger.info(
        "process.start filename=%s content_type=%s",
        file.filename,
        file.content_type,
    )
    if file.content_type not in {"application/pdf", "application/x-pdf"}:
        logger.warning("process.invalid_content_type content_type=%s", file.content_type)
        raise HTTPException(status_code=400, detail="Please upload a PDF")

    pdf_bytes = await file.read()
    logger.info("process.upload_read bytes=%s", len(pdf_bytes))
    try:
        text = extract_clean_text_from_pdf_bytes(pdf_bytes)
        logger.info("process.pdf_extracted chars=%s", len(text))
    except Exception as e:
        logger.exception("process.pdf_parse_failed")
        raise HTTPException(status_code=400, detail=f"Failed to parse PDF: {e}")

    session_id = str(uuid4())
    session = SessionState()
    try:
        build_index(session, text)
        logger.info("process.index_built session_id=%s chunks=%s", session_id, len(session.chunks))
    except Exception as e:
        logger.exception("process.index_build_failed session_id=%s", session_id)
        raise HTTPException(status_code=400, detail=str(e))

    SESSIONS[session_id] = session
    logger.info("process.done session_id=%s", session_id)
    return ProcessResponse(session_id=session_id)


@app.post("/api/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    logger.info("chat.start session_id=%s question_chars=%s", req.session_id, len(req.question))
    session = SESSIONS.get(req.session_id)
    if not session:
        logger.warning("chat.unknown_session session_id=%s", req.session_id)
        raise HTTPException(status_code=404, detail="Unknown session_id")

    context = retrieve_top_chunks(session, req.question)
    if not context:
        logger.warning("chat.no_context session_id=%s", req.session_id)
        raise HTTPException(status_code=400, detail="No paper indexed for this session")

    try:
        answer = groq_answer(context=context, question=req.question)
    except Exception as e:
        logger.exception("chat.groq_failed session_id=%s", req.session_id)
        raise HTTPException(status_code=500, detail=f"Groq error: {e}")

    logger.info("chat.done session_id=%s answer_chars=%s", req.session_id, len(answer))
    return ChatResponse(answer=answer)


@app.post("/api/summarize", response_model=SummarizeResponse)
def summarize(req: SummarizeRequest):
    logger.info("summarize.start session_id=%s", req.session_id)
    session = SESSIONS.get(req.session_id)
    if not session:
        logger.warning("summarize.unknown_session session_id=%s", req.session_id)
        raise HTTPException(status_code=404, detail="Unknown session_id")

    context = retrieve_top_chunks(session, "Summarize the paper")
    if not context:
        logger.warning("summarize.no_context session_id=%s", req.session_id)
        raise HTTPException(status_code=400, detail="No paper indexed for this session")

    try:
        summary = groq_summarize(context=context)
    except Exception as e:
        logger.exception("summarize.groq_failed session_id=%s", req.session_id)
        raise HTTPException(status_code=500, detail=f"Groq error: {e}")

    logger.info("summarize.done session_id=%s summary_chars=%s", req.session_id, len(summary))
    return SummarizeResponse(summary=summary)
