import streamlit as st

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


def login():
    if st.button("Log in"):
        st.session_state.logged_in = True
        st.rerun()


def logout():
    st.session_state.logged_in = False
    st.rerun()


sign_in_page = st.Page("pages/auth/authentication.py", title="Sign In", icon=":material/login:")
sign_up_page = st.Page("pages/auth/sign_up.py", title="Sign Up", icon=":material/person_add:")
logout_page = st.Page(logout, title="Sign Out", icon=":material/logout:")

account_details = st.Page("pages/account_details.py", title="Account Details", icon=":material/account_circle:")

dashboard = st.Page("pages/dashboard/logged_dashboard.py", title="Home Screen",
                    icon=":material/home:", default=True)
not_logged_dashboard = st.Page("pages/dashboard/not_logged_dashboard.py", title="Home Screen",
                               icon=":material/home:", default=True)

bugs = st.Page("reports/bugs.py", title="Bug reports", icon=":material/bug_report:")
alerts = st.Page("reports/alerts.py", title="System alerts", icon=":material/notification_important:")

search = st.Page("tools/search.py", title="Search", icon=":material/search:")
history = st.Page("tools/history.py", title="History", icon=":material/history:")

if st.session_state.logged_in:
    pg = st.navigation(
        {
            "Account": [logout_page, account_details],
            "Reports": [dashboard, bugs, alerts],
            "Tools": [search, history],
        }
    )
else:
    pg = st.navigation(
        {
            "Account": [sign_in_page],
            "Home": [not_logged_dashboard]
        }
    )

pg.run()
