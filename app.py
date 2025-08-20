import matplotlib.pyplot as plt
import streamlit as st
import PyPDF2
import docx

# ============================
# 🎨 Streamlit Page Config
# ============================
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================
# 📌 Data Setup
# ============================
# Common skills to detect
skill_keywords = [
    "Python", "Java", "C++", "C", "SQL", "HTML", "CSS", "JavaScript",
    "React", "Node.js", "Django", "Flask", "Machine Learning",
    "Deep Learning", "Data Science", "AI", "NLP", "Excel",
    "Tableau", "Power BI"
]

# Predefined Job Roles with Required Skills
job_roles = {
    "Data Scientist": ["Python", "SQL", "Machine Learning", "AI", "Data Science"],
    "Web Developer": ["HTML", "CSS", "JavaScript", "React", "Node.js"],
    "Software Engineer": ["Java", "C++", "Python", "SQL"],
    "Data Analyst": ["SQL", "Excel", "Tableau", "Power BI", "Python"]
}

# ============================
# 📌 Functions
# ============================
def check_sections(text):
    sections = ["Education", "Experience", "Skills", "Projects"]
    missing, present = [], []
    for sec in sections:
        if sec.lower() in text.lower():
            present.append(sec)
        else:
            missing.append(sec)
    return present, missing


def extract_skills(text):
    found = []
    for skill in skill_keywords:
        if skill.lower() in text.lower():
            found.append(skill)
    return list(set(found))  # remove duplicates


def match_job_role(skills):
    results = {}
    for role, req_skills in job_roles.items():
        match_count = len(set(skills) & set(req_skills))
        score = (match_count / len(req_skills)) * 100
        results[role] = round(score, 2)
    return results


def extract_text_from_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text


def extract_text_from_docx(file):
    doc = docx.Document(file)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text


# ============================
# 🚀 Streamlit App
# ============================
st.markdown("<h1 style='text-align: center; color: #4CAF50;'>📄 AI-Powered Resume Analyzer</h1>", unsafe_allow_html=True)
st.write("Upload your resume and get instant insights on skills, missing sections, and job role fit!")

uploaded_file = st.file_uploader("📂 Upload your Resume (PDF or DOCX)", type=["pdf", "docx"])

if uploaded_file is not None:
    # Extract text
    if uploaded_file.name.endswith(".pdf"):
        resume_text = extract_text_from_pdf(uploaded_file)
    elif uploaded_file.name.endswith(".docx"):
        resume_text = extract_text_from_docx(uploaded_file)
    else:
        resume_text = "❌ Unsupported file format"

    # Show extracted text (collapsible)
    with st.expander("📑 View Extracted Resume Text"):
        st.write(resume_text[:1500])  # limit characters

    # Section Check
    st.markdown("### 📌 Resume Sections")
    present, missing = check_sections(resume_text)

    col1, col2 = st.columns(2)
    with col1:
        st.success(f"✅ Found Sections: {', '.join(present) if present else 'None'}")
    with col2:
        st.error(f"❌ Missing Sections: {', '.join(missing) if missing else 'None'}")

    # Skill Extraction
    st.markdown("### 🛠️ Skills Detected")
    skills = extract_skills(resume_text)
    if skills:
        st.info(", ".join(skills))
    else:
        st.warning("❌ No skills detected. Try adding technical keywords in your resume.")

    # Job Role Matching
    st.markdown("### 📊 Job Role Fit Percentage")
    match_results = match_job_role(skills)
    for role, score in match_results.items():
        st.write(f"**{role}**: {score}%")

    # Visualization
    st.markdown("### 📊 Job Match Graph")
    roles = list(match_results.keys())
    scores = list(match_results.values())
    fig, ax = plt.subplots()
    ax.bar(roles, scores, color="#4CAF50")
    ax.set_ylabel("Match %")
    ax.set_title("Resume vs Job Role Fit")
    st.pyplot(fig)

    # Suggestions
    st.markdown("### 💡 Suggestions to Improve Resume")
    for role, req_skills in job_roles.items():
        missing_skills = set(req_skills) - set(skills)
        if missing_skills:
            st.warning(f"👉 To improve for **{role}**, add: {', '.join(missing_skills)}")
        else:
            st.success(f"✅ Your resume is strong for **{role}**")

# Footer
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>Made with ❤️ by Rupa Sri</p>", unsafe_allow_html=True)
