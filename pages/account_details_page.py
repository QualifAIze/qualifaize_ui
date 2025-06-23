from datetime import datetime, date

import streamlit as st

from api_client.services.user_service import UserService
from custom_styles import account_details_styles
from dialogs.update_user_details_dialog import update_user_dialog

user_service = UserService()


def get_account_type(roles):
    """Determine account type based on roles"""
    if not roles:
        return "Guest"

    if "ADMIN" in roles:
        return "Administrator"
    elif "USER" in roles:
        return "Standard User"
    elif "GUEST" in roles:
        return "Guest"
    else:
        return "Guest"


def get_user_details():
    """Fetch current user details from the API"""
    try:
        response = user_service.get_current_user_details()
        if response.is_success:
            return response.data
        else:
            st.error(f"Failed to fetch user details: {response.error}")
            return None
    except Exception as e:
        st.error(f"Error fetching user details: {str(e)}")
        return None


@st.dialog("Update User Details", width="large")
def show_update_user_dialog(current_user_data):
    update_user_dialog(current_user_data, user_service)


# Custom CSS for enhanced styling with theme support
st.markdown(account_details_styles, unsafe_allow_html=True)

# Check authentication
if not st.session_state.get('authenticated_user'):
    st.error("❌ You must be logged in to view account details")
    st.info("Please sign in to access your account information")
    st.stop()

# Page header
st.title("👤 Account Details")
st.markdown("*Manage your personal information and account settings*")

# Fetch user details
with st.spinner("Loading your account details..."):
    user_data = get_user_details()

if not user_data:
    st.error("Could not load account details. Please try again later.")
    st.stop()

st.markdown(
    f"### 🎯 Welcome, **{user_data.get('username', 'User')}!** <span class='account-type-badge'>{get_account_type(st.session_state.authenticated_user['roles'])}</span>",
    unsafe_allow_html=True)

st.divider()

info_cols = st.columns(2)

with info_cols[0]:
    st.markdown("**👤 Identity**")

    st.markdown(f'''
        <div class="info-field">
            <div class="info-label">Username</div>
            <div class="info-value">{user_data.get('username', 'Not provided')}</div>
        </div>
        ''', unsafe_allow_html=True)

    # First Name field
    st.markdown(f'''
        <div class="info-field">
            <div class="info-label">First Name</div>
            <div class="info-value">{user_data.get('firstName', 'Not provided')}</div>
        </div>
        ''', unsafe_allow_html=True)

    # Last Name field
    st.markdown(f'''
        <div class="info-field">
            <div class="info-label">Last Name</div>
            <div class="info-value">{user_data.get('lastName', 'Not provided')}</div>
        </div>
        ''', unsafe_allow_html=True)

with info_cols[1]:
    st.markdown("**📧 Contact & Personal**")

    # Email field
    st.markdown(f'''
        <div class="info-field">
            <div class="info-label">Email Address</div>
            <div class="info-value">{user_data.get('email', 'Not provided')}</div>
        </div>
        ''', unsafe_allow_html=True)

    # Format birth date
    birth_date_str = "Not provided"
    if user_data.get('birthDate'):
        try:
            birth_date_iso = user_data['birthDate']
            if birth_date_iso.endswith('Z'):
                birth_date_iso = birth_date_iso[:-1] + '+00:00'
            birth_date = datetime.fromisoformat(birth_date_iso)
            birth_date_str = birth_date.strftime('%B %d, %Y')
        except (ValueError, TypeError):
            birth_date_str = "Invalid date format"

    # Birth Date field
    st.markdown(f'''
        <div class="info-field">
            <div class="info-label">Birth Date</div>
            <div class="info-value">{birth_date_str}</div>
        </div>
        ''', unsafe_allow_html=True)

    if user_data.get('birthDate') and birth_date_str != "Not provided":
        try:
            birth_date_iso = user_data['birthDate']
            if birth_date_iso.endswith('Z'):
                birth_date_iso = birth_date_iso[:-1] + '+00:00'
            birth_date = datetime.fromisoformat(birth_date_iso).date()
            age = (date.today() - birth_date).days // 365

            st.markdown(f'''
                <div class="info-field">
                    <div class="info-label">Age</div>
                    <div class="info-value">{age} years old</div>
                </div>
                ''', unsafe_allow_html=True)
        except (ValueError, TypeError):
            pass
if st.button("✏️ Update Details", type="primary", use_container_width=True):
    show_update_user_dialog(user_data)

st.divider()

st.markdown("### 🔐 Account Status")

status_cols = st.columns(3)

with status_cols[0]:
    member_since_str = "Unknown"
    if user_data.get('memberSince'):
        try:
            member_since_iso = user_data['memberSince']
            if member_since_iso.endswith('Z'):
                member_since_iso = member_since_iso[:-1] + '+00:00'
            member_since = datetime.fromisoformat(member_since_iso)
            member_since_str = member_since.strftime('%B %d, %Y')
        except (ValueError, TypeError):
            member_since_str = "Invalid date"

    st.markdown(f'''
        <div class="info-field">
            <div class="info-label">📅 Member Since</div>
            <div class="info-value">{member_since_str}</div>
        </div>
        ''', unsafe_allow_html=True)

with status_cols[1]:
    # User ID field
    st.markdown(f'''
        <div class="info-field">
            <div class="info-label">🆔 User ID</div>
            <div class="info-value">{user_data.get('userId', 'N/A')}</div>
        </div>
        ''', unsafe_allow_html=True)

with status_cols[2]:
    # Account Status field
    st.markdown(f'''
        <div class="info-field">
            <div class="info-label">✅ Account Status</div>
            <div class="info-value"><span class="status-badge">Active</span></div>
        </div>
        ''', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Quick Actions Section
st.markdown("### ⚡ Quick Actions")

action_cols = st.columns(4)

with action_cols[0]:
    if st.button("🔑 Change Password", use_container_width=True, type="secondary"):
        st.info("🚧 Password change functionality will be implemented in a future update")

with action_cols[1]:
    if st.button("🖼️ Update Avatar", use_container_width=True, type="secondary"):
        st.info("🚧 Avatar upload functionality will be implemented in a future update")

with action_cols[2]:
    if st.button("🔔 Notifications", use_container_width=True, type="secondary"):
        st.info("🚧 Notification settings will be implemented in a future update")

with action_cols[3]:
    if st.button("📊 Activity Log", use_container_width=True, type="secondary"):
        st.info("🚧 Activity log will be implemented in a future update")

# Help Section
with st.expander("❓ Need Help?"):
    st.markdown("""
    **Common Questions:**

    - **How to update my information?** Click the "Update Details" button and modify the fields you want to change.
    - **How to change my password?** This feature is coming soon. Contact support for now.
    - **Can I change my username?** Yes, but make sure it's unique across the system.
    - **How to delete my account?** Contact our support team for account deletion requests.

    **Support Contact:**
    - 📧 Email: support@qualifaize.com
    - 🌐 Documentation: [Help Center](#)
    """)
