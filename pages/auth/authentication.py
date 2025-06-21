import streamlit as st
from pages.auth.sign_in import show_sign_in_page
from pages.auth.sign_up import show_sign_up_page

st.set_page_config(page_title="QualifAIze Authentication", layout="centered", page_icon="🛡️")

if "registration_view" not in st.session_state:
    st.session_state["registration_view"] = "sign_in"

view = st.session_state["registration_view"]

if view == "sign_in":
    show_sign_in_page()
elif view == "sign_up":
    show_sign_up_page()