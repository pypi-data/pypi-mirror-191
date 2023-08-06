
class Task:
    tasks = []
    def __init__(self, description, completed=False):
        self.description = description
        self.completed = completed
        Task.tasks.append(self)
    def complete(self):
        self.completed = True
