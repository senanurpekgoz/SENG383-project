"""
BeePlan - Çankaya Üniversitesi Ders Programı Hazırlama Sistemi
GUI Application for course schedule generation and management.
"""

import sys
import json
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, 
    QTableWidget, QTableWidgetItem, QFileDialog, QMessageBox, QWidget,
    QTabWidget, QLabel, QLineEdit, QSpinBox, QComboBox, QCheckBox,
    QGroupBox, QFormLayout, QTextEdit, QHeaderView, QListWidget, QListWidgetItem,
    QDialog, QScrollArea
)
from PyQt5.QtGui import QColor, QFont
from PyQt5.QtCore import Qt
from scheduler import Course, Instructor, Room, time_to_decimal
from controller import ScheduleController


class BeePlanGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        # Initialize controller (mediator between GUI and algorithm)
        self.controller = ScheduleController()
        self.init_data()
        self.init_ui()
        
    def init_data(self):
        """Initialize data containers."""
        self.courses = []
        self.instructors = []
        self.rooms = []
        self.time_slots = []
        self.schedule = {}
        self.all_available_courses = []  # Tüm mevcut dersler (JSON'dan yüklenecek)
        self.selected_courses = []  # Kullanıcının seçtiği dersler
        self.student_year = None  # Öğrencinin sınıfı
        self.max_credits = 17  # Maksimum kredi hakkı
        self.selected_credits = 0  # Seçilen toplam kredi
        
    def init_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle("BeePlan - Çankaya Üniversitesi Ders Programı Hazırlama Sistemi")
        self.setGeometry(100, 100, 1400, 800)
        
        # Create tab widget
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        
        # Create tabs
        self.create_schedule_tab()
        self.create_course_selection_tab()  # Ders seçimi sekmesi (önce)
        self.create_courses_tab()
        self.create_instructors_tab()
        self.create_rooms_tab()
        self.create_settings_tab()
        
        # Show login dialog after UI is created
        self.show_login_dialog()
    
    def show_login_dialog(self):
        """Show login dialog for student year selection."""
        login_dialog = QDialog(self)
        login_dialog.setWindowTitle("BeePlan - Giriş")
        login_dialog.setGeometry(300, 300, 400, 200)
        login_dialog.setModal(True)
        
        layout = QVBoxLayout(login_dialog)
        
        # Title
        title = QLabel("Hoş Geldiniz!")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Year selection
        year_label = QLabel("Lütfen sınıfınızı seçin:")
        year_label.setFont(QFont("Arial", 12))
        layout.addWidget(year_label)
        
        year_combo = QComboBox()
        year_combo.addItems(["1", "2", "3", "4"])
        layout.addWidget(year_combo)
        
        # Info label
        info_label = QLabel(f"Seçmeli dersler için {self.max_credits} kredi hakkınız var.")
        info_label.setStyleSheet("color: #666; font-size: 10px;")
        layout.addWidget(info_label)
        
        # Buttons
        button_layout = QHBoxLayout()
        login_button = QPushButton("Giriş Yap")
        login_button.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold; padding: 8px;")
        login_button.clicked.connect(lambda: self.handle_login(login_dialog, year_combo))
        button_layout.addWidget(login_button)
        layout.addLayout(button_layout)
        
        login_dialog.exec_()
    
    def handle_login(self, dialog, year_combo):
        """Handle login - set student year."""
        self.student_year = int(year_combo.currentText())
        dialog.accept()
        # Update course selection tab
        if hasattr(self, 'year_selection_combo'):
            self.year_selection_combo.setCurrentIndex(self.student_year - 1)
            self.update_available_courses(self.student_year)
            # Switch to course selection tab
            self.tabs.setCurrentIndex(1)
        
    def create_schedule_tab(self):
        """Create the main schedule visualization tab."""
        schedule_widget = QWidget()
        layout = QVBoxLayout(schedule_widget)
        
        # Buttons
        button_layout = QHBoxLayout()
        self.load_data_button = QPushButton("Veri Yükle (JSON)")
        self.load_data_button.clicked.connect(self.load_data)
        self.generate_button = QPushButton("Program Oluştur")
        self.generate_button.clicked.connect(self.generate_schedule)
        self.generate_button.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold;")
        self.save_button = QPushButton("Programı Kaydet")
        self.save_button.clicked.connect(self.save_schedule)
        self.clear_button = QPushButton("Temizle")
        self.clear_button.clicked.connect(self.clear_schedule)
        
        self.view_report_button = QPushButton("📊 Rapor Görüntüle")
        self.view_report_button.clicked.connect(self.view_report)
        self.view_report_button.setStyleSheet("background-color: #2196F3; color: white; font-weight: bold;")
        
        button_layout.addWidget(self.load_data_button)
        button_layout.addWidget(self.generate_button)
        button_layout.addWidget(self.view_report_button)
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.clear_button)
        button_layout.addStretch()
        
        layout.addLayout(button_layout)
        
        # Status label
        self.status_label = QLabel("Hazır")
        self.status_label.setStyleSheet("padding: 5px; background-color: #f0f0f0;")
        layout.addWidget(self.status_label)
        
        # Schedule Table
        self.schedule_table = QTableWidget()
        self.schedule_table.setEditTriggers(QTableWidget.DoubleClicked | QTableWidget.SelectedClicked)
        self.schedule_table.cellChanged.connect(self.on_cell_changed)
        layout.addWidget(self.schedule_table)
        
        self.tabs.addTab(schedule_widget, "📅 Ders Programı")
        
    def create_course_selection_tab(self):
        """Create tab for course selection by students."""
        selection_widget = QWidget()
        layout = QVBoxLayout(selection_widget)
        
        # Title
        title_label = QLabel("Ders Seçimi")
        title_label.setFont(QFont("Arial", 14, QFont.Bold))
        layout.addWidget(title_label)
        
        # Year selection
        year_group = QGroupBox("Sınıf Seçimi")
        year_layout = QHBoxLayout()
        year_label = QLabel("Sınıfınızı seçin:")
        self.year_selection_combo = QComboBox()
        self.year_selection_combo.addItems(["1", "2", "3", "4"])
        self.year_selection_combo.currentTextChanged.connect(self.on_year_selection_changed)
        year_layout.addWidget(year_label)
        year_layout.addWidget(self.year_selection_combo)
        year_layout.addStretch()
        year_group.setLayout(year_layout)
        layout.addWidget(year_group)
        
        # Main content area (two columns)
        content_layout = QHBoxLayout()
        
        # Left: Available courses for selected year
        left_group = QGroupBox("Mevcut Dersler")
        left_layout = QVBoxLayout()
        self.available_courses_list = QListWidget()
        self.available_courses_list.setSelectionMode(QListWidget.MultiSelection)
        left_layout.addWidget(self.available_courses_list)
        left_group.setLayout(left_layout)
        content_layout.addWidget(left_group, 1)
        
        # Middle: Buttons
        button_layout = QVBoxLayout()
        self.add_course_button = QPushButton("➡️\nEkle")
        self.add_course_button.clicked.connect(self.add_selected_courses)
        self.add_course_button.setEnabled(False)
        self.remove_course_button = QPushButton("⬅️\nÇıkar")
        self.remove_course_button.clicked.connect(self.remove_selected_courses)
        self.remove_course_button.setEnabled(False)
        button_layout.addWidget(self.add_course_button)
        button_layout.addWidget(self.remove_course_button)
        button_layout.addStretch()
        content_layout.addLayout(button_layout)
        
        # Right: Selected courses
        right_group = QGroupBox("Seçilen Dersler")
        right_layout = QVBoxLayout()
        self.selected_courses_list = QListWidget()
        self.selected_courses_list.setSelectionMode(QListWidget.MultiSelection)
        right_layout.addWidget(self.selected_courses_list)
        right_group.setLayout(right_layout)
        content_layout.addWidget(right_group, 1)
        
        layout.addLayout(content_layout)
        
        # Generate schedule button
        generate_from_selection_button = QPushButton("🎓 Seçilen Derslerle Program Oluştur")
        generate_from_selection_button.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold; padding: 10px;")
        generate_from_selection_button.clicked.connect(self.generate_schedule_from_selection)
        layout.addWidget(generate_from_selection_button)
        
        # Credit info label
        self.credit_info_label = QLabel(f"Seçmeli dersler için {self.max_credits} kredi hakkınız var.")
        self.credit_info_label.setStyleSheet("padding: 5px; background-color: #E3F2FD; font-weight: bold;")
        layout.addWidget(self.credit_info_label)
        
        # Status label
        self.selection_status_label = QLabel("Lütfen sınıfınızı seçin ve derslerinizi ekleyin.")
        self.selection_status_label.setStyleSheet("padding: 5px; background-color: #f0f0f0;")
        layout.addWidget(self.selection_status_label)
        
        # Connect list selection changes
        self.available_courses_list.itemSelectionChanged.connect(self.on_available_selection_changed)
        self.selected_courses_list.itemSelectionChanged.connect(self.on_selected_selection_changed)
        
        self.tabs.addTab(selection_widget, "🎓 Ders Seçimi")
        
    def on_year_selection_changed(self):
        """Update available courses when year selection changes."""
        year = int(self.year_selection_combo.currentText())
        self.update_available_courses(year)
        
    def find_lab_for_theory(self, theory_course):
        """Find the corresponding lab course for a theory course."""
        theory_code = theory_course.code
        
        for course in self.all_available_courses:
            if (course.course_type == 'lab' and 
                course.year == theory_course.year and
                course.instructor == theory_course.instructor):
                lab_code = course.code
                
                # Check various patterns:
                # 1. SENG101 -> SENG101L
                # 2. SENG101 -> SENG101Lab
                # 3. SENG101 -> SENG101 LAB
                # 4. Theory code is prefix of lab code
                theory_base = theory_code.strip()
                lab_base = lab_code.strip()
                
                # Remove common lab suffixes from lab code
                lab_without_suffix = lab_base.replace('L', '').replace('Lab', '').replace('LAB', '').strip()
                
                # Check if theory code matches lab code (with or without suffix)
                if (theory_code in lab_code or  # SENG101 in SENG101L
                    theory_base == lab_without_suffix or  # SENG101 == SENG101 (after removing L)
                    lab_code.startswith(theory_code)):  # SENG101L starts with SENG101
                    return course
        
        return None
    
    def get_course_credits(self, course):
        """Calculate total credits for a course."""
        if course.credits:
            try:
                if '+' in str(course.credits):
                    parts = str(course.credits).split('+')
                    return int(parts[0].strip()) + int(parts[1].strip())
                else:
                    return int(str(course.credits).strip())
            except (ValueError, IndexError):
                return course.hours if course.course_type == 'theory' else 0
        return course.hours if course.course_type == 'theory' else 0
    
    def update_available_courses(self, year):
        """Update the list of available courses for the selected year."""
        self.available_courses_list.clear()
        
        # Filter courses by year - only show theory courses (labs will be added automatically)
        year_courses = [c for c in self.all_available_courses 
                       if c.year == year and c.course_type == 'theory']
        
        for course in year_courses:
            # Check if this course has a lab
            lab_course = self.find_lab_for_theory(course)
            has_lab = lab_course is not None
            
            # Get credits
            credits = self.get_course_credits(course)
            if has_lab and lab_course:
                lab_credits = self.get_course_credits(lab_course)
                # Lab credits are usually included in the theory course credits
                # So we don't double count
            
            course_text = f"{course.code} - {course.name}"
            if credits > 0:
                course_text += f" ({credits} kredi)"
            if has_lab:
                course_text += " [Teori + Lab]"
            if not course.is_mandatory:
                course_text += " [Seçmeli]"
            
            item = QListWidgetItem(course_text)
            item.setData(Qt.UserRole, course)  # Store course object
            self.available_courses_list.addItem(item)
        
        self.selection_status_label.setText(f"{year}. sınıf için {len(year_courses)} ders bulundu.")
        
    def on_available_selection_changed(self):
        """Enable/disable add button based on selection."""
        self.add_course_button.setEnabled(len(self.available_courses_list.selectedItems()) > 0)
        
    def on_selected_selection_changed(self):
        """Enable/disable remove button based on selection."""
        self.remove_course_button.setEnabled(len(self.selected_courses_list.selectedItems()) > 0)
        
    def add_selected_courses(self):
        """Add selected courses from available list to selected list.
        Automatically adds corresponding lab courses if they exist."""
        selected_items = self.available_courses_list.selectedItems()
        
        for item in selected_items:
            course = item.data(Qt.UserRole)
            
            # Check if already selected
            already_selected = False
            for i in range(self.selected_courses_list.count()):
                existing_item = self.selected_courses_list.item(i)
                existing_course = existing_item.data(Qt.UserRole)
                if existing_course.course_id == course.course_id:
                    already_selected = True
                    break
            
            if not already_selected:
                # Check credit limit for elective courses
                if not course.is_mandatory:
                    course_credits = self.get_course_credits(course)
                    if self.selected_credits + course_credits > self.max_credits:
                        QMessageBox.warning(
                            self, 
                            "Kredi Limiti Aşıldı", 
                            f"{course.code} dersini ekleyemezsiniz.\n"
                            f"Seçilen kredi: {self.selected_credits}\n"
                            f"Ders kredisi: {course_credits}\n"
                            f"Toplam: {self.selected_credits + course_credits} (Maksimum: {self.max_credits})"
                        )
                        continue
                
                # Add theory course
                course_credits = self.get_course_credits(course)
                course_text = f"{course.code} - {course.name} (Teori)"
                if course_credits > 0:
                    course_text += f" [{course_credits} kredi]"
                if not course.is_mandatory:
                    course_text += " [Seçmeli]"
                
                new_item = QListWidgetItem(course_text)
                new_item.setData(Qt.UserRole, course)
                self.selected_courses_list.addItem(new_item)
                self.selected_courses.append(course)
                
                # Update selected credits for elective courses
                if not course.is_mandatory:
                    self.selected_credits += course_credits
                
                # Check if this course has a lab and add it automatically
                lab_course = self.find_lab_for_theory(course)
                if lab_course:
                    # Check if lab is already selected
                    lab_already_selected = False
                    for i in range(self.selected_courses_list.count()):
                        existing_item = self.selected_courses_list.item(i)
                        existing_course = existing_item.data(Qt.UserRole)
                        if existing_course.course_id == lab_course.course_id:
                            lab_already_selected = True
                            break
                    
                    if not lab_already_selected:
                        lab_credits = self.get_course_credits(lab_course)
                        lab_text = f"{lab_course.code} - {lab_course.name} (Lab)"
                        if lab_credits > 0:
                            lab_text += f" [{lab_credits} kredi]"
                        if not lab_course.is_mandatory:
                            lab_text += " [Seçmeli]"
                        
                        lab_item = QListWidgetItem(lab_text)
                        lab_item.setData(Qt.UserRole, lab_course)
                        self.selected_courses_list.addItem(lab_item)
                        self.selected_courses.append(lab_course)
        
        # Update status with credit information
        remaining_credits = self.max_credits - self.selected_credits
        status_text = f"{len(self.selected_courses)} ders seçildi (teori + lab dahil)."
        if self.selected_credits > 0:
            status_text += f"\nSeçilen kredi: {self.selected_credits}/{self.max_credits} (Kalan: {remaining_credits})"
        self.selection_status_label.setText(status_text)
        
    def remove_selected_courses(self):
        """Remove selected courses from selected list.
        If a theory course is removed, its lab is also removed automatically."""
        selected_items = self.selected_courses_list.selectedItems()
        courses_to_remove = []
        
        for item in selected_items:
            course = item.data(Qt.UserRole)
            courses_to_remove.append(course)
            
            # If removing a theory course, also remove its lab
            if course.course_type == 'theory':
                lab_course = self.find_lab_for_theory(course)
                if lab_course:
                    # Check if lab is in selected courses
                    for i in range(self.selected_courses_list.count()):
                        existing_item = self.selected_courses_list.item(i)
                        existing_course = existing_item.data(Qt.UserRole)
                        if existing_course.course_id == lab_course.course_id:
                            courses_to_remove.append(lab_course)
                            break
            # If removing a lab course, also remove its theory
            elif course.course_type == 'lab':
                # Find the theory course for this lab
                for theory_course in self.all_available_courses:
                    if (theory_course.course_type == 'theory' and
                        theory_course.year == course.year and
                        theory_course.instructor == course.instructor):
                        lab_course = self.find_lab_for_theory(theory_course)
                        if lab_course and lab_course.course_id == course.course_id:
                            courses_to_remove.append(theory_course)
                            break
        
        # Remove all courses (including related labs/theories) and update credits
        for course_to_remove in courses_to_remove:
            # Update credits if elective
            if not course_to_remove.is_mandatory:
                course_credits = self.get_course_credits(course_to_remove)
                self.selected_credits -= course_credits
                if self.selected_credits < 0:
                    self.selected_credits = 0
            
            # Find and remove from list widget
            for i in range(self.selected_courses_list.count()):
                item = self.selected_courses_list.item(i)
                if item.data(Qt.UserRole).course_id == course_to_remove.course_id:
                    self.selected_courses_list.takeItem(i)
                    break
            
            # Remove from selected courses list
            self.selected_courses = [c for c in self.selected_courses 
                                   if c.course_id != course_to_remove.course_id]
        
        # Update status with credit information
        remaining_credits = self.max_credits - self.selected_credits
        status_text = f"{len(self.selected_courses)} ders seçildi (teori + lab dahil)."
        if self.selected_credits > 0:
            status_text += f"\nSeçilen kredi: {self.selected_credits}/{self.max_credits} (Kalan: {remaining_credits})"
        self.selection_status_label.setText(status_text)
        
    def generate_schedule_from_selection(self):
        """Generate schedule from selected courses."""
        if not self.selected_courses:
            QMessageBox.warning(self, "Uyarı", "Lütfen en az bir ders seçin.")
            return
        
        if not self.rooms:
            QMessageBox.warning(self, "Uyarı", "Lütfen derslik bilgilerini yükleyin.")
            return
        
        if not self.time_slots:
            QMessageBox.warning(self, "Uyarı", "Lütfen zaman dilimlerini ayarlayın.")
            return
        
        try:
            # Update controller with current data
            self.controller.set_courses(self.selected_courses)
            self.controller.set_instructors(self.instructors)
            self.controller.set_rooms(self.rooms)
            self.controller.set_time_slots(self.time_slots)
            
            self.selection_status_label.setText("Program oluşturuluyor...")
            QApplication.processEvents()
            
            # Use selected courses to generate schedule through controller
            schedule = self.controller.generate_schedule(self.selected_courses)
            self.schedule = schedule
            
            # Switch to schedule tab and populate
            self.tabs.setCurrentIndex(0)  # Switch to schedule tab
            self.populate_table(schedule)
            
            self.selection_status_label.setText(f"Program başarıyla oluşturuldu! {len(self.selected_courses)} ders planlandı.")
            QMessageBox.information(self, "Başarılı", f"Seçtiğiniz {len(self.selected_courses)} ders için program oluşturuldu!")
            
        except Exception as e:
            self.selection_status_label.setText(f"Hata: {str(e)}")
            QMessageBox.critical(self, "Hata", f"Program oluşturulamadı: {e}")
        
    def create_courses_tab(self):
        """Create tab for managing courses."""
        courses_widget = QWidget()
        layout = QVBoxLayout(courses_widget)
        
        # Add course form
        form_group = QGroupBox("Yeni Ders Ekle")
        form_layout = QFormLayout()
        
        self.course_code_input = QLineEdit()
        self.course_name_input = QLineEdit()
        self.course_instructor_combo = QComboBox()
        self.course_hours_input = QSpinBox()
        self.course_hours_input.setRange(1, 8)
        self.course_type_combo = QComboBox()
        self.course_type_combo.addItems(["theory", "lab"])
        self.course_year_input = QSpinBox()
        self.course_year_input.setRange(1, 4)
        self.course_mandatory_check = QCheckBox()
        self.course_mandatory_check.setChecked(True)
        self.course_sections_input = QSpinBox()
        self.course_sections_input.setRange(1, 10)
        self.course_capacity_input = QSpinBox()
        self.course_capacity_input.setRange(1, 100)
        self.course_capacity_input.setValue(40)
        self.course_department_combo = QComboBox()
        self.course_department_combo.addItems(["SENG", "CENG", "PHYS", "MATH", "ENG"])
        
        form_layout.addRow("Ders Kodu:", self.course_code_input)
        form_layout.addRow("Ders Adı:", self.course_name_input)
        form_layout.addRow("Öğretim Elemanı:", self.course_instructor_combo)
        form_layout.addRow("Haftalık Saat:", self.course_hours_input)
        form_layout.addRow("Ders Tipi:", self.course_type_combo)
        form_layout.addRow("Sınıf:", self.course_year_input)
        form_layout.addRow("Zorunlu:", self.course_mandatory_check)
        form_layout.addRow("Şube Sayısı:", self.course_sections_input)
        form_layout.addRow("Kapasite:", self.course_capacity_input)
        form_layout.addRow("Bölüm:", self.course_department_combo)
        
        form_group.setLayout(form_layout)
        layout.addWidget(form_group)
        
        # Buttons
        button_layout = QHBoxLayout()
        add_course_button = QPushButton("Ders Ekle")
        add_course_button.clicked.connect(self.add_course)
        remove_course_button = QPushButton("Ders Sil")
        remove_course_button.clicked.connect(self.remove_course)
        button_layout.addWidget(add_course_button)
        button_layout.addWidget(remove_course_button)
        layout.addLayout(button_layout)
        
        # Courses table
        self.courses_table = QTableWidget()
        self.courses_table.setColumnCount(10)
        self.courses_table.setHorizontalHeaderLabels([
            "Kod", "Ad", "Öğretim Elemanı", "Saat", "Tip", "Sınıf", 
            "Zorunlu", "Şube", "Kapasite", "Bölüm"
        ])
        self.courses_table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.courses_table)
        
        self.tabs.addTab(courses_widget, "📚 Dersler")
        
    def create_instructors_tab(self):
        """Create tab for managing instructors."""
        instructors_widget = QWidget()
        layout = QVBoxLayout(instructors_widget)
        
        # Add instructor form
        form_group = QGroupBox("Yeni Öğretim Elemanı Ekle")
        form_layout = QFormLayout()
        
        self.instructor_name_input = QLineEdit()
        self.instructor_max_hours_input = QSpinBox()
        self.instructor_max_hours_input.setRange(1, 8)
        self.instructor_max_hours_input.setValue(4)
        
        form_layout.addRow("Ad Soyad:", self.instructor_name_input)
        form_layout.addRow("Günlük Max Teorik Saat:", self.instructor_max_hours_input)
        
        form_group.setLayout(form_layout)
        layout.addWidget(form_group)
        
        # Buttons
        button_layout = QHBoxLayout()
        add_instructor_button = QPushButton("Öğretim Elemanı Ekle")
        add_instructor_button.clicked.connect(self.add_instructor)
        remove_instructor_button = QPushButton("Öğretim Elemanı Sil")
        remove_instructor_button.clicked.connect(self.remove_instructor)
        button_layout.addWidget(add_instructor_button)
        button_layout.addWidget(remove_instructor_button)
        layout.addLayout(button_layout)
        
        # Instructors table
        self.instructors_table = QTableWidget()
        self.instructors_table.setColumnCount(2)
        self.instructors_table.setHorizontalHeaderLabels(["Ad Soyad", "Günlük Max Teorik Saat"])
        layout.addWidget(self.instructors_table)
        
        # Load default instructors
        self.load_default_instructors()
        
        self.tabs.addTab(instructors_widget, "👨‍🏫 Öğretim Elemanları")
        
    def create_rooms_tab(self):
        """Create tab for managing rooms."""
        rooms_widget = QWidget()
        layout = QVBoxLayout(rooms_widget)
        
        # Add room form
        form_group = QGroupBox("Yeni Derslik Ekle")
        form_layout = QFormLayout()
        
        self.room_name_input = QLineEdit()
        self.room_capacity_input = QSpinBox()
        self.room_capacity_input.setRange(1, 200)
        self.room_type_combo = QComboBox()
        self.room_type_combo.addItems(["theory", "lab"])
        
        form_layout.addRow("Derslik Adı:", self.room_name_input)
        form_layout.addRow("Kapasite:", self.room_capacity_input)
        form_layout.addRow("Tip:", self.room_type_combo)
        
        form_group.setLayout(form_layout)
        layout.addWidget(form_group)
        
        # Buttons
        button_layout = QHBoxLayout()
        add_room_button = QPushButton("Derslik Ekle")
        add_room_button.clicked.connect(self.add_room)
        remove_room_button = QPushButton("Derslik Sil")
        remove_room_button.clicked.connect(self.remove_room)
        button_layout.addWidget(add_room_button)
        button_layout.addWidget(remove_room_button)
        layout.addLayout(button_layout)
        
        # Rooms table
        self.rooms_table = QTableWidget()
        self.rooms_table.setColumnCount(3)
        self.rooms_table.setHorizontalHeaderLabels(["Derslik Adı", "Kapasite", "Tip"])
        layout.addWidget(self.rooms_table)
        
        # Load default rooms
        self.load_default_rooms()
        
        self.tabs.addTab(rooms_widget, "🏫 Derslikler")
        
    def create_settings_tab(self):
        """Create tab for time slots and settings."""
        settings_widget = QWidget()
        layout = QVBoxLayout(settings_widget)
        
        # Time slots info
        info_label = QLabel("Zaman Dilimleri ve Ayarlar")
        info_label.setFont(QFont("Arial", 12, QFont.Bold))
        layout.addWidget(info_label)
        
        self.time_slots_text = QTextEdit()
        self.time_slots_text.setPlaceholderText(
            "Zaman dilimlerini JSON formatında girin:\n"
            '[\n'
            '  ["Monday", "09:00"],\n'
            '  ["Monday", "10:00"],\n'
            '  ["Tuesday", "09:00"],\n'
            '  ...\n'
            ']'
        )
        layout.addWidget(self.time_slots_text)
        
        # Load default time slots
        self.load_default_time_slots()
        
        apply_button = QPushButton("Zaman Dilimlerini Uygula")
        apply_button.clicked.connect(self.apply_time_slots)
        layout.addWidget(apply_button)
        
        self.tabs.addTab(settings_widget, "⚙️ Ayarlar")
        
    def load_default_instructors(self):
        """Load default instructors from Çankaya University."""
        default_instructors = [
            ("B. Avenoğlu", 4),
            ("B. Çelikkale", 4),
            ("S. Esmelioğlu", 4),
            ("S.K. Tunç", 4),
            ("N. Çağıltay", 4),
            ("T. Karadeniz", 4),
        ]
        
        for name, max_hours in default_instructors:
            instructor = Instructor(name, max_hours, is_part_time=False, exclude_graduate_from_limit=False)
            self.instructors.append(instructor)
        
        self.update_instructors_table()
        self.update_instructor_combos()
        
    def load_default_rooms(self):
        """Load default rooms."""
        default_rooms = [
            ("D101", 60, "theory"),
            ("D102", 60, "theory"),
            ("D201", 60, "theory"),
            ("D202", 60, "theory"),
            ("Lab1", 40, "lab"),
            ("Lab2", 40, "lab"),
            ("Lab3", 40, "lab"),
        ]
        
        for name, capacity, room_type in default_rooms:
            room = Room(len(self.rooms), name, capacity, room_type)
            self.rooms.append(room)
        
        self.update_rooms_table()
        
    def load_default_time_slots(self):
        """Load default time slots (Monday-Friday, 09:00-17:00)."""
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        hours = ["09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00"]
        
        time_slots = []
        for day in days:
            for hour in hours:
                # Skip Friday 13:20-15:10 (exam period)
                if day == "Friday" and hour in ["13:00", "14:00", "15:00"]:
                    continue
                time_slots.append([day, hour])
        
        self.time_slots_text.setPlainText(json.dumps(time_slots, indent=2))
        self.apply_time_slots()
        
    def apply_time_slots(self):
        """Apply time slots from text input."""
        try:
            text = self.time_slots_text.toPlainText()
            self.time_slots = [tuple(ts) for ts in json.loads(text)]
            QMessageBox.information(self, "Başarılı", f"{len(self.time_slots)} zaman dilimi yüklendi.")
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Zaman dilimleri yüklenemedi: {e}")
    
    def update_instructors_table(self):
        """Update the instructors table display."""
        self.instructors_table.setRowCount(len(self.instructors))
        for i, instructor in enumerate(self.instructors):
            self.instructors_table.setItem(i, 0, QTableWidgetItem(instructor.name))
            self.instructors_table.setItem(i, 1, QTableWidgetItem(str(instructor.max_daily_theory_hours)))
    
    def update_instructor_combos(self):
        """Update instructor combo boxes."""
        self.course_instructor_combo.clear()
        for instructor in self.instructors:
            self.course_instructor_combo.addItem(instructor.name)
    
    def update_rooms_table(self):
        """Update the rooms table display."""
        self.rooms_table.setRowCount(len(self.rooms))
        for i, room in enumerate(self.rooms):
            self.rooms_table.setItem(i, 0, QTableWidgetItem(room.name))
            self.rooms_table.setItem(i, 1, QTableWidgetItem(str(room.capacity)))
            self.rooms_table.setItem(i, 2, QTableWidgetItem(room.room_type))
    
    def update_courses_table(self):
        """Update the courses table display."""
        self.courses_table.setRowCount(len(self.courses))
        for i, course in enumerate(self.courses):
            self.courses_table.setItem(i, 0, QTableWidgetItem(course.code))
            self.courses_table.setItem(i, 1, QTableWidgetItem(course.name))
            self.courses_table.setItem(i, 2, QTableWidgetItem(course.instructor))
            self.courses_table.setItem(i, 3, QTableWidgetItem(str(course.hours)))
            self.courses_table.setItem(i, 4, QTableWidgetItem(course.course_type))
            self.courses_table.setItem(i, 5, QTableWidgetItem(str(course.year)))
            self.courses_table.setItem(i, 6, QTableWidgetItem("Evet" if course.is_mandatory else "Hayır"))
            self.courses_table.setItem(i, 7, QTableWidgetItem(str(course.sections)))
            self.courses_table.setItem(i, 8, QTableWidgetItem(str(course.capacity)))
            self.courses_table.setItem(i, 9, QTableWidgetItem(course.department))
    
    def add_instructor(self):
        """Add a new instructor."""
        name = self.instructor_name_input.text().strip()
        if not name:
            QMessageBox.warning(self, "Uyarı", "Lütfen öğretim elemanı adı girin.")
            return
        
        max_hours = self.instructor_max_hours_input.value()
        instructor = Instructor(name, max_hours, is_part_time=False, exclude_graduate_from_limit=False)
        self.instructors.append(instructor)
        self.update_instructors_table()
        self.update_instructor_combos()
        self.instructor_name_input.clear()
        QMessageBox.information(self, "Başarılı", "Öğretim elemanı eklendi.")
    
    def remove_instructor(self):
        """Remove selected instructor."""
        row = self.instructors_table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Uyarı", "Lütfen silmek için bir öğretim elemanı seçin.")
            return
        
        self.instructors.pop(row)
        self.update_instructors_table()
        self.update_instructor_combos()
        QMessageBox.information(self, "Başarılı", "Öğretim elemanı silindi.")
    
    def add_room(self):
        """Add a new room."""
        name = self.room_name_input.text().strip()
        if not name:
            QMessageBox.warning(self, "Uyarı", "Lütfen derslik adı girin.")
            return
        
        capacity = self.room_capacity_input.value()
        room_type = self.room_type_combo.currentText()
        room = Room(len(self.rooms), name, capacity, room_type)
        self.rooms.append(room)
        self.update_rooms_table()
        self.room_name_input.clear()
        QMessageBox.information(self, "Başarılı", "Derslik eklendi.")
    
    def remove_room(self):
        """Remove selected room."""
        row = self.rooms_table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Uyarı", "Lütfen silmek için bir derslik seçin.")
            return
        
        self.rooms.pop(row)
        self.update_rooms_table()
        QMessageBox.information(self, "Başarılı", "Derslik silindi.")
    
    def add_course(self):
        """Add a new course."""
        code = self.course_code_input.text().strip()
        name = self.course_name_input.text().strip()
        instructor = self.course_instructor_combo.currentText()
        
        if not code or not name:
            QMessageBox.warning(self, "Uyarı", "Lütfen ders kodu ve adı girin.")
            return
        
        course = Course(
            course_id=len(self.courses),
            code=code,
            name=name,
            instructor=instructor,
            hours=self.course_hours_input.value(),
            course_type=self.course_type_combo.currentText(),
            year=self.course_year_input.value(),
            is_mandatory=self.course_mandatory_check.isChecked(),
            sections=self.course_sections_input.value(),
            capacity=self.course_capacity_input.value(),
            department=self.course_department_combo.currentText(),
            is_graduate=False,
            credits=None,
            groups=None,
            fixed_time_slot=None
        )
        
        self.courses.append(course)
        self.update_courses_table()
        
        # Clear inputs
        self.course_code_input.clear()
        self.course_name_input.clear()
        
        QMessageBox.information(self, "Başarılı", "Ders eklendi.")
    
    def remove_course(self):
        """Remove selected course."""
        row = self.courses_table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Uyarı", "Lütfen silmek için bir ders seçin.")
            return
        
        self.courses.pop(row)
        self.update_courses_table()
        QMessageBox.information(self, "Başarılı", "Ders silindi.")
    
    def load_data(self):
        """Load data from a JSON file."""
        file_name, _ = QFileDialog.getOpenFileName(self, "JSON Dosyası Aç", "", "JSON Files (*.json)")
        if not file_name:
            return
        
        try:
            with open(file_name, 'r', encoding='utf-8') as file:
                data = json.load(file)
            
            # Load instructors
            if "instructors" in data:
                self.instructors = [
                    Instructor(
                        inst["name"], 
                        inst.get("max_daily_theory_hours", 4),
                        is_part_time=inst.get("is_part_time", False),
                        exclude_graduate_from_limit=inst.get("exclude_graduate_from_limit", False)
                    )
                    for inst in data["instructors"]
                ]
                self.update_instructors_table()
                self.update_instructor_combos()
            
            # Load rooms
            if "rooms" in data:
                self.rooms = [
                    Room(i, room["name"], room["capacity"], room.get("type", "theory"))
                    for i, room in enumerate(data["rooms"])
                ]
                self.update_rooms_table()
            
            # Load courses
            if "courses" in data:
                self.courses = [
                    Course(
                        course_id=i,
                        code=c.get("code", ""),
                        name=c.get("name", ""),
                        instructor=c.get("instructor", ""),
                        hours=c.get("hours", 0),
                        course_type=c.get("type", "theory").lower(),
                        year=c.get("year", 1),
                        is_mandatory=c.get("is_mandatory", True),
                        sections=c.get("sections", 1),
                        capacity=c.get("capacity", 40),
                        department=c.get("department", "SENG"),
                        is_graduate=c.get("is_graduate", False),
                        credits=c.get("credits", None),
                        groups=c.get("groups", None),
                        fixed_time_slot=tuple(c.get("fixed_time_slot")) if c.get("fixed_time_slot") else None
                    )
                    for i, c in enumerate(data["courses"])
                ]
                # Also populate all_available_courses for course selection
                self.all_available_courses = self.courses.copy()
                self.update_courses_table()
                
                # Update course selection tab if year is selected
                if hasattr(self, 'year_selection_combo') and self.year_selection_combo.currentText():
                    year = int(self.year_selection_combo.currentText())
                    self.update_available_courses(year)
            
            # Load time slots
            if "time_slots" in data:
                self.time_slots = [tuple(ts) for ts in data["time_slots"]]
                self.time_slots_text.setPlainText(json.dumps(data["time_slots"], indent=2))
            
            QMessageBox.information(self, "Başarılı", "Veri başarıyla yüklendi!")
            self.status_label.setText(f"Veri yüklendi: {len(self.courses)} ders, {len(self.rooms)} derslik")
            
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Veri yüklenemedi: {e}")
    
    def generate_schedule(self):
        """Generate and display the schedule using the controller."""
        # Update controller with current data
        self.controller.set_courses(self.courses)
        self.controller.set_instructors(self.instructors)
        self.controller.set_rooms(self.rooms)
        self.controller.set_time_slots(self.time_slots)
        
        # Validate using controller
        is_valid, error_msg = self.controller.validate_schedule_data()
        if not is_valid:
            QMessageBox.warning(self, "Uyarı", error_msg)
            return
        
        try:
            self.status_label.setText("Program oluşturuluyor...")
            QApplication.processEvents()
            
            # Generate schedule through controller (which calls the algorithm)
            schedule = self.controller.generate_schedule()
            self.schedule = schedule
            self.populate_table(schedule)
            
            self.status_label.setText("Program başarıyla oluşturuldu!")
            QMessageBox.information(self, "Başarılı", "Ders programı başarıyla oluşturuldu!")
            
        except Exception as e:
            self.status_label.setText(f"Hata: {str(e)}")
            QMessageBox.critical(self, "Hata", f"Program oluşturulamadı: {e}")
    
    def validate_data(self):
        """Validate that the required data is loaded."""
        if not self.courses:
            QMessageBox.warning(self, "Uyarı", "Lütfen en az bir ders ekleyin.")
            return False
        if not self.rooms:
            QMessageBox.warning(self, "Uyarı", "Lütfen en az bir derslik ekleyin.")
            return False
        if not self.time_slots:
            QMessageBox.warning(self, "Uyarı", "Lütfen zaman dilimlerini ayarlayın.")
            return False
        return True
    
    def populate_table(self, schedule):
        """Populate the table widget with the generated schedule."""
        self.schedule_table.clear()
        
        # Get all days and hours
        days = sorted(set(day for day, _ in schedule.keys()))
        hours = sorted(set(hour for _, hour in schedule.keys()), 
                      key=lambda x: (int(x.split(':')[0]), int(x.split(':')[1])))
        
        # Setup table
        self.schedule_table.setRowCount(len(hours))
        self.schedule_table.setColumnCount(len(days))
        self.schedule_table.setHorizontalHeaderLabels(days)
        self.schedule_table.setVerticalHeaderLabels(hours)
        
        # Track which cells have been filled (for multi-hour courses)
        filled_cells = set()
        
        # Group courses by their time ranges - find start and end times for each course
        course_sessions = {}  # (course_id, day, room_name) -> [hours]
        
        for (day, hour), entries in schedule.items():
            for course, room in entries:
                key = (course.course_id, day, room.name)
                if key not in course_sessions:
                    course_sessions[key] = []
                course_sessions[key].append(hour)
        
        # Process each course session
        for (course_id, day, room_name), hour_list in course_sessions.items():
            # Sort hours
            hour_list.sort(key=lambda x: (int(x.split(':')[0]), int(x.split(':')[1])))
            
            # Find course object
            course = None
            for c in self.courses + self.all_available_courses:
                if c.course_id == course_id:
                    course = c
                    break
            
            if not course:
                continue
            
            # Get start and end hours
            start_hour = hour_list[0]
            end_hour = hour_list[-1]
            
            # Calculate time range string
            start_decimal = time_to_decimal(start_hour)
            end_decimal = time_to_decimal(end_hour) + 1  # Add 1 hour for end time
            
            start_h = int(start_decimal)
            start_m = int((start_decimal % 1) * 60)
            end_h = int(end_decimal)
            end_m = int((end_decimal % 1) * 60)
            
            time_range = f"{start_h:02d}:{start_m:02d}-{end_h:02d}:{end_m:02d}"
            
            # Find row for start hour
            if start_hour not in hours:
                continue
            row = hours.index(start_hour)
            col = days.index(day)
            
            # Check if this cell is already filled (conflict)
            has_conflict = (row, col) in filled_cells
            
            # Create cell text
            course_name_short = course.name[:20] if len(course.name) > 20 else course.name
            num_hours = len(hour_list)
            cell_text = f"{course.code}\n{course_name_short}\n{room_name}\n{course.instructor}\n{time_range} ({num_hours} saat)"
            
            cell_item = QTableWidgetItem(cell_text)
            cell_item.setFlags(cell_item.flags() | Qt.ItemIsEditable)
            
            # Color coding
            if has_conflict:
                cell_item.setBackground(QColor(255, 200, 200))  # Light red for conflicts
            elif course.course_type == 'lab':
                cell_item.setBackground(QColor(200, 255, 200))  # Light green for labs
            else:
                cell_item.setBackground(QColor(240, 240, 255))  # Light blue for theory
            
            self.schedule_table.setItem(row, col, cell_item)
            filled_cells.add((row, col))
            
            # Mark subsequent hours as continuation (if not already filled)
            for i in range(1, len(hour_list)):
                if hour_list[i] in hours:
                    next_row = hours.index(hour_list[i])
                    if (next_row, col) not in filled_cells:
                        # Mark as continuation with arrow or empty
                        continue_item = QTableWidgetItem("↓")
                        continue_item.setFlags(Qt.NoItemFlags)  # Not editable
                        continue_item.setTextAlignment(Qt.AlignCenter)
                        if course.course_type == 'lab':
                            continue_item.setBackground(QColor(200, 255, 200))
                        else:
                            continue_item.setBackground(QColor(240, 240, 255))
                        self.schedule_table.setItem(next_row, col, continue_item)
                        filled_cells.add((next_row, col))
        
        # Fill empty cells
        for row in range(len(hours)):
            for col in range(len(days)):
                if (row, col) not in filled_cells:
                    empty_item = QTableWidgetItem("")
                    empty_item.setFlags(Qt.NoItemFlags)
                    self.schedule_table.setItem(row, col, empty_item)
        
        # Resize columns
        self.schedule_table.resizeColumnsToContents()
        self.schedule_table.resizeRowsToContents()
    
    def on_cell_changed(self, row, col):
        """Handle manual cell editing."""
        # This allows manual editing of the schedule
        # No popup message - silent editing
        pass
    
    def save_schedule(self):
        """Save the current schedule to a JSON file."""
        if not self.schedule:
            QMessageBox.warning(self, "Uyarı", "Kaydedilecek program yok.")
            return
        
        file_name, _ = QFileDialog.getSaveFileName(self, "Programı Kaydet", "", "JSON Files (*.json)")
        if not file_name:
            return
        
        try:
            # Convert schedule to serializable format
            schedule_data = {
                str((day, hour)): [
                    {
                        "course": {
                            "code": course.code,
                            "name": course.name,
                            "instructor": course.instructor
                        },
                        "room": room.name
                    }
                    for course, room in entries
                ]
                for (day, hour), entries in self.schedule.items()
            }
            
            with open(file_name, 'w', encoding='utf-8') as file:
                json.dump(schedule_data, file, indent=2, ensure_ascii=False)
            
            QMessageBox.information(self, "Başarılı", "Program kaydedildi!")
            
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Program kaydedilemedi: {e}")
    
    def clear_schedule(self):
        """Clear the current schedule."""
        self.schedule_table.clear()
        self.schedule = {}
        self.status_label.setText("Program temizlendi.")
    
    def view_report(self):
        """Generate and display validation report."""
        if not self.schedule:
            QMessageBox.warning(self, "Uyarı", "Önce bir program oluşturun.")
            return
        
        # Generate validation report
        violations = self.validate_schedule()
        
        # Create report dialog
        report_dialog = QDialog(self)
        report_dialog.setWindowTitle("Program Doğrulama Raporu")
        report_dialog.setGeometry(200, 200, 800, 600)
        
        layout = QVBoxLayout(report_dialog)
        
        # Title
        title = QLabel("Program Doğrulama Raporu")
        title.setFont(QFont("Arial", 14, QFont.Bold))
        layout.addWidget(title)
        
        # Report text
        report_text = QTextEdit()
        report_text.setReadOnly(True)
        
        if not violations:
            report_text.setPlainText("✅ Program başarıyla doğrulandı!\n\nHiçbir ihlal bulunamadı.")
            report_text.setStyleSheet("background-color: #E8F5E9;")
        else:
            report_lines = ["⚠️ Program Doğrulama Raporu\n"]
            report_lines.append(f"Toplam {len(violations)} ihlal bulundu:\n")
            report_lines.append("=" * 60 + "\n\n")
            
            for i, violation in enumerate(violations, 1):
                report_lines.append(f"{i}. {violation}\n")
            
            report_text.setPlainText("\n".join(report_lines))
            report_text.setStyleSheet("background-color: #FFF3E0;")
        
        layout.addWidget(report_text)
        
        # Close button
        close_button = QPushButton("Kapat")
        close_button.clicked.connect(report_dialog.close)
        layout.addWidget(close_button)
        
        report_dialog.exec_()
    
    def validate_schedule(self):
        """Validate the current schedule and return list of violations."""
        violations = []
        
        if not self.schedule:
            return violations
        
        # Create instructors dictionary
        instructors_dict = {}
        for inst in self.instructors:
            instructors_dict[inst.name] = inst
        
        # Check for various violations
        from scheduler import (
            is_exam_block, exceeds_daily_theory_limit, has_instructor_conflict,
            has_room_conflict, has_year_mandatory_conflict, has_elective_conflict,
            is_lab_after_theory, is_valid_room_for_course, time_to_decimal
        )
        
        # Track instructor daily hours
        instructor_daily_hours = {}
        
        # Check each time slot
        for (day, hour), entries in self.schedule.items():
            # Check for multiple courses in same slot (room/instructor conflicts)
            if len(entries) > 1:
                course_codes = [e[0].code for e in entries]
                violations.append(
                    f"Çakışma: {day} {hour} - Aynı zaman diliminde birden fazla ders: {', '.join(course_codes)}"
                )
            
            for course, room in entries:
                # Check exam block
                if is_exam_block(day, hour):
                    violations.append(
                        f"Sınav Bloğu İhlali: {course.code} - Cuma 13:20-15:10 arası planlanamaz ({day} {hour})"
                    )
                
                # Check room capacity and type
                if not is_valid_room_for_course(room, course):
                    if course.course_type == 'lab' and room.room_type != 'lab':
                        violations.append(
                            f"Kapasite/Tip Hatası: {course.code} - Lab dersi lab dersliğinde olmalı (Derslik: {room.name})"
                        )
                    elif course.course_type == 'lab' and room.capacity < course.capacity:
                        violations.append(
                            f"Kapasite Hatası: {course.code} - Derslik kapasitesi yetersiz "
                            f"(Gerekli: {course.capacity}, Mevcut: {room.capacity}, Derslik: {room.name})"
                        )
                
                # Check instructor daily theory limit
                if course.course_type == 'theory':
                    instructor_obj = instructors_dict.get(course.instructor)
                    if instructor_obj:
                        day_key = (day, course.instructor)
                        if day_key not in instructor_daily_hours:
                            instructor_daily_hours[day_key] = 0
                        instructor_daily_hours[day_key] += course.theory_hours or course.hours
                        
                        if instructor_daily_hours[day_key] > instructor_obj.max_daily_theory_hours:
                            violations.append(
                                f"Öğretim Elemanı Sınırı: {course.instructor} - {day} günü "
                                f"{instructor_daily_hours[day_key]} saat teorik ders "
                                f"(Maksimum: {instructor_obj.max_daily_theory_hours} saat)"
                            )
                
                # Check lab after theory
                if course.course_type == 'lab':
                    if not is_lab_after_theory(course, self.schedule, day, hour, self.courses + self.all_available_courses):
                        violations.append(
                            f"Lab Sıralama: {course.code} - Lab dersi teorik dersinden önce planlanamaz ({day} {hour})"
                        )
                
                # Check for instructor conflicts (same instructor, different courses)
                for other_course, _ in entries:
                    if other_course.course_id != course.course_id and other_course.instructor == course.instructor:
                        violations.append(
                            f"Öğretim Elemanı Çakışması: {course.instructor} - "
                            f"Aynı anda iki ders ({course.code} ve {other_course.code}) - {day} {hour}"
                        )
                
                # Check for room conflicts
                for other_course, other_room in entries:
                    if other_course.course_id != course.course_id and other_room.name == room.name:
                        violations.append(
                            f"Derslik Çakışması: {room.name} - "
                            f"Aynı anda iki ders ({course.code} ve {other_course.code}) - {day} {hour}"
                        )
                
                # Check for same year mandatory conflicts
                for other_course, _ in entries:
                    if (other_course.course_id != course.course_id and
                        other_course.year == course.year and
                        course.is_mandatory and other_course.is_mandatory):
                        violations.append(
                            f"Aynı Sınıf Zorunlu Ders Çakışması: {course.code} ve {other_course.code} "
                            f"({course.year}. sınıf) - {day} {hour}"
                        )
                
                # Check for 3rd year courses and electives conflict
                for other_course, _ in entries:
                    if other_course.course_id != course.course_id:
                        # 3rd year courses should not overlap with electives
                        if ((course.year == 3 and not other_course.is_mandatory) or
                            (other_course.year == 3 and not course.is_mandatory)):
                            violations.append(
                                f"3. Sınıf Ders-Seçmeli Çakışması: {course.code} (Yıl {course.year}, "
                                f"{'Zorunlu' if course.is_mandatory else 'Seçmeli'}) ve "
                                f"{other_course.code} (Yıl {other_course.year}, "
                                f"{'Zorunlu' if other_course.is_mandatory else 'Seçmeli'}) - {day} {hour}"
                            )
        
        return violations


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BeePlanGUI()
    window.show()
    sys.exit(app.exec_())
