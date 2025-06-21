import json
import time

import pandas
import requests
import streamlit as st
import pandas as pd
from streamlit import container

from constants import BACKEND_BASE_URL


def get_files_info():
    response = requests.get(BACKEND_BASE_URL + "pdf/all", headers=st.session_state.auth_headers)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Cannot read the PDF list: {response.content}")

def delete_by_secondary_title(secondary_title):
    response = requests.delete(BACKEND_BASE_URL + "pdf/" + secondary_title, headers=st.session_state.auth_headers)
    if response.status_code == 204:
        st.rerun()
    else:
        st.error(f"Cannot read the PDF list: {response.content}")


@st.dialog("Upload PDF", width="small")
def handle_file_upload():
    if st.session_state["uploaded_file"] is not None:
        uploaded_file = st.session_state["uploaded_file"]

        # Display file information
        st.write("Filename:", uploaded_file.name)
        st.write("File type:", uploaded_file.type)
        st.write("File size:", uploaded_file.size / 1_000_000, "MB")

        secondary_file_name = st.text_input(label="Document Name", placeholder="Please Enter a Document Name")
        if st.button("Upload PDF", type="primary", use_container_width=True):
            if secondary_file_name != "":
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                data = {"secondary_file_name": secondary_file_name}
                response = requests.post(BACKEND_BASE_URL + "pdf/upload", files=files, data=data, headers=st.session_state.auth_headers)
                if response.status_code == 201:
                    st.success("File successfully uploaded to the system!")
                    time.sleep(1)
                    st.rerun()
                else:
                    error_message = json.loads(response.text)
                    st.error(f"{error_message['detail']} - {response.status_code}")
            else:
                st.error("Please enter a Document Name")


st.file_uploader(
    "Upload a file",
    label_visibility="collapsed",
    type=["pdf"],
    key="uploaded_file",
    on_change=handle_file_upload
)

container = st.container(border=True)
df = pd.DataFrame(get_files_info())

df = df.drop(columns=['id'], axis=1)

df['created_at'] = pd.to_datetime(df['created_at']) + pd.to_timedelta(2, unit='h')

col1, col2, col3, col4 = container.columns([2, 2, 2, 1])
with col1:
    st.markdown("<p style='text-align: center; margin-bottom: 0; font-weight: bold;'>Filename</p>", unsafe_allow_html=True)
with col2:
    st.markdown("<p style='text-align: center; margin-bottom: 0; font-weight: bold;'>Title</p>", unsafe_allow_html=True)
with col3:
    st.markdown("<p style='text-align: center; margin-bottom: 0; font-weight: bold;'>Uploaded At</p>", unsafe_allow_html=True)
with col4:
    st.markdown("<p style='text-align: center; margin-bottom: 0; font-weight: bold;'>Delete Document</p>", unsafe_allow_html=True)

container.divider()

for index, row in df.iterrows():
    col1_data, col2_data, col3_data, col4_data = container.columns([2, 2, 2, 1], vertical_alignment="center")
    with col1_data:
        st.markdown(f"<p style='text-align: center;'>{row['original_file_name']}</p>", unsafe_allow_html=True)
    with col2_data:
        st.markdown(f"<p style='text-align: center;'>{row['secondary_file_name']}</p>", unsafe_allow_html=True)
    with col3_data:
        st.markdown(f"<p style='text-align: center;'>{row['created_at']}</p>", unsafe_allow_html=True)
    with col4_data:
        delete_button = st.button(f"Delete", key=f"delete_{index}", type="primary", icon=":material/delete:", use_container_width=True)

        if delete_button:
            delete_by_secondary_title(row['secondary_file_name'])