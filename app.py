import streamlit as st
import google.generativeai as genai
from docx import Document
import fitz  # PyMuPDF

# 💫 Your Gemini API key here
genai.configure(api_key="AIzaSyATEszYwg7t-qmuBIqLVD3vuDUlHWZ5CSA")
model = genai.GenerativeModel("gemini-pro")

st.set_page_config(page_title="AI Resume & Cover Letter Generator", layout="centered")

st.title("💼 AI Resume + Cover Letter Generator")
st.markdown("Upload your resume and job description. Let AI handle the rest ✨")

# File reading functions
def read_text(file):
    return file.read().decode("utf-8")

def read_docx(file):
    doc = Document(file)
    return "\n".join([para.text for para in doc.paragraphs])

def read_pdf(file):
    pdf = fitz.open(stream=file.read(), filetype="pdf")
    return "\n".join([page.get_text() for page in pdf])

# Universal text extractor
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

# File uploaders
resume_file = st.file_uploader("📄 Upload your Resume (PDF/DOCX/TXT)", type=["pdf", "docx", "txt"])
job_file = st.file_uploader("🧾 Upload Job Description (PDF/DOCX/TXT)", type=["pdf", "docx", "txt"])

# Generate content
if st.button("Generate ✨"):
    if resume_file and job_file:
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

        st.success("Done! Here's your magic ✨")

        if "1." in response.text and "2." in response.text:
            resume_part = response.text.split("2.")[0].replace("1. 📄 Tailored Resume", "").strip()
            cover_letter_part = response.text.split("2.")[1].replace("💌 Personalized Cover Letter", "").strip()

            st.subheader("📄 Tailored Resume")
            st.text_area("Resume", resume_part, height=300)
            st.download_button("📥 Download Resume", resume_part, file_name="Tailored_Resume.txt")

            st.subheader("💌 Cover Letter")
            st.text_area("Cover Letter", cover_letter_part, height=300)
            st.download_button("📥 Download Cover Letter", cover_letter_part, file_name="Cover_Letter.txt")
        else:
            st.text_area("Output", response.text, height=600)
            st.download_button("💾 Download Result", response.text, file_name="resume_coverletter.txt")
    else:
        st.warning("Please upload both your resume and job description 💼🧾")
