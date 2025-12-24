"""
KidTask Controller - Mediator between GUI and Business Logic
This layer connects the GUI with the application logic.
"""

from kidtask_app import KidTaskApp
from user import User, UserRole
from task import Task
from wish import Wish
from datetime import datetime
from typing import Optional, List


class KidTaskController:
    """
    Controller class that mediates between GUI and business logic.
    This ensures separation of concerns while allowing them to work together.
    """
    
    def __init__(self, data_dir: str = "data"):
        """Initialize the controller with business logic."""
        self.app = KidTaskApp(data_dir)
        self.app.load_data()
        self.current_user: Optional[User] = None
    
    def login(self, username: str, password: str) -> Optional[User]:
        """
        Authenticate user.
        
        Args:
            username: Username
            password: Password
        
        Returns:
            User object if successful, None otherwise
        """
        user = self.app.find_user(username)
        if user and user.password == password:
            self.current_user = user
            return user
        return None
    
    def logout(self) -> None:
        """Logout current user and save data."""
        self.app.save_data()
        self.current_user = None
    
    def get_current_user(self) -> Optional[User]:
        """Get the current logged-in user."""
        return self.current_user
    
    def get_tasks(self, child_username: Optional[str] = None) -> List[Task]:
        """
        Get tasks for current user or specific child.
        
        Args:
            child_username: Optional child username (for Parent/Teacher)
        
        Returns:
            List of tasks
        """
        if self.current_user.role == UserRole.CHILD:
            return [t for t in self.app.tasks if t.child_username == self.current_user.username]
        elif child_username:
            return [t for t in self.app.tasks if t.child_username == child_username]
        else:
            return self.app.tasks
    
    def get_wishes(self, child_username: Optional[str] = None) -> List[Wish]:
        """
        Get wishes for current user or specific child.
        
        Args:
            child_username: Optional child username (for Parent/Teacher)
        
        Returns:
            List of wishes
        """
        if self.current_user.role == UserRole.CHILD:
            # Children only see wishes at their level
            child = self.current_user
            return [w for w in self.app.wishes 
                   if w.child_username == child.username and w.required_level <= child.level]
        elif child_username:
            return [w for w in self.app.wishes if w.child_username == child_username]
        else:
            return self.app.wishes
    
    def add_task(self, title: str, description: str, due_date: datetime, 
                 points: int, child_username: str) -> Task:
        """
        Add a new task.
        
        Args:
            title: Task title
            description: Task description
            due_date: Due date
            points: Points for the task
            child_username: Child username to assign task to
        
        Returns:
            Created Task object
        """
        created_by = self.current_user.username
        task = self.app.add_task(title, description, due_date, points, child_username, created_by)
        self.app.save_data()
        return task
    
    def complete_task(self, task_id: int) -> bool:
        """
        Mark a task as completed.
        
        Args:
            task_id: Task ID
        
        Returns:
            True if successful, False otherwise
        """
        task = self.app.find_task(task_id)
        if task and self.current_user.role == UserRole.CHILD:
            task.mark_completed()
            self.app.save_data()
            return True
        return False
    
    def approve_task(self, task_id: int, rating: float, child_username: Optional[str] = None) -> bool:
        """
        Approve a task.
        
        Args:
            task_id: Task ID
            rating: Rating (0-100)
            child_username: Optional child username
        
        Returns:
            True if successful, False otherwise
        """
        try:
            approver_role = self.current_user.role
            self.app.approve_task(task_id, rating, approver_role, child_username)
            self.app.save_data()
            return True
        except ValueError:
            return False
    
    def add_wish(self, description: str, cost: int, required_level: int, 
                 wish_type: str = "product") -> Wish:
        """
        Add a new wish.
        
        Args:
            description: Wish description
            cost: Wish cost in points
            required_level: Required level
            wish_type: Wish type (product/activity)
        
        Returns:
            Created Wish object
        """
        child_username = self.current_user.username
        wish = self.app.add_wish(description, cost, required_level, child_username, wish_type)
        self.app.save_data()
        return wish
    
    def approve_wish(self, wish_id: int) -> bool:
        """
        Approve a wish.
        
        Args:
            wish_id: Wish ID
        
        Returns:
            True if successful, False otherwise
        """
        try:
            approver_role = self.current_user.role
            self.app.approve_wish(wish_id, approver_role)
            self.app.save_data()
            return True
        except ValueError:
            return False
    
    def get_children(self) -> List[User]:
        """Get all child users."""
        return [u for u in self.app.users if u.role == UserRole.CHILD]
    
    def save_data(self) -> None:
        """Save all data."""
        self.app.save_data()


