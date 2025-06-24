import streamlit as st

from api_client.services.user_service import UserService
from custom_styles import user_management_styles
from dialogs.user_management_dialogs import add_new_user_dialog, edit_user_dialog
from utils import truncate_text, format_date, get_role_display, get_role_color

user_service = UserService()

@st.dialog("✏️ Edit User Details", width="large")
def show_edit_user_dialog(user_id_to_update, user_data_before_update):
    edit_user_dialog(user_id_to_update, user_data_before_update, user_service)


@st.dialog("👤 Add New User", width="large")
def show_add_user_dialog():
    add_new_user_dialog(user_service)


def confirm_delete_user(user_to_delete_id):
    """Confirm and delete user"""
    if st.button(
            f"🗑️ Confirm Delete",
            type="primary",
            key=f"confirm_delete_user_{user_to_delete_id}",
            use_container_width=True
    ):
        with st.spinner("Deleting user..."):
            try:
                delete_response = user_service.delete_user(user_to_delete_id)

                if delete_response.is_success:
                    st.success(f"✅ User '{username}' deleted successfully!")
                    st.rerun()
                else:
                    error_message = response.error or "Unknown error occurred"
                    st.error(f"❌ Delete failed: {error_message}")

            except Exception as e:
                st.error(f"❌ Error deleting user: {str(e)}")


st.set_page_config(page_title="User Management - QualifAIze", layout="wide", page_icon="👥")

st.markdown(user_management_styles, unsafe_allow_html=True)

st.title("👥 User Management")
st.markdown("*Manage user accounts and permissions in the system*")

current_user = st.session_state.get('authenticated_user', {})
user_roles = current_user.get('roles', [])

if not current_user:
    st.error("❌ You must be logged in to access user management")
    st.info("Please sign in to manage users")
    st.stop()

if "ADMIN" not in user_roles:
    st.error("❌ Access Denied")
    st.warning("You need administrator privileges to manage users")
    st.info("Contact your system administrator for access")
    st.stop()

if st.button("👤 Add New User", type="primary", use_container_width=True):
    show_add_user_dialog()

st.divider()

with st.spinner("Loading users..."):
    try:
        response = user_service.get_all_users()

        if response.is_success and response.data:
            users = response.data

            st.markdown(f"""
            <div class="section-header">
                <h3 style="margin: 0; color: #1e40af; font-size: 18px;">
                    👥 User Directory
                </h3>
                <p style="margin: 2px 0 0 0; color: #6b7280; font-size: 14px;">
                    {len(users)} users available
                </p>
            </div>
            """, unsafe_allow_html=True)

            for row_index in range(0, len(users), 3):
                user_cols = st.columns(3)
                row_users = users[row_index:row_index + 3]

                for col_index, user in enumerate(row_users):
                    with user_cols[col_index]:
                        with st.container(border=True):
                            user_id = user.get('userId')
                            username = user.get('username', 'Unknown')
                            first_name = user.get('firstName', '')
                            last_name = user.get('lastName', '')
                            email = user.get('email', '')
                            user_roles_display = user.get('roles', ['GUEST'])

                            full_name = f"{first_name} {last_name}".strip()
                            if not full_name:
                                full_name = username

                            display_name = full_name if full_name != username else username
                            st.markdown(f"""#### 👨🏻‍💼 {truncate_text(display_name, 25)}""")

                            if display_name != username:
                                st.markdown(f"""
                                <div class='user-meta'>
                                    🏷️ @{truncate_text(username, 20)}
                                </div>
                                """, unsafe_allow_html=True)

                            if email:
                                st.markdown(f"""
                                <div class='user-meta' title='{email}'>
                                    📧 {truncate_text(email, 22)}
                                </div>
                                """, unsafe_allow_html=True)

                            member_since = "Unknown"
                            if user.get('memberSince'):
                                member_since = format_date(user.get('memberSince'))

                            st.markdown(f"""
                            <div class='user-meta'>
                                📅 Member since {member_since}
                            </div>
                            """, unsafe_allow_html=True)

                            role_display = get_role_display(user_roles_display)
                            role_color = get_role_color(user_roles_display)

                            st.markdown(f"""
                                <div class='role-badge' style='color: {role_color}; border-color: {role_color}; background: {role_color}15;'>
                                    🛡️ {role_display}
                                </div>
                                """, unsafe_allow_html=True)

                            action_col1, action_col2 = st.columns(2)

                            current_user_data = st.session_state.get('authenticated_user', {})
                            current_user_id = current_user_data.get('user_id')

                            can_delete = (str(user_id) != str(current_user_id) and
                                          not ("ADMIN" in user_roles_display and str(current_user_id) != str(user_id)))

                            with action_col1:
                                if st.button("✏️ Edit",
                                             key=f"edit_user_{user_id}",
                                             help="Edit user details",
                                             use_container_width=True,
                                             type="secondary"):
                                    show_edit_user_dialog(user_id, user)

                            with action_col2:
                                delete_key = f"delete_confirm_user_{user_id}"
                                if delete_key not in st.session_state:
                                    st.session_state[delete_key] = False

                                if not can_delete:
                                    st.button("🔒 Protected",
                                              key=f"protected_user_{user_id}",
                                              help="Cannot delete this user",
                                              use_container_width=True,
                                              disabled=True,
                                              type="secondary")
                                elif not st.session_state[delete_key]:
                                    if st.button("🗑️ Delete",
                                                 key=f"delete_user_{user_id}",
                                                 help="Delete user",
                                                 use_container_width=True,
                                                 type="secondary"):
                                        st.session_state[delete_key] = True
                                        st.rerun()
                                else:
                                    if st.button("❌ Cancel",
                                                 key=f"cancel_delete_user_{user_id}",
                                                 help="Cancel deletion",
                                                 use_container_width=True,
                                                 type="secondary"):
                                        st.session_state[delete_key] = False
                                        st.rerun()

                            delete_key = f"delete_confirm_user_{user_id}"
                            if st.session_state.get(delete_key, False):
                                st.markdown('<div class="delete-confirmation">', unsafe_allow_html=True)

                                st.markdown(f"""
                                <div style="margin-bottom: 6px;">
                                    <span style="font-size: 14px; font-weight: 500; color: #dc2626;">
                                        ⚠️ Delete this user?
                                    </span>
                                </div>
                                """, unsafe_allow_html=True)

                                confirm_col1, confirm_col2 = st.columns(2)
                                with confirm_col1:
                                    if st.button("Cancel", key=f"cancel_confirm_user_{user_id}", type="secondary",
                                                 use_container_width=True):
                                        st.session_state[delete_key] = False
                                        st.rerun()
                                with confirm_col2:
                                    confirm_delete_user(user_id)

                                st.markdown('</div>', unsafe_allow_html=True)

                if row_index + 3 < len(users):
                    st.markdown('<div style="margin: 12px 0;"></div>', unsafe_allow_html=True)

        elif response.is_success and not response.data:
            st.markdown("""
            <div class="section-header">
                <h3 style="margin: 0; color: #1e40af; font-size: 18px;">
                    👥 User Directory
                </h3>
                <p style="margin: 2px 0 0 0; color: #6b7280; font-size: 14px;">
                    0 users available • Get started by adding your first user
                </p>
            </div>
            """, unsafe_allow_html=True)

        else:
            error_msg = response.error or "Unknown error occurred"
            st.error(f"❌ Failed to load users: {error_msg}")

            if st.button("🔄 Retry", type="secondary"):
                st.rerun()

    except Exception as e:
        st.error(f"❌ Error loading users: {str(e)}")

        if st.button("🔄 Retry", type="secondary"):
            st.rerun()

# Help section
with st.expander("ℹ️ User Management Help"):
    st.markdown("""
    **User Management Features:**

    **👤 Add New Users:**
    - Create accounts with username, email, and personal details
    - Set secure passwords and birth dates
    - Assign multiple roles (GUEST, USER, ADMIN)

    **✏️ Edit User Details:**
    - Update user information and roles
    - Modify account settings and permissions
    - Reset passwords when needed

    **🗑️ Delete Users:**
    - Remove user accounts from the system
    - **Protection:** Cannot delete your own account or other admins
    - **Warning:** This action cannot be undone

    **🛡️ Role Management:**
    - **GUEST**: Basic access to public features
    - **USER**: Can take interviews and view content
    - **ADMIN**: Full system access and user management

    **💡 Best Practices:**
    - Use descriptive usernames that identify the person
    - Assign minimal required roles for security
    - Regularly review user accounts and permissions
    - Use strong passwords for all accounts
    """)