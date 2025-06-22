from datetime import datetime

import streamlit as st

from pages.auth.sign_in import decode_jwt


def format_role_badge(role: str) -> str:
    """Format role as a colored badge"""
    color_map = {
        "ADMIN": "#FF4B4B",
        "USER": "#1F77B4",
        "GUEST": "#28A745"
    }
    color = color_map.get(role, "#6C757D")
    return f'<span style="background-color: {color}; color: white; padding: 4px 8px; border-radius: 12px; font-size: 12px; font-weight: bold; margin-right: 5px;">{role}</span>'


# Custom CSS for account details page
st.markdown("""
<style>
.account-header {
    background: linear-gradient(135deg, #FF4B4B, #FF6B6B);
    color: white;
    padding: 20px;
    border-radius: 10px;
    margin-bottom: 20px;
    text-align: center;
}
.account-header h1 {
    margin: 0;
    font-size: 2rem;
}
.account-header p {
    margin: 5px 0 0 0;
    opacity: 0.9;
}
.metric-card {
    background: #f8f9fa;
    padding: 15px;
    border-radius: 8px;
    border-left: 4px solid #FF4B4B;
    margin: 10px 0;
}
.security-status {
    background: #e8f5e8;
    border: 1px solid #28a745;
    border-radius: 8px;
    padding: 10px;
    margin: 5px 0;
}
</style>
""", unsafe_allow_html=True)

# Check if user is authenticated
if not st.session_state.authenticated_user:
    st.error("❌ You must be logged in to view account details")
    st.info("Please sign in to access your account information")
    st.stop()

# Get user data from session
logged_user = st.session_state.authenticated_user
user_data = decode_jwt(logged_user.get("token", ""))

# Header section
username = logged_user.get("username", "Unknown User")
roles = logged_user.get("roles", [])

st.markdown(f"""
<div class="account-header">
    <h1>👤 Account Details</h1>
    <p>Welcome back, <strong>{username}</strong>!</p>
</div>
""", unsafe_allow_html=True)

# User overview section
st.subheader("📋 Account Overview")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <h3>Username</h3>
        <p style="font-size: 1.2rem; font-weight: bold; color: #FF4B4B;">{username}</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    roles_html = "".join([format_role_badge(role) for role in roles])
    st.markdown(f"""
    <div class="metric-card">
        <h3>Roles</h3>
        <p>{roles_html}</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    account_type = "Administrator" if "ADMIN" in roles else "Standard User" if "USER" in roles else "Guest"
    st.markdown(f"""
    <div class="metric-card">
        <h3>Account Type</h3>
        <p style="font-size: 1.2rem; font-weight: bold; color: #28A745;">{account_type}</p>
    </div>
    """, unsafe_allow_html=True)

# Create tabs for different sections
tab1, tab2, tab3, tab4 = st.tabs(["🔐 Security", "👥 Permissions", "⚙️ Actions", "ℹ️ System"])

with tab1:
    st.subheader("🔐 Security & Session Information")

    col1, col2 = st.columns(2)

    with col1:
        st.write("**Session Details:**")
        st.write(f"• **Token Issued:** {user_data.get('issued_at', 'Unknown').strftime('%Y-%m-%d %H:%M:%S')}")
        st.write(f"• **Token Expires:** {user_data.get('expires_at', 'Unknown').strftime('%Y-%m-%d %H:%M:%S')}")

        # Calculate time remaining
        expires_at = user_data.get('expires_at')
        if expires_at:
            time_remaining = expires_at - datetime.now()
            if time_remaining.total_seconds() > 0:
                hours_remaining = int(time_remaining.total_seconds() // 3600)
                minutes_remaining = int((time_remaining.total_seconds() % 3600) // 60)
                st.write(f"• **Time Remaining:** {hours_remaining}h {minutes_remaining}m")
            else:
                st.error("⚠️ Token has expired!")

    with col2:
        st.markdown("""
        <div class="security-status">
            <h4>Security Status</h4>
            <p>✅ Session Active</p>
            <p>✅ JWT Token Valid</p>
            <p>✅ Secure Connection</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("🔄 Refresh Session", help="Extend your session"):
            st.info("Session refresh would be implemented here")

with tab2:
    st.subheader("👥 Permissions & Access Levels")

    # Define permissions for each role
    role_permissions = {
        "ADMIN": [
            "Full system administration",
            "User management",
            "Document management",
            "Interview creation and management",
            "System configuration",
            "View all analytics and reports"
        ],
        "USER": [
            "Create and participate in interviews",
            "Upload and manage personal documents",
            "View interview history",
            "Access personal analytics"
        ],
        "GUEST": [
            "Limited system access",
            "View public content",
            "Basic profile management"
        ]
    }

    for role in roles:
        with st.expander(f"{format_role_badge(role)} {role} Permissions", expanded=True):
            permissions = role_permissions.get(role, ["No specific permissions defined"])
            for permission in permissions:
                st.write(f"✓ {permission}")

with tab3:
    st.subheader("⚙️ Account Actions")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🔑 Change Password", use_container_width=True):
            st.info("Password change functionality would be implemented here")

    with col2:
        if st.button("📧 Update Email", use_container_width=True):
            st.info("Email update functionality would be implemented here")

    with col3:
        if st.button("🗑️ Delete Account", use_container_width=True, type="secondary"):
            st.warning("Account deletion would require confirmation")

with tab4:
    st.subheader("ℹ️ System Information")

    col1, col2 = st.columns(2)

    with col1:
        st.write("**Application Details:**")
        st.write("• **Platform:** QualifAIze Interview System")
        st.write("• **Version:** 1.0.0")
        st.write("• **Backend:** Spring Boot + PostgreSQL")
        st.write("• **Frontend:** Streamlit")

    with col2:
        st.write("**Technical Stack:**")
        st.write("• **Authentication:** JWT")
        st.write("• **API:** RESTful")
        st.write("• **AI Integration:** OpenAI & Mistral")
        st.write("• **Security:** Role-based Access Control")

# Footer with helpful information
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; font-size: 0.9rem;">
    <p>🛡️ Your account is secured with JWT authentication and role-based access control.</p>
    <p>For support, contact: <a href="mailto:support@qualifaize.com">support@qualifaize.com</a></p>
</div>
""", unsafe_allow_html=True)