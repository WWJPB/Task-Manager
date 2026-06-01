import streamlit as st
import pandas as pd
import requests

FASTAPI_URL = 'http://127.0.0.1:8000'

st.title("Task Manager")

tab_list, tab_add, tab_delete = st.tabs(["Tasks list", "Add task", "Delete task"])

with tab_list:
    st.subheader("List of tasks:")
    request = requests.get(f"{FASTAPI_URL}/tasks")
    if request.status_code == 200:
        tasks = request.json()["Tasks"]
        table = pd.DataFrame(tasks, columns=["Key", "Title", "Description", "Priority"])
        st.dataframe(table, use_container_width=True, hide_index=True)

    if st.button("🔄", type="primary"):
        st.rerun()

with tab_add:
    st.subheader("Add new task")

with tab_delete:
    st.subheader("Delete task")