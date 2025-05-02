# core_functions.py
from datetime import datetime
from typing import List

class Task:
    def __init__(self, title: str, due_date: str, category: str, priority: int, description: str = ""):
        self.title = title
        self.due_date = datetime.strptime(due_date, "%Y-%m-%d")
        self.category = category
        self.priority = priority
        self.description = description
        self.completed = False

    def mark_complete(self):
        self.completed = True

    def __str__(self):
        status = "✔" if self.completed else "✘"
        return f"[{status}] {self.title} | Due: {self.due_date.date()} | Category: {self.category} | Priority: {self.priority} | {self.description}"

class HighPriorityTask(Task):
    def __str__(self):
        return f"‼️HIGH PRIORITY ‼️ {super().__str__()}"

class TaskManager:
    def __init__(self):
        self.tasks: List[Task] = []

    def add_task(self, task: Task):
        self.tasks.append(task)

    def complete_task(self, title: str):
        for task in self.tasks:
            if task.title == title:
                task.mark_complete()

    def get_tasks(self, sort_by: str = None, filter_by: str = None, filter_value: str = None):
        filtered = self.tasks

        if filter_by == "category":
            filtered = [t for t in filtered if t.category.lower() == filter_value.lower()]
        elif filter_by == "due_date":
            try:
                date_obj = datetime.strptime(filter_value, "%Y-%m-%d").date()
                filtered = [t for t in filtered if t.due_date.date() == date_obj]
            except:
                pass

        if sort_by == "priority":
            filtered.sort(key=lambda x: x.priority)
        elif sort_by == "due_date":
            filtered.sort(key=lambda x: x.due_date)

        return filtered
