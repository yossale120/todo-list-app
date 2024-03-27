# Todo List Application

This is a simple Python application for managing a todo list. It allows users to view, add, update, and delete tasks from the list.


## Features
- View Tasks: Display all tasks in the list with their descriptions, due dates, and statuses.
- Add Task: Add a new task to the list with a description, due date, and optional status.
- Update Task: Modify an existing task in the list by providing its index and the attributes to  update (description, due date, or status).
- Delete Task: Remove a task from the list by specifying its index.

## Usage
- View Tasks: Choose option 1 to view all tasks in the list.
- Add Task: Select option 2 and provide a description, due date (in DD-MM-YYYY format), and optional status for the new task.
- Update Task: Choose option 3, enter the index of the task you want to update, and follow the prompts to provide new values for the task attributes.
- Delete Task: Pick option 4, input the index of the task you wish to delete, and confirm the deletion.

## Date Format
The application expects due dates to be provided in the format DD-MM-YYYY (e.g., 31-12-2024).

## Status Options
Tasks can have two statuses: "pending" (default) or "completed". When adding or updating a task, you can specify the status as "pending" or "completed".

## File Storage
Tasks are stored in a JSON file named tasks.json by default. The application automatically loads tasks from this file when started and saves any modifications back to it when tasks are added, updated, or deleted.
