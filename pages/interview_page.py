import streamlit as st
from api_client.services.interview_service import InterviewService
from datetime import datetime
import constants
from dialogs.assign_interview_dialog import assign_interview_dialog

interview_service = InterviewService()

current_user = st.session_state.get('authenticated_user', {})
user_roles = current_user.get('roles', [])
is_admin = constants.ROLE_ADMIN in user_roles


@st.dialog("Assign New Interview", width="large")
def show_assign_dialog():
    assign_interview_dialog()


if is_admin:
    if st.button("🎯 Assign New Interview", type="primary", icon="🚀", use_container_width=True):
        show_assign_dialog()

current_logged_user_assigned_interviews = interview_service.get_assigned_interviews(status="SCHEDULED")

if current_logged_user_assigned_interviews.data and len(current_logged_user_assigned_interviews.data) > 0:
    interview_container = st.container(border=True)

    with interview_container:
        st.markdown("### 🎯 **Assigned Interviews**")

        for interview in current_logged_user_assigned_interviews.data:

            status_color = {
                'SCHEDULED': '🟡',
                'IN_PROGRESS': '🟢',
                'COMPLETED': '🔵',
                'CANCELLED': '🔴'
            }.get(interview.get('status', 'UNKNOWN'), '⚪')

            st.markdown(
                f"**{interview.get('name', 'Unnamed Interview')}** {status_color} {interview.get('status', 'UNKNOWN')}")

            st.markdown(f"👤 **Created by:** {interview.get('createdBy', 'Unknown')}")
            st.markdown(f"📋 **Description:** {interview.get('description', 'No description available')}")
            st.markdown(f"⚡ **Difficulty:** {interview.get('difficulty', 'MEDIUM')}")

            if interview.get('scheduledDate'):
                try:
                    scheduled_dt = datetime.fromisoformat(interview['scheduledDate'].replace('Z', '+00:00'))
                    formatted_date = scheduled_dt.strftime("%B %d, %Y at %I:%M %p UTC")
                    st.markdown(f"📅 **Scheduled:** {formatted_date}")
                except (ValueError, TypeError):
                    st.markdown(f"📅 **Scheduled:** {interview['scheduledDate']}")

            interview_id = interview.get('interviewId')
            status = interview.get('status', '')

            if st.button("📝 Start Interview",
                         key=f"start_{interview_id}",
                         type="primary",
                         use_container_width=True):
                response = interview_service.change_interview_status(interview_id, "IN_PROGRESS")
                if response.is_success:
                    st.success("Interview started successfully!")
                    st.rerun()
                else:
                    st.error("Failed to start interview")

            if len(current_logged_user_assigned_interviews.data) > 1:
                st.divider()
else:
    if not is_admin:
        st.info("📋 No interviews currently assigned to you.")
    else:
        st.info("📋 No interviews currently assigned. Click 'Assign New Interview' to create one.")
