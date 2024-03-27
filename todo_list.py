import json
import os
from datetime import datetime

def validate_date_format(date_text):
    """Check if the date text matches the required date format.

    Args:
        date_text (str): The date string to validate.

    Returns:
        bool: True if the date is in the correct format, False otherwise.
    """
    try:
        datetime.strptime(date_text, "%d-%m-%Y")
        return True
    except ValueError:
        return False
    
class Task:
    """A class to represent a task.

    Attributes:
        description (str): Description of the task.
        due_date (str): The due date of the task in DD-MM-YYYY format.
        status (str): The current status of the task ('pending' by default).
    """

    def __init__(self, description, due_date, status="TODO"):
        """Initialize a Task object with description, due date, and status.

        Args:
            description (str): Description of the task.
            due_date (str): The due date of the task.
            status (str, optional): The current status of the task. Defaults to 'TODO'.
        """
        self.description = description
        self.due_date = due_date
        self.status = status

    def __str__(self):
        """Return a string representation of the task.

        Returns:
            str: A string representing the task details.
        """
        return f"Description: {self.description}\nDue Date: {self.due_date}\nStatus: {self.status}"

class TodoList:
    """A class to represent a list of tasks.

    Attributes:
        filename (str): The name of the file where tasks are saved.
        tasks (list): A list of Task objects.
    """

    def __init__(self, filename="tasks.json"):
        """Initialize a TodoList object with a filename and load tasks.

        Args:
            filename (str, optional): The name of the file where tasks are saved. Defaults to 'tasks.json'.
        """
        self.filename = filename
        self.tasks = self.load_tasks()
        
    def load_tasks(self):
        """Load tasks from a JSON file.

        Returns:
            list: A list of Task objects loaded from the file.
        """
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as file:
                tasks = json.load(file)
            return [Task(task['description'], task['due_date'], task['status']) for task in tasks]
        else:
            return []

    def save_tasks(self):
        """Save tasks to a JSON file."""
        with open(self.filename, 'w') as file:
            json.dump([task.__dict__ for task in self.tasks], file, indent=4)

    def view_tasks(self):
        """Print all tasks in the list."""
        print("\n".join(f"Task {i}:\n{task}" for i, task in enumerate(self.tasks, start=1)) or "No tasks in the list.")

    def add_task(self, description, due_date, status="pending"):
        """Add a new task to the list.

        Args:
            description (str): Description of the task.
            due_date (str): The due date of the task.
            status (str, optional): The current status of the task. Defaults to 'pending'.

        Returns:
            None
        """
        if not validate_date_format(due_date):
            print("Invalid date format. Please use DD-MM-YYYY.")
            return
        new_task = Task(description, due_date, status)
        self.tasks.append(new_task)
        self.save_tasks()
        print("Task added successfully.")

    def update_task(self, task_index, **kwargs):
        """Update an existing task in the list.

        Args:
            task_index (int): The index of the task to update.
            **kwargs: Arbitrary keyword arguments representing task attributes to update.

        Returns:
            None
        """
        task = self.get_task_by_index(task_index)
        if not task:
            print("Invalid task index.")
            return
        for attr, value in kwargs.items():
            if attr == 'new_due_date' and value and not validate_date_format(value):
                print("Invalid date format. Please use DD-MM-YYYY.")
                return
            if attr == 'new_status' and value not in ["pending", "completed"]:
                print("Invalid status. Status should be 'pending' or 'completed'.")
                return
            setattr(task, attr, value)
        self.save_tasks()
        print("Task updated successfully.")

    def delete_task(self, task_index):
        """Delete a task from the list.

        Args:
            task_index (int): The index of the task to delete.

        Returns:
            None
        """
        task = self.get_task_by_index(task_index)
        if task:
            self.tasks.remove(task)
            self.save_tasks()
            print("Task deleted successfully.")
        else:
            print("Invalid task index.")

    def get_task_by_index(self, task_index):
        """Get a task by its index in the list.

        Args:
            task_index (int): The index of the task to retrieve.

        Returns:
            Task: The Task object at the specified index, or None if the index is invalid.
        """
        return self.tasks[task_index - 1] if 0 < task_index <= len(self.tasks) else None

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
            updates = {}
            new_description = input("Enter new description (press Enter to skip): ")
            if new_description:
                updates['new_description'] = new_description
            new_due_date = input("Enter new due date (DD-MM-YYYY, press Enter to skip): ")
            if new_due_date:
                updates['new_due_date'] = new_due_date
            new_status = input("Enter new status (press Enter to skip): ")
            if new_status:
                updates['new_status'] = new_status

            if updates:
                todo_list.update_task(task_index, **updates)
            else:
                print("No updates provided.")
        elif choice == '4':
            todo_list.view_tasks()
            task_index = int(input("Enter the index of the task to delete: "))
            todo_list.delete_task(task_index)
        elif choice == '5':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")
