import json
import time

import streamlit as st
import requests
import pandas as pd
from constants import ADMIN_USER_ID, ROLES, BACKEND_BASE_URL


@st.dialog("Edit user")
def edit_user(user_data):
    id = st.text_input("ID", value=user_data["id"], disabled=True)
    username = st.text_input("Username", value=user_data["username"], disabled=True)
    full_name = st.text_input("Full name", value=user_data["full_name"])
    email = st.text_input("Email", value=user_data["email"])
    role = st.selectbox("Role", ROLES, ROLES.index(user_data["role"]))
    password = st.text_input("Password", type="password")

    user_dict = {
        "full_name": full_name,
        "email": email,
        "role": role
    }
    if password is not None and password.strip() != "":
        user_dict["password"] = password

    if st.button("Submit", type="primary", use_container_width=True):
        response = requests.put(f"{BACKEND_BASE_URL}/users/{user_data['id']}", data=json.dumps(user_dict),
                                headers=st.session_state.auth_headers)
        if response.status_code == 200:
            st.success("Successfully updated user!")
            time.sleep(1)
            st.rerun()
        else:
            st.error(f"Error updating user: {response.json()}")


@st.dialog("Create new user")
def create_new_user():
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    full_name = st.text_input("Full name")
    email = st.text_input("Email")
    role = st.selectbox("Role", ROLES, index=1)

    user_dict = {
        "username": username,
        "password": password,
        "full_name": full_name,
        "email": email,
        "role": role,
        "disabled": False,
    }

    if st.button("Submit", type="primary", use_container_width=True):
        if username.strip() == "":
            st.error("User name cannot be empty")
            return

        if password.strip() == "":
            st.error("Please, specify non empty password")
            return

        response = requests.post(f"{BACKEND_BASE_URL}/users", json.dumps(user_dict),
                                 headers=st.session_state.auth_headers)
        if response.status_code == 201:
            st.success("Successfully created user")
            time.sleep(1)
            st.rerun()
        else:
            st.error(f"Error creating user: {response.json()}")


def get_all_users():
    response = requests.get(f"{BACKEND_BASE_URL}/users", headers=st.session_state.auth_headers)
    if response.status_code == 200:
        return response.json()
    else:
        st.write("Error requesting Users!")


def delete_user(user_id):
    response = requests.delete(f"{BACKEND_BASE_URL}/users/{user_id}", headers=st.session_state.auth_headers)
    if response.status_code == 204:
        st.toast("User deleted successfully!", icon=":material/check_circle:")
    else:
        st.error(f"Error deleting user: {response.json()}")


st.markdown("## User Management")

st.sidebar.markdown("## User Management")

response = requests.get(f"{BACKEND_BASE_URL}/users", headers=st.session_state.auth_headers)

if st.button("Create new user", type="primary", use_container_width=True):
    create_new_user()

container = st.container(border=True)
df_users = pd.DataFrame(get_all_users())

col_distribution = [2, 2, 2, 2, 1, 1]
col1, col2, col3, col4, _, _ = container.columns(col_distribution)
with col1:
    st.markdown("<p style='text-align: center; margin-bottom: 0; font-weight: bold;'>Username</p>", unsafe_allow_html=True)
with col2:
    st.markdown("<p style='text-align: center; margin-bottom: 0; font-weight: bold;'>Full name</p>", unsafe_allow_html=True)
with col3:
    st.markdown("<p style='text-align: center; margin-bottom: 0; font-weight: bold;'>Email</p>", unsafe_allow_html=True)
with col4:
    st.markdown("<p style='text-align: center; margin-bottom: 0; font-weight: bold;'>Role</p>", unsafe_allow_html=True)

container.divider()

for index, row in df_users.iterrows():
    col1, col2, col3, col4, col5, col6 = container.columns(col_distribution, vertical_alignment="center")
    with col1:
        st.markdown(f"<p style='text-align: center;'>{row['username']}</p>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<p style='text-align: center;'>{row['full_name']}</p>", unsafe_allow_html=True)
    with col3:
        st.markdown(f"<p style='text-align: center;'>{row['email']}</p>", unsafe_allow_html=True)
    with col4:
        st.markdown(f"<p style='text-align: center;'>{row['role']}</p>", unsafe_allow_html=True)
    if row["id"] != ADMIN_USER_ID:
        col5.button('Edit', key=f'edit{row["id"]}', on_click=edit_user, args=(row,), use_container_width=True)
        col6.button('Delete', key=f'delete{row["id"]}', on_click=delete_user, args=(row["id"],), type="primary", use_container_width=True, icon=":material/delete:")
