# 📄 Resume Analyzer 101

**Resume Analyzer 101** is a modern Streamlit application that helps you analyze your resume or CV for any job role you are targeting. Upload your resume and a job description, and get detailed, AI-powered feedback on how well your resume matches the job, along with actionable suggestions for improvement.

---

## 🚀 Features

- **AI-Powered Resume Analysis:** Uses Google Gemini (via LangChain) to assess your resume against any job description.
- **PDF Support:** Upload your resume as a PDF; the app extracts both text and images for analysis.
- **Personalized Feedback:** Get strengths, weaknesses, and improvement tips tailored to your target job.
- **Interactive Q&A:** Ask follow-up questions about your resume and receive instant, context-aware answers.

---

## 🛠️ Tech Stack & Key Libraries

- [**Streamlit**](https://streamlit.io/) – For building the interactive web UI.
- [**LangChain**](https://python.langchain.com/) – For orchestrating LLM (Large Language Model) interactions.
- [**Google GenAI (Gemini)**](https://ai.google.dev/) – The LLM powering the resume analysis.
- [**pdf2image**](https://github.com/Belval/pdf2image) & [**PyPDF2**](https://pypdf2.readthedocs.io/) – For PDF parsing and image extraction.
- [**Pillow**](https://python-pillow.org/) – For image processing.
- [**python-dotenv**](https://pypi.org/project/python-dotenv/) – For environment variable management.

---

## ⚡ Quickstart

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/resume-analyzer-101.git
cd resume-analyzer-101
```

## Setup Virtual Environment for Local installation

### Using [uv](https://docs.astral.sh/uv/) - recommended approach
```bash
cd resume-analyzer-101
uv sync
```

### Using pip venv - recommended approach
```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

## 3. Configure Your Google API Key
- Get your API key from Google AI Studio.
- You can either:
    - Set it in a .env file as GOOGLE_API_KEY=your-key-here, or
    - Enter it directly in the app when prompted.

## 4. Running the app

```bash
streamlit run main.py
```

#### The app will open in your browser. Follow the on-screen instructions to upload your resume and job description.

## 🌐 Live Demo

The project will be available at:
[streamlit](resume-analyzer-101.streamlit.app)

## 📢 About
Built by **Aakrit** using **Streamlit, LangChain, and Google GenAI**.
Empowering job seekers to land their dream roles with smarter, AI-driven resume feedback!



