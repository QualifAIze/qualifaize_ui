import os
import time

import pandas as pd
import requests
import streamlit as st
from streamlit import rerun

from constants import SENIORITY_LEVELS, BACKEND_BASE_URL, COUNT_WRONG_ANSWERS_IN_PROGRESS


def get_cvs():
    response = requests.get(BACKEND_BASE_URL + "cv")
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Cannot read the CV list: {response.content}")


def get_pdf_file_titles():
    response = requests.get(BACKEND_BASE_URL + "pdf/titles")
    if response.status_code == 200:
        return response.json()["secondary_files_name"]
    else:
        st.error(f"Cannot read the PDF list: {response.content}")


def get_next_question_context(seniority_level, cv_id):
    context_request = {
        "seniority_level": seniority_level,
        "cv_id": cv_id,
        "answered_questions": st.session_state.answered_questions
    }
    response = requests.post(BACKEND_BASE_URL + "interview/choose_question_context",
                             json=context_request)
    if response.status_code != 200:
        st.error(f"Error reading next context: {response.content}")
        return {}
    else:
        return response.json()


def get_next_question(seniority_level, cv_id, context):
    question_request = {
        "seniority_level": seniority_level,
        "cv_id": cv_id,
        "question_context": context,
        "answered_questions": st.session_state.answered_questions
    }
    response = requests.post(BACKEND_BASE_URL + "interview/generate_question",
                             json=question_request)
    if response.status_code != 200:
        st.error(f"Error generating question: {response.content}")
        return {}
    else:
        return response.json()


def send_selected_titles():
    params = {'title': st.session_state.selected_pdf_titles}

    response = requests.get(BACKEND_BASE_URL + "pdf", params=params)
    if response.status_code == 202:
        return response.json()
    elif response.status_code == 422:
        st.toast("Invalid Request!", icon="❗")
        time.sleep(1)
        st.rerun()
    else:
        return f"Error: {response.status_code}"


def get_progress_by_answered_question(answered_question):
    difficulty = {
        "Easy": 3,
        "Medium": 5,
        "Hard": 7,
    }

    value_to_return = difficulty[answered_question["difficulty"]]
    if not answered_question["correct_answer"] and not COUNT_WRONG_ANSWERS_IN_PROGRESS:
        value_to_return = 0

    return value_to_return


def get_points_by_answered_question(answered_question):
    difficulty = {
        "Easy": 1,
        "Medium": 2,
        "Hard": 3,
    }

    current_question_points = difficulty[answered_question["difficulty"]]
    st.session_state.max_possible_interview_points += current_question_points
    return current_question_points if answered_question["correct_answer"] else 0


def make_summary_table():
    data = [{"№": q["question_number"], "Question Title": q["question"],
             "Earned Points": get_points_by_answered_question(q)} for q in
            st.session_state.answered_questions]

    total_points = sum(q["Earned Points"] for q in data)
    data.append({"№": "", "Question Title": "Total Points:", "Earned Points": total_points})

    df = pd.DataFrame(data)

    st.title("Questions and Earned Points Table")
    st.data_editor(
        df,
        column_config={
            "№": st.column_config.TextColumn(
                disabled=True,
                width="small"
            ),
            "Question Title": st.column_config.TextColumn(
                disabled=True,
                width="large"
            ),
            "Earned Points": st.column_config.NumberColumn(
                disabled=True,
                width="small"
            )
        },
        hide_index=True,
        use_container_width=True
    )


@st.dialog("Interview summary", width="large")
def show_interview_summary():
    if st.session_state.interview_progress >= 100:
        st.header(
            f"Your interview is finished! You have :green-background[{st.session_state.interview_points}] out of **{st.session_state.max_possible_interview_points}** maximum points!")
        make_summary_table()
    else:
        st.header("Interview is :red-background[NOT] finished!")

    reset_interview_counters()
    if st.button("Close", use_container_width=True, type="primary"):
        rerun()


def reset_interview_counters():
    st.session_state.interview_points = 0
    st.session_state.interview_progress = 0
    st.session_state.max_possible_interview_points = 0
    print(f"----------------------------------------------------------------"
          f"{os.linesep}Starting new interview{os.linesep}"
          f"----------------------------------------------------------------")


def stop_interview():
    st.session_state.in_interview = False
    st.session_state.question_counter = 1
    st.rerun()


@st.dialog("Question details", width="large")
def details_dialog():
    st.write("Context:")
    st.json(st.session_state.context)
    st.write("Question:")
    st.json(st.session_state.question)
    st.write("Previously answered questions:")
    st.json(st.session_state.answered_questions)


def interview(seniority_level, cv_id):
    st.markdown("### In interview")

    if "answered_questions" not in st.session_state:
        st.session_state.answered_questions = []
        reset_interview_counters()

    interview_progress = st.session_state.interview_progress
    is_interview_active = st.session_state.in_interview
    if interview_progress >= 100 and is_interview_active:
        interview_progress = 100
        stop_interview()

    progress_text = f"Interview progress ({interview_progress}%)"

    st.progress(interview_progress, text=progress_text)

    interview_side, history_side = st.columns([2, 1])

    with interview_side:
        placeholder = st.empty()
        if st.session_state.get("next_question", False):
            # show correct/wrong answer from previous question
            if len(st.session_state.answered_questions) > 0:
                last_answered_question = st.session_state.answered_questions[-1]
                if last_answered_question["correct_answer"]:
                    with placeholder:
                        st.success("Correct answer")
                else:
                    with placeholder:
                        st.error("Wrong answer")

            context = get_next_question_context(seniority_level, cv_id)
            question = get_next_question(seniority_level, cv_id, context["question_context"])
            st.session_state.context = context
            st.session_state.question = question

            st.session_state.next_question = False
            placeholder.empty()
        else:
            context = st.session_state.get("context", {})
            question = st.session_state.get("question", {})

        answers = question["answers"]
        difficulty = question["difficulty"]
        container = st.container(border=True)
        answer = container.radio(
            f"## {str(st.session_state.question_counter)}. {question['question']}  &nbsp; _({difficulty})_",
            range(len(answers)),
            format_func=lambda ans_idx: answers[ans_idx],
            index=None
        )

        col1, col2, col3 = st.columns([2, 1, 1])

        with col1:
            if st.button("Submit answer", use_container_width=True, type="primary"):
                if answer is not None:
                    answered_question = {
                        "caption_title": context["title"],
                        "question": question['question'],
                        "question_number": st.session_state.question_counter,
                        "correct_answer": answer == question["correct_answer_index"],
                        "difficulty": difficulty
                    }
                    st.session_state.answered_questions.append(answered_question)
                    st.session_state.next_question = True
                    st.session_state.question_counter += 1
                    st.session_state.interview_progress += get_progress_by_answered_question(answered_question)
                    st.session_state.interview_points += get_points_by_answered_question(answered_question)
                    print(
                        f"{answered_question.get('question_number')}. {answered_question.get('question')}{os.linesep}"
                        f"progress: {st.session_state.interview_progress}%{os.linesep}"
                        f"points: {st.session_state.interview_points} (of maximum possible: {st.session_state.max_possible_interview_points}){os.linesep}"
                        f"--------------------------------")
                    st.rerun()
                else:
                    st.toast("You must answer the question to continue!", icon="⚠️")

        with col2:
            if st.button("Show details", use_container_width=True):
                details_dialog()

        with col3:
            if st.button("Stop interview", use_container_width=True):
                stop_interview()

    with history_side:
        container = st.container(border=True)
        container.markdown("<h3 style='text-align: center; padding: 0 0 0 5%;'>Answered Questions</h3><hr>",
                           unsafe_allow_html=True)
        for question in reversed(st.session_state.answered_questions):
            color = "#50c16f" if question["correct_answer"] else "#ff4b4b"
            container.html(
                f"<p><span style='color: {color}; font-weight: bold;'>{question['question']}</span>  <span style='text-decoration:underline; font-style: italic;'>({question['difficulty']})</span></p>"
            )


def pdf_file_section():
    st.session_state.pdf_titles = get_pdf_file_titles()

    if 'selected_pdf_titles' not in st.session_state:
        st.session_state.selected_pdf_titles = []

    option = st.selectbox('Select file',
                          st.session_state.pdf_titles,
                          index=None,
                          disabled=in_interview)

    # options = st.multiselect('Select file',
    #                         st.session_state.pdf_titles,
    #                         #default=st.session_state.selected_pdf_titles,
    #                         disabled=in_interview,
    #                         max_selections=1)

    st.session_state.selected_pdf_titles = [option]


st.markdown(
    """<style>
div[class*="stRadio"] > label > div[data-testid="stMarkdownContainer"] {
    font-size: 20px;
}
    </style>
    """, unsafe_allow_html=True)

st.sidebar.markdown("## Interview")

st.title("Interview")

in_interview = st.session_state.get("in_interview", False)
if 'question_counter' not in st.session_state:
    st.session_state.question_counter = 1

if st.checkbox("Select CV", key="check_select_cv", disabled=in_interview):
    cvs = get_cvs()
    st.selectbox(
        "Select CV for interview",
        range(len(cvs)),
        format_func=lambda cv_idx: cvs[cv_idx]["file_name"],
        index=None,
        disabled=in_interview,
        key="select_cv",
    )

seniority_level = st.selectbox(
    "Select seniority level",
    options=SENIORITY_LEVELS,
    index=0,
    disabled=in_interview,
    key="seniority_level"
)

pdf_file_section()

if in_interview:
    cv_id = None
    if (st.session_state.get("check_select_cv", False) and
            st.session_state.get("select_cv", -1) >= 0):
        cv_id = cvs[st.session_state.select_cv]["id"]
    interview(seniority_level, cv_id)
else:
    if "interview_progress" in st.session_state and st.session_state.interview_progress > 0:
        show_interview_summary()
    if st.button("Start interview", use_container_width=True, type="primary"):
        if seniority_level is None:
            st.error("Please select seniority level for the interview")
        else:
            send_selected_titles()
            st.session_state.in_interview = True
            st.session_state.next_question = True
            st.session_state.answered_questions = []
            reset_interview_counters()
            st.rerun()
