import streamlit as st
import pandas as pd
import requests

FASTAPI_URL = 'http://127.0.0.1:8000'

st.title("Task Manager")

tab_list, tab_add, tab_edit,tab_delete = st.tabs(["Tasks list", "Add task", "Edit task","Delete task"])

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

with tab_edit:
    st.subheader("Edit task")
    key_edit = st.text_input("Enter key", key="edit_key_input")

    @st.dialog("Edit task data", width="medium")
    def edit_screen(task_key):
        try:
            response = requests.get(f"{FASTAPI_URL}/tasks/{task_key}")
            if response.status_code == 200:
                task_data = response.json()["Task"]
                current_title = task_data[1]
                current_description = task_data[2] or ""
                current_priority = task_data[3]
                current_status = task_data[4]
                current_assigned = task_data[5]
            else:
                st.error("Could not fetch task data.")
                return
        except requests.exceptions.ConnectionError:
            st.error("Could not connect to FastAPI server.")
            return

        title_edit = st.text_input("Title", value=current_title, key="title_edit")
        description_edit = st.text_input("Description (optional)", value=current_description, key="description_edit")

        priority_options = ['Low', 'Mid', 'High']
        default_priority = [current_priority]
        priority_list_edit = st.multiselect("Priority ", priority_options, default=default_priority,
                                            key="priority_edit")
        priority_edit = ''.join(priority_list_edit)

        status_options = ['New', 'In progress', 'Done']
        status_index = status_options.index(current_status)
        status_edit = st.selectbox("Status", status_options, index=status_index, key="status_edit")

        assigned_edit = st.text_input("Assign", value=current_assigned, key="assigned_edit")

        if st.button("Submit changes", type="primary"):
            data_edited = {
                "title": title_edit,
                "description": description_edit,
                "priority": priority_edit,
                "status": status_edit,
                "assigned": assigned_edit
            }
            try:
                request = requests.put(f"{FASTAPI_URL}/tasks/{task_key}", json=data_edited)
                if request.status_code == 200:
                    st.success("Task updated successfully")
                    st.rerun()
                else:
                    st.error(f"Error {request.status_code}: {request.json().get('detail')}")
            except requests.exceptions.ConnectionError:
                st.error("Could not connect to FastAPI server.")


    if st.button("Edit", type="primary"):
        if not key_edit:
            st.error("Please enter a key")
        else:
            edit_screen(key_edit)


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