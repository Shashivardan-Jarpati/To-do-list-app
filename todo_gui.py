#!/usr/bin/env python3
"""
Graphical User Interface for To-Do List Application
Provides a modern GUI using tkinter for managing tasks
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from task_manager import TaskManager
from datetime import datetime


class TodoGUI:
    """Graphical user interface for the To-Do List application"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List Application")
        self.root.geometry("900x600")
        self.root.configure(bg='#f0f0f0')
        
        self.manager = TaskManager()
        
        # Color scheme
        self.colors = {
            'primary': '#2196F3',
            'success': '#4CAF50',
            'danger': '#f44336',
            'warning': '#FF9800',
            'bg': '#f0f0f0',
            'card': '#ffffff'
        }
        
        self.setup_ui()
        self.refresh_task_list()
    
    def setup_ui(self):
        """Set up the user interface"""
        # Title
        title_frame = tk.Frame(self.root, bg=self.colors['primary'], height=60)
        title_frame.pack(fill='x', side='top')
        
        title_label = tk.Label(
            title_frame,
            text="📋 To-Do List Manager",
            font=('Arial', 20, 'bold'),
            bg=self.colors['primary'],
            fg='white',
            pady=10
        )
        title_label.pack()
        
        # Main container
        main_container = tk.Frame(self.root, bg=self.colors['bg'])
        main_container.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Left panel - Input form
        self.setup_input_panel(main_container)
        
        # Right panel - Task list
        self.setup_task_list_panel(main_container)
        
        # Bottom panel - Statistics and actions
        self.setup_bottom_panel()
    
    def setup_input_panel(self, parent):
        """Set up the input form panel"""
        input_frame = tk.Frame(parent, bg=self.colors['card'], relief='raised', bd=2)
        input_frame.pack(side='left', fill='y', padx=(0, 5), ipadx=10, ipady=10)
        
        # Title
        tk.Label(
            input_frame,
            text="Add New Task",
            font=('Arial', 14, 'bold'),
            bg=self.colors['card']
        ).pack(pady=(10, 20))
        
        # Task Title
        tk.Label(input_frame, text="Task Title:", bg=self.colors['card'], font=('Arial', 10)).pack(anchor='w', padx=10)
        self.title_entry = tk.Entry(input_frame, width=30, font=('Arial', 10))
        self.title_entry.pack(padx=10, pady=(0, 10), fill='x')
        
        # Description
        tk.Label(input_frame, text="Description:", bg=self.colors['card'], font=('Arial', 10)).pack(anchor='w', padx=10)
        self.desc_text = tk.Text(input_frame, width=30, height=4, font=('Arial', 9))
        self.desc_text.pack(padx=10, pady=(0, 10), fill='x')
        
        # Priority
        tk.Label(input_frame, text="Priority:", bg=self.colors['card'], font=('Arial', 10)).pack(anchor='w', padx=10)
        self.priority_var = tk.StringVar(value="Medium")
        priority_frame = tk.Frame(input_frame, bg=self.colors['card'])
        priority_frame.pack(padx=10, pady=(0, 10), fill='x')
        
        for priority in ['Low', 'Medium', 'High']:
            rb = tk.Radiobutton(
                priority_frame,
                text=priority,
                variable=self.priority_var,
                value=priority,
                bg=self.colors['card'],
                font=('Arial', 9)
            )
            rb.pack(side='left', padx=5)
        
        # Due Date
        tk.Label(input_frame, text="Due Date (YYYY-MM-DD):", bg=self.colors['card'], font=('Arial', 10)).pack(anchor='w', padx=10)
        self.due_date_entry = tk.Entry(input_frame, width=30, font=('Arial', 10))
        self.due_date_entry.pack(padx=10, pady=(0, 10), fill='x')
        
        # Add Button
        add_btn = tk.Button(
            input_frame,
            text="➕ Add Task",
            command=self.add_task,
            bg=self.colors['success'],
            fg='white',
            font=('Arial', 11, 'bold'),
            cursor='hand2',
            relief='flat',
            padx=20,
            pady=10
        )
        add_btn.pack(pady=20, padx=10, fill='x')
        
        # Clear Button
        clear_btn = tk.Button(
            input_frame,
            text="🗑️ Clear Form",
            command=self.clear_form,
            bg=self.colors['warning'],
            fg='white',
            font=('Arial', 10),
            cursor='hand2',
            relief='flat',
            padx=20,
            pady=8
        )
        clear_btn.pack(padx=10, fill='x')
    
    def setup_task_list_panel(self, parent):
        """Set up the task list panel"""
        list_frame = tk.Frame(parent, bg=self.colors['card'], relief='raised', bd=2)
        list_frame.pack(side='left', fill='both', expand=True, padx=(5, 0))
        
        # Header with filter
        header_frame = tk.Frame(list_frame, bg=self.colors['card'])
        header_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Label(
            header_frame,
            text="Task List",
            font=('Arial', 14, 'bold'),
            bg=self.colors['card']
        ).pack(side='left')
        
        # Filter dropdown
        tk.Label(header_frame, text="Filter:", bg=self.colors['card'], font=('Arial', 9)).pack(side='left', padx=(20, 5))
        self.filter_var = tk.StringVar(value="All")
        filter_combo = ttk.Combobox(
            header_frame,
            textvariable=self.filter_var,
            values=['All', 'Pending', 'Completed', 'High Priority', 'Medium Priority', 'Low Priority'],
            state='readonly',
            width=15,
            font=('Arial', 9)
        )
        filter_combo.pack(side='left')
        filter_combo.bind('<<ComboboxSelected>>', lambda e: self.refresh_task_list())
        
        # Search
        tk.Label(header_frame, text="Search:", bg=self.colors['card'], font=('Arial', 9)).pack(side='left', padx=(20, 5))
        self.search_var = tk.StringVar()
        self.search_var.trace('w', lambda *args: self.refresh_task_list())
        search_entry = tk.Entry(header_frame, textvariable=self.search_var, width=20, font=('Arial', 9))
        search_entry.pack(side='left')
        
        # Treeview for tasks
        tree_frame = tk.Frame(list_frame, bg=self.colors['card'])
        tree_frame.pack(fill='both', expand=True, padx=10, pady=(0, 10))
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side='right', fill='y')
        
        # Create Treeview
        self.task_tree = ttk.Treeview(
            tree_frame,
            columns=('ID', 'Title', 'Priority', 'Due Date', 'Status'),
            show='headings',
            yscrollcommand=scrollbar.set,
            selectmode='browse'
        )
        scrollbar.config(command=self.task_tree.yview)
        
        # Define columns
        self.task_tree.heading('ID', text='ID')
        self.task_tree.heading('Title', text='Title')
        self.task_tree.heading('Priority', text='Priority')
        self.task_tree.heading('Due Date', text='Due Date')
        self.task_tree.heading('Status', text='Status')
        
        self.task_tree.column('ID', width=50)
        self.task_tree.column('Title', width=250)
        self.task_tree.column('Priority', width=80)
        self.task_tree.column('Due Date', width=100)
        self.task_tree.column('Status', width=80)
        
        self.task_tree.pack(fill='both', expand=True)
        
        # Button frame
        btn_frame = tk.Frame(list_frame, bg=self.colors['card'])
        btn_frame.pack(fill='x', padx=10, pady=(0, 10))
        
        buttons = [
            ("✓ Complete", self.complete_task, self.colors['success']),
            ("↺ Uncomplete", self.uncomplete_task, self.colors['primary']),
            ("✎ Edit", self.edit_task, self.colors['warning']),
            ("✗ Delete", self.delete_task, self.colors['danger']),
        ]
        
        for text, command, color in buttons:
            btn = tk.Button(
                btn_frame,
                text=text,
                command=command,
                bg=color,
                fg='white',
                font=('Arial', 9, 'bold'),
                cursor='hand2',
                relief='flat',
                padx=15,
                pady=5
            )
            btn.pack(side='left', padx=5, expand=True, fill='x')
    
    def setup_bottom_panel(self):
        """Set up the bottom statistics panel"""
        bottom_frame = tk.Frame(self.root, bg=self.colors['primary'], height=50)
        bottom_frame.pack(fill='x', side='bottom')
        
        self.stats_label = tk.Label(
            bottom_frame,
            text="",
            font=('Arial', 10),
            bg=self.colors['primary'],
            fg='white',
            pady=10
        )
        self.stats_label.pack()
        
        self.update_statistics()
    
    def add_task(self):
        """Add a new task"""
        title = self.title_entry.get().strip()
        if not title:
            messagebox.showerror("Error", "Task title cannot be empty!")
            return
        
        description = self.desc_text.get('1.0', 'end-1c').strip()
        priority = self.priority_var.get()
        due_date = self.due_date_entry.get().strip()
        
        self.manager.add_task(title, description, priority, due_date)
        messagebox.showinfo("Success", "Task added successfully!")
        
        self.clear_form()
        self.refresh_task_list()
        self.update_statistics()
    
    def clear_form(self):
        """Clear the input form"""
        self.title_entry.delete(0, 'end')
        self.desc_text.delete('1.0', 'end')
        self.priority_var.set("Medium")
        self.due_date_entry.delete(0, 'end')
    
    def refresh_task_list(self):
        """Refresh the task list based on current filter"""
        # Clear existing items
        for item in self.task_tree.get_children():
            self.task_tree.delete(item)
        
        # Get tasks based on filter
        filter_value = self.filter_var.get()
        search_query = self.search_var.get().strip()
        
        if search_query:
            tasks = self.manager.search_tasks(search_query)
        elif filter_value == "All":
            tasks = self.manager.get_all_tasks()
        elif filter_value == "Pending":
            tasks = self.manager.get_all_tasks(include_completed=False)
        elif filter_value == "Completed":
            tasks = [t for t in self.manager.get_all_tasks() if t.completed]
        elif filter_value.endswith("Priority"):
            priority = filter_value.split()[0]
            tasks = self.manager.get_tasks_by_priority(priority)
        else:
            tasks = self.manager.get_all_tasks()
        
        # Add tasks to treeview
        for task in tasks:
            status = "✓ Done" if task.completed else "✗ Pending"
            self.task_tree.insert('', 'end', values=(
                task.id,
                task.title,
                task.priority,
                task.due_date,
                status
            ))
        
        self.update_statistics()
    
    def get_selected_task_id(self):
        """Get the ID of the selected task"""
        selection = self.task_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a task first!")
            return None
        
        item = self.task_tree.item(selection[0])
        return item['values'][0]
    
    def complete_task(self):
        """Mark selected task as completed"""
        task_id = self.get_selected_task_id()
        if task_id:
            if self.manager.complete_task(task_id):
                messagebox.showinfo("Success", "Task marked as completed!")
                self.refresh_task_list()
    
    def uncomplete_task(self):
        """Mark selected task as not completed"""
        task_id = self.get_selected_task_id()
        if task_id:
            if self.manager.uncomplete_task(task_id):
                messagebox.showinfo("Success", "Task marked as pending!")
                self.refresh_task_list()
    
    def edit_task(self):
        """Edit selected task"""
        task_id = self.get_selected_task_id()
        if not task_id:
            return
        
        task = self.manager.get_task(task_id)
        if not task:
            messagebox.showerror("Error", "Task not found!")
            return
        
        # Create edit dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("Edit Task")
        dialog.geometry("400x400")
        dialog.configure(bg=self.colors['bg'])
        
        # Title
        tk.Label(dialog, text="Title:", bg=self.colors['bg']).pack(anchor='w', padx=10, pady=(10, 0))
        title_entry = tk.Entry(dialog, width=40)
        title_entry.insert(0, task.title)
        title_entry.pack(padx=10, pady=(0, 10), fill='x')
        
        # Description
        tk.Label(dialog, text="Description:", bg=self.colors['bg']).pack(anchor='w', padx=10)
        desc_text = tk.Text(dialog, width=40, height=5)
        desc_text.insert('1.0', task.description)
        desc_text.pack(padx=10, pady=(0, 10), fill='x')
        
        # Priority
        tk.Label(dialog, text="Priority:", bg=self.colors['bg']).pack(anchor='w', padx=10)
        priority_var = tk.StringVar(value=task.priority)
        priority_frame = tk.Frame(dialog, bg=self.colors['bg'])
        priority_frame.pack(padx=10, pady=(0, 10), fill='x')
        
        for priority in ['Low', 'Medium', 'High']:
            tk.Radiobutton(priority_frame, text=priority, variable=priority_var, value=priority, bg=self.colors['bg']).pack(side='left', padx=5)
        
        # Due Date
        tk.Label(dialog, text="Due Date:", bg=self.colors['bg']).pack(anchor='w', padx=10)
        due_date_entry = tk.Entry(dialog, width=40)
        due_date_entry.insert(0, task.due_date)
        due_date_entry.pack(padx=10, pady=(0, 10), fill='x')
        
        # Save button
        def save_changes():
            new_title = title_entry.get().strip()
            if not new_title:
                messagebox.showerror("Error", "Title cannot be empty!")
                return
            
            self.manager.update_task(
                task_id,
                title=new_title,
                description=desc_text.get('1.0', 'end-1c').strip(),
                priority=priority_var.get(),
                due_date=due_date_entry.get().strip()
            )
            messagebox.showinfo("Success", "Task updated successfully!")
            dialog.destroy()
            self.refresh_task_list()
        
        tk.Button(
            dialog,
            text="Save Changes",
            command=save_changes,
            bg=self.colors['success'],
            fg='white',
            font=('Arial', 10, 'bold'),
            cursor='hand2',
            relief='flat',
            padx=20,
            pady=10
        ).pack(pady=20)
    
    def delete_task(self):
        """Delete selected task"""
        task_id = self.get_selected_task_id()
        if not task_id:
            return
        
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this task?"):
            if self.manager.delete_task(task_id):
                messagebox.showinfo("Success", "Task deleted successfully!")
                self.refresh_task_list()
    
    def update_statistics(self):
        """Update the statistics display"""
        stats = self.manager.get_statistics()
        stats_text = f"Total: {stats['total']} | Completed: {stats['completed']} | Pending: {stats['pending']} | High: {stats['priority_counts']['High']} | Medium: {stats['priority_counts']['Medium']} | Low: {stats['priority_counts']['Low']}"
        self.stats_label.config(text=stats_text)


def main():
    """Entry point for the GUI application"""
    root = tk.Tk()
    app = TodoGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
