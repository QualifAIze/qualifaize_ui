import streamlit as st

from custom_styles import auth_styles

def show_sign_in_page():
    st.markdown(auth_styles, unsafe_allow_html=True)
    st.markdown('<div class="login-title">Sign In</div>', unsafe_allow_html=True)
    username = st.text_input("Username", placeholder="Enter your username", key="sign_in_username")
    password = st.text_input("Password", type="password", placeholder="Enter your password", key="sign_in_password")
    login_clicked = st.button("Sign in", use_container_width=True, type="primary", icon=":material/login:")
    register = st.button("Sign up", type="secondary", use_container_width=True, icon=":material/person_add:")

    if login_clicked:
        if username == "admin" and password == "admin123":
            st.success("Login successful")
        else:
            st.error("Invalid credentials")

    if register:
        st.session_state["registration_view"] = "sign_up"
        st.rerun()
