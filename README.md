# Task Manager 
It is a web app that stores tasks and allows you to manage them.

It has a simple and intuitive UI.
### It uses:
* Python 3.10.12
* FastAPI 0.141.1
* Pydantic 2.13.4
* Streamlit 1.58.0
* Pandas 2.3.3
* Requests 2.34.2
* Uvicorn 0.49.0
* SQLite

### Installation
```bash
pip install -r requirements.txt
```

### Run app
To run the app, simply run:
```bash
python3 run.py
```
The *run.py* script simplifies the process of starting the app.
## Guide
### 1. List of tasks
<img src="https://i.postimg.cc/WpKHzbPC/List.png">
This page displays the list of tasks. Click the "Refresh" button to refresh the list after adding, deleting, or editing tasks.
You can also filter your tasks by clicking the "Filter" button.
<img src="https://i.postimg.cc/FKR61f1j/filter.png">
Here you can set your preferences and filter tasks by them. After setting them, click "Submit" button.

### 2. Add task
<img src="https://i.postimg.cc/ht3ry2PM/add.png">
You can add a task here, to do so, fill in the form and click "Submit" button.
"Description" and "Assign to" are optional.

### 3. Edit task
<img src="https://i.postimg.cc/pXLzwK7M/edit1.png">
To edit a task you must input the key of a task and then click "Edit" button.
<img src="https://i.postimg.cc/d3HksSfm/edit2.png">
You can edit what you want about a task except for the key. The key is a unique 4-digit identifier. Once assigned, it cannot be changed or reused.
When you are done click "Submit changes" button.

### 4. Delete task
<img src="https://i.postimg.cc/Kz9vB351/delete.png">
In order to delete a task, you must type in key of a task you want to delete and then click the trash can button.
