from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QStackedWidget, QLineEdit, QMessageBox, QComboBox, QTableWidget, QTableWidgetItem, QHeaderView, QSplitter, QFrame
from PySide6.QtCore import Qt, Signal, Slot, QMargins
from PySide6.QtGui import QFont, QColor, QPalette
from PySide6.QtCharts import QChart, QChartView, QLineSeries, QDateTimeAxis, QValueAxis, QBarSeries, QBarSet, QBarCategoryAxis, QPieSeries, QPieSlice

class LoginView(QWidget):
    """Login view component"""
    login_requested = Signal(str, str)
    register_requested = Signal(str, str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        # Create main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(50, 50, 50, 50)
        main_layout.setSpacing(20)
        
        # Title
        title_label = QLabel("Stock Market Analysis")
        title_font = QFont()
        title_font.setPointSize(24)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)
        
        # Subtitle
        subtitle_label = QLabel("Login to your account")
        subtitle_font = QFont()
        subtitle_font.setPointSize(14)
        subtitle_label.setFont(subtitle_font)
        subtitle_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(subtitle_label)
        
        # Spacer
        main_layout.addSpacing(30)
        
        # Email field
        email_label = QLabel("Email:")
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Enter your email")
        main_layout.addWidget(email_label)
        main_layout.addWidget(self.email_input)
        
        # Password field
        password_label = QLabel("Password:")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter your password")
        self.password_input.setEchoMode(QLineEdit.Password)
        main_layout.addWidget(password_label)
        main_layout.addWidget(self.password_input)
        
        # Buttons layout
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(10)
        
        # Login button
        self.login_button = QPushButton("Login")
        self.login_button.setMinimumHeight(40)
        self.login_button.clicked.connect(self.on_login_clicked)
        buttons_layout.addWidget(self.login_button)
        
        # Register button
        self.register_button = QPushButton("Register")
        self.register_button.setMinimumHeight(40)
        self.register_button.clicked.connect(self.on_register_clicked)
        buttons_layout.addWidget(self.register_button)
        
        main_layout.addLayout(buttons_layout)
        
        # Add stretch to push everything to the top
        main_layout.addStretch(1)
        
    def on_login_clicked(self):
        email = self.email_input.text().strip()
        password = self.password_input.text()
        
        if not email or not password:
            QMessageBox.warning(self, "Login Error", "Please enter both email and password.")
            return
        
        self.login_requested.emit(email, password)
        
    def on_register_clicked(self):
        email = self.email_input.text().strip()
        password = self.password_input.text()
        
        if not email or not password:
            QMessageBox.warning(self, "Registration Error", "Please enter both email and password.")
            return
        
        self.register_requested.emit(email, password)
        
    def clear_fields(self):
        self.email_input.clear()
        self.password_input.clear()
        
    def show_error(self, message):
        QMessageBox.critical(self, "Error", message)
        
    def show_success(self, message):
        QMessageBox.information(self, "Success", message)
