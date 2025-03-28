import tkinter as tk
from tkinter import messagebox, ttk
import datetime
import json

# File for saving tasks
TASKS_FILE = "todo_tasks.json"

# Load tasks from file
def load_tasks():
    try:
        with open(TASKS_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

# Save tasks to file
def save_tasks():
    with open(TASKS_FILE, "w") as file:
        json.dump(tasks, file, indent=4)

# Function to add a task
def add_task():
    work = work_entry.get()
    date = date_entry.get()
    time = time_entry.get()

    if not work or not date or not time:
        messagebox.showerror("Error", "All fields must be filled!")
        return

    try:
        datetime.datetime.strptime(date, "%Y-%m-%d")  # Validate date
        datetime.datetime.strptime(time, "%H:%M")  # Validate time
    except ValueError:
        messagebox.showerror("Error", "Invalid date or time format!")
        return

    task_id = str(len(tasks) + 1)
    tasks[task_id] = {"Work": work, "Date": date, "Time": time, "Status": "Pending"}
    save_tasks()
    update_task_list()
    work_entry.delete(0, tk.END)
    date_entry.delete(0, tk.END)
    time_entry.delete(0, tk.END)
    messagebox.showinfo("Success", "Task added successfully!")

# Function to update task list
def update_task_list():
    task_list.delete(*task_list.get_children())  # Clear existing tasks
    now = datetime.datetime.now()
    
    for task_id, details in tasks.items():
        task_time = datetime.datetime.strptime(details["Date"] + " " + details["Time"], "%Y-%m-%d %H:%M")
        
        if details["Status"] == "Completed":
            color = "#90EE90"  # Light Green
        elif task_time < now:
            color = "#FF6347"  # Red
        else:
            color = "#FFD700"  # Yellow

        task_list.insert("", "end", values=(task_id, details["Work"], details["Date"], details["Time"], details["Status"]), tags=(color,))
    
    task_list.tag_configure("#90EE90", background="#90EE90")
    task_list.tag_configure("#FF6347", background="#FF6347")
    task_list.tag_configure("#FFD700", background="#FFD700")


# Function to mark task as completed
def complete_task():
    selected_item = task_list.selection()
    if not selected_item:
        messagebox.showerror("Error", "Select a task first!")
        return

    task_id = str(task_list.item(selected_item[0], "values")[0])  # Ensure it's a string
    if task_id in tasks:
        tasks[task_id]["Status"] = "Completed"
        save_tasks()
        update_task_list()
        messagebox.showinfo("Success", "Task marked as completed!")
    else:
        messagebox.showerror("Error", "Task not found!")

# Function to delete a task
def delete_task():
    selected_item = task_list.selection()
    if not selected_item:
        messagebox.showerror("Error", "Select a task first!")
        return

    task_id = str(task_list.item(selected_item[0], "values")[0])  # Ensure it's a string
    if task_id in tasks:
        tasks.pop(task_id, None)  # Safe removal
        save_tasks()
        update_task_list()
        messagebox.showinfo("Success", "Task deleted!")
    else:
        messagebox.showerror("Error", "Task not found!")

# Function to sort tasks
def sort_tasks(by="date"):
    global tasks
    if by == "date":
        sorted_tasks = sorted(tasks.items(), key=lambda x: (x[1]["Date"], x[1]["Time"]))
    else:
        sorted_tasks = sorted(tasks.items(), key=lambda x: x[1]["Work"].lower())

    tasks = dict(sorted_tasks)
    update_task_list()

# Load existing tasks
tasks = load_tasks()

# GUI Window
root = tk.Tk()
root.title("To-Do List")
root.geometry("700x500")
root.configure(bg="#f0f0f0")

# Buttons at the top
top_frame = tk.Frame(root, bg="#d3d3d3")
top_frame.pack(fill=tk.X, padx=10, pady=5)

tk.Button(top_frame, text="Add Task", command=add_task, bg="#ADD8E6").pack(side=tk.LEFT, padx=5)
tk.Button(top_frame, text="Mark Completed", command=complete_task, bg="#90EE90").pack(side=tk.LEFT, padx=5)
tk.Button(top_frame, text="Delete Task", command=delete_task, bg="#FF6347").pack(side=tk.LEFT, padx=5)
tk.Button(top_frame, text="Sort by Date", command=lambda: sort_tasks("date"), bg="#FFD700").pack(side=tk.LEFT, padx=5)
tk.Button(top_frame, text="Sort Alphabetically", command=lambda: sort_tasks("alpha"), bg="#DDA0DD").pack(side=tk.LEFT, padx=5)

# Input fields
input_frame = tk.Frame(root, bg="#f0f0f0")
input_frame.pack(pady=10)

tk.Label(input_frame, text="Work:", bg="#f0f0f0").grid(row=0, column=0, padx=5, pady=5)
work_entry = tk.Entry(input_frame, width=40)
work_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(input_frame, text="Date (YYYY-MM-DD):", bg="#f0f0f0").grid(row=1, column=0, padx=5, pady=5)
date_entry = tk.Entry(input_frame, width=20)
date_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(input_frame, text="Time (HH:MM):", bg="#f0f0f0").grid(row=2, column=0, padx=5, pady=5)
time_entry = tk.Entry(input_frame, width=20)
time_entry.grid(row=2, column=1, padx=5, pady=5)

# Task List Table
columns = ("ID", "Work", "Date", "Time", "Status")
task_list = ttk.Treeview(root, columns=columns, show="headings")
for col in columns:
    task_list.heading(col, text=col)
task_list.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Update task list initially
update_task_list()

# Run the application
root.mainloop()
