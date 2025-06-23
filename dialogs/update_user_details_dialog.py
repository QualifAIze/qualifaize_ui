import streamlit as st
from datetime import datetime, date


def update_user_dialog(current_user_data, user_service):
    """Dialog for updating user details"""

    st.markdown("### 📝 Update Your Information")
    st.markdown("*Modify your account details below. Only fill in the fields you want to update.*")

    with st.form("update_user_form", clear_on_submit=False):

        st.markdown("#### 👤 Basic Information")
        col1, col2 = st.columns(2)

        with col1:
            new_username = st.text_input(
                "Username",
                value=current_user_data.get('username', ''),
                placeholder="Enter new username",
                help="Username can't be changed! Contact support if you really need it.",
                disabled=True
            )

            new_first_name = st.text_input(
                "First Name",
                value=current_user_data.get('firstName', '') or '',
                placeholder="Enter your first name"
            )

        with col2:
            new_email = st.text_input(
                "Email",
                value=current_user_data.get('email', '') or '',
                placeholder="Enter your email address",
                help="Must be a valid email address"
            )

            new_last_name = st.text_input(
                "Last Name",
                value=current_user_data.get('lastName', '') or '',
                placeholder="Enter your last name"
            )

        st.markdown("#### 📅 Personal Information")

        current_birth_date = None
        if current_user_data.get('birthDate'):
            try:
                birth_date_str = current_user_data['birthDate']
                if birth_date_str.endswith('Z'):
                    birth_date_str = birth_date_str[:-1] + '+00:00'
                birth_datetime = datetime.fromisoformat(birth_date_str)
                current_birth_date = birth_datetime.date()
            except (ValueError, TypeError) as e:
                st.warning(f"Could not parse current birth date: {e}")

        new_birth_date = st.date_input(
            "Birth Date",
            value=current_birth_date,
            min_value=date(1900, 1, 1),
            max_value=date.today(),
            help="Select your date of birth"
        )

        st.divider()
        col1, col2 = st.columns([1, 1])

        with col1:
            cancel_button = st.form_submit_button(
                "❌ Cancel",
                use_container_width=True,
                type="secondary"
            )

        with col2:
            update_button = st.form_submit_button(
                "💾 Update Details",
                use_container_width=True,
                type="primary"
            )

        if cancel_button:
            st.rerun()

        if update_button:
            with st.spinner("Updating your details..."):
                try:
                    current_user = st.session_state.get('authenticated_user', {})
                    user_id = current_user.get('user_id')

                    response = user_service.update_user_details(user_id, new_username, new_email, new_first_name, new_last_name, new_birth_date.strftime('%Y-%m-%dT00:00:00Z'))

                    if response.is_success:
                        st.success("✅ Your details have been updated successfully!")
                        st.session_state.authenticated_user['username'] = new_username
                        st.rerun()
                    else:
                        error_msg = response.error or "Unknown error occurred"
                        st.error(f"❌ Failed to update details: {error_msg}")

                except Exception as e:
                    st.error(f"❌ Error updating details: {str(e)}")
