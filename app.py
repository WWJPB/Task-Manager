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
    key = st.text_input("Enter key")
    title = st.text_input("Enter title")
    description = st.text_input("Describe task(optional)")
    priority_list = st.multiselect("Set priority: ", ['Low', 'Mid', 'High'])
    priority = ''.join(priority_list)
    assigned = st.text_input("Assign to")
    if st.button("Submit", type="primary"):
        if not key or not title:
            st.error("Key and Title are required")
        else:
            data = {
                "key": key,
                "title": title,
                "description": description,
                "priority": priority,
                "assigned": assigned
            }
        try:
            request = requests.post(f"{FASTAPI_URL}/tasks", json=data)
            if request.status_code == 201:
                st.success("Task added successfully")
            else:
                st.error(f"Error {request.status_code}: {request.json().get('detail')}")
        except requests.exceptions.ConnectionError:
                st.error("Could not connect to FastAPI server.")

with tab_delete:
    st.subheader("Delete task")
    key_delete = st.text_input("Enter key", key="delete_key_input")

    if st.button("🗑️", type="primary"):
        if not key_delete:
            st.error("Please enter a key to delete.")
        else:
            try:
                request = requests.delete(f"{FASTAPI_URL}/tasks/{key_delete}")

                if request.status_code == 200:
                    st.success(f"Task with key {key_delete} deleted successfully")
                else:
                    error_detail = request.json().get('detail', 'Unknown error')
                    st.error(f"Error {request.status_code}: {error_detail}")
            except requests.exceptions.ConnectionError:
                st.error("Could not connect to FastAPI server.")