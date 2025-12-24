"""
KidTask - Task and Wish Management Application
PyQt5 GUI Application for managing tasks, wishes, and tracking points/levels.
"""

import sys
from datetime import datetime, timedelta
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit, QTextEdit, QTableWidget, QTableWidgetItem,
    QTabWidget, QMessageBox, QDialog, QDialogButtonBox, QFormLayout,
    QDateEdit, QSpinBox, QComboBox, QProgressBar, QGroupBox, QListWidget,
    QListWidgetItem, QHeaderView
)
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt, QDate
from kidtask_app import KidTaskApp
from controller import KidTaskController
from user import User, UserRole
from task import Task
from wish import Wish


class LoginDialog(QDialog):
    """Login dialog for user authentication with role selection."""
    
    def __init__(self, controller: KidTaskController, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.current_user = None
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("KidTask - Giriş")
        self.setGeometry(100, 100, 450, 300)
        
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("KidTask - Giriş Yap")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Role selection
        role_group = QGroupBox("Rol Seçimi")
        role_layout = QVBoxLayout()
        
        self.role_combo = QComboBox()
        self.role_combo.addItem("Çocuk", UserRole.CHILD)
        self.role_combo.addItem("Ebeveyn", UserRole.PARENT)
        self.role_combo.addItem("Öğretmen", UserRole.TEACHER)
        self.role_combo.currentIndexChanged.connect(self.on_role_changed)
        
        role_layout.addWidget(self.role_combo)
        role_group.setLayout(role_layout)
        layout.addWidget(role_group)
        
        # Form
        form_layout = QFormLayout()
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Kullanıcı adı")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Şifre")
        self.password_input.setEchoMode(QLineEdit.Password)
        
        form_layout.addRow("Kullanıcı Adı:", self.username_input)
        form_layout.addRow("Şifre:", self.password_input)
        
        layout.addLayout(form_layout)
        
        # Buttons
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.login)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
        
        self.setLayout(layout)
        self.on_role_changed()  # Initial filter
        
    def on_role_changed(self):
        """Filter users by selected role."""
        selected_role = self.role_combo.currentData()
        # Role-based filtering will be done in login method
        
    def login(self):
        """Handle login through controller."""
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        selected_role = self.role_combo.currentData()
        
        if not username or not password:
            QMessageBox.warning(self, "Hata", "Lütfen kullanıcı adı ve şifre girin.")
            return
        
        # Use controller to authenticate
        user = self.controller.login(username, password)
        if not user:
            QMessageBox.warning(self, "Hata", "Kullanıcı adı veya şifre yanlış.")
            return
        
        # Check if user role matches selected role
        if user.role != selected_role:
            role_names = {"Child": "Çocuk", "Parent": "Ebeveyn", "Teacher": "Öğretmen"}
            QMessageBox.warning(self, "Hata", 
                              f"Bu kullanıcı {role_names[user.role.value]} rolünde. "
                              f"Lütfen {role_names[selected_role.value]} rolünü seçin.")
            return
        
        self.current_user = user
        self.accept()


class KidTaskGUI(QMainWindow):
    """Main GUI window for KidTask application."""
    
    def __init__(self):
        super().__init__()
        # Initialize controller (mediator between GUI and business logic)
        self.controller = KidTaskController()
        self.current_user = None
        self.selected_child = None  # For Parent: selected child to view
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("KidTask - Task and Wish Management")
        self.setGeometry(100, 100, 1200, 800)
        
        # Show login dialog
        if not self.show_login():
            sys.exit(0)
        
        # Create central widget with tabs
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        
        # Top bar with welcome and child selection (for Parent)
        top_layout = QHBoxLayout()
        
        welcome_text = f"Hoş geldiniz, {self.current_user.username} ({self.current_user.role.value})"
        if self.current_user.role == UserRole.PARENT and self.selected_child:
            welcome_text += f" - Çocuk: {self.selected_child}"
        
        self.welcome_label = QLabel(welcome_text)
        self.welcome_label.setFont(QFont("Arial", 14, QFont.Bold))
        top_layout.addWidget(self.welcome_label)
        
        # Child selection for Parent
        if self.current_user.role == UserRole.PARENT:
            self.child_combo = QComboBox()
            self.child_combo.addItem("Tüm Çocuklar", None)
            children = self.controller.get_children()
            for child in children:
                self.child_combo.addItem(child.username, child.username)
            self.child_combo.currentIndexChanged.connect(self.on_child_selected)
            top_layout.addWidget(QLabel("Çocuk Seç:"))
            top_layout.addWidget(self.child_combo)
        
        top_layout.addStretch()
        
        # Logout button
        logout_btn = QPushButton("Çıkış Yap")
        logout_btn.clicked.connect(self.logout)
        top_layout.addWidget(logout_btn)
        
        self.layout.addLayout(top_layout)
        
        # Create tabs
        self.tabs = QTabWidget()
        self.create_dashboard_tab()
        self.create_tasks_tab()
        self.create_wishes_tab()
        self.create_progress_tab()
        
        self.layout.addWidget(self.tabs)
        
    def show_login(self):
        """Show login dialog and return True if login successful."""
        dialog = LoginDialog(self.controller, self)
        if dialog.exec_() == QDialog.Accepted:
            self.current_user = dialog.current_user
            self.controller.current_user = self.current_user
            return True
        return False
    
    def logout(self):
        """Logout and show login dialog again."""
        reply = QMessageBox.question(self, "Çıkış", "Çıkış yapmak istediğinize emin misiniz?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.controller.logout()
            self.selected_child = None  # Reset child selection
            if not self.show_login():
                self.close()
            else:
                # Recreate UI for new user
                self.central_widget = QWidget()
                self.setCentralWidget(self.central_widget)
                self.layout = QVBoxLayout(self.central_widget)
                
                # Recreate top bar
                top_layout = QHBoxLayout()
                welcome_text = f"Hoş geldiniz, {self.current_user.username} ({self.current_user.role.value})"
                if self.current_user.role == UserRole.PARENT and self.selected_child:
                    welcome_text += f" - Çocuk: {self.selected_child}"
                
                self.welcome_label = QLabel(welcome_text)
                self.welcome_label.setFont(QFont("Arial", 14, QFont.Bold))
                top_layout.addWidget(self.welcome_label)
                
                # Child selection for Parent
                if self.current_user.role == UserRole.PARENT:
                    self.child_combo = QComboBox()
                    self.child_combo.addItem("Tüm Çocuklar", None)
                    children = self.controller.get_children()
                    for child in children:
                        self.child_combo.addItem(child.username, child.username)
                    self.child_combo.currentIndexChanged.connect(self.on_child_selected)
                    top_layout.addWidget(QLabel("Çocuk Seç:"))
                    top_layout.addWidget(self.child_combo)
                
                top_layout.addStretch()
                logout_btn = QPushButton("Çıkış Yap")
                logout_btn.clicked.connect(self.logout)
                top_layout.addWidget(logout_btn)
                self.layout.addLayout(top_layout)
                
                # Recreate tabs
                self.tabs = QTabWidget()
                self.create_dashboard_tab()
                self.create_tasks_tab()
                self.create_wishes_tab()
                self.create_progress_tab()
                self.layout.addWidget(self.tabs)
    
    def create_dashboard_tab(self):
        """Create main dashboard tab."""
        dashboard = QWidget()
        layout = QVBoxLayout(dashboard)
        
        # Dashboard content based on user role
        if self.current_user.role == UserRole.CHILD:
            self.create_child_dashboard(layout)
        elif self.current_user.role == UserRole.PARENT:
            self.create_parent_dashboard(layout)
        elif self.current_user.role == UserRole.TEACHER:
            self.create_teacher_dashboard(layout)
        
        self.tabs.addTab(dashboard, "🏠 Ana Sayfa")
    
    def create_child_dashboard(self, layout):
        """Create dashboard for Child users."""
        # Points and Level display
        points_group = QGroupBox("Puanlar ve Seviye")
        points_layout = QVBoxLayout()
        
        if self.current_user.total_points is not None:
            points_label = QLabel(f"Toplam Puan: {self.current_user.total_points}")
            points_label.setFont(QFont("Arial", 12))
            points_layout.addWidget(points_label)
            
            level_label = QLabel(f"Seviye: {self.current_user.level}")
            level_label.setFont(QFont("Arial", 12, QFont.Bold))
            points_layout.addWidget(level_label)
            
            # Progress bar for level
            progress = QProgressBar()
            avg_rating = self.current_user.get_average_rating()
            progress.setMaximum(100)
            progress.setValue(int(avg_rating))
            progress.setFormat(f"Ortalama Puan: {avg_rating:.1f}%")
            points_layout.addWidget(progress)
        
        points_group.setLayout(points_layout)
        layout.addWidget(points_group)
        
        # Recent tasks
        tasks_group = QGroupBox("Son Görevler")
        tasks_layout = QVBoxLayout()
        
        child_tasks = [t for t in self.app.tasks if t.child_username == self.current_user.username]
        recent_tasks = sorted(child_tasks, key=lambda x: x.due_date, reverse=True)[:5]
        
        if recent_tasks:
            for task in recent_tasks:
                status = "✅ Tamamlandı" if task.is_completed else "⏳ Devam Ediyor"
                task_label = QLabel(f"{task.title} - {status} ({task.points} puan)")
                tasks_layout.addWidget(task_label)
        else:
            no_tasks = QLabel("Henüz görev yok.")
            tasks_layout.addWidget(no_tasks)
        
        tasks_group.setLayout(tasks_layout)
        layout.addWidget(tasks_group)
        
        layout.addStretch()
    
    def create_parent_dashboard(self, layout):
        """Create dashboard for Parent users."""
        info_label = QLabel("Ebeveyn Paneli - Üstteki menüden çocuğunuzu seçebilir, görev ve dilek ekleyebilirsiniz.")
        info_label.setFont(QFont("Arial", 12))
        layout.addWidget(info_label)
        
        # Child selection reminder
        if not self.selected_child:
            reminder = QLabel("💡 İpucu: Üstteki menüden bir çocuk seçerek sadece o çocuğun görevlerini görebilirsiniz.")
            reminder.setStyleSheet("color: #FF9800; font-weight: bold;")
            layout.addWidget(reminder)
        
        # Statistics
        stats_group = QGroupBox("İstatistikler")
        stats_layout = QVBoxLayout()
        
        # Filter tasks by selected child if any
        if self.selected_child:
            child_tasks = [t for t in self.app.tasks if t.child_username == self.selected_child]
            total_tasks = len(child_tasks)
            completed_tasks = len([t for t in child_tasks if t.is_completed])
            pending_approvals = len([t for t in child_tasks if t.is_completed and not t.is_approved])
            stats_layout.addWidget(QLabel(f"Seçili Çocuğun Görevleri:"))
        else:
            total_tasks = len(self.app.tasks)
            completed_tasks = len([t for t in self.app.tasks if t.is_completed])
            pending_approvals = len([t for t in self.app.tasks if t.is_completed and not t.is_approved])
            stats_layout.addWidget(QLabel(f"Tüm Çocukların Görevleri:"))
        
        stats_layout.addWidget(QLabel(f"Toplam Görev: {total_tasks}"))
        stats_layout.addWidget(QLabel(f"Tamamlanan: {completed_tasks}"))
        stats_layout.addWidget(QLabel(f"Onay Bekleyen: {pending_approvals}"))
        
        stats_group.setLayout(stats_layout)
        layout.addWidget(stats_group)
        
        layout.addStretch()
    
    def create_teacher_dashboard(self, layout):
        """Create dashboard for Teacher users."""
        info_label = QLabel("Öğretmen Paneli - Okul görevleri ekleyebilir ve tamamlanan görevleri değerlendirebilirsiniz.")
        info_label.setFont(QFont("Arial", 12))
        layout.addWidget(info_label)
        
        # Statistics
        stats_group = QGroupBox("İstatistikler")
        stats_layout = QVBoxLayout()
        
        school_tasks = len([t for t in self.app.tasks if t.created_by == self.current_user.username])
        pending_ratings = len([t for t in self.app.tasks if t.is_completed and not t.is_approved and t.created_by == self.current_user.username])
        
        stats_layout.addWidget(QLabel(f"Oluşturduğum Görevler: {school_tasks}"))
        stats_layout.addWidget(QLabel(f"Değerlendirme Bekleyen: {pending_ratings}"))
        
        stats_group.setLayout(stats_layout)
        layout.addWidget(stats_group)
        
        layout.addStretch()
    
    def create_tasks_tab(self):
        """Create tasks management tab."""
        tasks_widget = QWidget()
        layout = QVBoxLayout(tasks_widget)
        
        # Filter buttons
        filter_layout = QHBoxLayout()
        all_btn = QPushButton("Tümü")
        daily_btn = QPushButton("Günlük")
        weekly_btn = QPushButton("Haftalık")
        
        all_btn.clicked.connect(lambda: self.filter_tasks("all"))
        daily_btn.clicked.connect(lambda: self.filter_tasks("daily"))
        weekly_btn.clicked.connect(lambda: self.filter_tasks("weekly"))
        
        filter_layout.addWidget(all_btn)
        filter_layout.addWidget(daily_btn)
        filter_layout.addWidget(weekly_btn)
        filter_layout.addStretch()
        
        layout.addLayout(filter_layout)
        
        # Tasks table
        self.tasks_table = QTableWidget()
        self.tasks_table.setColumnCount(8)
        self.tasks_table.setHorizontalHeaderLabels([
            "✓", "ID", "Başlık", "Açıklama", "Bitiş Tarihi", "Puan", "Durum", "Puanlama"
        ])
        self.tasks_table.horizontalHeader().setStretchLastSection(True)
        self.tasks_table.setSelectionBehavior(QTableWidget.SelectRows)
        # Set checkbox column width
        self.tasks_table.setColumnWidth(0, 50)
        layout.addWidget(self.tasks_table)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        if self.current_user.role in [UserRole.PARENT, UserRole.TEACHER]:
            add_task_btn = QPushButton("➕ Yeni Görev Ekle")
            add_task_btn.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold;")
            add_task_btn.clicked.connect(self.add_task_dialog)
            button_layout.addWidget(add_task_btn)
        
        if self.current_user.role == UserRole.CHILD:
            complete_task_btn = QPushButton("✅ Seçili Görevleri Tamamla")
            complete_task_btn.setStyleSheet("background-color: #2196F3; color: white; font-weight: bold;")
            complete_task_btn.clicked.connect(self.complete_selected_tasks)
            button_layout.addWidget(complete_task_btn)
        
        if self.current_user.role in [UserRole.PARENT, UserRole.TEACHER]:
            approve_task_btn = QPushButton("Görevi Onayla ve Puanla")
            approve_task_btn.clicked.connect(self.approve_task_dialog)
            button_layout.addWidget(approve_task_btn)
        
        button_layout.addStretch()
        layout.addLayout(button_layout)
        
        self.tabs.addTab(tasks_widget, "📋 Görevler")
        self.refresh_tasks_table()
    
    def create_wishes_tab(self):
        """Create wishes management tab."""
        wishes_widget = QWidget()
        layout = QVBoxLayout(wishes_widget)
        
        # Wishes list
        self.wishes_list = QListWidget()
        layout.addWidget(self.wishes_list)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        if self.current_user.role == UserRole.CHILD:
            add_wish_btn = QPushButton("⭐ Yeni Dilek Ekle")
            add_wish_btn.setStyleSheet("background-color: #FF9800; color: white; font-weight: bold; padding: 10px;")
            add_wish_btn.clicked.connect(self.add_wish_dialog)
            button_layout.addWidget(add_wish_btn)
        
        if self.current_user.role in [UserRole.PARENT, UserRole.TEACHER]:
            approve_wish_btn = QPushButton("Dileği Onayla")
            approve_wish_btn.clicked.connect(self.approve_wish)
            button_layout.addWidget(approve_wish_btn)
            
            reject_wish_btn = QPushButton("Dileği Reddet")
            reject_wish_btn.clicked.connect(self.reject_wish)
            button_layout.addWidget(reject_wish_btn)
        
        button_layout.addStretch()
        layout.addLayout(button_layout)
        
        self.tabs.addTab(wishes_widget, "⭐ Dilekler")
        self.refresh_wishes_list()
    
    def create_progress_tab(self):
        """Create progress tracking tab."""
        progress_widget = QWidget()
        layout = QVBoxLayout(progress_widget)
        
        if self.current_user.role == UserRole.CHILD:
            # Points display
            points_group = QGroupBox("Puan Bilgileri")
            points_layout = QVBoxLayout()
            
            total_points_label = QLabel(f"Toplam Puan: {self.current_user.total_points}")
            total_points_label.setFont(QFont("Arial", 14, QFont.Bold))
            points_layout.addWidget(total_points_label)
            
            level_label = QLabel(f"Seviye: {self.current_user.level}")
            level_label.setFont(QFont("Arial", 14, QFont.Bold))
            points_layout.addWidget(level_label)
            
            avg_rating = self.current_user.get_average_rating()
            avg_label = QLabel(f"Ortalama Puan: {avg_rating:.2f}")
            avg_label.setFont(QFont("Arial", 12))
            points_layout.addWidget(avg_label)
            
            # Progress bar
            progress_bar = QProgressBar()
            progress_bar.setMaximum(100)
            progress_bar.setValue(int(avg_rating))
            progress_bar.setFormat(f"{avg_rating:.1f}%")
            progress_bar.setStyleSheet("QProgressBar::chunk { background-color: #4CAF50; }")
            points_layout.addWidget(progress_bar)
            
            points_group.setLayout(points_layout)
            layout.addWidget(points_group)
            
            # Completed tasks
            completed_group = QGroupBox("Tamamlanan Görevler")
            completed_layout = QVBoxLayout()
            
            child_tasks = [t for t in self.app.tasks 
                          if t.child_username == self.current_user.username and t.is_approved]
            
            if child_tasks:
                for task in child_tasks:
                    task_text = f"{task.title} - {task.points} puan"
                    if task.rating:
                        task_text += f" (Puanlama: {task.rating})"
                    task_label = QLabel(task_text)
                    completed_layout.addWidget(task_label)
            else:
                no_tasks = QLabel("Henüz tamamlanmış görev yok.")
                completed_layout.addWidget(no_tasks)
            
            completed_group.setLayout(completed_layout)
            layout.addWidget(completed_group)
        
        else:
            # For Parent/Teacher: Show all children's progress
            children_group = QGroupBox("Çocukların İlerlemeleri")
            children_layout = QVBoxLayout()
            
            children = [u for u in self.app.users if u.role == UserRole.CHILD]
            
            if children:
                for child in children:
                    child_info = QLabel(
                        f"{child.username}: {child.total_points} puan, Seviye {child.level}"
                    )
                    children_layout.addWidget(child_info)
            else:
                no_children = QLabel("Henüz çocuk kullanıcı yok.")
                children_layout.addWidget(no_children)
            
            children_group.setLayout(children_layout)
            layout.addWidget(children_group)
        
        layout.addStretch()
        self.tabs.addTab(progress_widget, "📊 İlerleme")
    
    def on_child_selected(self):
        """Handle child selection change for Parent users."""
        self.selected_child = self.child_combo.currentData()
        welcome_text = f"Hoş geldiniz, {self.current_user.username} ({self.current_user.role.value})"
        if self.selected_child:
            welcome_text += f" - Çocuk: {self.selected_child}"
        self.welcome_label.setText(welcome_text)
        self.refresh_all_tabs()
    
    def refresh_all_tabs(self):
        """Refresh all tabs with current data."""
        self.refresh_tasks_table()
        self.refresh_wishes_list()
        # Recreate tabs to update dashboard
        self.tabs.clear()
        self.create_dashboard_tab()
        self.create_tasks_tab()
        self.create_wishes_tab()
        self.create_progress_tab()
    
    def filter_tasks(self, filter_type):
        """Filter tasks by type (all, daily, weekly)."""
        self.refresh_tasks_table(filter_type)
    
    def refresh_tasks_table(self, filter_type="all"):
        """Refresh tasks table with current data."""
        self.tasks_table.setRowCount(0)
        
        # Get tasks based on user role
        if self.current_user.role == UserRole.CHILD:
            tasks = [t for t in self.app.tasks if t.child_username == self.current_user.username]
        elif self.current_user.role == UserRole.PARENT:
            # If child selected, show only that child's tasks
            if self.selected_child:
                tasks = [t for t in self.app.tasks if t.child_username == self.selected_child]
            else:
                tasks = self.app.tasks
        elif self.current_user.role == UserRole.TEACHER:
            tasks = [t for t in self.app.tasks if t.created_by == self.current_user.username or 
                    (t.child_username and self.app.find_user(t.child_username))]
        
        # Apply filter
        now = datetime.now()
        if filter_type == "daily":
            tasks = [t for t in tasks if t.due_date.date() == now.date()]
        elif filter_type == "weekly":
            week_end = now + timedelta(days=7)
            tasks = [t for t in tasks if t.due_date.date() <= week_end.date()]
        
        # Populate table
        for task in tasks:
            row = self.tasks_table.rowCount()
            self.tasks_table.insertRow(row)
            
            # Checkbox column (only for Child users and incomplete tasks)
            checkbox_item = QTableWidgetItem()
            checkbox_item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
            if self.current_user.role == UserRole.CHILD and not task.is_completed:
                checkbox_item.setCheckState(Qt.Unchecked)
            elif task.is_completed:
                checkbox_item.setCheckState(Qt.Checked)
                checkbox_item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)  # Keep enabled but checked
            else:
                checkbox_item.setCheckState(Qt.Unchecked)
                checkbox_item.setFlags(Qt.NoItemFlags)  # Disable for Parent/Teacher
            self.tasks_table.setItem(row, 0, checkbox_item)
            
            # Store task_id in checkbox item for easy access
            checkbox_item.setData(Qt.UserRole, task.task_id)
            
            self.tasks_table.setItem(row, 1, QTableWidgetItem(str(task.task_id)))
            self.tasks_table.setItem(row, 2, QTableWidgetItem(task.title))
            self.tasks_table.setItem(row, 3, QTableWidgetItem(task.description))
            self.tasks_table.setItem(row, 4, QTableWidgetItem(task.due_date.strftime("%Y-%m-%d %H:%M")))
            self.tasks_table.setItem(row, 5, QTableWidgetItem(str(task.points)))
            
            if task.is_approved:
                status = f"✅ Onaylandı ({task.rating})"
            elif task.is_completed:
                status = "⏳ Onay Bekliyor"
            else:
                status = "📝 Devam Ediyor"
            self.tasks_table.setItem(row, 6, QTableWidgetItem(status))
            
            rating_text = str(task.rating) if task.rating else "-"
            self.tasks_table.setItem(row, 7, QTableWidgetItem(rating_text))
    
    def refresh_wishes_list(self):
        """Refresh wishes list with current data."""
        self.wishes_list.clear()
        
        # Get wishes based on user role
        if self.current_user.role == UserRole.CHILD:
            # Only show wishes visible to child's level
            wishes = [w for w in self.app.wishes 
                     if w.is_visible_to_level(self.current_user.level) and
                     (w.child_username == self.current_user.username or not w.child_username)]
        else:
            wishes = self.app.wishes
        
        for wish in wishes:
            status = "✅ Onaylandı" if wish.is_approved else "⏳ Onay Bekliyor"
            wish_text = f"[{wish.wish_id}] {wish.description} - {wish.cost} puan - {status} (Min. Seviye: {wish.required_level})"
            if wish.child_username:
                wish_text += f" - {wish.child_username}"
            
            item = QListWidgetItem(wish_text)
            item.setData(Qt.UserRole, wish.wish_id)
            self.wishes_list.addItem(item)
    
    def add_task_dialog(self):
        """Show dialog to add new task."""
        dialog = QDialog(self)
        dialog.setWindowTitle("Yeni Görev Ekle")
        dialog.setGeometry(200, 200, 500, 400)
        
        layout = QVBoxLayout()
        form = QFormLayout()
        
        title_input = QLineEdit()
        description_input = QTextEdit()
        description_input.setMaximumHeight(100)
        due_date_input = QDateEdit()
        due_date_input.setDate(QDate.currentDate())
        due_date_input.setCalendarPopup(True)
        points_input = QSpinBox()
        points_input.setRange(1, 1000)
        points_input.setValue(10)
        
        # Child selection (for Parent/Teacher)
        child_combo = QComboBox()
        children = [u for u in self.app.users if u.role == UserRole.CHILD]
        child_combo.addItem("Seçiniz...", None)
        for child in children:
            child_combo.addItem(child.username, child.username)
        
        # If Parent has selected a child, pre-select it
        if self.current_user.role == UserRole.PARENT and self.selected_child:
            for i in range(child_combo.count()):
                if child_combo.itemData(i) == self.selected_child:
                    child_combo.setCurrentIndex(i)
                    break
        
        form.addRow("Başlık:", title_input)
        form.addRow("Açıklama:", description_input)
        form.addRow("Bitiş Tarihi:", due_date_input)
        form.addRow("Puan:", points_input)
        form.addRow("Çocuk:", child_combo)
        
        layout.addLayout(form)
        
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)
        
        dialog.setLayout(layout)
        
        if dialog.exec_() == QDialog.Accepted:
            child_username = child_combo.currentData()
            if not child_username:
                QMessageBox.warning(self, "Hata", "Lütfen bir çocuk seçin.")
                return
            
            due_date = due_date_input.date().toPyDate()
            due_datetime = datetime.combine(due_date, datetime.now().time())
            
            new_task = Task(
                title=title_input.text(),
                description=description_input.toPlainText(),
                due_date=due_datetime,
                points=points_input.value(),
                child_username=child_username,
                created_by=self.current_user.username
            )
            
            self.app.tasks.append(new_task)
            self.app.save_data()
            self.refresh_tasks_table()
            QMessageBox.information(self, "Başarılı", "Görev eklendi!")
    
    def complete_selected_tasks(self):
        """Mark checked tasks as completed."""
        completed_count = 0
        errors = []
        
        for row in range(self.tasks_table.rowCount()):
            checkbox_item = self.tasks_table.item(row, 0)
            if checkbox_item and checkbox_item.checkState() == Qt.Checked:
                task_id = checkbox_item.data(Qt.UserRole)
                
                if task_id is None:
                    # Try to get task_id from the ID column instead
                    id_item = self.tasks_table.item(row, 1)
                    if id_item:
                        try:
                            task_id = int(id_item.text())
                        except ValueError:
                            errors.append(f"Satır {row+1}: Geçersiz görev ID'si")
                            continue
                    else:
                        errors.append(f"Satır {row+1}: Görev ID'si bulunamadı")
                        continue
                
                task = self.app.find_task(task_id)
                
                if not task:
                    errors.append(f"Görev ID {task_id} bulunamadı")
                    continue
                
                if task.is_completed:
                    continue  # Already completed, skip
                
                task.complete()
                completed_count += 1
        
        if completed_count > 0:
            self.app.save_data()
            self.refresh_tasks_table()
            msg = f"{completed_count} görev tamamlandı olarak işaretlendi!"
            if errors:
                msg += f"\n\nUyarılar:\n" + "\n".join(errors)
            QMessageBox.information(self, "Başarılı", msg)
        else:
            if errors:
                QMessageBox.warning(self, "Hata", "Görevler tamamlanırken hatalar oluştu:\n" + "\n".join(errors))
            else:
                QMessageBox.warning(self, "Uyarı", "Lütfen tamamlamak istediğiniz görevleri işaretleyin.")
    
    def complete_task(self):
        """Mark selected task as completed (legacy method)."""
        selected = self.tasks_table.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "Uyarı", "Lütfen bir görev seçin.")
            return
        
        task_id = int(self.tasks_table.item(selected, 1).text())  # ID is now in column 1
        task = self.app.find_task(task_id)
        
        if not task:
            QMessageBox.warning(self, "Hata", "Görev bulunamadı.")
            return
        
        if task.is_completed:
            QMessageBox.information(self, "Bilgi", "Bu görev zaten tamamlanmış.")
            return
        
        task.complete()
        self.app.save_data()
        self.refresh_tasks_table()
        QMessageBox.information(self, "Başarılı", "Görev tamamlandı olarak işaretlendi!")
    
    def approve_task_dialog(self):
        """Show dialog to approve and rate task."""
        selected = self.tasks_table.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "Uyarı", "Lütfen bir görev seçin.")
            return
        
        task_id = int(self.tasks_table.item(selected, 1).text())  # ID is now in column 1
        task = self.app.find_task(task_id)
        
        if not task:
            QMessageBox.warning(self, "Hata", "Görev bulunamadı.")
            return
        
        if not task.is_completed:
            QMessageBox.warning(self, "Uyarı", "Görev tamamlanmadan onaylanamaz.")
            return
        
        if task.is_approved:
            QMessageBox.information(self, "Bilgi", "Bu görev zaten onaylanmış.")
            return
        
        dialog = QDialog(self)
        dialog.setWindowTitle("Görevi Onayla ve Puanla")
        dialog.setGeometry(200, 200, 300, 150)
        
        layout = QVBoxLayout()
        form = QFormLayout()
        
        rating_input = QSpinBox()
        rating_input.setRange(0, 100)
        rating_input.setValue(50)
        rating_input.setSuffix(" puan")
        
        form.addRow("Puanlama (0-100):", rating_input)
        layout.addLayout(form)
        
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)
        
        dialog.setLayout(layout)
        
        if dialog.exec_() == QDialog.Accepted:
            try:
                self.app.approve_task(
                    task_id=task_id,
                    rating=float(rating_input.value()),
                    approver_role=self.current_user.role,
                    child_username=task.child_username
                )
                self.app.save_data()
                self.refresh_all_tabs()
                QMessageBox.information(self, "Başarılı", "Görev onaylandı ve puanlandı!")
            except Exception as e:
                QMessageBox.critical(self, "Hata", f"Onaylama hatası: {e}")
    
    def add_wish_dialog(self):
        """Show dialog to add new wish."""
        dialog = QDialog(self)
        dialog.setWindowTitle("Yeni Dilek Ekle")
        dialog.setGeometry(200, 200, 500, 300)
        
        layout = QVBoxLayout()
        form = QFormLayout()
        
        description_input = QTextEdit()
        description_input.setMaximumHeight(100)
        cost_input = QSpinBox()
        cost_input.setRange(1, 10000)
        cost_input.setValue(50)
        level_input = QSpinBox()
        level_input.setRange(1, 3)
        level_input.setValue(self.current_user.level)
        type_combo = QComboBox()
        type_combo.addItems(["product", "activity"])
        
        form.addRow("Açıklama:", description_input)
        form.addRow("Maliyet (Puan):", cost_input)
        form.addRow("Gerekli Seviye:", level_input)
        form.addRow("Tip:", type_combo)
        
        layout.addLayout(form)
        
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)
        
        dialog.setLayout(layout)
        
        if dialog.exec_() == QDialog.Accepted:
            new_wish = Wish(
                description=description_input.toPlainText(),
                cost=cost_input.value(),
                required_level=level_input.value(),
                child_username=self.current_user.username,
                wish_type=type_combo.currentText()
            )
            
            self.app.wishes.append(new_wish)
            self.app.save_data()
            self.refresh_wishes_list()
            QMessageBox.information(self, "Başarılı", "Dilek eklendi!")
    
    def approve_wish(self):
        """Approve selected wish."""
        selected = self.wishes_list.currentItem()
        if not selected:
            QMessageBox.warning(self, "Uyarı", "Lütfen bir dilek seçin.")
            return
        
        wish_id = selected.data(Qt.UserRole)
        wish = self.app.find_wish(wish_id)
        
        if not wish:
            QMessageBox.warning(self, "Hata", "Dilek bulunamadı.")
            return
        
        if wish.is_approved:
            QMessageBox.information(self, "Bilgi", "Bu dilek zaten onaylanmış.")
            return
        
        try:
            self.app.approve_wish(wish_id, self.current_user.role)
            self.app.save_data()
            self.refresh_wishes_list()
            QMessageBox.information(self, "Başarılı", "Dilek onaylandı!")
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Onaylama hatası: {e}")
    
    def reject_wish(self):
        """Reject selected wish (remove it)."""
        selected = self.wishes_list.currentItem()
        if not selected:
            QMessageBox.warning(self, "Uyarı", "Lütfen bir dilek seçin.")
            return
        
        wish_id = selected.data(Qt.UserRole)
        wish = self.app.find_wish(wish_id)
        
        if not wish:
            QMessageBox.warning(self, "Hata", "Dilek bulunamadı.")
            return
        
        reply = QMessageBox.question(self, "Onay", "Bu dileği silmek istediğinize emin misiniz?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.app.wishes = [w for w in self.app.wishes if w.wish_id != wish_id]
            self.app.save_data()
            self.refresh_wishes_list()
            QMessageBox.information(self, "Başarılı", "Dilek silindi.")
    
    def closeEvent(self, event):
        """Save data when closing application through controller."""
        self.controller.save_data()
        event.accept()


def main():
    app = QApplication(sys.argv)
    window = KidTaskGUI()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

