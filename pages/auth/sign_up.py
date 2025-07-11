import datetime

import streamlit as st
from custom_styles import auth_styles
from api_client.services.user_service import UserService
from pages.auth.sign_in import decode_jwt


def show_sign_up_page():
    st.markdown(auth_styles, unsafe_allow_html=True)
    st.markdown('<div class="login-title">Sign Up</div>', unsafe_allow_html=True)
    guest_mode = st.toggle("Continue as guest")
    username = st.text_input("Username", placeholder="Enter your username", key="sign_up_username")

    firstname = None
    lastname = None
    email = None
    birthdate = None

    if not guest_mode:
        firstname = st.text_input("First Name", placeholder="Enter your first name", key="sign_up_firstname")
        lastname = st.text_input("Last Name", placeholder="Enter your last name", key="sign_up_lastname")
        email = st.text_input("Email", placeholder="Enter your email address", key="sign_up_email")
        birthdate = st.date_input("When's your birthday",
                                  value=None,
                                  min_value=datetime.date(1900, 1, 1),
                                  max_value="today")
    password = st.text_input("Password", type="password", placeholder="Enter your password", key="sign_up_password")
    sign_up = st.button("Sign Up", use_container_width=True, key="sign_up", type="primary",
                        icon=":material/person_add:")
    back = st.button("Back to Sign in", use_container_width=True, key="back_to_sign_in", icon=":material/login:")

    if back:
        st.session_state["registration_view"] = "sign_in"
        st.rerun()

    if sign_up:
        user_service = UserService()
        birthdate_as_string = None
        roles = ["GUEST"]
        if not guest_mode:
            roles.append("USER")
            birthdate_as_string = "{:04d}-{:02d}-{:02d}T00:00:00Z".format(birthdate.year, birthdate.month, birthdate.day)
        response = user_service.register(username, password, email, firstname, lastname, birthdate_as_string, roles)
        logged_user = decode_jwt(response.data["token"])
        st.session_state.authenticated_user = logged_user
        st.rerun()
