import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(page_title="Interview System", layout="wide")

# Demo data for public view
demo_upcoming = [
    {"Candidate": "Sample A", "Position": "Data Scientist", "Date": (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d'), "Time": "10:00", "Status": "Scheduled"},
    {"Candidate": "Sample B", "Position": "Backend Engineer", "Date": (datetime.now() + timedelta(days=2)).strftime('%Y-%m-%d'), "Time": "14:00", "Status": "Confirmed"},
    {"Candidate": "Sample C", "Position": "UI/UX Designer", "Date": (datetime.now() + timedelta(days=3)).strftime('%Y-%m-%d'), "Time": "11:30", "Status": "Awaiting Candidate"},
]
demo_results = [
    {"Candidate": "Sample D", "Position": "Product Manager", "Date": (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d'), "Result": "Passed"},
    {"Candidate": "Sample E", "Position": "QA Analyst", "Date": (datetime.now() - timedelta(days=2)).strftime('%Y-%m-%d'), "Result": "Pending Feedback"},
]
demo_stats = {
    "Total Candidates": 120,
    "Interviews This Week": 23,
    "Pending Feedback": 4
}

# Convert to DataFrames
upcoming_df = pd.DataFrame(demo_upcoming)
results_df = pd.DataFrame(demo_results)

# UI
st.title("Welcome to Interview System")
st.markdown("""
> **Streamline your hiring and interview process.  
> Schedule, manage, and review interviews — all in one place!**
""")

st.info("You are not logged in. Sign up or log in to access full features.")

cta_cols = st.columns(2)
cta_cols[0].button("Login")
cta_cols[1].button("Register")

st.header("Platform Highlights")

feature_cols = st.columns(3)
feature_cols[0].markdown("#### 🗓️ Easy Interview Scheduling\nQuickly book and track interviews with top candidates.")
feature_cols[1].markdown("#### 📈 Candidate Analytics\nGet insights into candidate performance and feedback.")
feature_cols[2].markdown("#### 🛡️ Secure & Reliable\nYour data is safe and always accessible.")

st.subheader("Sample Interview Data")
stat_cols = st.columns(3)
stat_cols[0].metric("Total Candidates", demo_stats["Total Candidates"])
stat_cols[1].metric("Interviews This Week", demo_stats["Interviews This Week"])
stat_cols[2].metric("Pending Feedback", demo_stats["Pending Feedback"])

st.markdown("##### Upcoming Interviews (Sample)")
st.table(upcoming_df)

st.markdown("##### Recent Results (Sample)")
st.table(results_df)
