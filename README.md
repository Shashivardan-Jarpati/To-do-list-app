To-Do List Application
A comprehensive task management application with both Command-Line Interface (CLI) and
Graphical User Interface (GUI) built using Python.
Features
• Create tasks with title, description, priority, and due date
• Update existing tasks
• Delete tasks
• Mark tasks as completed or pending
• Search tasks by title or description
• Filter tasks by priority or status
• View task statistics
• Automatic data persistence using JSON
Priority Levels
High – Urgent and important tasks
Medium – Regular priority tasks
Low – Less urgent tasks
Project Structure
task_manager.py – Core task logic and data persistence
todo_cli.py – Command-line interface
todo_gui.py – Graphical user interface (tkinter)
requirements.txt – Project requirements
tasks.json – Auto-generated task data file
Installation
Prerequisites:
• Python 3.7 or higher
• tkinter (comes with Python)
Run the application from the project directory. No external libraries are required.
How to Run
GUI Version:
python todo_gui.py
CLI Version:
python todo_cli.py
Data Storage
All tasks are automatically saved in tasks.json. The file is created on first run and updated after
every change.
Technical Overview
This project demonstrates object-oriented programming, file handling with JSON, GUI development
using tkinter, and CLI-based application design