import streamlit as st
import google.generativeai as genai
from docx import Document
import fitz  # PyMuPDF

# 💫 Your Gemini API key here
genai.configure(api_key="YOUR_API_KEY_HERE")
model = genai.GenerativeModel("gemini-pro")

st.set_page_config(page_title="AI Resume & Cover Letter Generator", layout="centered")

st.title("💼 AI Resume + Cover Letter Generator")
st.markdown("Upload your resume and job description. Let AI handle the rest ✨")

def read_text(file):
    return file.read().decode("utf-8")

def read_docx(file):
    doc = Document(file)
    return "\n".join([para.text for para in doc.paragraphs])

def read_pdf(file):
    pdf = fitz.open(stream=file.read(), filetype="pdf")
    return "\n".join([page.get_text() for page in pdf])

def extract_text(uploaded_file):
    if uploaded_file is None:
        return ""
    if uploaded_file.type == "application/pdf":
        return read_pdf(uploaded_file)
    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        return read_docx(uploaded_file)
    elif uploaded_file.type == "text/plain":
        return read_text(uploaded_file)
    else:
        return "Unsupported file format."

resume_file = st.file_uploader("📄 Upload your Resume (PDF/DOCX/TXT)", type=["pdf", "docx", "txt"])
job_file = st.file_uploader("🧾 Upload Job Description (PDF/DOCX/TXT)", type=["pdf", "docx", "txt"])

if st.button("Generate ✨") and resume_file and job_file:
    resume_text = extract_text(resume_file)
    job_text = extract_text(job_file)

    prompt = f"""
    You are a professional career coach. Based on the following RESUME and JOB DESCRIPTION, tailor and improve the resume and write a customized cover letter.

    RESUME:
    {resume_text}

    JOB DESCRIPTION:
    {job_text}

    Return both:
    1. 📄 Tailored Resume
    2. 💌 Personalized Cover Letter
    """

    with st.spinner("Generating with love... 💗"):
        response = model.generate_content(prompt)

    st.success("Done! Here’s your magic ✨")

    st.subheader("📄 Tailored Resume + 💌 Cover Letter")
    st.text_area("Output", response.text, height=600)

    st.download_button("💾 Download Result", response.text, file_name="resume_coverletter.txt")


