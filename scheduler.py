"""
Project: BeePlan
Goal: Generate a conflict-free course schedule using a backtracking algorithm.

CONSTRAINTS & RULES:
1. No courses between 13:20-15:10 on Fridays (Exam Period).
2. A lecturer can teach max 4 hours of theory per day.
3. Lab sessions must strictly follow theory hours (e.g., Theory at 10:00, Lab at 11:00).
4. 3rd-year courses must not overlap with departmental electives.
5. CENG and SENG electives must not overlap.
6. Lab capacity must not exceed 40 students.

INPUT DATA STRUCTURE:
- Courses have: name, instructor, hours, type (Theory/Lab), year.
- Rooms have: capacity, type.
"""

from collections import defaultdict

class Course:
    """Represents a course with its attributes."""
    def __init__(self, course_id, name, instructor, hours, course_type, year):
        self.course_id = course_id
        self.name = name
        self.instructor = instructor
        self.hours = hours
        self.course_type = course_type  # 'theory' or 'lab'
        self.year = year  # e.g., 1, 2, 3

    def __repr__(self):
        return f"{self.name} ({self.course_type}, {self.hours}h)"


def is_exam_block(day, start_hour):
    """Checks if the given time falls within the exam block."""
    return day == "Friday" and 13.33 <= start_hour < 15.17


def exceeds_daily_theory_limit(schedule, instructor, day):
    """Checks if an instructor exceeds the daily theory limit."""
    total_hours = sum(
        course.hours for course in schedule.get((day, instructor), [])
        if course.course_type == 'theory'
    )
    return total_hours > 4


def is_valid_assignment(schedule, course, day, start_hour, room):
    """Validates if a course can be scheduled in the given slot."""
    # Check exam block constraint
    if is_exam_block(day, start_hour):
        return False

    # Check instructor's daily theory limit
    if exceeds_daily_theory_limit(schedule, course.instructor, day):
        return False

    # Check for instructor overlap
    if any(scheduled_course.instructor == course.instructor
           for scheduled_course, _ in schedule.get((day, start_hour), [])):
        return False

    # Check for room double booking
    if any(scheduled_room == room
           for _, scheduled_room in schedule.get((day, start_hour), [])):
        return False

    return True


def generate_schedule(courses, rooms, time_slots):
    """
    Generates a conflict-free schedule using backtracking.
    Returns the schedule if successful, otherwise None.
    """
    if not courses or not rooms or not time_slots:
        raise ValueError("Courses, rooms, and time slots must be non-empty lists.")

    schedule = defaultdict(list)

    def backtrack(course_index):
        # Base case: all courses are scheduled
        if course_index == len(courses):
            return True

        course = courses[course_index]

        # Try all combinations of day, start_hour, and room
        for day, start_hour in time_slots:
            for room in rooms:
                if is_valid_assignment(schedule, course, day, start_hour, room):
                    # Assign the course to the schedule
                    schedule[(day, start_hour)].append((course, room))

                    # Recur to schedule the next course
                    if backtrack(course_index + 1):
                        return True

                    # Backtrack: remove the course from the schedule
                    schedule[(day, start_hour)].remove((course, room))

        return False

    # Start the backtracking process
    if backtrack(0):
        return schedule

    raise RuntimeError("No valid schedule could be generated.")
