#!/usr/bin/env python3
"""
Command Line Interface for To-Do List Application
Provides an interactive terminal-based interface for managing tasks
"""

import sys
from task_manager import TaskManager


class TodoCLI:
    """Command-line interface for the To-Do List application"""
    
    def __init__(self):
        self.manager = TaskManager()
        self.running = True
    
    def display_menu(self):
        """Display the main menu"""
        print("\n" + "="*50)
        print("           TO-DO LIST APPLICATION")
        print("="*50)
        print("1.  Add New Task")
        print("2.  View All Tasks")
        print("3.  View Pending Tasks")
        print("4.  View Completed Tasks")
        print("5.  Complete Task")
        print("6.  Uncomplete Task")
        print("7.  Update Task")
        print("8.  Delete Task")
        print("9.  Search Tasks")
        print("10. Filter by Priority")
        print("11. View Statistics")
        print("0.  Exit")
        print("="*50)
    
    def add_task(self):
        """Add a new task"""
        print("\n--- Add New Task ---")
        title = input("Enter task title: ").strip()
        if not title:
            print("❌ Task title cannot be empty!")
            return
        
        description = input("Enter task description (optional): ").strip()
        
        print("\nPriority levels: Low, Medium, High")
        priority = input("Enter priority (default: Medium): ").strip() or "Medium"
        if priority not in ['Low', 'Medium', 'High']:
            print("⚠️  Invalid priority. Setting to Medium.")
            priority = "Medium"
        
        due_date = input("Enter due date (YYYY-MM-DD) (optional): ").strip()
        
        task = self.manager.add_task(title, description, priority, due_date)
        print(f"✅ Task added successfully! ID: {task.id}")
    
    def view_tasks(self, task_list=None, title="All Tasks"):
        """Display tasks in a formatted table"""
        if task_list is None:
            task_list = self.manager.get_all_tasks()
        
        if not task_list:
            print(f"\n📋 No tasks to display in '{title}'")
            return
        
        print(f"\n{'='*80}")
        print(f"{title:^80}")
        print(f"{'='*80}")
        print(f"{'ID':<10} {'Status':<8} {'Title':<25} {'Priority':<10} {'Due Date':<15}")
        print(f"{'-'*80}")
        
        for task in task_list:
            status = "✓ Done" if task.completed else "✗ Pending"
            title_short = task.title[:22] + "..." if len(task.title) > 25 else task.title
            print(f"{task.id:<10} {status:<8} {title_short:<25} {task.priority:<10} {task.due_date:<15}")
        
        print(f"{'='*80}")
        print(f"Total: {len(task_list)} tasks")
    
    def view_all_tasks(self):
        """View all tasks"""
        self.view_tasks(self.manager.get_all_tasks(), "All Tasks")
    
    def view_pending_tasks(self):
        """View only pending tasks"""
        self.view_tasks(self.manager.get_all_tasks(include_completed=False), "Pending Tasks")
    
    def view_completed_tasks(self):
        """View only completed tasks"""
        completed = [t for t in self.manager.get_all_tasks() if t.completed]
        self.view_tasks(completed, "Completed Tasks")
    
    def complete_task(self):
        """Mark a task as completed"""
        self.view_pending_tasks()
        try:
            task_id = int(input("\nEnter task ID to mark as completed: "))
            if self.manager.complete_task(task_id):
                print("✅ Task marked as completed!")
            else:
                print("❌ Task not found!")
        except ValueError:
            print("❌ Invalid task ID!")
    
    def uncomplete_task(self):
        """Mark a task as not completed"""
        completed = [t for t in self.manager.get_all_tasks() if t.completed]
        self.view_tasks(completed, "Completed Tasks")
        try:
            task_id = int(input("\nEnter task ID to mark as pending: "))
            if self.manager.uncomplete_task(task_id):
                print("✅ Task marked as pending!")
            else:
                print("❌ Task not found!")
        except ValueError:
            print("❌ Invalid task ID!")
    
    def update_task(self):
        """Update a task's details"""
        self.view_all_tasks()
        try:
            task_id = int(input("\nEnter task ID to update: "))
            task = self.manager.get_task(task_id)
            
            if not task:
                print("❌ Task not found!")
                return
            
            print(f"\nCurrent task details:")
            print(f"Title: {task.title}")
            print(f"Description: {task.description}")
            print(f"Priority: {task.priority}")
            print(f"Due Date: {task.due_date}")
            
            print("\nEnter new values (press Enter to keep current value):")
            
            title = input(f"Title [{task.title}]: ").strip()
            description = input(f"Description [{task.description}]: ").strip()
            priority = input(f"Priority [{task.priority}]: ").strip()
            due_date = input(f"Due Date [{task.due_date}]: ").strip()
            
            updates = {}
            if title: updates['title'] = title
            if description: updates['description'] = description
            if priority: updates['priority'] = priority
            if due_date: updates['due_date'] = due_date
            
            if updates:
                self.manager.update_task(task_id, **updates)
                print("✅ Task updated successfully!")
            else:
                print("ℹ️  No changes made.")
                
        except ValueError:
            print("❌ Invalid task ID!")
    
    def delete_task(self):
        """Delete a task"""
        self.view_all_tasks()
        try:
            task_id = int(input("\nEnter task ID to delete: "))
            confirm = input(f"Are you sure you want to delete task {task_id}? (yes/no): ").lower()
            
            if confirm in ['yes', 'y']:
                if self.manager.delete_task(task_id):
                    print("✅ Task deleted successfully!")
                else:
                    print("❌ Task not found!")
            else:
                print("ℹ️  Deletion cancelled.")
                
        except ValueError:
            print("❌ Invalid task ID!")
    
    def search_tasks(self):
        """Search for tasks"""
        query = input("\nEnter search query: ").strip()
        if not query:
            print("❌ Search query cannot be empty!")
            return
        
        results = self.manager.search_tasks(query)
        self.view_tasks(results, f"Search Results for '{query}'")
    
    def filter_by_priority(self):
        """Filter tasks by priority"""
        print("\nPriority levels: Low, Medium, High")
        priority = input("Enter priority to filter: ").strip()
        
        if priority not in ['Low', 'Medium', 'High']:
            print("❌ Invalid priority level!")
            return
        
        results = self.manager.get_tasks_by_priority(priority)
        self.view_tasks(results, f"{priority} Priority Tasks")
    
    def view_statistics(self):
        """Display task statistics"""
        stats = self.manager.get_statistics()
        
        print("\n" + "="*50)
        print("           TASK STATISTICS")
        print("="*50)
        print(f"Total Tasks:      {stats['total']}")
        print(f"Completed Tasks:  {stats['completed']}")
        print(f"Pending Tasks:    {stats['pending']}")
        print("\nPending by Priority:")
        print(f"  High Priority:   {stats['priority_counts']['High']}")
        print(f"  Medium Priority: {stats['priority_counts']['Medium']}")
        print(f"  Low Priority:    {stats['priority_counts']['Low']}")
        print("="*50)
    
    def run(self):
        """Main application loop"""
        print("\n🎯 Welcome to the To-Do List Application!")
        
        while self.running:
            self.display_menu()
            choice = input("\nEnter your choice: ").strip()
            
            if choice == '1':
                self.add_task()
            elif choice == '2':
                self.view_all_tasks()
            elif choice == '3':
                self.view_pending_tasks()
            elif choice == '4':
                self.view_completed_tasks()
            elif choice == '5':
                self.complete_task()
            elif choice == '6':
                self.uncomplete_task()
            elif choice == '7':
                self.update_task()
            elif choice == '8':
                self.delete_task()
            elif choice == '9':
                self.search_tasks()
            elif choice == '10':
                self.filter_by_priority()
            elif choice == '11':
                self.view_statistics()
            elif choice == '0':
                print("\n👋 Thank you for using To-Do List Application!")
                self.running = False
            else:
                print("\n❌ Invalid choice! Please try again.")
            
            if self.running and choice != '0':
                input("\nPress Enter to continue...")


def main():
    """Entry point for the CLI application"""
    try:
        app = TodoCLI()
        app.run()
    except KeyboardInterrupt:
        print("\n\n👋 Application terminated by user.")
        sys.exit(0)


if __name__ == "__main__":
    main()
