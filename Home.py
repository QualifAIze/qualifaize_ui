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
    available_pages["Home"].extend([bugs, alerts])
    return available_pages


def get_available_authenticated_admin_role_pages():
    available_pages = get_available_authenticated_user_role_pages()
    available_pages.update({
        "Tools": [search, history]
    })
    return available_pages


def logout():
    st.session_state.authenticated_user = None
    st.rerun()


sign_in_page = st.Page("pages/auth/authentication.py", title="Sign In", icon=":material/login:")
sign_up_page = st.Page("pages/auth/sign_up.py", title="Sign Up", icon=":material/person_add:")
logout_page = st.Page(logout, title="Sign Out", icon=":material/logout:")

account_details = st.Page("pages/account_details.py", title="Account Details", icon=":material/account_circle:")

dashboard = st.Page("pages/dashboard.py", title="Home Screen",
                    icon=":material/home:", default=True)

bugs = st.Page("reports/bugs.py", title="Bug reports", icon=":material/bug_report:")
alerts = st.Page("reports/alerts.py", title="System alerts", icon=":material/notification_important:")

search = st.Page("tools/search.py", title="Search", icon=":material/search:")
history = st.Page("tools/history.py", title="History", icon=":material/history:")

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
