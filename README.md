
# Paperly: Research Paper Assistant

[![Live Demo](https://img.shields.io/badge/demo-online-green)](https://paperly.streamlit.app/) [![License: MIT](https://img.shields.io/badge/License-MIT-blue)](LICENSE) [![Python 3.8+](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)

A web app that leverages AI to provide **research paper summarization** and **contextual Q&A** in one intuitive interface.

---

## 📖 Table of Contents

1. [🚀 Features](#-features)  
2. [🛠️ Technologies](#️-technologies)  
3. [📦 Installation](#-installation)  
4. [▶️ Usage](#️-usage)   
5. [📜 License](#-license)  
6. [✉️ Contact](#️-contact)  

---

## 🚀 Features

- 🔍 **PDF Upload & Summarization**  
  Extract and distill key insights from any research paper.  
- 💬 **Interactive Q&A**  
  Ask detailed questions about the paper and get contextual, on-point answers.  

---

## 🛠️ Technologies

| Tool / Library     | Purpose                                   |
| ------------------ | ----------------------------------------- |
| **Python 3.8+**    | Backend language                          |
| **FastAPI**        | Backend API                               |
| **FAISS**          | Vector search index                       |
| **SentenceTransformers** | Embeddings                          |
| **Groq**           | LLM backend (Llama 70B)                   |
| **React (Vite)**   | Frontend UI                               |
| **PyMuPDF**        | PDF parsing & text extraction             |
| **python-dotenv**  | Environment variable management           |

---

## 📦 Installation

```bash
# 1. Clone the repo
git clone https://github.com/Ruudra1/paperly.git
cd paperly

# 2. Create & activate a venv
python -m venv venv
# macOS/Linux
source venv/bin/activate
# Windows
venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Copy & configure .env
cp .env.example .env
# Then edit .env with your API keys:
# OPENAI_API_KEY=your_openai_api_key
# GEMINI_API_KEY=your_gemini_pro_key
```

## 📜 License

This project is distributed under the MIT License.
See the full text in LICENSE for details.

## ▶️ Usage

1. **Configure environment**

   ```bash
   cp .env.example .env
   # edit .env and set GROQ_API_KEY
   ```

2. **Start the backend API**

   ```bash
   cd backend
   ./run.sh
   ```
   Backend runs at:

   ```text
   http://localhost:8000
   ```

3. **Start the React frontend**

   ```bash
   cd frontend
   npm install
   npm run dev
   ```
   Frontend runs at:

   ```text
   http://localhost:5173
   ```

4. **Upload & interact**
   - Upload a PDF
   - Click **Process Paper**
   - Use **Summarize** or **Chat**


## **✉️ Contact**

For questions, feedback, or partnership inquiries, reach out to the Paperly team:

- **Ruudra Patel** – ruudra.patel@gmail.com

- **Mahitha Borra** – bslmahitha@gmail.com

- **Pancham Desai** – panchamdesai847@gmail.com
