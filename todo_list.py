import json
import os
from datetime import datetime

def validate_date_format(date_text):
    try:
        datetime.strptime(date_text, "%d-%m-%Y")
        return True
    except ValueError:
        return False
    
class Task:
    def __init__(self, description, due_date, status="TODO"):
        self.description = description
        self.due_date = due_date
        self.status = status

    def __str__(self):
        return f"Description: {self.description}\nDue Date: {self.due_date}\nStatus: {self.status}"

class TodoList:
    def __init__(self, filename="tasks.json"):
        self.filename = filename
        self.tasks = self.load_tasks()

    def load_tasks(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as file:
                tasks = json.load(file)
            return [Task(task['description'], task['due_date'], task['status']) for task in tasks]
        else:
            return []

    def save_tasks(self):
        with open(self.filename, 'w') as file:
            tasks_data = [{'description': task.description, 'due_date': task.due_date, 'status': task.status} for task in self.tasks]
            json.dump(tasks_data, file, indent=4)

    def view_tasks(self):
        if self.tasks:
            for i, task in enumerate(self.tasks, start=1):
                print(f"Task {i}:\n{task}\n")
        else:
            print("No tasks in the list.")

    def add_task(self, description, due_date, status="TODO"):
        if not validate_date_format(due_date):
            print("Invalid date format. Please use DD-MM-YYYY.")
            return
        new_task = Task(description, due_date, status)
        self.tasks.append(new_task)
        self.save_tasks()
        print("Task added successfully.")

    def update_task(self, task_index, new_description=None, new_due_date=None, new_status=None):
        task = self.get_task_by_index(task_index)
        if not task:
            print("Invalid task index.")
            return
      
        if new_due_date and not validate_date_format(new_due_date):
            print("Invalid date format. Please use DD-MM-YYYY.")
            return
        
        if new_description:
            task.description = new_description
        if new_due_date:
            task.due_date = new_due_date
        if new_status:
            task.status = new_status
        self.save_tasks()
        print("Task updated successfully.")


    def delete_task(self, task_index):
        task = self.get_task_by_index(task_index)
        if task:
            self.tasks.remove(task)
            self.save_tasks()
            print("Task deleted successfully.")
        else:
            print("Invalid task index.")

    def get_task_by_index(self, task_index):
        try:
            return self.tasks[task_index - 1]
        except IndexError:
            return None

if __name__ == "__main__":
    todo_list = TodoList()

    while True:
        print("\n1. View Tasks")
        print("2. Add Task")
        print("3. Update Task")
        print("4. Delete Task")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            print("\n--- All Tasks ---")
            todo_list.view_tasks()
        elif choice == '2':
            description = input("Enter task description: ")
            due_date = input("Enter due date (DD-MM-YYYY): ")
            todo_list.add_task(description, due_date)
        elif choice == '3':
            todo_list.view_tasks()
            task_index = int(input("Enter the index of the task to update: "))
            new_description = input("Enter new description (press Enter to skip): ")
            new_due_date = input("Enter new due date (YYYY-MM-DD, press Enter to skip): ")
            new_status = input("Enter new status (press Enter to skip): ")
            todo_list.update_task(task_index, new_description, new_due_date, new_status)
        elif choice == '4':
            todo_list.view_tasks()
            task_index = int(input("Enter the index of the task to delete: "))
            todo_list.delete_task(task_index)
        elif choice == '5':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")
