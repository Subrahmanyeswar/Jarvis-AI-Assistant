# C:\Users\SUBBU\Downloads\RealTimeSecuritySystem\productivity\to_do.py

import os

_project_root = os.path.dirname(os.path.dirname(__file__))
TODO_FILE = os.path.join(_project_root, "todo_list.txt")

def add_todo_item(task: str):
    """Adds a task to the to-do list."""
    print(f"🛠️ TOOL: Running add_todo_item(task='{task}')...")
    with open(TODO_FILE, "a") as f:
        f.write(task + "\n")
    return f"Successfully added '{task}' to your to-do list."

def read_todo_list():
    """Reads all tasks from the to-do list."""
    print("🛠️ TOOL: Running read_todo_list...")
    if not os.path.exists(TODO_FILE) or os.path.getsize(TODO_FILE) == 0:
        return "Your to-do list is currently empty."
    with open(TODO_FILE, "r") as f:
        tasks = f.readlines()
    formatted_tasks = "Here is your to-do list:\n" + "".join(f"{i}. {task.strip()}\n" for i, task in enumerate(tasks, 1))
    return formatted_tasks