import time
from datetime import date, datetime

import streamlit as st


def add_new_user_dialog(user_service):
    """Dialog for adding new users"""

    st.markdown("*Create a new user account in the system*")

    # User basic information
    st.markdown("#### 👤 Basic Information")
    col1, col2 = st.columns(2)

    with col1:
        username = st.text_input(
            "Username *",
            placeholder="Enter unique username",
            help="Username must be unique in the system"
        )

        first_name = st.text_input(
            "First Name *",
            placeholder="Enter first name"
        )

    with col2:
        email = st.text_input(
            "Email *",
            placeholder="Enter email address",
            help="Must be a valid email address"
        )

        last_name = st.text_input(
            "Last Name *",
            placeholder="Enter last name"
        )

    # Password and birth date
    st.markdown("#### 🔐 Account Details")
    col1, col2 = st.columns(2)

    with col1:
        password = st.text_input(
            "Password *",
            type="password",
            placeholder="Enter secure password",
            help="Choose a strong password"
        )

    with col2:
        birth_date = st.date_input(
            "Birth Date *",
            value=None,
            min_value=date(1900, 1, 1),
            max_value=date.today(),
            help="Select date of birth"
        )

    # Role selection
    st.markdown("#### 🏷️ User Roles")
    roles = st.multiselect(
        "Assign Roles",
        options=["GUEST", "USER", "ADMIN"],
        default=["GUEST"],
        help="Select one or more roles for the user"
    )

    # Action buttons
    st.markdown("---")
    col1, col2 = st.columns([1, 1])

    with col1:
        if st.button("❌ Cancel", use_container_width=True):
            st.rerun()

    with col2:
        create_disabled = not (username and username.strip() and
                               email and email.strip() and
                               first_name and first_name.strip() and
                               last_name and last_name.strip() and
                               password and password.strip() and
                               birth_date and roles)

        if st.button(
                "🚀 Create User",
                type="primary",
                use_container_width=True,
                disabled=create_disabled
        ):
            if not all([username, email, first_name, last_name, password, birth_date]):
                st.error("❌ Please fill in all required fields")
            else:
                # Create user
                with st.spinner("Creating user account..."):
                    try:
                        birth_date_str = birth_date.strftime('%Y-%m-%dT00:00:00Z')

                        response = user_service.register(
                            username=username.strip(),
                            password=password.strip(),
                            email=email.strip(),
                            first_name=first_name.strip(),
                            last_name=last_name.strip(),
                            birth_date=birth_date_str,
                            roles=roles
                        )

                        if response.is_success:
                            st.success(f"✅ User '{username}' created successfully!")
                            st.info("🔄 The page will refresh to show the new user...")
                            time.sleep(2)
                            st.rerun()
                        else:
                            error_msg = response.error or "Unknown error occurred"
                            st.error(f"❌ User creation failed: {error_msg}")

                    except Exception as e:
                        st.error(f"❌ Error creating user: {str(e)}")

def edit_user_dialog(user_id, current_user_data, user_service):
    """Dialog for editing user details"""

    st.markdown(f"*Edit details for user: **{current_user_data.get('username', 'Unknown')}***")

    st.markdown("#### 👤 Basic Information")
    col1, col2 = st.columns(2)

    with col1:
        new_username = st.text_input(
            "Username",
            value=current_user_data.get('username', ''),
            placeholder="Enter username",
            help="Username must be unique in the system"
        )

        new_first_name = st.text_input(
            "First Name",
            value=current_user_data.get('firstName', '') or '',
            placeholder="Enter first name"
        )

    with col2:
        new_email = st.text_input(
            "Email",
            value=current_user_data.get('email', '') or '',
            placeholder="Enter email address",
            help="Must be a valid email address"
        )

        new_last_name = st.text_input(
            "Last Name",
            value=current_user_data.get('lastName', '') or '',
            placeholder="Enter last name"
        )

    # Birth date and role management
    col1, col2 = st.columns(2)

    with col1:
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
            help="Select date of birth"
        )

    with col2:
        st.markdown("#### 🛡️ Role Management")

        current_roles = current_user_data.get('roles', ['GUEST'])
        current_user_session = st.session_state.get('authenticated_user', {})
        current_user_id = current_user_session.get('user_id')

        # Determine highest current role
        role_hierarchy = {"GUEST": 0, "USER": 1, "ADMIN": 2}
        highest_role = max(current_roles, key=lambda x: role_hierarchy.get(x, 0))

        # Role promotion options
        role_options = ["GUEST", "USER", "ADMIN"]
        current_role_index = role_options.index(highest_role) if highest_role in role_options else 0

        # Prevent demoting yourself or promoting others to admin unless you're admin
        is_self = str(user_id) == str(current_user_id)
        current_user_roles = current_user_session.get('roles', [])
        is_current_admin = 'ADMIN' in current_user_roles

        if is_self and highest_role == "ADMIN":
            st.info("🔒 You cannot change your own admin role")
            new_role = highest_role
        elif not is_current_admin and "ADMIN" in role_options:
            # Remove ADMIN option for non-admin users
            available_options = ["GUEST", "USER"]
            if highest_role == "ADMIN":
                st.info("🔒 Only admins can manage admin roles")
                new_role = highest_role
            else:
                new_role = st.selectbox(
                    "Primary Role",
                    options=available_options,
                    index=available_options.index(highest_role) if highest_role in available_options else 0,
                    help="Select the primary role for this user"
                )
        else:
            new_role = st.selectbox(
                "Primary Role",
                options=role_options,
                index=current_role_index,
                help="Select the primary role for this user"
            )

        # Show current roles
        if current_roles:
            roles_str = ", ".join(current_roles)
            st.markdown(f"**Current roles:** {roles_str}")

    # Action buttons
    st.markdown("---")
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("❌ Cancel", use_container_width=True):
            st.rerun()

    with col2:
        # Update details button
        if st.button(
                "💾 Update Details",
                type="secondary",
                use_container_width=True
        ):
            # Update user details (without role change)
            with st.spinner("Updating user details..."):
                try:
                    birth_date_str = new_birth_date.strftime('%Y-%m-%dT00:00:00Z') if new_birth_date else None

                    response = user_service.update_user_details(
                        user_id=user_id,
                        username=new_username.strip() if new_username else None,
                        email=new_email.strip() if new_email else None,
                        first_name=new_first_name.strip() if new_first_name else None,
                        last_name=new_last_name.strip() if new_last_name else None,
                        birth_date=birth_date_str
                    )

                    if response.is_success:
                        st.success(f"✅ User details updated successfully!")
                        time.sleep(1)
                        st.rerun()
                    else:
                        error_msg = response.error or "Unknown error occurred"
                        st.error(f"❌ Update failed: {error_msg}")

                except Exception as e:
                    st.error(f"❌ Error updating user: {str(e)}")

    with col3:
        # Promote/change role button
        role_changed = new_role != highest_role
        promote_disabled = not role_changed or (is_self and highest_role == "ADMIN")

        if st.button(
                f"🔄 Change to {new_role}",
                type="primary",
                use_container_width=True,
                disabled=promote_disabled,
                help="Change user role" if not promote_disabled else "Cannot change role"
        ):
            # Promote/change user role
            with st.spinner(f"Changing role to {new_role}..."):
                try:
                    response = user_service.promote_user(user_id, new_role)

                    if response.is_success:
                        st.success(f"✅ User role changed to {new_role} successfully!")
                        time.sleep(1)
                        st.rerun()
                    else:
                        error_msg = response.error or "Unknown error occurred"
                        st.error(f"❌ Role change failed: {error_msg}")

                except Exception as e:
                    st.error(f"❌ Error changing role: {str(e)}")