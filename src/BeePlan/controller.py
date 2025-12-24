"""
BeePlan Controller - Mediator between GUI and Algorithm
This layer connects the GUI with the scheduling algorithm.
"""

from scheduler import generate_schedule, Course, Instructor, Room
from typing import List, Dict, Tuple, Optional


class ScheduleController:
    """
    Controller class that mediates between GUI and scheduling algorithm.
    This ensures separation of concerns while allowing them to work together.
    """
    
    def __init__(self):
        """Initialize the controller."""
        self.courses: List[Course] = []
        self.instructors: List[Instructor] = []
        self.rooms: List[Room] = []
        self.time_slots: List[Tuple[str, str]] = []
        self.schedule: Dict = {}
    
    def set_courses(self, courses: List[Course]) -> None:
        """Set the courses for scheduling."""
        self.courses = courses
    
    def set_instructors(self, instructors: List[Instructor]) -> None:
        """Set the instructors for scheduling."""
        self.instructors = instructors
    
    def set_rooms(self, rooms: List[Room]) -> None:
        """Set the rooms for scheduling."""
        self.rooms = rooms
    
    def set_time_slots(self, time_slots: List[Tuple[str, str]]) -> None:
        """Set the time slots for scheduling."""
        self.time_slots = time_slots
    
    def generate_schedule(self, courses: Optional[List[Course]] = None) -> Dict:
        """
        Generate schedule using the algorithm.
        
        Args:
            courses: Optional list of courses. If None, uses self.courses.
        
        Returns:
            Dictionary mapping (day, hour) to list of (course, room) tuples
        
        Raises:
            ValueError: If required data is missing
            RuntimeError: If schedule cannot be generated
        """
        # Use provided courses or default to self.courses
        courses_to_schedule = courses if courses is not None else self.courses
        
        # Validate data
        if not courses_to_schedule:
            raise ValueError("No courses provided for scheduling.")
        if not self.rooms:
            raise ValueError("No rooms provided for scheduling.")
        if not self.time_slots:
            raise ValueError("No time slots provided for scheduling.")
        
        # Call the algorithm
        schedule = generate_schedule(
            courses_to_schedule,
            self.rooms,
            self.time_slots,
            self.instructors
        )
        
        # Store the schedule
        self.schedule = schedule
        
        return schedule
    
    def get_schedule(self) -> Dict:
        """Get the current schedule."""
        return self.schedule
    
    def validate_schedule_data(self) -> Tuple[bool, Optional[str]]:
        """
        Validate that all required data is present.
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not self.courses:
            return False, "En az bir ders eklenmelidir."
        if not self.rooms:
            return False, "En az bir derslik eklenmelidir."
        if not self.time_slots:
            return False, "Zaman dilimleri ayarlanmalıdır."
        
        return True, None


