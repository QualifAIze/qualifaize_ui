import streamlit as st

from custom_styles import dashboard_styles

st.set_page_config(page_title="QualifAIze", layout="wide", page_icon="<UNK>")

st.markdown(dashboard_styles, unsafe_allow_html=True)

if st.session_state.authenticated_user:
    logged_user = st.session_state.authenticated_user
    st.header("Welcome, " + logged_user["username"] + "!")

st.title("Welcome to QualifAIze - An AI Automated Interview System")
st.markdown("""
> #### **Automated AI Interviews: Just Upload One Document**
>
> **Save time, remove bias, and streamline hiring.**  
> Upload a candidate’s resume or profile, and our AI creates a tailored interview, scores responses, and delivers detailed insights—automatically.
""")


if st.session_state.authenticated_user:
    st.info("You are logged in now! If you need more permissions feel free to contact us.")
    st.header("Thank you for choosing our AI Interview Platform!")
else:
    st.info("You are not logged in. Please login or register to unlock the full capabilities of automated AI interviews.")
    st.header("Why Choose our AI Interview Platform?")


# Features content
features = [
    ("🤖 AI-Driven Interviews",
     "Tailored interview questions generated in seconds by advanced AI. No templates, no manual setup."),
    ("📄 One-Document Simplicity",
     "Upload a resume or profile, and the AI builds a relevant, fair interview instantly."),
    ("⏱️ Save Time & Resources",
     "Automated assessments and reporting free your team to focus on connecting with top talent."),
    ("📊 Actionable Insights",
     "AI scoring and analytics highlight strengths and fit. Fast, consistent, and bias-resistant."),
    ("🔒 Secure & Private",
     "All candidate data and interviews are encrypted, private, and never shared."),
    ("🌍 Accessible Anywhere",
     "Interview candidates for any role, in any language, from any device worldwide.")
]

# Feature cards in rows of 3
for i in range(0, len(features), 3):
    cols = st.columns(3)
    for j, col in enumerate(cols):
        if i + j < len(features):
            title, desc = features[i + j]
            col.markdown(
                f"""
                <div class="feature-card">
                    <div class="feature-title">{title}</div>
                    <div>{desc}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

st.header("How It Works")

steps = [
    ("Upload", "Choose a resume or profile document to get started."),
    ("AI Analyzes", "Our AI instantly reads and understands the candidate’s experience and skills."),
    ("Custom Interview", "A unique interview is automatically generated—no human setup required."),
    ("Candidate Responds", "The candidate completes the interview online at their convenience."),
    ("Automated Scoring", "AI scores answers and generates a detailed report with strengths and improvement areas."),
    ("Review Insights", "Access all results securely from your dashboard and make confident decisions.")
]

for idx, (action, detail) in enumerate(steps, 1):
    st.markdown(
        f"""
        <span class="step-number">{idx}</span> **{action}:** {detail}
        """,
        unsafe_allow_html=True
    )

st.header("Frequently Asked Questions")

with st.expander("How does the AI create interviews?"):
    st.write(
        "Our AI reads the uploaded document and instantly creates a set of role-relevant, personalized questions. Every candidate receives a unique interview tailored to their background—no generic forms or templates.")
with st.expander("Is my data secure?"):
    st.write(
        "Absolutely. All uploads, responses, and results are encrypted and protected with enterprise-grade security. Data is never sold or shared.")
with st.expander("Which file types are supported?"):
    st.write("You can upload resumes, CVs, or detailed profiles in PDF or DOCX format.")
with st.expander("Can I adjust or review the AI-generated interviews?"):
    st.write("Yes! After logging in, you can customize focus areas, review generated questions, and add your own.")

st.header("Ready to Get Started?")

st.markdown("""
- **Sign up** for a smarter, fairer, and faster hiring process.
- **Contact us:** [support@qualifaize.com](mailto:support@qualifaize.com)
""")

st.success("Empower your hiring process with automated, AI-driven interviews. All you need is a single document!")
