import streamlit as st
from jose import jwt

from api_client.services.user_service import UserService
from constants import SECRET_KEY, ALGORITHM
from custom_styles import auth_styles


def decode_jwt(token):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    username = payload.get("sub")
    user_id = payload.get("userId")
    roles = payload.get("roles")

    user_object = {
        "token": token,
        "username": username,
        "user_id": user_id,
        "roles": roles,
        "auth_headers": {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
    }

    return user_object



def show_sign_in_page():
    st.markdown(auth_styles, unsafe_allow_html=True)
    st.markdown('<div class="login-title">Sign In</div>', unsafe_allow_html=True)

    user_service = UserService()

    username = st.text_input("Username", placeholder="Enter your username", key="sign_in_username")
    password = st.text_input("Password", type="password", placeholder="Enter your password", key="sign_in_password")

    login_clicked = st.button("Sign in", use_container_width=True, type="primary", icon=":material/login:")
    register = st.button("Sign up", type="secondary", use_container_width=True, icon=":material/person_add:")

    if login_clicked:
        if not username or not password:
            st.error("Please enter both username and password")
        else:
            with st.spinner("Signing in..."):
                response = user_service.login(username, password)

                if response.is_success:
                    logged_user = decode_jwt(response.data["token"])
                    st.session_state.authenticated_user = logged_user
                    st.rerun()
                else:
                    st.error("Invalid username or password")

    if register:
        st.session_state["registration_view"] = "sign_up"
        st.rerun()