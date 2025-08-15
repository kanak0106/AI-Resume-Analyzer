
from typing import List, Tuple, Dict
from dataclasses import dataclass
import re, io, json
import numpy as np
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Light-weight PDF/DOCX text extraction
def extract_text_from_pdf(file_bytes: bytes) -> str:
    from PyPDF2 import PdfReader
    reader = PdfReader(io.BytesIO(file_bytes))
    text = []
    for page in reader.pages:
        try:
            text.append(page.extract_text() or "")
        except Exception:
            continue
    return "\n".join(text)

def extract_text_from_docx(file_bytes: bytes) -> str:
    from docx import Document
    f = io.BytesIO(file_bytes)
    doc = Document(f)
    return "\n".join(p.text for p in doc.paragraphs)

SECTION_HEADERS = [
    "summary","objective","experience","work experience","employment",
    "projects","education","skills","certifications","achievements",
    "awards","publications","volunteer","interests","contact"
]

def normalize(text: str) -> str:
    return re.sub(r'\s+', ' ', text.lower()).strip()

def split_into_sections(text: str) -> Dict[str, str]:
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    sections: Dict[str, str] = {}
    current = "general"
    sections[current] = []
    for ln in lines:
        key = normalize(ln)
        if any(key.startswith(h) for h in SECTION_HEADERS):
            current = key.split(":")[0]
            sections[current] = []
        else:
            sections.setdefault(current, [])
            sections[current].append(ln)
    return {k: "\n".join(v) if isinstance(v, list) else v for k, v in sections.items()}

STOPWORDS = set("""
a an the and or if else of to in on for with by from at as is are was were be been being have has had
i me my we our you your he she it they them this that these those not no than then over under above
""".split())

def tokenize(text: str) -> List[str]:
    return [t for t in re.findall(r"[a-zA-Z][a-zA-Z\-+.#]*", text.lower()) if t not in STOPWORDS]

def top_keywords(text: str, n: int = 20) -> List[Tuple[str, float]]:
    vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1,2), max_features=5000)
    try:
        X = vectorizer.fit_transform([text])
        idx_to_term = {i: t for t, i in vectorizer.vocabulary_.items()}
        scores = np.asarray(X.sum(axis=0)).ravel()
        ranked = sorted([(idx_to_term[i], s) for i, s in enumerate(scores)], key=lambda x: x[1], reverse=True)
        return ranked[:n]
    except Exception:
        # fallback: frequency
        toks = tokenize(text)
        counts = Counter(toks)
        total = sum(counts.values()) or 1
        return [(w, c/total) for w, c in counts.most_common(n)]

def jd_match_score(resume_text: str, jd_text: str) -> float:
    if not resume_text or not jd_text:
        return 0.0
    vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1,2), max_features=10000)
    X = vectorizer.fit_transform([resume_text, jd_text])
    sim = cosine_similarity(X[0], X[1])[0][0]
    return float(sim)

def load_skill_list() -> List[str]:
    import json, os
    here = os.path.dirname(__file__)
    path = os.path.join(here, "skills.json")
    with open(path, "r") as f:
        return json.load(f)

def extract_skills(text: str) -> List[str]:
    skill_lib = set(load_skill_list())
    toks = set(tokenize(text))
    # simple match + multi-word skills
    found = set()
    for s in skill_lib:
        if " " in s:
            if s.lower() in text.lower():
                found.add(s)
        else:
            if s.lower() in toks:
                found.add(s)
    return sorted(found)

def keyword_gaps(resume_text: str, jd_text: str, top_k: int = 25) -> List[str]:
    jd_terms = [w for w, _ in top_keywords(jd_text, n=top_k)]
    res_terms = set([w for w, _ in top_keywords(resume_text, n=top_k)])
    return [w for w in jd_terms if w not in res_terms]

def bullet_point_suggestions(jd_text: str, missing: List[str]) -> List[str]:
    # Very simple templates that the user can edit
    ideas = []
    for kw in missing[:6]:
        ideas.append(f"• Demonstrated proficiency with {kw} to deliver measurable outcomes (e.g., +X% efficiency, -Y% cost).")
    ideas += [
        "• Quantified impact using numbers (users, revenue, latency, accuracy) to strengthen achievements.",
        "• Began bullets with strong verbs: Built, Shipped, Led, Optimized, Automated, Reduced, Improved.",
        "• Grouped skills into a TECH STACK line under each project."
    ]
    return ideas

@dataclass
class AnalysisResult:
    clean_text: str
    sections: Dict[str, str]
    score: float
    skills: List[str]
    gaps: List[str]
    suggestions: List[str]
    jd_keywords: List[str]

def analyze_resume(resume_text: str, jd_text: str) -> AnalysisResult:
    sections = split_into_sections(resume_text)
    score = jd_match_score(resume_text, jd_text) if jd_text else 0.0
    skills = extract_skills(resume_text)
    gaps = keyword_gaps(resume_text, jd_text) if jd_text else []
    suggestions = bullet_point_suggestions(jd_text, gaps) if jd_text else []
    jd_kws = [w for w, _ in top_keywords(jd_text, n=20)] if jd_text else []
    return AnalysisResult(
        clean_text=resume_text,
        sections=sections,
        score=round(score * 100, 2),
        skills=skills,
        gaps=gaps,
        suggestions=suggestions,
        jd_keywords=jd_kws
    )
