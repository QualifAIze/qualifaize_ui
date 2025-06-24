import streamlit as st

from api_client.services.document_service import DocumentService
from custom_styles import document_management_styles
from dialogs.document_management_dialogs import upload_document_dialog, update_document_title_dialog
from utils import truncate_text, format_date

document_service = DocumentService()


@st.dialog("📤 Upload New Document", width="large")
def show_upload_dialog():
    upload_document_dialog(document_service)


@st.dialog("✏️ Update Document Title", width="large")
def show_update_title_dialog(document_id, current_title):
    update_document_title_dialog(document_service, document_id, current_title)


def confirm_delete_document(document_id, document_title):
    """Confirm and delete document"""
    if st.button(
            f"🗑️ Confirm Delete",
            type="primary",
            key=f"confirm_delete_{document_id}",
            use_container_width=True
    ):
        with st.spinner("Deleting document..."):
            try:
                deletion_response = document_service.delete_document(document_id)

                if deletion_response.is_success:
                    st.success(f"✅ Document '{document_title}' deleted successfully!")
                    st.rerun()
                else:
                    error_message = deletion_response.error or "Unknown error occurred"
                    st.error(f"❌ Delete failed: {error_message}")

            except Exception as e:
                st.error(f"❌ Error deleting document: {str(e)}")


st.set_page_config(page_title="Document Management - QualifAIze", layout="wide", page_icon="📁")

st.markdown(document_management_styles, unsafe_allow_html=True)

st.title("📁 Document Management")
st.markdown("*Manage PDF documents used for AI-powered interview generation*")

current_user = st.session_state.get('authenticated_user', {})
user_roles = current_user.get('roles', [])

if not current_user:
    st.error("❌ You must be logged in to access document management")
    st.info("Please sign in to manage documents")
    st.stop()

if "ADMIN" not in user_roles:
    st.error("❌ Access Denied")
    st.warning("You need administrator privileges to manage documents")
    st.info("Contact your system administrator for access")
    st.stop()

if st.button("📤 Upload New Document", type="primary", use_container_width=True):
    show_upload_dialog()

st.divider()

with st.spinner("Loading documents..."):
    try:
        response = document_service.get_all_documents()

        if response.is_success and response.data:
            documents = response.data

            st.markdown(f"""
            <div class="section-header">
                <h3 style="margin: 0; color: #1e40af; font-size: 18px;">
                    📋 Document Library
                </h3>
                <p style="margin: 2px 0 0 0; color: #6b7280; font-size: 14px;">
                    {len(documents)} documents available
                </p>
            </div>
            """, unsafe_allow_html=True)

            for row_index in range(0, len(documents), 3):
                doc_cols = st.columns(3)
                row_docs = documents[row_index:row_index + 3]

                for col_index, doc in enumerate(row_docs):
                    with doc_cols[col_index]:
                        with st.container(border=True):
                            doc_id = doc.get('id')
                            full_title = doc.get('secondaryFilename', 'Untitled Document')

                            st.markdown(f""" #### 📄 {truncate_text(full_title, 50)} """, unsafe_allow_html=True)

                            original_name = doc.get('filename', 'Unknown')
                            upload_date = format_date(doc.get('createdAt'))

                            st.markdown(f"""
                            <div class='doc-meta' title='{original_name}'>
                                📎 {truncate_text(original_name, 50)}
                            </div>
                            <div class='doc-meta'>
                                📅 {upload_date}
                            </div>
                            """, unsafe_allow_html=True)

                            uploader_name = "Unknown"
                            if doc.get('uploadedBy'):
                                uploader_info = doc['uploadedBy']
                                first_name = uploader_info.get('firstName', '')
                                last_name = uploader_info.get('lastName', '')
                                uploader_name = f"{first_name} {last_name}".strip()
                                if not uploader_name:
                                    uploader_name = uploader_info.get('username', 'Unknown')

                            st.markdown(f"""
                            <div class='uploader-badge' title='{uploader_name}'>
                                👤 {truncate_text(uploader_name, 15)}
                            </div>
                            """, unsafe_allow_html=True)

                            action_col1, action_col2 = st.columns(2)

                            with action_col1:
                                if st.button("✏️ Edit",
                                             key=f"edit_{doc_id}",
                                             help="Edit document title",
                                             use_container_width=True,
                                             type="secondary"):
                                    show_update_title_dialog(doc_id, doc.get('secondaryFilename', ''))

                            with action_col2:
                                delete_key = f"delete_confirm_{doc_id}"
                                if delete_key not in st.session_state:
                                    st.session_state[delete_key] = False

                                if not st.session_state[delete_key]:
                                    if st.button("🗑️ Delete",
                                                 key=f"delete_{doc_id}",
                                                 help="Delete document",
                                                 use_container_width=True,
                                                 type="secondary"):
                                        st.session_state[delete_key] = True
                                        st.rerun()
                                else:
                                    if st.button("❌ Cancel",
                                                 key=f"cancel_delete_{doc_id}",
                                                 help="Cancel deletion",
                                                 use_container_width=True,
                                                 type="secondary"):
                                        st.session_state[delete_key] = False
                                        st.rerun()

                            delete_key = f"delete_confirm_{doc_id}"
                            if st.session_state.get(delete_key, False):
                                st.markdown('<div class="delete-confirmation">', unsafe_allow_html=True)

                                st.markdown(f"""
                                <div style="margin-bottom: 6px;">
                                    <span style="font-size: 14px; font-weight: 500; color: #dc2626;">
                                        ⚠️ Delete this document?
                                    </span>
                                </div>
                                """, unsafe_allow_html=True)

                                confirm_col1, confirm_col2 = st.columns(2)
                                with confirm_col1:
                                    if st.button("Cancel", key=f"cancel_confirm_{doc_id}", type="secondary",
                                                 use_container_width=True):
                                        st.session_state[delete_key] = False
                                        st.rerun()
                                with confirm_col2:
                                    confirm_delete_document(doc_id, full_title)

                                st.markdown('</div>', unsafe_allow_html=True)

                if row_index + 3 < len(documents):
                    st.markdown('<div style="margin: 12px 0;"></div>', unsafe_allow_html=True)

        elif response.is_success and not response.data:
            st.info("📭 No documents found in the system")
            st.markdown("""
            **Get started by uploading your first document:**
            1. Click the "Upload New Document" button above
            2. Select a PDF file from your computer
            3. Enter a descriptive title
            4. Click "Upload Document" to process it
            """)

        else:
            error_msg = response.error or "Unknown error occurred"
            st.error(f"❌ Failed to load documents: {error_msg}")

            if st.button("🔄 Retry", type="secondary"):
                st.rerun()

    except Exception as e:
        st.error(f"❌ Error loading documents: {str(e)}")

        if st.button("🔄 Retry", type="secondary"):
            st.rerun()

# Help section
with st.expander("ℹ️ Document Management Help"):
    st.markdown("""
    **Document Management Features:**

    **📤 Upload Documents:**
    - Support for PDF files up to 50MB
    - Documents are automatically processed for AI interview generation
    - Each document needs a unique, descriptive title

    **✏️ Edit Document Titles:**
    - Click the ✏️ button to update document titles
    - Titles are used throughout the system to identify documents

    **🗑️ Delete Documents:**
    - Click the 🗑️ button and confirm to permanently remove documents
    - **Warning:** This action cannot be undone

    **💡 Best Practices:**
    - Use descriptive titles that indicate the document's purpose
    - Keep document sizes reasonable for faster processing
    - Regularly review and clean up unused documents
    """)