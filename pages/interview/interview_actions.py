import streamlit as st

from dialogs.interview_page_dialogs import completion_dialog
from pages.interview.interview_state_manager import set_interview_active, get_interview_state, set_current_question, \
    add_question_to_history, update_progress, set_answer_feedback, reset_interview_state


@st.dialog("🎉 Interview Completed!", width="large")
def show_completion_dialog(total_questions, correct_answers, accuracy):
    completion_dialog(total_questions, correct_answers, accuracy)

def start_interview(interview_service, interview_id, interview_name):
    """Start an interview and change status to IN_PROGRESS"""
    with st.spinner("Starting interview..."):
        try:
            # Change interview status to IN_PROGRESS
            response = interview_service.change_interview_status(interview_id, "IN_PROGRESS")
            if response.is_success:
                # Initialize interview state
                set_interview_active(interview_id, interview_name)

                # Get first question
                get_next_question(interview_service)
                st.success("Interview started successfully!")
                st.rerun()
            else:
                st.error(f"Failed to start interview: {response.error}")
        except Exception as e:
            st.error(f"Error starting interview: {str(e)}")


def get_next_question(interview_service):
    """Fetch the next question from the API"""
    interview_state = get_interview_state()
    interview_id = interview_state["interview_id"]

    with st.spinner("Loading next question..."):
        try:
            response = interview_service.get_next_question(interview_id)
            if response.is_success:
                question_data = response.data
                set_current_question(question_data)
                st.rerun()
            else:
                st.error(f"Failed to load question: {response.error}")
                # If no more questions, complete the interview
                if "no more questions" in str(response.error).lower():
                    complete_interview(interview_service)
        except Exception as e:
            st.error(f"Error loading question: {str(e)}")


def submit_answer(interview_service, question_id, selected_answer):
    """Submit the selected answer"""
    with st.spinner("Submitting answer..."):
        try:
            response = interview_service.submit_answer(question_id, selected_answer)
            if response.is_success:
                answer_data = response.data

                # Add to history
                interview_state = get_interview_state()
                question_info = interview_state["current_question"].copy()
                question_info["submitted_answer"] = selected_answer
                # Fix: Handle both possible field names
                question_info["is_correct"] = answer_data.get("isCorrect", answer_data.get("correct", False))
                question_info["correct_answer"] = answer_data.get("correctAnswer", "")
                question_info["explanation"] = answer_data.get("explanation", "")

                add_question_to_history(question_info)

                # Update progress
                progress = answer_data.get("currentProgress", 0)
                update_progress(progress)

                # Check if interview is complete
                if progress >= 100:
                    complete_interview(interview_service)
                    return

                # Show result and wait for next question
                set_answer_feedback(answer_data)

                st.rerun()
            else:
                st.error(f"Failed to submit answer: {response.error}")
        except Exception as e:
            st.error(f"Error submitting answer: {str(e)}")


def complete_interview(interview_service):
    """Complete the interview and return to normal view"""
    interview_state = get_interview_state()
    interview_id = interview_state["interview_id"]

    # Change interview status to COMPLETED
    try:
        response = interview_service.change_interview_status(interview_id, "COMPLETED")
    except Exception as e:
        st.warning(f"Could not update interview status: {str(e)}")

    # Calculate final statistics
    question_history = interview_state["question_history"]
    total_questions = len(question_history)
    correct_answers = sum(1 for q in question_history
                          if q.get("is_correct", False) == True)
    accuracy = (correct_answers / total_questions * 100) if total_questions > 0 else 0

    # Show completion dialog
    show_completion_dialog(total_questions, correct_answers, accuracy)

    # Reset interview state
    reset_interview_state()


def cancel_interview(interview_service):
    """Cancel the interview"""
    interview_state = get_interview_state()
    interview_id = interview_state["interview_id"]

    # Change interview status to CANCELLED
    try:
        response = interview_service.change_interview_status(interview_id, "CANCELLED")
    except Exception as e:
        st.warning(f"Could not update interview status: {str(e)}")

    # Reset interview state
    reset_interview_state()