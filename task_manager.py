"""
Task Manager Module
Handles all task-related operations including CRUD operations and persistence
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Optional


class Task:
    """Represents a single task with all its properties"""
    
    def __init__(self, title: str, description: str = "", priority: str = "Medium", 
                 due_date: str = "", task_id: Optional[int] = None):
        self.id = task_id if task_id is not None else id(self)
        self.title = title
        self.description = description
        self.priority = priority  # Low, Medium, High
        self.due_date = due_date
        self.completed = False
        self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
    def to_dict(self) -> Dict:
        """Convert task to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'priority': self.priority,
            'due_date': self.due_date,
            'completed': self.completed,
            'created_at': self.created_at
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Task':
        """Create task from dictionary"""
        task = cls(
            title=data['title'],
            description=data.get('description', ''),
            priority=data.get('priority', 'Medium'),
            due_date=data.get('due_date', ''),
            task_id=data.get('id')
        )
        task.completed = data.get('completed', False)
        task.created_at = data.get('created_at', datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        return task
    
    def __str__(self) -> str:
        status = "✓" if self.completed else "✗"
        return f"[{status}] {self.title} (Priority: {self.priority})"


class TaskManager:
    """Manages the collection of tasks and handles persistence"""
    
    def __init__(self, filename: str = "tasks.json"):
        self.filename = filename
        self.tasks: List[Task] = []
        self.load_tasks()
    
    def add_task(self, title: str, description: str = "", priority: str = "Medium", 
                 due_date: str = "") -> Task:
        """Add a new task to the list"""
        task = Task(title, description, priority, due_date)
        self.tasks.append(task)
        self.save_tasks()
        return task
    
    def get_task(self, task_id: int) -> Optional[Task]:
        """Get a task by its ID"""
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None
    
    def update_task(self, task_id: int, **kwargs) -> bool:
        """Update a task's properties"""
        task = self.get_task(task_id)
        if not task:
            return False
        
        for key, value in kwargs.items():
            if hasattr(task, key):
                setattr(task, key, value)
        
        self.save_tasks()
        return True
    
    def delete_task(self, task_id: int) -> bool:
        """Delete a task by its ID"""
        task = self.get_task(task_id)
        if task:
            self.tasks.remove(task)
            self.save_tasks()
            return True
        return False
    
    def complete_task(self, task_id: int) -> bool:
        """Mark a task as completed"""
        task = self.get_task(task_id)
        if task:
            task.completed = True
            self.save_tasks()
            return True
        return False
    
    def uncomplete_task(self, task_id: int) -> bool:
        """Mark a task as not completed"""
        task = self.get_task(task_id)
        if task:
            task.completed = False
            self.save_tasks()
            return True
        return False
    
    def get_all_tasks(self, include_completed: bool = True) -> List[Task]:
        """Get all tasks, optionally filtering out completed ones"""
        if include_completed:
            return self.tasks
        return [task for task in self.tasks if not task.completed]
    
    def get_tasks_by_priority(self, priority: str) -> List[Task]:
        """Get all tasks with a specific priority"""
        return [task for task in self.tasks if task.priority == priority]
    
    def search_tasks(self, query: str) -> List[Task]:
        """Search tasks by title or description"""
        query = query.lower()
        return [task for task in self.tasks 
                if query in task.title.lower() or query in task.description.lower()]
    
    def save_tasks(self):
        """Save tasks to JSON file"""
        data = [task.to_dict() for task in self.tasks]
        with open(self.filename, 'w') as f:
            json.dump(data, f, indent=2)
    
    def load_tasks(self):
        """Load tasks from JSON file"""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as f:
                    data = json.load(f)
                    self.tasks = [Task.from_dict(task_data) for task_data in data]
            except (json.JSONDecodeError, KeyError):
                self.tasks = []
        else:
            self.tasks = []
    
    def get_statistics(self) -> Dict:
        """Get statistics about tasks"""
        total = len(self.tasks)
        completed = sum(1 for task in self.tasks if task.completed)
        pending = total - completed
        
        priority_counts = {
            'High': sum(1 for task in self.tasks if task.priority == 'High' and not task.completed),
            'Medium': sum(1 for task in self.tasks if task.priority == 'Medium' and not task.completed),
            'Low': sum(1 for task in self.tasks if task.priority == 'Low' and not task.completed)
        }
        
        return {
            'total': total,
            'completed': completed,
            'pending': pending,
            'priority_counts': priority_counts
        }
