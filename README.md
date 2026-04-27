
# Paperly: Research Paper Assistant

[![Live Demo](https://img.shields.io/badge/demo-online-green)](https://paperly-streamlit.vercel.app/) [![License: MIT](https://img.shields.io/badge/License-MIT-blue)](LICENSE) [![Python 3.8+](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)

A web app that leverages AI to provide **research paper summarization** and **contextual Q&A** in one intuitive interface.

## 📸 Screenshot

![Paperly Screenshot](/screenshot/ss1.png)

---

## 📖 Table of Contents

1. [🚀 Features](#-features)
2. [🛠️ Technologies](#️-technologies)
3. [📦 Installation](#-installation)
4. [▶️ Usage](#️-usage)
5. [🌐 Deployment](#-deployment)
6. [📜 License](#-license)
7. [✉️ Contact](#️-contact)

---

## 🚀 Features

- 🔍 **PDF Upload & Summarization**
  Extract and distill key insights from any research paper.
- 💬 **Interactive Q&A**
  Ask detailed questions about the paper and get contextual, on-point answers using RAG (Retrieval-Augmented Generation).
- ⚡ **Fast Processing**
  Cohere embeddings API for vector search, no local model installation required.
- 🎨 **Modern UI**
  React + Vite frontend with real-time progress indicators.

---

## 🛠️ Technologies

| Tool / Library | Purpose |
| -------------- | ------- |
| **Python 3.8+** | Backend language |
| **FastAPI** | Backend API |
| **FAISS** | Vector search index |
| **Cohere** | Embeddings API (embed-english-v3.0) |
| **Groq** | LLM backend (llama-3.1-8b-instant) |
| **React (Vite)** | Frontend UI |
| **TypeScript** | Frontend type safety |
| **PyMuPDF** | PDF parsing & text extraction |
| **python-dotenv** | Environment variable management |

---

## 📦 Installation

```bash
# 1. Clone the repo
git clone https://github.com/Ruudra1/paperly-streamlit.git
cd paperly-streamlit

# 2. Create & activate a venv
python -m venv venv
# macOS/Linux
source venv/bin/activate
# Windows
venv\Scripts\activate

# 3. Install Python dependencies
pip install -r requirements.txt

# 4. Copy & configure .env
cp .env.example .env
# Then edit .env with your API keys:
# GROQ_API_KEY=your_groq_api_key
# COHERE_API_KEY=your_cohere_api_key

# 5. Install frontend dependencies
cd frontend
npm install
```

---

## ▶️ Usage

1. **Configure environment**

   ```bash
   cp .env.example .env
   # edit .env and set GROQ_API_KEY and COHERE_API_KEY
   ```

2. **Start the backend API**

   ```bash
   cd backend
   uvicorn app:app --host 127.0.0.1 --port 8080
   ```
   Backend runs at:

   ```text
   http://127.0.0.1:8080
   ```

3. **Start the React frontend**

   ```bash
   cd frontend
   npm run dev
   ```
   Frontend runs at:

   ```text
   http://localhost:5173
   ```

4. **Upload & interact**
   - Upload a PDF
   - Click **Process Paper** (watch the progress indicator)
   - Use **Summarize** to get a paper summary
   - Use **Chat** to ask questions about the paper

---

## 🌐 Deployment

### Frontend (Vercel)

```bash
# From project root
vercel
```

When prompted:
- **Root directory**: `frontend`
- **Framework preset**: Vite
- **Environment variables**: `VITE_API_BASE` = your backend URL

### Backend (Railway / Render)

**Railway** (recommended):
1. Connect your GitHub repo
2. Railway auto-detects Python + FastAPI
3. Add environment variables: `GROQ_API_KEY`, `COHERE_API_KEY`

**Render**:
1. Create new web service
2. Build command: `pip install -r requirements.txt`
3. Start command: `uvicorn app:app --host 0.0.0.0 --port $PORT`
4. Add environment variables: `GROQ_API_KEY`, `COHERE_API_KEY`

---

## 📜 License

This project is distributed under the MIT License.
See the full text in LICENSE for details.

---

## ✉️ Contact

For questions, feedback, or partnership inquiries, reach out to the Paperly team:

- **Ruudra Patel** – ruudra.patel@gmail.com
- **Mahitha Borra** – bslmahitha@gmail.com
- **Pancham Desai** – panchamdesai847@gmail.com
