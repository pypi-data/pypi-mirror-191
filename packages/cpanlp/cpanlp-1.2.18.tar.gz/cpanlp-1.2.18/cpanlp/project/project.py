from cpanlp.project.task import *

class Project:
    projects = []
    def __init__(self, name):
        self.name = name
        self.tasks = []
        Project.projects.append(self)
    def add_task(self, task):
        self.tasks.append(task)
    def remaining_tasks(self):
        return [task for task in self.tasks if not task.completed]
def main():
    project = Project("My Project")
    task1 = Task("Do task 1")
    task2 = Task("Do task 2")
    project.add_task(task1)
    project.add_task(task2)
    for task in project.remaining_tasks():
        print(task.description)
if __name__ == '__main__':
    main()






