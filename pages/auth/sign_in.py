import streamlit as st
from custom_styles import auth_styles
from auth_handler import AuthHandler


def show_sign_in_page():
    st.markdown(auth_styles, unsafe_allow_html=True)
    st.markdown('<div class="login-title">Sign In</div>', unsafe_allow_html=True)

    # Initialize auth handler
    auth_handler = AuthHandler()

    # Form inputs
    username = st.text_input("Username", placeholder="Enter your username", key="sign_in_username")
    password = st.text_input("Password", type="password", placeholder="Enter your password", key="sign_in_password")

    # Buttons
    login_clicked = st.button("Sign in", use_container_width=True, type="primary", icon=":material/login:")
    register = st.button("Sign up", type="secondary", use_container_width=True, icon=":material/person_add:")

    # Handle login
    if login_clicked:
        if not username or not password:
            st.error("Please enter both username and password")
        else:
            with st.spinner("Signing in..."):
                success = auth_handler.login(username, password)

                if success:
                    st.success("Login successful!")
                    st.balloons()
                    # Redirect to main application
                    st.session_state["page"] = "dashboard"
                    st.rerun()
                else:
                    st.error("Invalid username or password")

    # Handle registration redirect
    if register:
        st.session_state["registration_view"] = "sign_up"
        st.rerun()