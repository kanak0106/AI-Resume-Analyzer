
# 📄 AI Resume Analyzer (Streamlit)

An end-to-end, resume-ready project you can deploy quickly. Upload a PDF/DOCX resume and paste a Job Description (JD) to get:
- **ATS-style match score** (TF‑IDF + cosine similarity)
- **Detected skills** (matches from a small, editable skill library)
- **Keyword gaps** vs JD
- **Auto-parsed sections** (Experience, Projects, Education, Skills, etc.)
- **Actionable suggestions** to improve bullet points

## 🏗️ Tech Stack
- **Python 3.10+**
- **Streamlit** for the UI
- **Scikit‑learn** (TF‑IDF, cosine similarity)
- **PyPDF2**, **python-docx** for text extraction

> No external paid APIs; runs entirely locally. You can later swap in embeddings or LLMs if desired.

## 🚀 Quickstart

```bash
# 1) Clone
git clone https://github.com/<your-username>/ai-resume-analyzer.git
cd ai-resume-analyzer

# 2) Create venv (recommended)
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 3) Install deps
pip install -r requirements.txt

# 4) Run
streamlit run app.py
```

Open the local URL shown in your terminal.

## 🧩 Project Structure
```
ai-resume-analyzer/
├─ app.py
├─ requirements.txt
├─ resume_analyzer/
│  ├─ core.py
│  └─ skills.json
├─ sample_data/
├─ .gitignore
└─ LICENSE
```

## 🧠 How it Works (simple)
1. **Extract text** from PDF/DOCX.
2. **Split sections** using common headers (Experience, Projects, Skills, …).
3. Compute a **match score** between resume and JD using TF‑IDF vectors and cosine similarity.
4. **Detect skills** by matching tokens against `skills.json` (you can expand this list).
5. Find **keyword gaps**: the JD’s top terms that do not appear in the resume.
6. Generate **bullet suggestions** using templates you can edit.

## 🛠️ Roadmap Ideas (easy to present in interviews)
- Swap TF‑IDF for **Sentence Transformers** embeddings to improve the score.
- **NER** with spaCy to pull roles, companies, dates.
- **PDF layout** extraction (headers, two-column) using `pdfplumber`/`unstructured`.
- **Export** tailored resume with highlighted changes.
- **Multi-resume compare** and analytics dashboard.
- **Docker** + one-click deploy (Streamlit Cloud / Hugging Face Spaces).

## ☁️ Deploy (fastest)
- **Streamlit Community Cloud**
  - Push to GitHub
  - New app → point to your repo → `app.py` is the entrypoint
- **Hugging Face Spaces**
  - Create Space → Streamlit → connect GitHub
- **Render.com** (optional) with a simple `start` command: `streamlit run app.py`

## 🧪 Test Tips
Use the `sample_data/` folder to keep a few anonymized resumes and JDs for demo.

## 📝 Resume Bullet (you can use this)
- Built and deployed an **AI Resume Analyzer** (Streamlit) that scores resume‑JD fit using TF‑IDF similarity, auto‑extracts skills/sections, and recommends keyword‑based improvements; deployed on Streamlit Cloud for public access.

---

**MIT License**
