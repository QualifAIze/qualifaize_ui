import streamlit as st

def initialize_interview_state():
    """Initialize interview state if not exists"""
    if "current_interview_state" not in st.session_state:
        st.session_state.current_interview_state = {
            "is_active": False,
            "interview_id": None,
            "interview_name": None,
            "current_question": None,
            "selected_answer": None,
            "progress": 0,
            "question_history": [],
            "is_waiting_for_next": False,
            "last_answer_result": None
        }

def reset_interview_state():
    """Reset interview state to default"""
    st.session_state.current_interview_state = {
        "is_active": False,
        "interview_id": None,
        "interview_name": None,
        "current_question": None,
        "selected_answer": None,
        "progress": 0,
        "question_history": [],
        "is_waiting_for_next": False,
        "last_answer_result": None
    }

def get_interview_state():
    """Get current interview state"""
    return st.session_state.current_interview_state

def update_interview_state(key, value):
    """Update specific key in interview state"""
    st.session_state.current_interview_state[key] = value

def set_interview_active(interview_id, interview_name):
    """Set interview as active"""
    st.session_state.current_interview_state.update({
        "is_active": True,
        "interview_id": interview_id,
        "interview_name": interview_name,
        "current_question": None,
        "selected_answer": None,
        "progress": 0,
        "question_history": [],
        "is_waiting_for_next": False,
        "last_answer_result": None
    })

def add_question_to_history(question_info):
    """Add question to history"""
    st.session_state.current_interview_state["question_history"].append(question_info)

def set_current_question(question_data):
    """Set current question data"""
    st.session_state.current_interview_state.update({
        "current_question": question_data,
        "selected_answer": None,
        "is_waiting_for_next": False,
        "last_answer_result": None
    })

def set_answer_feedback(answer_data):
    """Set answer feedback data"""
    st.session_state.current_interview_state.update({
        "is_waiting_for_next": True,
        "last_answer_result": answer_data
    })

def update_progress(progress):
    """Update interview progress"""
    st.session_state.current_interview_state["progress"] = progress