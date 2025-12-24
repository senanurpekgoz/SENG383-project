"""
Project: BeePlan - Çankaya Üniversitesi Ders Programı Hazırlama Sistemi
Goal: Generate a conflict-free course schedule using a backtracking algorithm.

CONSTRAINTS & RULES (Hard Constraints):
1. Günlük Sınır: Bir hoca günde en fazla 4 saat teorik ders verebilir.
2. Cuma Kısıtı: Cuma günleri 13:20 - 15:10 arası "Ortak Sınavlar" için ayrılmıştır, ders konulamaz.
3. Lab Sıralama: Lab dersleri kesinlikle teorik derslerden sonra planlanmalı ve ardışık 2 saat olmalıdır.
4. Çakışma Önleme: Aynı sınıf seviyesindeki zorunlu dersler ve aynı hocanın farklı dersleri asla çakışmamalıdır.
5. Kapasite: Lab derslerinde bir şube 40 öğrenciyi geçemez.
6. CENG ve SENG seçmeli derslerinin çakışmaması önceliği.
"""

from collections import defaultdict
from typing import List, Dict, Tuple, Optional


class Course:
    """Represents a course with its attributes."""
    def __init__(self, course_id, code, name, instructor, hours, course_type, year, 
                 is_mandatory=True, sections=1, capacity=40, department="SENG",
                 is_graduate=False, credits=None, groups=None, fixed_time_slot=None):
        self.course_id = course_id
        self.code = code  # e.g., "SENG101", "CENG201", "PHYS101"
        self.name = name
        self.instructor = instructor
        self.hours = hours  # Weekly hours (kept for backward compatibility)
        self.course_type = course_type.lower()  # 'theory' or 'lab'
        self.year = year  # 1, 2, 3, 4
        self.is_mandatory = is_mandatory  # True for mandatory, False for elective
        self.sections = sections  # Number of sections
        self.capacity = capacity  # Max students per section
        self.department = department  # SENG, CENG, PHYS, MATH, ENG, TURK, HIST, BIO, ESR
        self.is_graduate = is_graduate  # True for graduate courses
        self.credits = credits  # Credit hours (e.g., "3+2" means 3 theory + 2 lab)
        self.groups = groups if groups else []  # List of groups (e.g., ["G1", "G2"]) for multi-department courses
        self.fixed_time_slot = fixed_time_slot  # Fixed time slot (day, start_hour) if course has predetermined schedule
        
        # Parse credits to get theory and lab hours
        self.theory_hours = 0
        self.lab_hours = 0
        if credits:
            self.parse_credits(credits)
        else:
            # If no credits, use hours based on course type
            if self.course_type == 'theory':
                self.theory_hours = hours
                self.lab_hours = 0
            else:
                self.theory_hours = 0
                self.lab_hours = hours
        
        # Check if this is a common course (should be prioritized)
        self.is_common_course = department in ["PHYS", "MATH", "ENG", "TURK", "HIST"]
    
    def parse_credits(self, credits_str):
        """Parse credits string like '3+2' to theory_hours and lab_hours."""
        try:
            if '+' in credits_str:
                parts = credits_str.split('+')
                self.theory_hours = int(parts[0].strip())
                self.lab_hours = int(parts[1].strip())
            else:
                # If no +, assume it's all theory
                self.theory_hours = int(credits_str.strip())
                self.lab_hours = 0
        except (ValueError, IndexError):
            # If parsing fails, use the hours value
            if self.course_type == 'theory':
                self.theory_hours = self.hours
                self.lab_hours = 0
            else:
                self.theory_hours = 0
                self.lab_hours = self.hours

    def __repr__(self):
        return f"{self.code} - {self.name} ({self.course_type}, {self.hours}h, Y{self.year})"


class Instructor:
    """Represents an instructor with their constraints."""
    def __init__(self, name, max_daily_theory_hours=4, is_part_time=False, 
                 exclude_graduate_from_limit=False):
        self.name = name
        self.max_daily_theory_hours = max_daily_theory_hours
        self.is_part_time = is_part_time  # Part-time instructors have flexible scheduling
        self.exclude_graduate_from_limit = exclude_graduate_from_limit  # For heavy load instructors
        
    def __repr__(self):
        return self.name


class Room:
    """Represents a room with its capacity and type."""
    def __init__(self, room_id, name, capacity, room_type="theory"):
        self.room_id = room_id
        self.name = name
        self.capacity = capacity
        self.room_type = room_type.lower()  # 'theory' or 'lab'
        
    def __repr__(self):
        return f"{self.name} ({self.room_type}, cap:{self.capacity})"


def time_to_decimal(time_str):
    """Convert time string (HH:MM) to decimal hours."""
    if isinstance(time_str, (int, float)):
        return float(time_str)
    parts = time_str.split(':')
    return float(parts[0]) + float(parts[1]) / 60.0


def is_exam_block(day, start_hour):
    """Checks if the given time falls within the exam block (Friday 13:20-15:10)."""
    if day.lower() != "friday":
        return False
    start_decimal = time_to_decimal(start_hour)
    # 13:20 = 13.33, 15:10 = 15.17
    return 13.33 <= start_decimal < 15.17


def exceeds_daily_theory_limit(schedule, course, instructor_obj, day):
    """Checks if an instructor exceeds the daily theory limit (4 hours).
    
    For instructors with exclude_graduate_from_limit=True, graduate courses
    are not counted towards the 4-hour limit.
    """
    total_hours = 0
    for (sched_day, sched_hour), entries in schedule.items():
        if sched_day == day:
            for scheduled_course, _ in entries:
                if (scheduled_course.instructor == course.instructor and 
                    scheduled_course.course_type == 'theory'):
                    # If excluding graduate courses and this is a graduate course, skip
                    if (instructor_obj and instructor_obj.exclude_graduate_from_limit and 
                        scheduled_course.is_graduate):
                        continue
                    total_hours += scheduled_course.theory_hours
    
    # Also count the current course being scheduled
    if course.course_type == 'theory':
        if not (instructor_obj and instructor_obj.exclude_graduate_from_limit and course.is_graduate):
            total_hours += course.theory_hours
    
    max_hours = instructor_obj.max_daily_theory_hours if instructor_obj else 4
    return total_hours > max_hours


def has_instructor_conflict(schedule, course, day, start_hour):
    """Check if instructor has another course at the same time."""
    for scheduled_course, _ in schedule.get((day, start_hour), []):
        if scheduled_course.instructor == course.instructor:
            return True
    return False


def has_room_conflict(schedule, room, day, start_hour):
    """Check if room is already booked at the same time."""
    for _, scheduled_room in schedule.get((day, start_hour), []):
        if scheduled_room.name == room.name:
            return True
    return False


def has_year_mandatory_conflict(schedule, course, day, start_hour):
    """Check if same year mandatory courses conflict."""
    if not course.is_mandatory:
        return False
    
    for scheduled_course, _ in schedule.get((day, start_hour), []):
        if (scheduled_course.year == course.year and 
            scheduled_course.is_mandatory and 
            scheduled_course.course_id != course.course_id):
            return True
    return False


def has_elective_conflict(schedule, course, day, start_hour):
    """Check if CENG and SENG electives conflict.
    
    Special attention: 3rd year technical electives should not conflict
    to allow students to choose them.
    Also: 3rd-year courses should not overlap with electives.
    """
    for scheduled_course, _ in schedule.get((day, start_hour), []):
        # CENG and SENG electives should not conflict
        if (not course.is_mandatory and not scheduled_course.is_mandatory):
            if ((course.department == "CENG" and scheduled_course.department == "SENG") or
                (course.department == "SENG" and scheduled_course.department == "CENG")):
                return True
            
            # 3rd year technical electives should not conflict with each other
            if (course.year == 3 and scheduled_course.year == 3 and
                course.department in ["SENG", "CENG"] and 
                scheduled_course.department in ["SENG", "CENG"]):
                return True
        
        # 3rd-year courses should not overlap with electives
        if ((course.year == 3 and not scheduled_course.is_mandatory) or
            (scheduled_course.year == 3 and not course.is_mandatory)):
            return True
    
    return False


def find_corresponding_theory_course(lab_course, all_courses):
    """Find the corresponding theory course for a lab course."""
    # Remove common lab suffixes from lab code
    lab_code_base = lab_course.code.replace('L', '').replace('Lab', '').replace('LAB', '').strip()
    
    for course in all_courses:
        if (course.course_type == 'theory' and
            course.year == lab_course.year and
            course.instructor == lab_course.instructor):
            # Check if codes match
            theory_code = course.code.strip()
            if (lab_code_base in theory_code or 
                theory_code in lab_code_base or
                theory_code.replace('T', '').replace('Theory', '').strip() == lab_code_base):
                return course
    return None

def is_lab_after_theory(course, schedule, day, start_hour, all_courses):
    """Check if lab course can be scheduled (must be after corresponding theory course).
    
    Returns False if:
    - Lab course's theory course is not yet scheduled
    - Lab course is scheduled before its theory course on the same day
    """
    if course.course_type != 'lab':
        return True  # Theory courses don't need this check
    
    # Find corresponding theory course
    theory_course = find_corresponding_theory_course(course, all_courses)
    if not theory_course:
        # If no corresponding theory course found, don't allow lab scheduling
        return False
    
    # Check if theory course is already scheduled
    theory_scheduled = False
    theory_scheduled_time = None
    
    for (sched_day, sched_hour), entries in schedule.items():
        for scheduled_course, _ in entries:
            if scheduled_course.course_id == theory_course.course_id:
                theory_scheduled = True
                theory_scheduled_time = (sched_day, time_to_decimal(sched_hour))
                break
        if theory_scheduled:
            break
    
    # Lab cannot be scheduled if theory is not yet scheduled
    if not theory_scheduled:
        return False
    
    # Lab must be scheduled after theory on the same day
    start_decimal = time_to_decimal(start_hour)
    if theory_scheduled_time[0] == day and start_decimal > theory_scheduled_time[1]:
        return True
    
    # Lab cannot be scheduled before theory or on a different day
    return False


def is_valid_room_for_course(room, course):
    """Check if room type matches course type and capacity is sufficient."""
    if course.course_type == 'lab' and room.room_type != 'lab':
        return False
    if course.course_type == 'lab' and room.capacity < course.capacity:
        return False
    return True


def is_valid_assignment(schedule, course, day, start_hour, room, instructors_dict=None, all_courses=None):
    """Validates if a course can be scheduled in the given slot."""
    # Check if course has a fixed time slot
    if course.fixed_time_slot:
        fixed_day, fixed_hour = course.fixed_time_slot
        if day != fixed_day or start_hour != fixed_hour:
            return False
    
    # Check exam block constraint
    if is_exam_block(day, start_hour):
        return False
    
    # Check room type and capacity
    if not is_valid_room_for_course(room, course):
        return False
    
    # Check instructor's daily theory limit
    instructor_obj = instructors_dict.get(course.instructor) if instructors_dict else None
    if course.course_type == 'theory' and exceeds_daily_theory_limit(schedule, course, instructor_obj, day):
        return False
    
    # Check for instructor overlap
    if has_instructor_conflict(schedule, course, day, start_hour):
        return False
    
    # Check for room double booking
    if has_room_conflict(schedule, room, day, start_hour):
        return False
    
    # Check for same year mandatory course conflicts
    if has_year_mandatory_conflict(schedule, course, day, start_hour):
        return False
    
    # Check for CENG/SENG elective conflicts
    if has_elective_conflict(schedule, course, day, start_hour):
        return False
    
    # Check lab after theory constraint - lab cannot be scheduled before theory
    if all_courses and not is_lab_after_theory(course, schedule, day, start_hour, all_courses):
        return False
    
    return True


def generate_schedule(courses: List[Course], rooms: List[Room], time_slots: List[Tuple[str, str]], 
                     instructors: List[Instructor] = None):
    """
    Generates a conflict-free schedule using backtracking.
    Returns the schedule if successful, otherwise raises RuntimeError.
    
    Priority order:
    1. Common courses (PHYS, MATH, ENG, TURK, HIST) - scheduled first
    2. Theory courses before lab courses
    3. Lower year courses before higher year courses
    4. Mandatory courses before electives
    
    Args:
        courses: List of Course objects
        rooms: List of Room objects
        time_slots: List of (day, hour) tuples, e.g., [("Monday", "09:00"), ...]
        instructors: Optional list of Instructor objects for constraint checking
    
    Returns:
        Dictionary mapping (day, hour) to list of (course, room) tuples
    """
    if not courses or not rooms or not time_slots:
        raise ValueError("Courses, rooms, and time slots must be non-empty lists.")

    # Create instructors dictionary for quick lookup
    instructors_dict = {}
    if instructors:
        for inst in instructors:
            instructors_dict[inst.name] = inst
    
    # Sort courses by priority:
    # 1. Courses with fixed time slots first (must be scheduled at specific times)
    # 2. Common courses (PHYS, MATH, ENG, TURK, HIST)
    # 3. Theory before lab
    # 4. Lower year before higher year
    # 5. Mandatory before elective
    def course_priority(c):
        fixed_priority = 0 if c.fixed_time_slot else 1
        common_priority = 0 if c.is_common_course else 1
        type_priority = 0 if c.course_type == 'theory' else 1
        return (fixed_priority, common_priority, type_priority, c.year, not c.is_mandatory, c.code)
    
    sorted_courses = sorted(courses, key=course_priority)
    
    schedule = defaultdict(list)

    def backtrack(course_index):
        # Base case: all courses are scheduled
        if course_index == len(sorted_courses):
            return True

        course = sorted_courses[course_index]

        # For each section of the course
        for section in range(course.sections):
            # If course has fixed time slot, only try that slot
            if course.fixed_time_slot:
                day, start_hour = course.fixed_time_slot
                slots_to_try = [(day, start_hour)]
            else:
                slots_to_try = time_slots
            
            # Determine how many consecutive hours this course needs
            if course.course_type == 'lab':
                required_hours = course.lab_hours if course.lab_hours > 0 else course.hours
            else:  # theory
                required_hours = course.theory_hours if course.theory_hours > 0 else course.hours
            
            # Try all combinations of day, start_hour, and room
            for day, start_hour in slots_to_try:
                for room in rooms:
                    if is_valid_assignment(schedule, course, day, start_hour, room, instructors_dict, sorted_courses):
                        scheduled_hours = []  # Track all hours for this course
                        
                        # If course needs multiple hours, schedule them consecutively
                        if required_hours > 1:
                            start_decimal = time_to_decimal(start_hour)
                            all_hours_scheduled = True
                            scheduled_hours = [(day, start_hour)]
                            
                            for hour_num in range(1, required_hours):
                                next_hour_decimal = start_decimal + hour_num
                                next_hour_h = int(next_hour_decimal)
                                next_hour_m = int((next_hour_decimal % 1) * 60)
                                next_hour = f"{next_hour_h}:{next_hour_m:02d}"
                                
                                # Check if next hour slot exists and is valid
                                if (day, next_hour) in time_slots:
                                    # Check if this slot is also valid for the course
                                    if is_valid_assignment(schedule, course, day, next_hour, room, instructors_dict, sorted_courses):
                                        scheduled_hours.append((day, next_hour))
                                    else:
                                        all_hours_scheduled = False
                                        break
                                else:
                                    all_hours_scheduled = False
                                    break
                            
                            if not all_hours_scheduled:
                                # If not all hours available, skip this assignment
                                continue
                            
                            # Schedule all consecutive hours
                            for hour_slot in scheduled_hours:
                                schedule[hour_slot].append((course, room))
                        else:
                            # Single hour course
                            scheduled_hours = [(day, start_hour)]
                            schedule[(day, start_hour)].append((course, room))
                        
                        # Recur to schedule the next course/section
                        if backtrack(course_index + 1):
                            return True

                        # Backtrack: remove the course from the schedule
                        for hour_slot in scheduled_hours:
                            if hour_slot in schedule:
                                schedule[hour_slot] = [
                                    (c, r) for c, r in schedule[hour_slot]
                                    if c.course_id != course.course_id
                                ]

        return False

    # Start the backtracking process
    if backtrack(0):
        return dict(schedule)

    raise RuntimeError("No valid schedule could be generated with the given constraints.")
