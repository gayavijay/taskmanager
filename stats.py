# stats.py
from database import get_all_tasks

def get_completion_stats():
    tasks = get_all_tasks()
    completed = sum(1 for task in tasks if task.completed)
    incomplete = len(tasks) - completed
    return completed, incomplete
