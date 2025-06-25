import streamlit as st

from api_client.services.interview_service import InterviewService
from custom_styles import interview_page_styles, history_page_styles

st.set_page_config(page_title="Interview History - QualifAIze", layout="wide", page_icon="📋")

st.markdown(interview_page_styles, unsafe_allow_html=True)

st.markdown(history_page_styles, unsafe_allow_html=True)

st.title("📋 Interview History")
st.markdown("*View your completed and scheduled interviews with detailed results*")

interview_service = InterviewService()

current_user = st.session_state.get('authenticated_user', {})
if not current_user:
    st.error("❌ You must be logged in to view interview history")
    st.info("Please sign in to access your interview history")
    st.stop()


def get_status_badge(status):
    """Get status badge HTML based on interview status"""
    status_classes = {
        'COMPLETED': 'status-completed',
        'SCHEDULED': 'status-scheduled',
        'IN_PROGRESS': 'status-in-progress',
        'CANCELLED': 'status-cancelled'
    }

    status_icons = {
        'COMPLETED': '✅',
        'SCHEDULED': '📅',
        'IN_PROGRESS': '🔄',
        'CANCELLED': '❌'
    }

    css_class = status_classes.get(status, 'status-scheduled')
    icon = status_icons.get(status, '❓')

    return f'<span class="{css_class}">{icon} {status.replace("_", " ").title()}</span>'


def get_difficulty_color(difficulty):
    """Get color for difficulty level"""
    colors = {
        'EASY': '#10b981',
        'MEDIUM': '#f59e0b',
        'HARD': '#ef4444'
    }
    return colors.get(difficulty, '#6b7280')


def format_duration(duration_seconds):
    """Format duration in seconds to human readable format"""
    if duration_seconds is None:
        return "N/A"

    minutes = duration_seconds // 60
    seconds = duration_seconds % 60

    if minutes > 0:
        return f"{minutes}m {seconds}s"
    else:
        return f"{seconds}s"


def calculate_performance_stats(questions):
    """Calculate performance statistics from questions"""
    if not questions:
        return {
            'total': 0,
            'answered': 0,
            'correct': 0,
            'accuracy': 0.0,
            'avg_time': 0
        }

    total = len(questions)
    answered = sum(1 for q in questions if q.get('submittedAnswer') is not None)
    correct = sum(1 for q in questions if q.get('isCorrect') is True)

    accuracy = (correct / answered * 100) if answered > 0 else 0.0

    answer_times = [q.get('answerTimeInMillis', 0) for q in questions
                    if q.get('answerTimeInMillis') is not None]
    avg_time = sum(answer_times) / len(answer_times) if answer_times else 0
    avg_time_seconds = avg_time / 1000 if avg_time > 0 else 0

    return {
        'total': total,
        'answered': answered,
        'correct': correct,
        'accuracy': accuracy,
        'avg_time': avg_time_seconds
    }


def render_question_details(questions):
    """Render detailed question information"""
    if not questions:
        st.info("📝 No questions found for this interview")
        return

    st.markdown("### 📚 Question Details")

    for i, question in enumerate(questions, 1):
        is_correct = question.get('isCorrect')
        submitted_answer = question.get('submittedAnswer')
        correct_answer = question.get('correctOption')

        if submitted_answer is None:
            status_class = "question-unanswered"
            status_icon = "⏳"
            status_text = "Not Answered"
        elif is_correct is True:
            status_class = "question-correct"
            status_icon = "✅"
            status_text = "Correct"
        else:
            status_class = "question-incorrect"
            status_icon = "❌"
            status_text = "Incorrect"

        with st.container():
            st.markdown(f"""
            <div class="question-item {status_class}">
                <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px;">
                    <div style="flex: 1;">
                        <strong>Question {question.get('questionOrder', i)}: {question.get('questionText', 'No question text')}</strong>
                    </div>
                    <div style="margin-left: 16px;">
                        <span style="font-weight: 600;">{status_icon} {status_text}</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)

            col1, col2 = st.columns(2)

            with col1:
                st.markdown(f"**A.** {question.get('optionA', 'N/A')}")
                st.markdown(f"**B.** {question.get('optionB', 'N/A')}")

            with col2:
                st.markdown(f"**C.** {question.get('optionC', 'N/A')}")
                st.markdown(f"**D.** {question.get('optionD', 'N/A')}")

            # Show answer details
            detail_col1, detail_col2, detail_col3 = st.columns(3)

            with detail_col1:
                if submitted_answer:
                    st.markdown(f"**Your Answer:** {submitted_answer}")
                else:
                    st.markdown("**Your Answer:** Not answered")

            with detail_col2:
                st.markdown(f"**Correct Answer:** {correct_answer}")

            with detail_col3:
                answer_time = question.get('answerTimeInMillis')
                if answer_time:
                    time_seconds = answer_time / 1000
                    st.markdown(f"**Time Taken:** {time_seconds:.1f}s")
                else:
                    st.markdown("**Time Taken:** N/A")

            st.markdown("</div>", unsafe_allow_html=True)

            if i < len(questions):
                st.divider()


def render_interview_summary(interview):
    """Render summary information for interview in expanded state"""
    created_by = interview.get('createdBy', {})
    created_by_name = f"{created_by.get('firstName', '')} {created_by.get('lastName', '')}".strip()
    if not created_by_name:
        created_by_name = created_by.get('username', 'Unknown')

    difficulty = interview.get('difficulty', 'MEDIUM')
    difficulty_color = get_difficulty_color(difficulty)

    stats = calculate_performance_stats(interview.get('questions', []))

    st.markdown(f"""
    <div class="interview-summary">
        <div style="display: flex; justify-content: space-between; align-items: center; font-size: 14px; color: #6b7280;">
            <div>
                <span style="font-size: 16px; font-weight: 600;">{interview.get('name', 'Unnamed Interview')}</span>
                {get_status_badge(interview.get('status', 'UNKNOWN'))}
            </div>
            <div>
                👤 Created by: <strong>{created_by_name}</strong>
            </div>
            <div>
                📄 Document: <strong>{interview.get('documentTitle', 'Unknown')}</strong>
            </div>
            <div>
                📊 {stats['correct']}/{stats['answered']} correct {f" ({stats['accuracy']:.1f}%)" if stats['answered'] > 0 else ""}
            </div>
            <div style="text-align: right;">
                <span style="color: {difficulty_color}; font-weight: 600; font-size: 14px;">
                    ⚡ {difficulty}
                </span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


with st.spinner("Loading interview history..."):
    try:
        response = interview_service.get_assigned_interviews()

        if response.is_success and response.data:
            detailed_response = interview_service.get_interviews_with_questions()

            if detailed_response.is_success and detailed_response.data:
                all_interviews = detailed_response.data
                filtered_interviews = [
                    interview for interview in all_interviews
                    if interview.get('status') in ['COMPLETED', 'CANCELLED']
                ]

                interviews = filtered_interviews

                st.markdown(f"""
                <div style="
                    background: rgba(59, 130, 246, 0.08);
                    border-left: 3px solid #3b82f6;
                    border-radius: 0 4px 4px 0;
                    padding: 12px 16px;
                    margin: 16px 0;
                ">
                    <h3 style="margin: 0; color: #1e40af; font-size: 18px;">
                        📊 Interview History Overview
                    </h3>
                    <p style="margin: 4px 0 0 0; color: #6b7280; font-size: 14px;">
                        You have {len(interviews)} interview(s) in your history
                    </p>
                </div>
                """, unsafe_allow_html=True)


                def sort_key(interview):
                    status_priority = {
                        'COMPLETED': 0,
                        'IN_PROGRESS': 1,
                        'SCHEDULED': 2,
                        'CANCELLED': 3
                    }
                    return status_priority.get(interview.get('status', 'UNKNOWN'), 4), interview.get('name', '')


                sorted_interviews = sorted(interviews, key=sort_key)

                for interview in sorted_interviews:
                    interview_name = interview.get('name', 'Unnamed Interview')
                    status = interview.get('status', 'UNKNOWN')

                    with st.expander(
                            f"{interview_name} ({status.replace('_', ' ').title()})",
                            expanded=False
                    ):
                        render_interview_summary(interview)

                        st.divider()

                        detail_col1, detail_col2 = st.columns(2)

                        with detail_col1:
                            st.markdown("### 📝 Interview Information")

                            description = interview.get('description', 'No description provided')
                            st.markdown(f"**Description:** {description}")

                            created_by = interview.get('createdBy', {})
                            created_by_name = f"{created_by.get('firstName', '')} {created_by.get('lastName', '')}".strip()
                            if not created_by_name:
                                created_by_name = created_by.get('username', 'Unknown')
                            st.markdown(f"**Created by:** {created_by_name}")

                            document_title = interview.get('documentTitle', 'Unknown Document')
                            st.markdown(f"**Based on:** {document_title}")

                        with detail_col2:
                            st.markdown("### 📊 Performance Metrics")

                            stats = calculate_performance_stats(interview.get('questions', []))

                            metric_col1, metric_col2 = st.columns(2)

                            with metric_col1:
                                st.markdown(f"""
                                <div class="metric-card">
                                    <div style="font-size: 24px; font-weight: 700; color: #3b82f6;">
                                        {stats['total']}
                                    </div>
                                    <div style="font-size: 14px; color: #6b7280;">
                                        Total Questions
                                    </div>
                                </div>
                                """, unsafe_allow_html=True)

                                if stats['answered'] > 0:
                                    st.markdown(f"""
                                    <div class="metric-card" style="margin-top: 8px;">
                                        <div style="font-size: 24px; font-weight: 700; color: #10b981;">
                                            {stats['accuracy']:.1f}%
                                        </div>
                                        <div style="font-size: 14px; color: #6b7280;">
                                            Accuracy
                                        </div>
                                    </div>
                                    """, unsafe_allow_html=True)

                            with metric_col2:
                                st.markdown(f"""
                                <div class="metric-card">
                                    <div style="font-size: 24px; font-weight: 700; color: #f59e0b;">
                                        {stats['answered']}/{stats['total']}
                                    </div>
                                    <div style="font-size: 14px; color: #6b7280;">
                                        Answered
                                    </div>
                                </div>
                                """, unsafe_allow_html=True)

                                duration = interview.get('durationInSeconds')
                                if duration:
                                    st.markdown(f"""
                                    <div class="metric-card" style="margin-top: 8px;">
                                        <div style="font-size: 24px; font-weight: 700; color: #8b5cf6;">
                                            {format_duration(duration)}
                                        </div>
                                        <div style="font-size: 14px; color: #6b7280;">
                                            Duration
                                        </div>
                                    </div>
                                    """, unsafe_allow_html=True)

                        if interview.get('questions'):
                            st.divider()
                            render_question_details(interview.get('questions', []))

                        st.divider()
                        st.markdown("### 💬 Feedback")

                        candidate_review = interview.get('candidateReview')

                        if candidate_review and candidate_review.strip():
                            with st.expander("📝 Your review is ready! (click to see it)", expanded=False):
                                with st.container(border=True):
                                    st.markdown(candidate_review)
                        else:
                            st.markdown(f"""
                            <div class="feedback-section feedback-pending">
                                <h4 style="margin-top: 0; color: #d97706;">
                                    ⏳ Feedback Pending
                                </h4>
                                <p style="margin: 8px 0 0 0; color: #92400e;">
                                    Your feedback is not ready yet. Please check back later or contact the interview creator.
                                </p>
                            </div>
                            """, unsafe_allow_html=True)

            else:
                error_msg = detailed_response.error or "Failed to load detailed interview data"
                st.error(f"❌ {error_msg}")

        elif response.is_success and not response.data:
            st.markdown("""
            <div style="text-align: center; padding: 60px 20px;">
                <div style="font-size: 64px; margin-bottom: 20px;">📭</div>
                <h3 style="color: #6b7280; margin-bottom: 16px;">No Interview History</h3>
                <p style="color: #9ca3af; font-size: 16px;">
                    You haven't taken any interviews yet.<br>
                    Check the Interview page to see if there are any assigned to you.
                </p>
            </div>
            """, unsafe_allow_html=True)

        else:
            error_msg = response.error or "Unknown error occurred"
            st.error(f"❌ Failed to load interview history: {error_msg}")

            if st.button("🔄 Retry", type="secondary"):
                st.rerun()

    except Exception as e:
        st.error(f"❌ Error loading interview history: {str(e)}")

        if st.button("🔄 Retry", type="secondary"):
            st.rerun()

# Help section
with st.expander("ℹ️ Interview History Help"):
    st.markdown("""
    **What's shown here:**
    - Only **completed** and **cancelled** interviews
    - For scheduled interviews, go to the **Interview page**

    **Status indicators:**
    - **✅ Completed:** Interview finished and submitted
    - **❌ Cancelled:** Interview was cancelled

    **Performance metrics:**
    - **Total Questions:** Number of questions in the interview
    - **Accuracy:** Percentage of correct answers
    - **Duration:** Time taken to complete

    **Feedback:**
    - Provided by interview creators for completed interviews
    - Check back periodically for updates

    **Tips:**
    - Review incorrect answers to improve
    - Compare performance across interviews
    - Check Interview page for new assignments
    """)
