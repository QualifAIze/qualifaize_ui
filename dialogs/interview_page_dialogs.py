import streamlit as st
from api_client.services.interview_service import InterviewService
from api_client.services.document_service import DocumentService
from api_client.services.user_service import UserService
from datetime import datetime, timedelta
import constants


def assign_interview_dialog():
    """
    Dialog component for creating and assigning new interviews.
    Requires admin role to access.
    """

    # Initialize services
    interview_service = InterviewService()
    document_service = DocumentService()
    user_service = UserService()

    st.markdown("*Create and assign interviews based on uploaded documents*")

    # Interview Basic Information
    st.markdown("#### 📋 Interview Details")
    interview_name = st.text_input(
        "Interview Name *",
        placeholder="e.g., Java Spring Boot Technical Interview",
        help="Provide a descriptive name for the interview"
    )

    interview_description = st.text_area(
        "Description *",
        placeholder="Brief description of the interview focus and objectives...",
        height=100,
        help="Provide details about what this interview will cover"
    )

    # Single row for Difficulty, Date, and Time
    st.markdown("#### ⚙️ Interview Configuration")
    config_col1, config_col2, config_col3 = st.columns([1, 1, 1])

    with config_col1:
        difficulty_level = st.segmented_control(
            "Difficulty Level *",
            options=constants.DIFFICULTY,
            default="MEDIUM",
            help="Select the overall difficulty level for the interview"
        )

    with config_col2:
        # Date selection with better future date handling
        default_date = datetime.now().date()
        if datetime.now().hour >= 18:  # If it's evening, suggest tomorrow
            default_date = (datetime.now() + timedelta(days=1)).date()

        schedule_date = st.date_input(
            "Interview Date *",
            value=default_date,
            min_value=datetime.now().date(),
            help="Select the date for the interview"
        )

    with config_col3:
        # Time selection with common business hours as options
        current_time = datetime.now().time()

        # Suggest next available hour during business hours (9 AM - 6 PM)
        if current_time.hour < 9:
            suggested_time = datetime.strptime("09:00", "%H:%M").time()
        elif current_time.hour >= 18:
            suggested_time = datetime.strptime("09:00", "%H:%M").time()
        else:
            # Round up to next hour
            next_hour = (current_time.hour + 1) % 24
            suggested_time = datetime.strptime(f"{next_hour:02d}:00", "%H:%M").time()

        schedule_time = st.time_input(
            "Interview Time *",
            value=suggested_time,
            help="Select the time for the interview"
        )

    # Combine date and time
    scheduled_datetime = datetime.combine(schedule_date, schedule_time)
    scheduled_date = scheduled_datetime.isoformat() + "Z"

    # Show formatted schedule for confirmation
    formatted_schedule = scheduled_datetime.strftime("%A, %B %d, %Y at %I:%M %p")
    st.info(f"📅 **Scheduled for:** {formatted_schedule}")

    # Document Selection
    st.markdown("#### 📄 Base Document")
    documents_response = document_service.get_all_documents()
    selected_document_id = None

    if documents_response.is_success and documents_response.data:
        document_options = {}
        for doc in documents_response.data:
            display_name = f"{doc['secondaryFilename']}"
            if doc.get('filename') and doc['filename'] != doc['secondaryFilename']:
                display_name += f" ({doc['filename']})"
            document_options[display_name] = doc['id']

        selected_document_display = st.selectbox(
            "Select Document *",
            options=list(document_options.keys()),
            help="Choose the document that will be used to generate interview questions"
        )
        selected_document_id = document_options.get(selected_document_display)
    else:
        st.error("❌ No documents available. Please upload documents first.")

    # User Assignment (Required)
    st.markdown("#### 👤 Assign to User")
    users_response = user_service.get_all_users()
    selected_user_id = None

    if users_response.is_success and users_response.data:
        user_options = {}

        for user in users_response.data:
            # Create display name with fallback for missing names
            first_name = user.get('firstName') or ''
            last_name = user.get('lastName') or ''
            username = user.get('username', 'Unknown')

            if first_name and last_name:
                display_name = f"{first_name} {last_name} (@{username})"
            elif first_name:
                display_name = f"{first_name} (@{username})"
            elif last_name:
                display_name = f"{last_name} (@{username})"
            else:
                display_name = f"@{username}"

            user_options[display_name] = user['userId']

        selected_user_display = st.selectbox(
            "Select User *",
            options=[None] + list(user_options.keys()),
            format_func=lambda x: "-- Select a user --" if x is None else x,
            help="Choose the user who will take this interview"
        )
        selected_user_id = user_options.get(selected_user_display) if selected_user_display else None
    else:
        st.error("❌ Could not load users. Cannot create interview without user assignment.")
        selected_user_id = None


    # Dialog Action Buttons
    st.divider()
    col1, col2 = st.columns([1, 1])

    with col1:
        if st.button("❌ Cancel", use_container_width=True):
            st.rerun()

    with col2:
        create_disabled = not (
                interview_name and interview_name.strip() and
                interview_description and interview_description.strip() and
                difficulty_level and
                selected_document_id and
                selected_user_id and
                schedule_date and
                schedule_time
        )

        if st.button(
                "🚀 Create Interview",
                type="primary",
                use_container_width=True,
                disabled=create_disabled
        ):
            # Validate required fields
            if not interview_name or not interview_name.strip():
                st.error("❌ Interview name is required")
            elif not interview_description or not interview_description.strip():
                st.error("❌ Interview description is required")
            elif not difficulty_level:
                st.error("❌ Please select a difficulty level")
            elif not selected_document_id:
                st.error("❌ Please select a base document")
            elif not selected_user_id:
                st.error("❌ Please assign the interview to a user")
            elif not schedule_date or not schedule_time:
                st.error("❌ Please schedule the interview date and time")
            else:
                # Create interview
                with st.spinner("Creating interview..."):
                    try:
                        response = interview_service.create_interview(
                            name=interview_name.strip(),
                            document_id=selected_document_id,
                            description=interview_description.strip(),
                            difficulty=difficulty_level,
                            assigned_to_user_id=selected_user_id,
                            scheduled_date=scheduled_date
                        )

                        if response.is_success:
                            interview_id = response.data.get('interviewId', 'Unknown')
                            st.success(f"✅ Interview '{interview_name}' created successfully!")
                            st.info(f"Interview ID: {interview_id}")

                            if selected_user_id:
                                assigned_user_name = selected_user_display.split(' (@')[
                                    0] if ' (@' in selected_user_display else selected_user_display
                                st.info(f"📧 Assigned to: {assigned_user_name}")

                            st.rerun()
                        else:
                            error_msg = response.error or "Unknown error occurred"
                            st.error(f"❌ Failed to create interview: {error_msg}")

                    except Exception as e:
                        st.error(f"❌ Error creating interview: {str(e)}")

    # Help section in dialog
    with st.expander("ℹ️ How Interview Assignment Works"):
        st.markdown("""
        **Interview Creation Process:**
        1. **Document Selection**: Choose a PDF that serves as the knowledge base
        2. **User Assignment**: Assign to a specific user (required)
        3. **Schedule**: Set date and time for the interview (required)
        4. **AI Generation**: Questions are generated dynamically during the interview
        5. **Adaptive Difficulty**: AI adjusts complexity based on performance

        **Difficulty Levels:**
        - **EASY**: Basic concepts and fundamental questions
        - **MEDIUM**: Moderate complexity with practical scenarios  
        - **HARD**: Advanced questions requiring deep understanding
        """)

def completion_dialog(total_questions, correct_answers, accuracy):
    """Show completion dialog with results"""

    st.markdown(f"""
        <div style="text-align: center; padding: 20px;">
            <div style="font-size: 48px; margin-bottom: 20px;">🎉</div>
            <h2 style="color: #10b981; margin-bottom: 16px;">Congratulations!</h2>
            <p style="font-size: 18px; margin-bottom: 20px;">
                You have successfully completed the interview.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("### 📊 Your Performance")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Questions", total_questions)
    with col2:
        st.metric("Correct Answers", correct_answers)
    with col3:
        st.metric("Final Score", f"{accuracy:.1f}%")

    st.divider()

    performance_msg, performance_color = get_performance_feedback(accuracy)

    st.markdown(f"""
        <div style="
            background: rgba(16, 185, 129, 0.1);
            border: 1px solid {performance_color};
            border-radius: 8px;
            padding: 16px;
            margin: 16px 0;
            color: {performance_color};
        ">
            {performance_msg}
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    render_next_steps()

    if st.button("✅ Close", type="primary", use_container_width=True):
        st.rerun()


def get_performance_feedback(accuracy):
    """Get performance feedback message and color based on accuracy"""
    if accuracy >= 80:
        return "🌟 **Excellent Performance!** You demonstrated strong knowledge in this area.", "#10b981"
    elif accuracy >= 60:
        return "👍 **Good Performance!** You showed solid understanding with room for improvement.", "#f59e0b"
    else:
        return "📚 **Learning Opportunity!** Consider reviewing the topics covered in this interview.", "#ef4444"


def render_next_steps():
    """Render next steps information"""
    st.markdown("### 📋 Next Steps")
    st.info("""
        **Your interview has been completed and submitted successfully.**

        Please wait for feedback from the person who created this interview. 
        You will be notified once the review is complete.

        Thank you for your time and effort!
        """)
