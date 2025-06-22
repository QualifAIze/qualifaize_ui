import streamlit as st

import constants

if "authenticated_user" not in st.session_state:
    st.session_state.authenticated_user = None


def get_available_not_authenticated_pages():
    return {
        "Account": [sign_in_page],
        "Home": [dashboard]
    }


def get_available_authenticated_guest_role_pages():
    return {
        "Account": [logout_page, account_details],
        "Home": [dashboard]
    }


def get_available_authenticated_user_role_pages():
    available_pages = get_available_authenticated_guest_role_pages()
    available_pages["Home"].extend([interview, interview_history])
    return available_pages


def get_available_authenticated_admin_role_pages():
    available_pages = get_available_authenticated_user_role_pages()
    available_pages.update({
        "Management": [document_management, user_management]
    })
    return available_pages


def logout():
    st.session_state.authenticated_user = None
    st.rerun()


sign_in_page = st.Page("pages/auth/authentication_page.py", title="Sign In", icon=":material/login:")
logout_page = st.Page(logout, title="Sign Out", icon=":material/logout:")

account_details = st.Page("pages/account_details_page.py", title="Account Details", icon=":material/account_circle:")

dashboard = st.Page("pages/dashboard_page.py", title="Home Screen",
                    icon=":material/home:", default=True)

interview = st.Page("pages/interview_page.py", title="Interview", icon=":material/adaptive_audio_mic:")
interview_history = st.Page("pages/interview_history_page.py", title="History", icon=":material/history:")

document_management = st.Page("pages/management/pdf_management_page.py", title="Document Management",
                              icon=":material/folder_managed:")
user_management = st.Page("pages/management/user_management_page.py", title="User Management",
                          icon=":material/manage_accounts:")

if st.session_state.authenticated_user is not None:
    logged_user = st.session_state.authenticated_user

    available_authenticated_pages = get_available_authenticated_guest_role_pages()

    if constants.ROLE_USER in logged_user['roles']:
        available_authenticated_pages = get_available_authenticated_user_role_pages()

    if constants.ROLE_ADMIN in logged_user['roles']:
        available_authenticated_pages = get_available_authenticated_admin_role_pages()

    pg = st.navigation(available_authenticated_pages)

else:
    pg = st.navigation(get_available_not_authenticated_pages())

pg.run()
