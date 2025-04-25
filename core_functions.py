from database import add_task, get_all_tasks, delete_task, mark_task_complete

class TaskManager:
    def add(self, title, due_date, priority, category):
        add_task(title, due_date, priority, category)

    def get_tasks(self):
        return get_all_tasks()

    def complete(self, task_id):
        mark_task_complete(task_id)

    def delete(self, task_id):
        delete_task(task_id)