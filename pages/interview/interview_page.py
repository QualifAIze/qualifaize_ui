import streamlit as st
from datetime import datetime
import constants
from api_client.services.interview_service import InterviewService
from custom_styles import interview_page_styles
from dialogs.interview_page_dialogs import assign_interview_dialog
from pages.interview.interview_actions import start_interview, submit_answer, get_next_question, cancel_interview
from pages.interview.interview_components import render_answer_feedback
from pages.interview.interview_state_manager import get_interview_state, initialize_interview_state, \
    reset_interview_state

st.set_page_config(page_title="Interview - QualifAIze", layout="wide", page_icon="🎯")

st.markdown(interview_page_styles, unsafe_allow_html=True)

interview_service = InterviewService()

current_user = st.session_state.get('authenticated_user', {})
user_roles = current_user.get('roles', [])
is_admin = constants.ROLE_ADMIN in user_roles

initialize_interview_state()


@st.dialog("Assign New Interview", width="large")
def show_assign_dialog():
    assign_interview_dialog()


def render_interview_view():
    """Render the active interview interface"""
    interview_state = get_interview_state()

    st.markdown(f"""
    <div class="interview-header">
        <div style="font-size: 24px; font-weight: 700; margin-bottom: 8px;">
            🎯 {interview_state["interview_name"]}
        </div>
        <div style="font-size: 16px; opacity: 0.9;">
            AI-Powered Technical Interview
        </div>
    </div>
    """, unsafe_allow_html=True)

    progress = interview_state["progress"]
    progress_col1, progress_col2 = st.columns([4, 1])

    with progress_col1:
        st.progress(progress / 100, text=f"Progress: {progress}%")

    with progress_col2:
        if st.button("❌ Quit",
                     type="secondary",
                     use_container_width=True,
                     help="Quit interview",
                     key="quit_interview_btn"):
            cancel_interview(interview_service)
            st.rerun()

    st.divider()

    current_question = interview_state["current_question"]

    if current_question is None:
        st.info("🔄 Loading question...")
        return

    if interview_state["is_waiting_for_next"]:
        render_answer_feedback(get_next_question, interview_service)
    else:
        render_current_question(current_question)


def render_current_question(current_question):
    """Render the current question interface"""
    interview_state = get_interview_state()

    question_number = len(interview_state["question_history"]) + 1
    st.markdown(f"""
    <div class="question-counter">
        📝 Question {question_number}
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="question-card">
        <h3 style="margin-top: 0; color: #1f2937; font-size: 20px;">
            {current_question['title']}
        </h3>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("#### Choose your answer:")

    options = {
        "A": current_question['optionA'],
        "B": current_question['optionB'],
        "C": current_question['optionC'],
        "D": current_question['optionD']
    }

    selected_option = st.radio(
        "Select one:",
        options=list(options.keys()),
        format_func=lambda x: f"**{x}.** {options[x]}",
        key=f"question_{current_question['questionId']}_radio",
        help="Choose the best answer from the options below"
    )

    st.session_state.current_interview_state["selected_answer"] = selected_option

    st.divider()

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("📤 Submit Answer",
                     type="primary",
                     use_container_width=True,
                     disabled=selected_option is None,
                     help="Submit your selected answer",
                     key=f"submit_answer_{current_question['questionId']}_btn"):
            submit_answer(interview_service, current_question['questionId'], selected_option)


def render_normal_view():
    """Render the normal interview assignment view"""

    if is_admin:
        if st.button("🎯 Assign New Interview",
                     type="primary",
                     icon="🚀",
                     use_container_width=True,
                     key="assign_new_interview_btn"):
            show_assign_dialog()
        st.divider()

    try:
        assigned_interviews_response = interview_service.get_assigned_interviews(status="SCHEDULED")
    except Exception as e:
        st.error(f"Error loading interviews: {str(e)}")
        return

    if assigned_interviews_response.is_success and assigned_interviews_response.data and len(
            assigned_interviews_response.data) > 0:
        st.markdown("""
        <div class="interview-container">
            <h3 style="margin-top: 0; color: #1f2937;">
                🎯 Assigned Interviews
            </h3>
            <p style="color: #6b7280; margin-bottom: 20px;">
                Select an interview to begin your assessment
            </p>
        </div>
        """, unsafe_allow_html=True)

        for interview in assigned_interviews_response.data:
            render_interview_card(interview)
    else:
        render_empty_state()


def render_interview_card(interview):
    """Render individual interview card"""
    with st.container(border=True):
        status = interview.get('status', 'UNKNOWN')
        status_colors = {
            'SCHEDULED': ('🟡', '#f59e0b', 'Scheduled'),
            'IN_PROGRESS': ('🟢', '#10b981', 'In Progress'),
            'COMPLETED': ('🔵', '#3b82f6', 'Completed'),
            'CANCELLED': ('🔴', '#ef4444', 'Cancelled')
        }

        status_emoji, status_color, status_text = status_colors.get(status, ('⚪', '#6b7280', status))

        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"### {interview.get('name', 'Unnamed Interview')}")
        with col2:
            st.markdown(f"""
            <div class="status-badge" style="
                background: rgba(59, 130, 246, 0.1);
                color: {status_color};
            ">
                {status_emoji} {status_text}
            </div>
            """, unsafe_allow_html=True)

        detail_row1_col1, detail_row1_col2 = st.columns(2)
        with detail_row1_col1:
            st.markdown(f"👤 **Created by:** {interview.get('createdBy', 'Unknown')}")
        with detail_row1_col2:
            if interview.get('scheduledDate'):
                try:
                    scheduled_dt = datetime.fromisoformat(interview['scheduledDate'].replace('Z', '+00:00'))
                    formatted_date = scheduled_dt.strftime("%B %d, %Y at %I:%M %p UTC")
                    st.markdown(f"📅 **Scheduled:** {formatted_date}")
                except (ValueError, TypeError):
                    st.markdown(f"📅 **Scheduled:** {interview['scheduledDate']}")

        detail_row2_col1, detail_row2_col2 = st.columns(2)
        with detail_row2_col1:
            if interview.get('description'):
                st.markdown(f"📋 **Description:** {interview.get('description', 'No description available')}")
        with detail_row2_col2:
            st.markdown(f"⚡ **Difficulty:** {interview.get('difficulty', 'MEDIUM')}")

        st.divider()

        interview_id = interview.get('interviewId')
        interview_name = interview.get('name', 'Unnamed Interview')

        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            start_button_key = f"start_interview_{interview_id}_btn"
            if st.button(f"🚀 Start Interview: {interview_name}",
                         key=start_button_key,
                         type="primary",
                         use_container_width=True,
                         help=f"Begin the {interview.get('difficulty', 'MEDIUM').lower()} difficulty interview"):
                start_interview(interview_service, interview_id, interview_name)

        st.divider()


def render_empty_state():
    """Render empty state when no interviews available"""
    st.markdown("""
    <div class="interview-container" style="text-align: center; padding: 40px;">
        <div style="font-size: 48px; margin-bottom: 16px;">📭</div>
        <h3 style="color: #6b7280; margin-bottom: 8px;">No Interviews Available</h3>
    """, unsafe_allow_html=True)

    if not is_admin:
        st.markdown("""
        <p style="color: #9ca3af;">
            You don't have any interviews assigned at the moment.<br>
            Check back later or contact your administrator.
        </p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <p style="color: #9ca3af;">
            No interviews have been assigned yet.<br>
            Click 'Assign New Interview' above to create one.
        </p>
        </div>
        """, unsafe_allow_html=True)


if st.session_state.current_interview_state["is_active"]:
    render_interview_view()
else:
    render_normal_view()
