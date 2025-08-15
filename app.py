
import streamlit as st
from resume_analyzer.core import (
    extract_text_from_pdf, extract_text_from_docx, analyze_resume
)

st.set_page_config(page_title="AI Resume Analyzer", page_icon="📄", layout="wide")
st.title("📄 AI Resume Analyzer")
st.write("Upload your resume and paste a Job Description (JD). Get an ATS-style score, keyword gaps, skills, and actionable suggestions.")

with st.sidebar:
    st.header("Inputs")
    up = st.file_uploader("Upload Resume (PDF or DOCX)", type=["pdf","docx"])
    jd = st.text_area("Paste Job Description (JD)", height=220, placeholder="Paste the JD here...")
    analyze_btn = st.button("Analyze")

def read_file(uploaded):
    if uploaded is None:
        return ""
    data = uploaded.read()
    if uploaded.name.lower().endswith(".pdf"):
        return extract_text_from_pdf(data)
    elif uploaded.name.lower().endswith(".docx"):
        return extract_text_from_docx(data)
    else:
        return ""

if analyze_btn:
    with st.spinner("Analyzing..."):
        resume_text = read_file(up)
        if not resume_text:
            st.error("Couldn't read the resume. Upload a valid PDF or DOCX.")
        else:
            result = analyze_resume(resume_text, jd)
            col1, col2, col3 = st.columns(3)
            col1.metric("ATS Match Score", f"{result.score} / 100")
            col2.metric("Skills Detected", f"{len(result.skills)}")
            col3.metric("JD Keywords Missing", f"{len(result.gaps)}")

            st.subheader("Detected Skills")
            st.write(", ".join(result.skills) if result.skills else "No skills detected.")

            st.subheader("JD Keywords (Top)")
            st.write(", ".join(result.jd_keywords) if result.jd_keywords else "Paste JD to view.")

            st.subheader("Keyword Gaps")
            if result.gaps:
                st.warning(", ".join(result.gaps))
            else:
                st.success("No major gaps detected or no JD provided.")

            st.subheader("Actionable Suggestions")
            for s in result.suggestions:
                st.write(s)

            st.subheader("Auto-Parsed Sections")
            for k, v in result.sections.items():
                with st.expander(k.title()):
                    st.write(v)

            st.download_button("Download Raw Analysis JSON",
                               data=st.session_state.get("analysis_json", "").encode("utf-8") if "analysis_json" in st.session_state else str(result).encode("utf-8"),
                               file_name="analysis.json",
                               mime="application/json")
else:
    st.info("Upload a resume and paste a JD to begin.")
