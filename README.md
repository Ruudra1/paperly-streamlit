
# Paperly: Research Paper Assistant  
[![Live Demo](https://img.shields.io/badge/demo-online-green)](https://paperly.streamlit.app/) [![License: MIT](https://img.shields.io/badge/License-MIT-blue)](LICENSE) [![Python 3.8+](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)  

A Streamlit app that leverages AI to provide **research paper summarization**, **contextual Q&A**, and **highlight extraction** in one intuitive interface.

---

## 📖 Table of Contents
1. [🚀 Features](#-features)  
2. [🛠️ Technologies](#️-technologies)  
3. [📦 Installation](#-installation)  
4. [▶️ Usage](#️-usage)  
5. [🤝 Contributing](#-contributing)  
6. [📜 License](#-license)  
7. [✉️ Contact](#️-contact)  

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
| **Python 3.8+**    | Core language                            |
| **Streamlit**      | Front-end web framework                  |
| **LangChain**      | LLM orchestration pipelines              |
| **Gemini Pro** & **OpenAI API** | LLM backends                     |
| **NLTK**           | Text preprocessing                       |
| **PyPDF2**         | PDF parsing & text extraction            |
| **python-dotenv**  | Environment variable management          |

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


## ▶️ Usage

1. **Start the Streamlit app**  
   ```bash
   streamlit run app.py
   ```
 2. **Open your browser**
    Navigate to:
    ```bash
    http://localhost:8501
    ```
3.  **Upload & interact**
    
    -   Click “Browse files” or drag-and-drop your PDF
	-   Process it and run either summary or chat with Paperly
    -   Use the “Ask a question” box for contextual Q&A


## **✉️ Contact**

For questions, feedback, or partnership inquiries, reach out to the Paperly team:

-   **Ruudra Patel** – ruudra.patel@gmail.com
    
-   **Mahitha Borra** – bslmahitha@gmail.com
    
-   **Pancham Desai** – 
