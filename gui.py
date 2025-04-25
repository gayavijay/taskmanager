import tkinter as tk
from tkinter import messagebox
from core_functions import TaskManager
from stats import get_completion_stats
from utils import parse_date
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

class LockedInApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("LockedIn Task Manager")
        self.root.geometry("600x600")
        self.manager = TaskManager()

        self.title_entry = tk.Entry(self.root, width=30)
        self.title_entry.grid(row=0, column=1)
        tk.Label(self.root, text="Task Title:").grid(row=0, column=0)

        self.date_entry = tk.Entry(self.root, width=30)
        self.date_entry.grid(row=1, column=1)
        tk.Label(self.root, text="Due Date (YYYY-MM-DD):").grid(row=1, column=0)

        self.priority_entry = tk.Entry(self.root, width=30)
        self.priority_entry.grid(row=2, column=1)
        tk.Label(self.root, text="Priority:").grid(row=2, column=0)

        self.category_entry = tk.Entry(self.root, width=30)
        self.category_entry.grid(row=3, column=1)
        tk.Label(self.root, text="Category:").grid(row=3, column=0)

        tk.Button(self.root, text="Add Task", command=self.add_task).grid(row=4, column=1)

        self.task_list = tk.Listbox(self.root, width=70)
        self.task_list.grid(row=5, column=0, columnspan=2)
        self.task_list.bind("<Double-Button-1>", self.mark_complete)

        tk.Button(self.root, text="Delete Task", command=self.delete_task).grid(row=6, column=1)
        tk.Button(self.root, text="Show Completion Chart", command=self.show_chart).grid(row=6, column=0)

        self.chart_canvas = None

        self.refresh_task_list()

    def add_task(self):
        title = self.title_entry.get()
        date_str = self.date_entry.get()
        priority = self.priority_entry.get()
        category = self.category_entry.get()
        due_date = parse_date(date_str)

        if due_date:
            self.manager.add(title, due_date, priority, category)
            self.refresh_task_list()
        else:
            messagebox.showerror("Invalid date", "Please enter date in YYYY-MM-DD format")

    def refresh_task_list(self):
        self.task_list.delete(0, tk.END)
        tasks = self.manager.get_tasks()
        for task in tasks:
            status = "✓" if task.completed else "✗"
            display = f"[{status}] {task.id}: {task.title} - {task.due_date} - {task.priority} - {task.category}"
            self.task_list.insert(tk.END, display)

    def mark_complete(self, event):
        selection = self.task_list.curselection()
        if selection:
            task_line = self.task_list.get(selection[0])
            task_id = int(task_line.split()[1].replace(":", ""))
            self.manager.complete(task_id)
            self.refresh_task_list()

    def delete_task(self):
        selection = self.task_list.curselection()
        if selection:
            task_line = self.task_list.get(selection[0])
            task_id = int(task_line.split()[1].replace(":", ""))
            self.manager.delete(task_id)
            self.refresh_task_list()

    def show_chart(self):
        if self.chart_canvas:
            self.chart_canvas.get_tk_widget().destroy()

        completed, incomplete = get_completion_stats()
        fig, ax = plt.subplots(figsize=(4, 4))
        ax.pie([completed, incomplete], labels=["Completed", "Incomplete"], autopct="%1.1f%%", colors=["#8BC34A", "#FFC107"])
        ax.set_title("Task Completion Status")

        self.chart_canvas = FigureCanvasTkAgg(fig, master=self.root)
        self.chart_canvas.draw()
        self.chart_canvas.get_tk_widget().grid(row=7, column=0, columnspan=2)

    def run(self):
        self.root.mainloop()