import tkinter as tk
from tkinter import messagebox
from database import cursor, conn

# Create the main window
root = tk.Tk()
root.title("Task Manager")

# Function to create a new task
def create_task():
    title = title_entry.get()
    description = description_text.get("1.0", "end-1c")
    
    if title and description:
        cursor.execute("INSERT INTO tasks (title, description) VALUES (?, ?)", (title, description))
        conn.commit()
        title_entry.delete(0, "end")
        description_text.delete("1.0", "end")
        list_tasks()
    else:
        messagebox.showwarning("Warning", "Please enter both title and description!")

# Function to list all tasks
def list_tasks():
    tasks_listbox.delete(0, "end")
    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()
    
    for task in tasks:
        tasks_listbox.insert("end", f"{task[0]}. {task[1]}")
        
# Function to update a task
def update_task():
    selected_task = tasks_listbox.get("active")
    if selected_task:
        # Split the selected_task string by the first period
        task_id, _ = selected_task.split(".", 1)
        new_description = description_text.get("1.0", "end-1c")
        cursor.execute("UPDATE tasks SET description = ? WHERE id = ?", (new_description, task_id))
        conn.commit()
        list_tasks()
    else:
        messagebox.showwarning("Warning", "Please select a task to update!")

# Function to delete a task
def delete_task():
    selected_task = tasks_listbox.get("active")
    if selected_task:
        task_id = selected_task.split(".")[0]
        cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        conn.commit()
        list_tasks()
    else:
        messagebox.showwarning("Warning", "Please select a task to delete!")

# Create labels, entry fields, and buttons
title_label = tk.Label(root, text="Title:")
title_label.pack()

title_entry = tk.Entry(root)
title_entry.pack()

description_label = tk.Label(root, text="Description:")
description_label.pack()

description_text = tk.Text(root, height=5, width=40)
description_text.pack()

create_button = tk.Button(root, text="Create Task", command=create_task)
create_button.pack()

list_button = tk.Button(root, text="List Tasks", command=list_tasks)
list_button.pack()

update_button = tk.Button(root, text="Update Task", command=update_task)
update_button.pack()

delete_button = tk.Button(root, text="Delete Task", command=delete_task)
delete_button.pack()

tasks_listbox = tk.Listbox(root, height=10, width=50)
tasks_listbox.pack()

list_tasks()

# Start the main loop
root.mainloop()
