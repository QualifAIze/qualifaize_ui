import time

import streamlit as st

from utils import format_file_size


def upload_document_dialog(document_service):
    """Dialog for uploading new PDF documents"""

    st.markdown("*Upload a PDF document to generate AI-powered interview questions*")

    st.markdown("#### 📄 Select Document")
    uploaded_file = st.file_uploader(
        "Choose PDF file",
        type=['pdf'],
        help="Select a PDF document (max 50MB)",
        accept_multiple_files=False
    )

    st.markdown("#### 📝 Document Details")
    document_title = st.text_input(
        "Document Title *",
        placeholder="Enter a descriptive title for the document",
        help="This title will be used to identify the document in the system"
    )

    if uploaded_file is not None:
        st.markdown("#### 📋 File Information")
        col1, col2 = st.columns(2)

        with col1:
            st.info(f"**Filename:** {uploaded_file.name}")
            st.info(f"**File Size:** {format_file_size(uploaded_file.size)}")

        with col2:
            st.info(f"**File Type:** {uploaded_file.type}")
            if uploaded_file.size > 50 * 1024 * 1024:  # 50MB limit
                st.error("⚠️ File size exceeds 50MB limit")

    st.divider()
    col1, col2 = st.columns([1, 1])

    with col1:
        if st.button("❌ Cancel", use_container_width=True):
            st.rerun()

    with col2:
        if st.button(
                "🚀 Upload Document",
                type="primary",
                use_container_width=True
        ):
            if not uploaded_file:
                st.error("❌ Please select a PDF file")
            elif not document_title or not document_title.strip():
                st.error("❌ Please enter a document title")
            elif uploaded_file.size > 50 * 1024 * 1024:
                st.error("❌ File size exceeds 50MB limit")
            else:
                with st.spinner("Uploading and processing document..."):
                    try:
                        response = document_service.upload_pdf_from_buffer(
                            file_buffer=uploaded_file,
                            secondary_file_name=document_title.strip(),
                            filename=uploaded_file.name
                        )

                        if response.is_success:
                            st.success(f"✅ Document '{document_title}' uploaded successfully!")
                            st.info("🔄 The page will refresh to show the new document...")
                            time.sleep(2)
                            st.rerun()
                        else:
                            error_msg = response.error or "Unknown error occurred"
                            st.error(f"❌ Upload failed: {error_msg}")

                    except Exception as e:
                        st.error(f"❌ Error during upload: {str(e)}")

def update_document_title_dialog(document_service, document_id, current_title):
    """Dialog for updating document title"""

    st.markdown(f"*Update the title for document: **{current_title}***")

    new_title = st.text_input(
        "New Document Title",
        value=current_title,
        placeholder="Enter the new title",
        help="The new title will be used to identify this document"
    )

    st.markdown("---")
    col1, col2 = st.columns([1, 1])

    with col1:
        if st.button("❌ Cancel", use_container_width=True):
            st.rerun()

    with col2:
        update_disabled = not new_title or not new_title.strip() or new_title.strip() == current_title

        if st.button(
                "💾 Update Title",
                type="primary",
                use_container_width=True,
                disabled=update_disabled
        ):
            if not new_title or not new_title.strip():
                st.error("❌ Please enter a valid title")
            elif new_title.strip() == current_title:
                st.warning("⚠️ New title is the same as current title")
            else:
                with st.spinner("Updating document title..."):
                    try:
                        response = document_service.update_document_title(
                            document_id=document_id,
                            new_title=new_title.strip()
                        )

                        if response.is_success:
                            st.success(f"✅ Document title updated successfully!")
                            st.rerun()
                        else:
                            error_msg = response.error or "Unknown error occurred"
                            st.error(f"❌ Update failed: {error_msg}")

                    except Exception as e:
                        st.error(f"❌ Error updating title: {str(e)}")