import streamlit as st

from pages.interview.interview_state_manager import get_interview_state


def render_answer_feedback(get_next_question, interview_service):
    """Render feedback after answer submission"""
    interview_state = get_interview_state()
    last_result = interview_state.get("last_answer_result", {})

    feedback_col, history_col = st.columns([2, 1])

    with feedback_col:
        render_feedback_content(last_result, interview_state, get_next_question, interview_service)

    with history_col:
        render_question_history_sidebar()


def render_feedback_content(last_result, interview_state, get_next_question, interview_service):
    """Render the main feedback content"""
    is_correct = last_result.get("isCorrect", last_result.get("correct", False))

    if isinstance(is_correct, str):
        is_correct = is_correct.lower() == "true"

    submitted_answer = last_result.get("submittedAnswer", "")
    correct_answer = last_result.get("correctAnswer", "")
    explanation = last_result.get("explanation", "")

    # Render feedback message
    if is_correct:
        st.markdown(f"""
        <div class="feedback-correct">
            <h4 style="margin-top: 0; color: #065f46;">
                ✅ Excellent! Correct Answer
            </h4>
            <p style="margin-bottom: 0;">
                You answered: <strong>{submitted_answer}</strong>
            </p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="feedback-incorrect">
            <h4 style="margin-top: 0; color: #991b1b;">
                ❌ Incorrect Answer
            </h4>
            <p style="margin-bottom: 8px;">
                You answered: <strong>{submitted_answer}</strong>
            </p>
            <p style="margin-bottom: 0;">
                💡 The correct answer was: <strong>{correct_answer}</strong>
            </p>
        </div>
        """, unsafe_allow_html=True)

    if explanation:
        with st.expander("📖 Detailed Explanation", expanded=True):
            st.markdown(explanation)

    render_statistics(interview_state)

    st.divider()

    render_next_question_button(interview_state, get_next_question, interview_service)


def render_statistics(interview_state):
    """Render performance statistics"""
    total_questions = len(interview_state["question_history"])
    correct_answers = sum(1 for q in interview_state["question_history"]
                          if q.get("is_correct", False) == True)
    accuracy = (correct_answers / total_questions * 100) if total_questions > 0 else 0

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Questions Answered", total_questions)
    with col2:
        st.metric("Correct Answers", correct_answers)
    with col3:
        st.metric("Accuracy", f"{accuracy:.1f}%")


def render_next_question_button(interview_state, get_next_question, interview_service):
    """Render the next question button"""
    next_question_key = f"next_question_btn_{len(interview_state['question_history'])}"
    if st.button("➡️ Next Question",
                 type="primary",
                 use_container_width=True,
                 help="Continue to the next question",
                 key=next_question_key):
        get_next_question(interview_service)


def render_question_history_sidebar():
    """Render compact question history for sidebar"""
    interview_state = get_interview_state()
    question_history = interview_state.get("question_history", [])

    if not question_history:
        st.info("📝 No questions answered yet")
        return

    st.markdown("### 📋 History")
    st.markdown(f"**{len(question_history)} answered**")

    reversed_history = list(reversed(question_history))

    for question in reversed_history:
        is_correct = question.get("is_correct", False)
        question_title = question.get("title", "Question")

        status_icon = "✅" if is_correct else "❌"
        status_text = "Correct" if is_correct else "Incorrect"
        status_color = "#10b981" if is_correct else "#ef4444"

        with st.container(border=True):
            st.markdown(f"""
            <div style="font-size: 14px;">
                <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 8px;">
                    <div style="flex: 1; margin-right: 8px;">
                        <strong>{question_title}</strong>
                    </div>
                    <div style="display: flex; flex-direction: column; align-items: center; min-width: 60px;">
                        <span style="color: {status_color}; font-size: 16px;">{status_icon}</span>
                        <span style="color: {status_color}; font-size: 11px; font-weight: bold;">{status_text}</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
