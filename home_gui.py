import tkinter as tk
from tkinter import messagebox
from core_functions import TaskManager
from stats import get_completion_stats
from utils import parse_date
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import datetime

CATEGORY_COLORS = {
    "Work": "lightblue",
    "Personal": "#E6CCFF",
    "School": "#FFDAB9",
    "Urgent": "lightcoral",
    "Other": "lightgray"
}

class LockedInApp:
    def __init__(self, user_id):
        self.root = tk.Tk()
        self.root.title("LockedIn Task Manager")
        self.root.geometry("600x700")
        self.user_id = user_id
        self.manager = TaskManager(user_id)

        # --- Configure Grid Weights ---
        for i in range(12):  # Update for however many rows you use
            self.root.grid_rowconfigure(i, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        # --- Input Fields ---
        tk.Label(self.root, text="Task Title:").grid(row=0, column=0, sticky="w")
        self.title_entry = tk.Entry(self.root)
        self.title_entry.grid(row=0, column=1, sticky="ew")

        tk.Label(self.root, text="Due Date (YYYY-MM-DD):").grid(row=1, column=0, sticky="w")
        self.date_entry = tk.Entry(self.root)
        self.date_entry.grid(row=1, column=1, sticky="ew")

        tk.Label(self.root, text="Priority:").grid(row=2, column=0, sticky="w")
        self.priority_var = tk.StringVar()
        self.priority_var.set("Medium")
        self.priority_menu = tk.OptionMenu(self.root, self.priority_var, "High", "Medium", "Low")
        self.priority_menu.grid(row=2, column=1, sticky="ew")

        tk.Label(self.root, text="Category:").grid(row=3, column=0, sticky="w")
        self.category_entry = tk.Entry(self.root)
        self.category_entry.grid(row=3, column=1, sticky="ew")

        tk.Label(self.root, text="Description (optional):").grid(row=4, column=0, sticky="w")
        self.description_entry = tk.Entry(self.root)
        self.description_entry.grid(row=4, column=1, sticky="ew")

        tk.Button(self.root, text="Add Task", command=self.add_task).grid(row=5, column=1, sticky="ew")

        # --- Task List ---
        self.task_list = tk.Listbox(self.root)
        self.task_list.grid(row=6, column=0, columnspan=2, sticky="nsew")
        self.task_list.bind("<Double-Button-1>", self.mark_complete)

        # --- Buttons ---
        tk.Button(self.root, text="Delete Task", command=self.delete_task).grid(row=7, column=1, sticky="ew")
        tk.Button(self.root, text="Show Completion Chart", command=self.show_chart).grid(row=7, column=0, sticky="ew")
        tk.Button(self.root, text="Close Chart", command=self.close_chart).grid(row=10, column=0, columnspan=2, sticky="ew")

        # --- Sorting and Filtering ---
        tk.Label(self.root, text="Sort By:").grid(row=8, column=0, sticky="w")
        self.sort_var = tk.StringVar()
        self.sort_var.set("Priority")
        self.sort_menu = tk.OptionMenu(self.root, self.sort_var, "Priority", "Due Date", "Category", command=self.change_sort)
        self.sort_menu.grid(row=8, column=1, sticky="ew")

        tk.Label(self.root, text="Filter By:").grid(row=9, column=0, sticky="w")
        self.filter_var = tk.StringVar()
        self.filter_var.set("All")
        self.filter_menu = tk.OptionMenu(self.root, self.filter_var, "All", "Completed", "Incomplete", "Overdue", "Category", command=self.change_filter)
        self.filter_menu.grid(row=9, column=1, sticky="ew")

        # --- Full-Screen Toggle ---
        tk.Button(self.root, text="Toggle Full-Screen", command=self.toggle_fullscreen).grid(row=11, column=0, columnspan=2, sticky="ew")

        self.chart_canvas = None
        self.refresh_task_list()

    def add_task(self):
        title = self.title_entry.get()
        date_str = self.date_entry.get()
        priority = self.priority_var.get()
        category = self.category_entry.get()
        description = self.description_entry.get()
        due_date = parse_date(date_str)

        if due_date:
            self.manager.add(title, due_date, priority, category, description)
            self.refresh_task_list()
        else:
            messagebox.showerror("Invalid date", "Please enter date in YYYY-MM-DD format.")

    def refresh_task_list(self):
        self.task_list.delete(0, tk.END)
        tasks = self.manager.get_tasks()

        # Apply filter
        filter_method = self.filter_var.get()
        if filter_method == "Completed":
            tasks = [t for t in tasks if t.completed]
        elif filter_method == "Incomplete":
            tasks = [t for t in tasks if not t.completed]
        elif filter_method == "Overdue":
            tasks = [t for t in tasks if not t.completed and t.due_date < datetime.date.today()]
        elif filter_method == "Category":
            category_filter = self.category_entry.get().lower()
            tasks = [t for t in tasks if t.category.lower() == category_filter]

        # Apply sorting
        sort_method = self.sort_var.get()
        if sort_method == "Priority":
            priority_order = {"High": 1, "Medium": 2, "Low": 3}
            tasks.sort(key=lambda t: priority_order.get(t.priority, 4))
        elif sort_method == "Due Date":
            tasks.sort(key=lambda t: t.due_date)
        elif sort_method == "Category":
            tasks.sort(key=lambda t: t.category.lower())

        for index, task in enumerate(tasks):
            status = "✓" if task.completed else "✗"
            display = f"[{status}] {task.id}: {task.title} - {task.due_date} - {task.priority} - {task.category} - {task.description or 'No description'}"
            self.task_list.insert(tk.END, display)

            color = CATEGORY_COLORS.get(task.category, "white")
            self.task_list.itemconfig(index, bg=color)

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

        tasks = self.manager.get_tasks()
        completed = sum(1 for t in tasks if t.completed)
        incomplete = sum(1 for t in tasks if not t.completed and t.due_date >= datetime.date.today())
        overdue = sum(1 for t in tasks if not t.completed and t.due_date < datetime.date.today())

        sizes = [completed, incomplete, overdue]
        labels = ["Completed", "Incomplete", "Overdue"]
        colors = ["#4CAF50", "#FFC107", "#F44336"]

        fig, ax = plt.subplots(figsize=(5, 5))
        wedges, texts, autotexts = ax.pie(
            sizes,
            autopct="%1.1f%%",
            colors=colors,
            startangle=140,
            wedgeprops=dict(width=0.5)
        )

        ax.legend(wedges, labels, title="Task Status", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
        ax.set_title("Task Status Overview")

        self.chart_canvas = FigureCanvasTkAgg(fig, master=self.root)
        self.chart_canvas.draw()
        self.chart_canvas.get_tk_widget().grid(row=10, column=0, columnspan=2, sticky="nsew")

    def close_chart(self):
        if self.chart_canvas:
            self.chart_canvas.get_tk_widget().destroy()
            self.chart_canvas = None
            plt.close('all')

    def change_sort(self, *args):
        self.refresh_task_list()

    def change_filter(self, *args):
        self.refresh_task_list()

    def toggle_fullscreen(self):
        is_fullscreen = self.root.attributes('-fullscreen')
        self.root.attributes('-fullscreen', not is_fullscreen)
        if not is_fullscreen:
            self.root.geometry("600x700")
        else:
            self.root.geometry(f"{self.root.winfo_screenwidth()}x{self.root.winfo_screenheight()}")

    def run(self):
        self.root.mainloop()